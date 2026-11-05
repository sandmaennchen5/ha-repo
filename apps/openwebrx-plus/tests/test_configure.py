import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "rootfs/opt/ha-openwebrx/configure.py"
spec = importlib.util.spec_from_file_location("configure", MODULE)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


class ConfigurationTests(unittest.TestCase):
    def options(self):
        return dict(rtl_serial="00001002", initial_frequency=145500000,
                    sample_rate=1024000, rf_gain=29, ppm=0)

    def test_reserved_serial_and_indices_rejected(self):
        for serial in ("", "00001001", "0", "1", "0001", " 00001002", "a;bad"):
            with self.subTest(serial=serial), self.assertRaises(ValueError):
                config.validate_serial(serial)
        self.assertEqual(config.validate_serial("00001002"), "00001002")

    def test_initial_profile_and_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            directory = config.configure(self.options(), data)
            path = directory / "settings.json"
            settings = json.loads(path.read_text())
            receiver = settings["sdrs"]["dedicated_rtl"]
            self.assertEqual(receiver["device"], "00001002")
            self.assertEqual(receiver["profiles"]["zvei"]["start_mod"], "zvei")
            receiver["profiles"]["zvei"]["start_freq"] = 144800000
            settings["receiver_name"] = "Saved in UI"
            path.write_text(json.dumps(settings))
            options = self.options()
            options.update(rtl_serial="00001003", ppm=4)
            config.configure(options, data)
            saved = json.loads(path.read_text())
            self.assertEqual(saved["receiver_name"], "Saved in UI")
            receiver = saved["sdrs"]["dedicated_rtl"]
            self.assertEqual(receiver["profiles"]["zvei"]["start_freq"], 144800000)
            self.assertEqual(receiver["device"], "00001003")
            self.assertEqual(receiver["ppm"], 4)
            self.assertIn("port = 8073", (data / "openwebrx.conf").read_text())

    def test_upgrade_adds_presets_once_and_preserves_ui_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            directory = data / "openwebrx"
            directory.mkdir()
            path = directory / "settings.json"
            original = {"version": 8, "receiver_name": "My receiver",
                        "sdrs": {"dedicated_rtl": {"profiles": {
                            "zvei": {"name": "My ZVEI", "start_freq": 85000000},
                            "custom": {"name": "My custom profile"},
                        }}}}
            path.write_text(json.dumps(original))
            config.configure(self.options(), data)
            settings = json.loads(path.read_text())
            profiles = settings["sdrs"]["dedicated_rtl"]["profiles"]
            self.assertEqual(profiles["zvei"], original["sdrs"]["dedicated_rtl"]["profiles"]["zvei"])
            self.assertIn("custom", profiles)
            self.assertIn("fm_88500", profiles)
            del profiles["aprs"]
            profiles["fm_88500"]["start_freq"] = 89000000
            path.write_text(json.dumps(settings))
            config.configure(self.options(), data)
            saved = json.loads(path.read_text())["sdrs"]["dedicated_rtl"]["profiles"]
            self.assertNotIn("aprs", saved)
            self.assertEqual(saved["fm_88500"]["start_freq"], 89000000)

    def test_presets_cover_fm_band_and_stay_inside_sample_windows(self):
        presets = config.preset_profiles(145500000, 1024000, 29)
        windows = sorted((p["center_freq"] - p["samp_rate"] / 2,
                          p["center_freq"] + p["samp_rate"] / 2)
                         for p in presets.values() if p["start_mod"] == "wfm")
        upper = 87500000
        for lower, end in windows:
            self.assertLessEqual(lower, upper)
            upper = max(upper, end)
        self.assertGreaterEqual(upper, 108000000)
        for profile in presets.values():
            self.assertLessEqual(abs(profile["start_freq"] - profile["center_freq"]),
                                 profile["samp_rate"] / 2)
            self.assertGreaterEqual(profile["samp_rate"], 250000)
            self.assertLessEqual(profile["samp_rate"], 2400000)
            self.assertNotIn("device", profile)
        self.assertEqual(presets["aprs"]["start_mod"], "packet")
        self.assertEqual(presets["ism433"]["start_mod"], "ism")

    def test_monitor_enable_disable_restores_receiver_and_profiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            directory = config.configure(self.options(), data)
            path = directory / "settings.json"
            original = json.loads(path.read_text())
            options = {**self.options(), "monitor_enabled": True, "monitor_frequency": 85000000}
            config.configure(options, data)
            enabled = json.loads(path.read_text())
            receiver = enabled["sdrs"]["dedicated_rtl"]
            self.assertTrue(receiver["always-on"])
            self.assertTrue(enabled["services_enabled"])
            self.assertEqual(next(iter(receiver["profiles"])), "_zvei_monitor")
            self.assertEqual(receiver["profiles"]["_zvei_monitor"]["start_freq"], 85000000)
            config.configure(options, data)  # Repeat start must not overwrite the snapshot.
            config.configure(self.options(), data)
            self.assertEqual(json.loads(path.read_text()), original)
            self.assertFalse((data / "zvei-monitor-restore.json").exists())

    def test_monitor_uses_existing_zvei_frequency_when_option_is_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            directory = config.configure(self.options(), data)
            path = directory / "settings.json"
            settings = json.loads(path.read_text())
            settings["sdrs"]["dedicated_rtl"]["profiles"]["zvei"]["start_freq"] = 85000000
            path.write_text(json.dumps(settings))
            config.configure({**self.options(), "monitor_enabled": True, "monitor_frequency": 0}, data)
            saved = json.loads(path.read_text())
            self.assertEqual(saved["sdrs"]["dedicated_rtl"]["profiles"]["_zvei_monitor"]["start_freq"], 85000000)

    def test_invalid_options_do_not_write_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            options = self.options()
            options["sample_rate"] = True
            with self.assertRaises(ValueError):
                config.configure(options, Path(tmp))
            self.assertFalse((Path(tmp) / "openwebrx/settings.json").exists())

    def test_extra_receiver_and_corrupt_json_fail_closed(self):
        for text in ('{"sdrs": {"unsafe": {}}}', 'invalid json'):
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp) / "openwebrx"
                directory.mkdir()
                path = directory / "settings.json"
                path.write_text(text)
                with self.assertRaises(ValueError):
                    config.configure(self.options(), Path(tmp))
                self.assertEqual(path.read_text(), text)


if __name__ == "__main__":
    unittest.main()
