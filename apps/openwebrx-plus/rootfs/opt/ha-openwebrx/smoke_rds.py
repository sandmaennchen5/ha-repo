"""Build-time RDS parser-hook test with real upstream classes, without RF."""
from pathlib import Path
from owrx.config.core import CoreConfig
CoreConfig.load(Path("/etc/openwebrx/openwebrx.conf"))
from owrx.toolbox import RdsParser
from rds import install


class Sink:
    events = []
    def receive_metadata(self, values):
        self.events.append(values)


sink = Sink()
install(sink)
parser = RdsParser()
parser.setDialFrequency(100000000)
result = parser.parse(b'{"pi":"0x1234","ps":"TEST FM"}')
assert result["ps"] == "TEST FM", "Browser metadata changed"
assert sink.events[-1]["ps"] == "TEST FM", "RDS hook did not capture metadata"
parser.setDialFrequency(101000000)
parser.parse(b'{"pi":"0x5678","ps":"SECOND"}')
assert sink.events[-1]["frequency_hz"] == 101000000
assert sink.events[-1]["pi"] == "0x5678"
print("RDS parser hook and retuning smoke test passed")
