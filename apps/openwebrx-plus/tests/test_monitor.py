import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

BASE = Path(__file__).resolve().parents[1] / "rootfs/opt/ha-openwebrx"
spec = importlib.util.spec_from_file_location("monitor", BASE / "monitor.py")
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class MonitorTests(unittest.TestCase):
    def test_five_tones_repeat_tone_and_invalid_input(self):
        events = list(monitor.parse_sequences(b"ZVEI1: 1E2E3 ZVEI2: 12345"))
        self.assertEqual([e["sequence"] for e in events], ["11223", "12345"])
        self.assertEqual(events[0]["tones"], "1E2E3")
        for line in ("ZVEI1: 1234", "ZVEI1: 123456", "ZVEI1: E1234", "ZVEI1: 12A45", "DTMF: 12345", "noise"):
            self.assertEqual(list(monitor.parse_sequences(line)), [])

    def test_window_margin_and_retuning(self):
        self.assertTrue(monitor.monitoring_in_window(85000000, 85000000, 1024000))
        self.assertFalse(monitor.monitoring_in_window(85000000, 100000000, 2400000))
        self.assertFalse(monitor.monitoring_in_window(85000000, 85510000, 1024000))

    def test_durable_log_deduplication_and_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            now = [0.0]
            sink = monitor.EventSink({"rtl_serial": "00001002"}, 85000000, data, clock=lambda: now[0])
            sink.receive(b"ZVEI1: 12345")
            sink.receive(b"ZVEI2: 12345")
            now[0] = 3
            sink.receive(b"ZVEI1: 12345")
            sink.close()
            sink = monitor.EventSink({"rtl_serial": "00001002"}, 85000000, data)
            sink.receive(b"ZVEI1: 67890")
            sink.close()
            events = [json.loads(line) for line in (data / "zvei/events.jsonl").read_text().splitlines()]
            self.assertEqual([e["sequence"] for e in events], ["12345", "12345", "67890"])
            self.assertEqual(events[0]["frequency_hz"], 85000000)
            self.assertTrue(events[0]["timestamp"].endswith("+00:00"))
            self.assertEqual(sink.handler.maxBytes, 5 * 1024 * 1024)
            self.assertEqual(sink.handler.backupCount, 5)

    def test_mqtt_events_not_retained_or_replayed(self):
        mqtt = monitor.MqttEvents.__new__(monitor.MqttEvents)
        mqtt.base = "openwebrx/zvei/00001002"
        mqtt.client = MagicMock()
        mqtt.connected = False
        mqtt.event({"event_type": "zvei", "sequence": "12345"})
        mqtt.client.publish.assert_not_called()
        mqtt.connected = True
        mqtt.event({"event_type": "zvei", "sequence": "12345"})
        calls = mqtt.client.publish.call_args_list
        self.assertTrue(calls[0].args[0].endswith("/event"))
        self.assertFalse(calls[0].kwargs["retain"])
        self.assertTrue(calls[1].args[0].endswith("/last"))
        self.assertTrue(calls[1].kwargs["retain"])

    def test_discovery_and_reconnect_status(self):
        mqtt = monitor.MqttEvents.__new__(monitor.MqttEvents)
        mqtt.base = "openwebrx/zvei/00001002"
        mqtt.node = "owrx_zvei_00001002"
        mqtt.client = MagicMock()
        mqtt.sink = MagicMock(status_value={"monitoring": False, "reason": "frequency_outside_window"})
        mqtt.on_connect(mqtt.client, None, {}, 0)
        mqtt.client.subscribe.assert_called_once_with("homeassistant/status")
        calls = mqtt.client.publish.call_args_list
        configs = [json.loads(c.args[1]) for c in calls if c.args[0].endswith("/config")]
        self.assertEqual(len(configs), 3)
        self.assertEqual(len({c["unique_id"] for c in configs}), 3)
        self.assertTrue(any(c.get("event_types") == ["zvei"] for c in configs))
        self.assertEqual(json.loads(calls[-1].args[1])["reason"], "frequency_outside_window")
        before = mqtt.client.publish.call_count
        message = MagicMock(topic="homeassistant/status", payload=b"online")
        mqtt.on_message(mqtt.client, None, message)
        self.assertEqual(mqtt.client.publish.call_count - before, 4)

    def test_invalid_mqtt_configuration(self):
        for values in ({"monitor_frequency": 100}, {"monitor_frequency": True},
                       {"mqtt_enabled": True, "mqtt_host": ""},
                       {"mqtt_enabled": True, "mqtt_host": "broker", "mqtt_topic": "alarm/#"}):
            with self.assertRaises(ValueError):
                monitor.validate_monitor_options(values)


if __name__ == "__main__":
    unittest.main()
