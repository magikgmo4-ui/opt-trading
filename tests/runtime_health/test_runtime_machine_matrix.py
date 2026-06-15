from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.runtime_machine_matrix import build_records, render_markdown


class TestRuntimeMachineMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = build_records(REPO_ROOT / "config" / "machine_runtime_map.yml")
        cls.by_machine = {record["machine"]: record for record in cls.records}

    def test_all_expected_machines_present(self):
        for machine in ["admin-trading", "db-layer", "cursor-ai", "fantome", "student"]:
            self.assertIn(machine, self.by_machine)

    def test_cursor_ai_is_windows_task_model(self):
        record = self.by_machine["cursor-ai"]
        self.assertEqual(record["os_family"], "windows")
        self.assertEqual(record["activation_model"], "windows_task")
        self.assertEqual(record["required_services"], [])

    def test_fantome_contains_openclaw_gateway(self):
        record = self.by_machine["fantome"]
        self.assertIn("openclaw-gateway.service", record["required_services"])
        self.assertIn("localcms:127.0.0.1:8700", record["required_ports"])

    def test_db_layer_algo_hf_api_port_is_9100(self):
        record = self.by_machine["db-layer"]
        self.assertIn("algo_hf_api:127.0.0.1:9100", record["optional_ports"])

    def test_markdown_render_mentions_activation_surfaces(self):
        text = render_markdown(self.records)
        self.assertIn("Runtime Machine Matrix", text)
        self.assertIn("config/machine_runtime_map.yml", text)
        self.assertIn("deploy/systemd/openclaw-gateway.service", text)


if __name__ == "__main__":
    unittest.main()
