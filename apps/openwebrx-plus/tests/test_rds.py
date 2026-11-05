import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import MagicMock, patch

BASE = Path(__file__).resolve().parents[1] / "rootfs/opt/ha-openwebrx"
sys.path.insert(0, str(BASE))
import rds


class RdsTests(unittest.TestCase):
    def test_partial_updates_and_group_only_duplicates(self):
        state = rds.RdsAccumulator()
        first = state.update({"pi": "0xd3c2", "ps": "MDR JUMP", "group": "0A"}, 100000000)
        self.assertEqual(first["pi"], "0xD3C2")
        second = state.update({"pi": "0xD3C2", "radiotext": "Title", "ta": False}, 100000000)
        self.assertEqual(second["ps"], "MDR JUMP")
        self.assertEqual(second["radiotext"], "Title")
        self.assertFalse(second["ta"])
        self.assertEqual(state.update({"group": "2A"}, 100000000), second)

    def test_retune_and_pi_change_do_not_mix_stations(self):
        state = rds.RdsAccumulator()
        state.update({"pi": "0x1234", "ps": "FIRST", "radiotext": "Old title"}, 100000000)
        self.assertIsNone(state.update({"radiotext": "Partial"}, 101000000))
        result = state.update({"pi": "0x5678", "ps": "SECOND"}, 101000000)
        self.assertNotIn("radiotext", result)
        self.assertEqual(result["frequency_hz"], 101000000)
        result = state.update({"pi": "0x1111"}, 101000000)
        self.assertNotIn("ps", result)
        self.assertNotIn("radiotext", result)

    def test_invalid_input_and_text_limits(self):
        state = rds.RdsAccumulator()
        for value, frequency in (({}, 100000000), ({"pi": "bad"}, 100000000),
                                 ({"pi": "0x1234"}, 145000000), ([], 100000000)):
            self.assertIsNone(state.update(value, frequency))
        result = state.update({"pi": 4660, "ps": "123456789", "radiotext": "x" * 100}, 100000000)
        self.assertEqual(result["pi"], "0x1234")
        self.assertEqual(len(result["ps"]), 8)
        self.assertEqual(len(result["radiotext"]), 64)

    def test_persistent_log_dedup_and_no_old_radiotext(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            sink = rds.RdsSink({"rtl_serial": "00001002"}, data=path)
            first = {"frequency_hz": 100000000, "pi": "0x1234", "ps": "STATION", "radiotext": "Title"}
            sink.receive_metadata(first)
            sink.receive_metadata(first)
            sink.receive_metadata({"frequency_hz": 101000000, "pi": "0x5678"})
            sink.receive_metadata({"frequency_hz": 100000000, "pi": "0x1234"})
            self.assertNotIn("radiotext", sink.last_event)
            sink.close()
            events = [json.loads(line) for line in (path / "rds/events.jsonl").read_text().splitlines()]
            self.assertEqual(len(events), 3)
            self.assertEqual(events[0]["event_type"], "rds")
            self.assertTrue(events[0]["timestamp"].endswith("+00:00"))
            sink = rds.RdsSink({"rtl_serial": "00001002"}, data=path)
            sink.receive_metadata(first)
            sink.close()
            self.assertEqual(len((path / "rds/events.jsonl").read_text().splitlines()), 4)

    def test_mqtt_sensor_discovery_and_reconnect_without_event_replay(self):
        mqtt = rds.RdsMqtt.__new__(rds.RdsMqtt)
        mqtt.node = "owrx_rds_00001002"
        mqtt.base = "openwebrx/rds/00001002"
        mqtt.connected = True
        mqtt.client = MagicMock()
        mqtt.sink = MagicMock(last_event={"event_type": "rds", "pi": "0x1234"})
        mqtt.on_connect(mqtt.client, None, {}, 0)
        calls = mqtt.client.publish.call_args_list
        configs = [json.loads(c.args[1]) for c in calls if c.args[0].endswith("/config")]
        self.assertEqual(len(configs), 5)
        self.assertEqual(len({c["unique_id"] for c in configs}), 5)
        self.assertTrue(all(c["state_topic"] == mqtt.base + "/last" for c in configs))
        self.assertTrue(any(c.get("unit_of_measurement") == "MHz" for c in configs))
        self.assertTrue(calls[-1].args[0].endswith("/last"))
        self.assertFalse(any(c.args[0].endswith("/event") for c in calls))

    def test_parser_hook_preserves_browser_result_and_survives_log_error(self):
        class Parser:
            frequency = 100000000
            def parse(self, line):
                return browser_result
            def setDialFrequency(self, frequency):
                self.frequency = frequency

        browser_result = {"ps": "BROWSER"}
        toolbox = ModuleType("owrx.toolbox")
        toolbox.RdsParser = Parser
        root = ModuleType("owrx")
        root.toolbox = toolbox
        sink = MagicMock()
        with patch.dict(sys.modules, {"owrx": root, "owrx.toolbox": toolbox}):
            rds.install(sink)
            parser = Parser()
            self.assertIs(parser.parse(b'{"pi":"0x1234","ps":"STATION"}'), browser_result)
            self.assertEqual(sink.receive_metadata.call_args.args[0]["ps"], "STATION")
            parser.setDialFrequency(101000000)
            parser.parse(b'{"radiotext":"not complete"}')
            self.assertEqual(sink.receive_metadata.call_count, 1)
            sink.receive_metadata.side_effect = OSError("disk full")
            with self.assertLogs("rds", level="ERROR"):
                self.assertIs(parser.parse(b'{"pi":"0x5678"}'), browser_result)


if __name__ == "__main__":
    unittest.main()
