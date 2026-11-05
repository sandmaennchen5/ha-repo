"""ZVEI event parsing, bounded persistent log and optional MQTT discovery."""
from datetime import datetime, timezone
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re
import threading
import time

LOG = logging.getLogger(__name__)
DECODERS = ("ZVEI1", "ZVEI2", "ZVEI3", "DZVEI", "PZVEI")
PATTERN = re.compile(r"(?:^|\s)(ZVEI1|ZVEI2|ZVEI3|DZVEI|PZVEI):\s*([0-9A-Fa-f ]+?)(?=\s+(?:ZVEI[123]|DZVEI|PZVEI):|$)")


def parse_sequences(line):
    """Accept exactly five tones; expand E (repeat tone), retain original tones."""
    if isinstance(line, bytes):
        line = line.decode("ascii", "replace")
    for match in PATTERN.finditer(line.strip()):
        tones = match[2].replace(" ", "").upper()
        if not re.fullmatch(r"[0-9E]{5}", tones) or tones[0] == "E":
            continue
        sequence = ""
        for tone in tones:
            sequence += sequence[-1] if tone == "E" else tone
        yield dict(decoder=match[1], tones=tones, sequence=sequence)


def monitoring_in_window(frequency, center, sample_rate):
    # Keep the complete NFM passband inside the sampled window.
    return abs(frequency - center) + 6000 < sample_rate / 2


def validate_monitor_options(options):
    if type(options.get("monitor_enabled", False)) is not bool:
        raise ValueError("monitor_enabled must be a boolean")
    frequency = options.get("monitor_frequency", 0)
    if type(frequency) is not int or not (frequency == 0 or 24000000 <= frequency <= 1766000000):
        raise ValueError("monitor_frequency must be 0 or a frequency in Hz from 24000000 to 1766000000")
    for key in ("mqtt_enabled", "mqtt_tls", "rds_logging"):
        if type(options.get(key, False)) is not bool:
            raise ValueError(f"{key} must be a boolean")
    if options.get("mqtt_enabled", False):
        if not isinstance(options.get("mqtt_host"), str) or not options["mqtt_host"].strip():
            raise ValueError("mqtt_host is required")
        port = options.get("mqtt_port", 1883)
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError("mqtt_port must be 1-65535")
        for key, default in (("mqtt_topic", "openwebrx/zvei"), ("rds_mqtt_topic", "openwebrx/rds")):
            if not re.fullmatch(r"[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*", options.get(key, default)):
                raise ValueError(f"{key} must contain plain topic segments without wildcards")


class EventSink:
    family = "zvei"

    def __init__(self, options, frequency, data=Path("/data"), clock=time.monotonic):
        self.frequency = frequency
        self.serial = options["rtl_serial"]
        self.clock = clock
        self.recent = {}
        self.lock = threading.RLock()
        directory = data / self.family
        directory.mkdir(parents=True, exist_ok=True)
        self.handler = RotatingFileHandler(directory / "events.jsonl", maxBytes=5 * 1024 * 1024,
                                           backupCount=5, encoding="utf-8")
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger = logging.Logger(self.family + "-events")
        self.logger.addHandler(self.handler)
        self.mqtt = None
        self.status_value = dict(monitoring=False, reason="starting", frequency_hz=frequency)
        if options.get("mqtt_enabled", False):
            self.mqtt = self.mqtt_factory(options)

    def mqtt_factory(self, options):
        return MqttEvents(options, self)

    def status(self, active, reason):
        with self.lock:
            state = dict(monitoring=bool(active), reason=reason, frequency_hz=self.frequency)
            if state == self.status_value:
                return
            self.status_value = state
            LOG.info("%s monitor: %s at %s Hz", self.family.upper(), reason, self.frequency)
            if self.mqtt:
                self.mqtt.publish_status()

    def receive(self, line):
        for parsed in parse_sequences(line):
            with self.lock:
                now = self.clock()
                self.recent = {key: value for key, value in self.recent.items() if now - value < 2}
                key = parsed["sequence"]
                if key in self.recent:
                    continue
                self.recent[key] = now
                event = dict(event_type="zvei", timestamp=datetime.now(timezone.utc).isoformat(),
                             frequency_hz=self.frequency, rtl_serial=self.serial, **parsed)
                self.logger.info(json.dumps(event, ensure_ascii=True))
                self.handler.flush()
                if self.mqtt:
                    self.mqtt.event(event)

    def close(self):
        self.status(False, "stopped")
        if self.mqtt:
            self.mqtt.close()
        self.handler.close()


class MqttEvents:
    family = "zvei"

    def __init__(self, options, sink):
        from paho.mqtt.client import Client, MQTTv311
        self.sink = sink
        self.connected = False
        self.node = "owrx_" + self.family + "_" + options["rtl_serial"]
        topic_key = "rds_mqtt_topic" if self.family == "rds" else "mqtt_topic"
        self.base = options.get(topic_key, "openwebrx/" + self.family) + "/" + options["rtl_serial"]
        self.client = Client(client_id=self.node, protocol=MQTTv311)
        self.client.max_queued_messages_set(20)
        self.client.will_set(self.base + "/availability", "offline", qos=1, retain=True)
        if options.get("mqtt_user"):
            self.client.username_pw_set(options["mqtt_user"], options.get("mqtt_password", ""))
        if options.get("mqtt_tls", False):
            self.client.tls_set()  # System trust store; certificate verification remains enabled.
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_message = self.on_message
        self.client.reconnect_delay_set(min_delay=1, max_delay=60)
        self.client.connect_async(options["mqtt_host"], options.get("mqtt_port", 1883), keepalive=30)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.connected = rc == 0
        if not self.connected:
            LOG.warning("%s MQTT connection rejected (code %s); local logging continues", self.family.upper(), rc)
            return
        client.subscribe("homeassistant/status")
        self.discovery()
        client.publish(self.base + "/availability", "online", qos=1, retain=True)
        self.publish_status()

    def on_connect_fail(self, client, userdata):
        LOG.warning("%s MQTT broker unavailable; local logging continues", self.family.upper())

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc:
            LOG.warning("%s MQTT disconnected; events remain in the local log", self.family.upper())

    def on_message(self, client, userdata, message):
        if message.topic == "homeassistant/status" and message.payload == b"online":
            self.discovery()
            self.publish_status()

    def discovery(self):
        device = dict(identifiers=[self.node], name="OpenWebRX+ ZVEI",
                      manufacturer="Local HAOS add-on", model="RTL-SDR ZVEI monitor")
        common = dict(device=device, availability_topic=self.base + "/availability")
        entities = {
            "event": dict(name="Tonfolge", event_types=["zvei"], state_topic=self.base + "/event"),
            "sensor": dict(name="Letzte Tonfolge", state_topic=self.base + "/last",
                           value_template="{{ value_json.sequence }}", json_attributes_topic=self.base + "/last"),
            "binary_sensor": dict(name="Überwachung", state_topic=self.base + "/status",
                                  value_template="{{ 'ON' if value_json.monitoring else 'OFF' }}",
                                  json_attributes_topic=self.base + "/status"),
        }
        for component, fields in entities.items():
            payload = dict(common, unique_id=self.node + "_" + component, **fields)
            self.client.publish(f"homeassistant/{component}/{self.node}/config", json.dumps(payload), qos=1, retain=True)

    def publish_status(self):
        if self.connected:
            self.client.publish(self.base + "/status", json.dumps(self.sink.status_value), qos=1, retain=True)

    def event(self, event):
        if self.connected:
            payload = json.dumps(event)
            # Never retain/replay an alarm event after reconnect or HA restart.
            self.client.publish(self.base + "/event", payload, qos=0, retain=False)
            self.client.publish(self.base + "/last", payload, qos=1, retain=True)

    def close(self):
        try:
            if self.connected:
                result = self.client.publish(self.base + "/availability", "offline", qos=1, retain=True)
                result.wait_for_publish(timeout=2)
        except RuntimeError:
            LOG.warning("MQTT offline announcement failed; broker Last Will remains configured")
        finally:
            self.client.disconnect()
            self.client.loop_stop()
