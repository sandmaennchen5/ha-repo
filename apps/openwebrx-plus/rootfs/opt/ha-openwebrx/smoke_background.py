"""Build-time test with a real OpenWebRX DSP chain but no USB hardware."""
import threading
from pathlib import Path
from owrx.config.core import CoreConfig
CoreConfig.load(Path("/etc/openwebrx/openwebrx.conf"))
from pycsdr.modules import Buffer
from pycsdr.types import Format
from background import install


class Sink:
    frequency = 145500000
    def status(self, active, reason):
        self.active, self.reason = active, reason
    def receive(self, line):
        pass


class Source:
    props = dict(center_freq=145500000, samp_rate=1024000)
    buffer = Buffer(Format.COMPLEX_FLOAT)
    def isAvailable(self):
        return True
    def getProps(self):
        return self.props
    def getBuffer(self):
        return self.buffer


sink = Sink()
install(sink)
from owrx.service import ServiceHandler
handler = ServiceHandler.__new__(ServiceHandler)
handler.source = Source()
handler.lock = threading.RLock()
handler.services, handler.resamplers = [], []
try:
    handler.updateServices()
    assert sink.active and len(handler.services) == 1, "Background DSP chain did not start"
    handler.source.props["center_freq"] = 100000000
    handler.updateServices()
    assert not sink.active and not handler.services, "Retuning did not stop the monitor"
    assert sink.reason == "frequency_outside_window"
finally:
    handler.stopServices()
print("Background DSP creation, shutdown and retuning smoke test passed")
