"""Capture existing WFM RDS metadata, preserving upstream browser output."""
from collections import OrderedDict
from datetime import datetime, timezone
import json
import logging
import re

from monitor import EventSink, MqttEvents

LOG = logging.getLogger(__name__)


class RdsAccumulator:
    def __init__(self):
        self.frequency = None
        self.values = {}

    def update(self, data, frequency):
        if type(frequency) not in (int, float) or not 87500000 <= frequency <= 108000000:
            self.frequency, self.values = None, {}
            return None
        frequency = int(frequency)
        if frequency != self.frequency:
            self.frequency, self.values = frequency, {}
        if not isinstance(data, dict):
            return None
        pi = data.get("pi")
        if pi is not None:
            if type(pi) is int and 0 <= pi <= 65535:
                pi = f"0x{pi:04X}"
            elif isinstance(pi, str) and re.fullmatch(r"0[xX][0-9a-fA-F]{4}", pi):
                pi = "0x" + pi[2:].upper()
            else:
                return None
            if pi != self.values.get("pi"):
                self.values = {"pi": pi}
        if "pi" not in self.values:
            return None
        for key, maximum in (("ps", 8), ("radiotext", 64), ("prog_type", 64)):
            if isinstance(data.get(key), str):
                self.values[key] = "".join(c for c in data[key] if c.isprintable()).strip()[:maximum]
        for key in ("tp", "ta"):
            if type(data.get(key)) is bool:
                self.values[key] = data[key]
        return dict(frequency_hz=frequency, **self.values)


class RdsSink(EventSink):
    family = "rds"

    def __init__(self, options, **kwargs):
        self.stations = OrderedDict()
        self.last_event = None
        super().__init__(options, 0, **kwargs)

    def mqtt_factory(self, options):
        return RdsMqtt(options, self)

    def receive_metadata(self, values):
        with self.lock:
            key = (values["frequency_hz"], values["pi"])
            previous = self.stations.get(key, {})
            # Values are a complete parser snapshot. Do not carry radiotext
            # over from a previous tuning session or another station.
            merged = dict(values)
            last_key = None if self.last_event is None else (self.last_event["frequency_hz"], self.last_event["pi"])
            if merged == previous and last_key == key:
                return
            self.stations[key] = merged
            self.stations.move_to_end(key)
            while len(self.stations) > 128:
                self.stations.popitem(last=False)
            event = dict(event_type="rds", timestamp=datetime.now(timezone.utc).isoformat(),
                         rtl_serial=self.serial, **merged)
            self.last_event = event
            self.logger.info(json.dumps(event, ensure_ascii=True))
            self.handler.flush()
            if self.mqtt:
                self.mqtt.event(event)


class RdsMqtt(MqttEvents):
    family = "rds"

    def discovery(self):
        device = dict(identifiers=[self.node], name="OpenWebRX+ RDS",
                      manufacturer="Local HAOS add-on", model="WFM RDS metadata")
        fields = {
            "station": ("Zuletzt empfangener Sender", "{{ value_json.ps | default(value_json.pi, true) }}", {}),
            "pi": ("RDS PI", "{{ value_json.pi }}", {}),
            "radiotext": ("Radiotext", "{{ value_json.radiotext | default('') }}", {}),
            "frequency": ("RDS Frequenz", "{{ value_json.frequency_hz / 1000000 }}", {"unit_of_measurement": "MHz"}),
            "programme": ("Programmtyp", "{{ value_json.prog_type | default('') }}", {}),
        }
        for key, (name, template, extra) in fields.items():
            payload = dict(device=device, name=name, unique_id=self.node + "_" + key,
                           state_topic=self.base + "/last", value_template=template,
                           json_attributes_topic=self.base + "/last",
                           availability_topic=self.base + "/availability", **extra)
            self.client.publish(f"homeassistant/sensor/{self.node}/{key}/config",
                                json.dumps(payload), qos=1, retain=True)

    def publish_status(self):
        # Refresh last-known metadata after a broker/HA restart, never an event.
        if self.connected and self.sink.last_event is not None:
            self.client.publish(self.base + "/last", json.dumps(self.sink.last_event), qos=1, retain=True)


def check_api():
    from owrx.toolbox import RdsParser
    for name in ("parse", "setDialFrequency"):
        if not callable(getattr(RdsParser, name, None)):
            raise RuntimeError(f"OpenWebRX+ RDS parser API changed: {name}")


def install(sink):
    check_api()
    from owrx.toolbox import RdsParser
    original = RdsParser.parse

    def parse(parser, message):
        result = original(parser, message)
        try:
            data = json.loads(message)
            if not hasattr(parser, "_ha_rds_accumulator"):
                parser._ha_rds_accumulator = RdsAccumulator()
            values = parser._ha_rds_accumulator.update(data, parser.frequency)
            if values:
                sink.receive_metadata(values)
        except Exception:
            # Logging/MQTT failure must not interrupt audio or browser metadata.
            LOG.exception("Cannot record RDS metadata")
        return result

    RdsParser.parse = parse
