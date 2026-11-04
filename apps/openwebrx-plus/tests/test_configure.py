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
