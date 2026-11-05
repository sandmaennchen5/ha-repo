"""Add one ZVEI service to OpenWebRX's shared source; no second USB reader."""
import logging
from monitor import DECODERS, monitoring_in_window

LOG = logging.getLogger(__name__)


def check_api():
    from owrx.service import ServiceHandler
    from owrx.modes import Modes, DigitalMode
    from owrx.toolbox import TextParser
    from csdr.chain.toolbox import MultimonDemodulator
    mode = Modes.findByModulation("zvei")
    if not isinstance(mode, DigitalMode):
        raise RuntimeError("Compatible OpenWebRX+ ZVEI mode required")
    for name in ("setupService", "stopServices", "updateServices", "_getSecondaryDemodulator"):
        if not callable(getattr(ServiceHandler, name, None)):
            raise RuntimeError(f"OpenWebRX+ service API changed: {name}")
    if not callable(getattr(TextParser, "setDialFrequency", None)):
        raise RuntimeError("OpenWebRX+ parser API changed")
    return mode


def install(sink):
    import owrx.service as services
    from owrx.toolbox import TextParser
    from csdr.chain.toolbox import MultimonDemodulator
    mode = check_api()
    mode.service = True
    original_handler = services.ServiceHandler

    class MonitorParser(TextParser):
        def __init__(self):
            # Log structured five-tone events ourselves, not upstream's /tmp files.
            super().__init__(filePrefix=None, service=True)

        def parse(self, line):
            sink.receive(line)
            return None

    class MonitorHandler(original_handler):
        def stopServices(self):
            super().stopServices()
            sink.status(False, "paused_or_source_stopped")

        def updateServices(self):
            with self.lock:
                self.stopServices()
                if not self.source.isAvailable():
                    sink.status(False, "source_unavailable")
                    return
                props = self.source.getProps()
                if not monitoring_in_window(sink.frequency, props["center_freq"], props["samp_rate"]):
                    sink.status(False, "frequency_outside_window")
                    return
                try:
                    chain = self.setupService(dict(mode="zvei", frequency=sink.frequency), self.source)
                    self.services.append(chain)
                    sink.status(True, "monitoring")
                except Exception:
                    sink.status(False, "decoder_error")
                    LOG.exception("Cannot start background ZVEI decoder")

        def _getSecondaryDemodulator(self, modulation):
            if modulation == "zvei":
                return MultimonDemodulator(list(DECODERS), MonitorParser())
            return super()._getSecondaryDemodulator(modulation)

    services.ServiceHandler = MonitorHandler
