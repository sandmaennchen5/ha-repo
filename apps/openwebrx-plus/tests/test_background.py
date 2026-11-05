import importlib.util
from pathlib import Path
import sys
import threading
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

BASE = Path(__file__).resolve().parents[1] / "rootfs/opt/ha-openwebrx"
sys.path.insert(0, str(BASE))
import background


class BaseHandler:
    def __init__(self, source):
        self.source = source
        self.services = []
        self.resamplers = []
        self.lock = threading.RLock()
    def stopServices(self):
        self.services.clear()
    def setupService(self, dial, source):
        return (dial, source)


class Parser:
    def __init__(self, **kwargs):
        self.settings = kwargs


class BackgroundTests(unittest.TestCase):
    def test_shared_source_start_stop_and_retune(self):
        service = ModuleType("owrx.service")
        service.ServiceHandler = BaseHandler
        owrx = ModuleType("owrx")
        owrx.service = service
        toolbox = ModuleType("owrx.toolbox")
        toolbox.TextParser = Parser
        csdr = ModuleType("csdr")
        chain = ModuleType("csdr.chain")
        demod = ModuleType("csdr.chain.toolbox")
        demod.MultimonDemodulator = MagicMock()
        modules = {"owrx": owrx, "owrx.service": service, "owrx.toolbox": toolbox,
                   "csdr": csdr, "csdr.chain": chain, "csdr.chain.toolbox": demod}
        sink = MagicMock(frequency=85000000)
        source = MagicMock()
        source.isAvailable.return_value = True
        source.getProps.return_value = {"center_freq": 85000000, "samp_rate": 1024000}
        mode = SimpleNamespace(service=False)
        with patch.dict(sys.modules, modules), patch.object(background, "check_api", return_value=mode):
            background.install(sink)
            self.assertTrue(mode.service)
            handler = service.ServiceHandler(source)
            handler.updateServices()
            self.assertEqual(len(handler.services), 1)
            self.assertIs(handler.services[0][1], source)
            self.assertEqual(handler.services[0][0], {"mode": "zvei", "frequency": 85000000})
            sink.status.assert_called_with(True, "monitoring")
            handler._getSecondaryDemodulator("zvei")
            parser = demod.MultimonDemodulator.call_args.args[1]
            self.assertEqual(parser.settings, {"filePrefix": None, "service": True})
            parser.parse(b"ZVEI1: 12345")
            sink.receive.assert_called_once_with(b"ZVEI1: 12345")
            source.getProps.return_value["center_freq"] = 100000000
            handler.updateServices()
            self.assertEqual(handler.services, [])
            sink.status.assert_called_with(False, "frequency_outside_window")
            source.isAvailable.return_value = False
            handler.updateServices()
            sink.status.assert_called_with(False, "source_unavailable")

    def test_decoder_failure_reports_inactive(self):
        # Exercise the installed handler's failure branch through the same test
        # fixture by making setupService fail on its first call.
        with patch.object(BaseHandler, "setupService", side_effect=RuntimeError("test DSP failure")):
            # The normal fixture asserts success; use its module scaffolding
            # through a minimal installation instead.
            service = ModuleType("owrx.service")
            service.ServiceHandler = BaseHandler
            root = ModuleType("owrx")
            root.service = service
            toolbox = ModuleType("owrx.toolbox")
            toolbox.TextParser = Parser
            demod = ModuleType("csdr.chain.toolbox")
            demod.MultimonDemodulator = MagicMock()
            modules = {"owrx": root, "owrx.service": service, "owrx.toolbox": toolbox,
                       "csdr": ModuleType("csdr"), "csdr.chain": ModuleType("csdr.chain"),
                       "csdr.chain.toolbox": demod}
            sink = MagicMock(frequency=85000000)
            source = MagicMock()
            source.getProps.return_value = {"center_freq": 85000000, "samp_rate": 1024000}
            with patch.dict(sys.modules, modules), patch.object(background, "check_api", return_value=SimpleNamespace()):
                background.install(sink)
                handler = service.ServiceHandler(source)
                with self.assertLogs("background", level="ERROR"):
                    handler.updateServices()
                self.assertEqual(handler.services, [])
                sink.status.assert_called_with(False, "decoder_error")


if __name__ == "__main__":
    unittest.main()
