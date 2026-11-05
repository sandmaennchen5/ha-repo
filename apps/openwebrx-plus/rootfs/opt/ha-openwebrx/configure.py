"""Persist UI settings while enforcing the dedicated receiver on every start."""
import json
import os
from pathlib import Path
import re
import subprocess


def read_options(path=Path("/data/options.json")):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_serial(value):
    # Short numbers may be interpreted as device indices by librtlsdr.
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{4,64}", value):
        raise ValueError("Set the actual second RTL-SDR serial (4-64 letters/digits/_/-)")
    if "00001001".startswith(value) or "00001001".endswith(value) or (value.isdecimal() and int(value) < 1000):
        raise ValueError("00001001 is reserved for wmbusmeters; indices are forbidden")
    return value


def integer(options, key, lower, upper):
    value = options[key]
    if type(value) is not int or not lower <= value <= upper:
        raise ValueError(f"{key} must be an integer from {lower} to {upper}")
    return value


def preset_profiles(frequency, rate, gain):
    """A single receiver with selectable windows, not simultaneous channels."""
    def profile(name, center, mode, sample_rate=2400000, step="12500"):
        return dict(name=name, center_freq=center, start_freq=center,
                    start_mod=mode, samp_rate=sample_rate, rf_gain=gain,
                    tuning_step=step)

    presets = {"zvei": profile("ZVEI (FM)", frequency, "zvei", rate)}
    # Overlapping windows cover the complete European broadcast FM band.
    for center in [*range(88500000, 108000000, 2000000), 107500000]:
        presets[f"fm_{center // 1000}"] = profile(
            f"UKW {center / 1e6:.1f} MHz / RDS", center, "wfm", step="100000")
    presets.update({
        "cb": profile("CB 27 MHz / AM", 27200000, "am", step="10000"),
        "airband": profile("Flugfunk 121.5 MHz / AM", 121500000, "am", step="8333"),
        "ham_2m": profile("Amateurfunk 2 m / FM", 145000000, "nfm"),
        "aprs": profile("APRS 144.800 MHz", 144800000, "packet", 1024000),
        "ham_70cm": profile("Amateurfunk 70 cm / FM", 434000000, "nfm"),
        "pmr446": profile("PMR446 / FM", 446100000, "nfm", 1024000),
        "ism433": profile("ISM 433.920 MHz / rtl_433", 433920000, "ism", 250000),
    })
    return presets


def configure_monitor(options, settings, data):
    receiver = settings["sdrs"]["dedicated_rtl"]
    state_path = data / "zvei-monitor-restore.json"
    if options.get("monitor_enabled", False):
        if not state_path.exists():
            snapshot = {
                "global": {key: settings[key] for key in ("services_enabled", "services_decoders") if key in settings},
                "receiver": {key: receiver[key] for key in ("always-on", "services") if key in receiver},
            }
            state_path.write_text(json.dumps(snapshot), encoding="utf-8")
        profiles = receiver["profiles"]
        frequency = options.get("monitor_frequency", 0) or profiles.get("zvei", {}).get("start_freq", options["initial_frequency"])
        if type(frequency) is not int or not 24000000 <= frequency <= 1766000000:
            raise ValueError("Invalid background ZVEI frequency")
        profile = preset_profiles(frequency, options["sample_rate"], options["rf_gain"])["zvei"]
        profile["name"] = "ZVEI Dauerüberwachung"
        # Make monitoring the initial profile while preserving other profiles.
        receiver["profiles"] = {"_zvei_monitor": profile, **{k: v for k, v in profiles.items() if k != "_zvei_monitor"}}
        receiver["always-on"] = True
        receiver["services"] = True
        settings["services_enabled"] = True
        settings["services_decoders"] = ["zvei"]
    elif state_path.exists():
        snapshot = json.loads(state_path.read_text(encoding="utf-8"))
        for target, saved, keys in (
            (settings, snapshot["global"], ("services_enabled", "services_decoders")),
            (receiver, snapshot["receiver"], ("always-on", "services")),
        ):
            for key in keys:
                target.pop(key, None)
                if key in saved:
                    target[key] = saved[key]
        receiver.get("profiles", {}).pop("_zvei_monitor", None)
        # Keep the snapshot until settings.json has been persisted successfully.


def configure(options, data=Path("/data")):
    serial = validate_serial(options["rtl_serial"])
    frequency = integer(options, "initial_frequency", 24000000, 1766000000)
    rate = integer(options, "sample_rate", 250000, 2400000)
    gain = integer(options, "rf_gain", 0, 50)
    ppm = integer(options, "ppm", -200, 200)
    directory = data / "openwebrx"
    directory.mkdir(parents=True, exist_ok=True)
    settings_path = directory / "settings.json"
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        settings = {
            "version": 8,
            "receiver_name": "Home Assistant OpenWebRX+",
            "allow_center_freq_changes": True,
            "services_enabled": False,
            "report_radio": False,
            "report_clients": False,
            "sdrs": {"dedicated_rtl": {
                "name": "Dedicated RTL-SDR", "type": "rtl_sdr",
                "profiles": {},
            }},
        }
    if set(settings.get("sdrs", {})) != {"dedicated_rtl"}:
        raise ValueError("Only dedicated_rtl is allowed in settings.json")
    receiver = settings["sdrs"]["dedicated_rtl"]
    receiver.update(type="rtl_sdr", device=serial, ppm=ppm)
    preset_marker = data / "profile-presets-v1.json"
    if not preset_marker.exists():
        profiles = receiver.setdefault("profiles", {})
        for key, value in preset_profiles(frequency, rate, gain).items():
            # Existing UI edits always win over shipped presets.
            profiles.setdefault(key, value)
    for profile in receiver.get("profiles", {}).values():
        profile.pop("device", None)
        profile.pop("type", None)
    configure_monitor(options, settings, data)
    temporary = settings_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    temporary.replace(settings_path)
    if not options.get("monitor_enabled", False):
        (data / "zvei-monitor-restore.json").unlink(missing_ok=True)
    if not preset_marker.exists():
        preset_marker.write_text('{"version": 1}\n', encoding="utf-8")
    (data / "openwebrx.conf").write_text(
        f"[core]\ndata_directory = {directory.as_posix()}\n"
        "temporary_directory = /tmp\n[web]\nport = 8073\n"
        "ipv6 = false\nbind_address = 0.0.0.0\n", encoding="utf-8"
    )
    return directory


def main():
    options = read_options()
    from monitor import validate_monitor_options
    validate_monitor_options(options)
    password = options.get("admin_password", "")
    if not Path("/data/openwebrx/users.json").exists() and len(password) < 12:
        raise ValueError("Set admin_password to at least 12 characters for initial setup")
    directory = configure(options)
    if not (directory / "users.json").exists():
        environment = os.environ.copy()
        environment["OWRX_PASSWORD"] = password
        subprocess.run([
            "/usr/bin/openwebrx", "-c", "/data/openwebrx.conf",
            "admin", "--noninteractive", "adduser", "admin",
        ], env=environment, check=True)
        if not (directory / "users.json").exists():
            raise ValueError("Administrator was not persisted")
    print(f"Using dedicated RTL-SDR serial {options['rtl_serial']}; web port 8073", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        raise SystemExit(f"OpenWebRX+ configuration refused: {error}")
