"""Start upstream with optional shared-source ZVEI and RDS extensions."""
import json
from pathlib import Path
from configure import read_options
from monitor import EventSink


def main():
    sinks = []
    options = read_options()
    zvei_sink = rds_sink = None
    try:
        if options.get("monitor_enabled", False):
            settings = json.loads(Path("/data/openwebrx/settings.json").read_text(encoding="utf-8"))
            frequency = settings["sdrs"]["dedicated_rtl"]["profiles"]["_zvei_monitor"]["start_freq"]
            zvei_sink = EventSink(options, frequency)
            sinks.append(zvei_sink)
        if options.get("rds_logging", True):
            from rds import RdsSink
            rds_sink = RdsSink(options)
            sinks.append(rds_sink)
        if sinks:
            from owrx.config.core import CoreConfig
            original_load = CoreConfig.load

            def load(file=None):
                original_load(file)
                if zvei_sink:
                    from background import install
                    install(zvei_sink)
                if rds_sink:
                    from rds import install
                    install(rds_sink)

            CoreConfig.load = staticmethod(load)
        from owrx.__main__ import main as upstream_main
        return upstream_main()
    finally:
        for sink in reversed(sinks):
            sink.close()


if __name__ == "__main__":
    raise SystemExit(main())
