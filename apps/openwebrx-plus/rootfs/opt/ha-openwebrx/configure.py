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
                "profiles": {"zvei": {
                    "name": "ZVEI (FM)", "center_freq": frequency,
                    "start_freq": frequency, "start_mod": "zvei",
                    "samp_rate": rate, "rf_gain": gain, "tuning_step": "12500",
                }},
            }},
        }
    if set(settings.get("sdrs", {})) != {"dedicated_rtl"}:
        raise ValueError("Only dedicated_rtl is allowed in settings.json")
    receiver = settings["sdrs"]["dedicated_rtl"]
    receiver.update(type="rtl_sdr", device=serial, ppm=ppm)
    for profile in receiver.get("profiles", {}).values():
        profile.pop("device", None)
        profile.pop("type", None)
    temporary = settings_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    temporary.replace(settings_path)
    (data / "openwebrx.conf").write_text(
        f"[core]\ndata_directory = {directory.as_posix()}\n"
        "temporary_directory = /tmp\n[web]\nport = 8073\n"
        "ipv6 = false\nbind_address = 0.0.0.0\n", encoding="utf-8"
    )
    return directory


def main():
    options = read_options()
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
