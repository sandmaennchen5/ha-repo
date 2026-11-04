import ctypes
import importlib.util
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("configure", ROOT / "rootfs/opt/ha-openwebrx/configure.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


class ConnectorTests(unittest.TestCase):
    def invoke(self, arguments, serials):
        library = MagicMock()
        library.rtlsdr_get_device_count.return_value = len(serials)

        def descriptor(index, manufacturer, product, value):
            value.value = serials[index].encode("ascii")
            return 0

        library.rtlsdr_get_device_usb_strings.side_effect = descriptor
        with patch.dict(sys.modules, {"configure": config}), \
             patch.object(config, "read_options", return_value={"rtl_serial": "00001002"}), \
             patch.object(sys, "argv", ["rtl_connector", *arguments]), \
             patch("ctypes.util.find_library", return_value="fake"), \
             patch("ctypes.CDLL", return_value=library), \
             patch("os.execv", side_effect=RuntimeError("EXECUTED")) as execute:
            try:
                runpy.run_path(str(ROOT / "rootfs/usr/bin/rtl_connector"), run_name="__main__")
            except RuntimeError as error:
                self.assertEqual(str(error), "EXECUTED")
                return execute.call_args.args
        self.fail("Connector unexpectedly returned")

    def test_exact_serial_executes(self):
        binary, arguments = self.invoke(["-d", "00001002", "-s", "1024000"], ["00001001", "00001002"])
        self.assertEqual(binary, "/usr/bin/rtl_connector.real")
        self.assertEqual(arguments[1:3], ["-d", "00001002"])

    def test_missing_duplicate_and_wrong_selection_refused(self):
        for arguments, serials in (
            (["-d", "00001002"], ["00001001"]),
            (["-d", "00001002"], ["00001002", "00001002"]),
            (["-d", "00001001"], ["00001001", "00001002"]),
            (["-d", "0"], ["00001002"]),
            ([], ["00001002"]),
            (["-d", "00001002", "-d", "00001001"], ["00001002"]),
        ):
            with self.subTest(arguments=arguments, serials=serials), self.assertRaises(SystemExit):
                self.invoke(arguments, serials)

    def test_version_probe_needs_no_usb_device(self):
        _, arguments = self.invoke(["--version"], [])
        self.assertEqual(arguments, ["rtl_connector", "--version"])
