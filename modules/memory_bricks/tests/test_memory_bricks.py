from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from app.schemas.brick_schema import BrickModel
from app.services.create_brick import create_brick
from app.services.export_bricks import export_bricks
from app.services.handoff_bricks import handoff_bricks
from app.services.link_bricks import link_bricks
from app.services.list_bricks import list_bricks
from app.services.merge_bricks import merge_bricks
from app.services.rebuild_index import rebuild_index
from app.services.show_brick import show_brick
from app.services.update_status import update_status


class MemoryBricksTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        os.environ["MEMORY_BRICKS_STATE_ROOT"] = str(Path(self.tmpdir.name) / "state")

    def tearDown(self) -> None:
        os.environ.pop("MEMORY_BRICKS_STATE_ROOT", None)
        self.tmpdir.cleanup()

    def create_sample(self, **overrides):
        payload = {
            "brick_type": "resume_point",
            "title": "Sample Brick",
            "ia": "chatgpt",
            "machine": "student",
            "surface": "terminal_linux",
            "project": "opt-trading",
            "module_name": "memory_bricks",
            "status": "resumed",
            "summary_short": "Short summary.",
            "resume_point": "Continue here.",
            "tags": ["memory", "test"],
        }
        payload.update(overrides)
        return create_brick(**payload)

    def test_brick_model_validate(self) -> None:
        brick = BrickModel(
            id="MB-00001",
            title="Test",
            date="2026-03-25T10:00:00-04:00",
            type="reference",
            status="draft",
            ia="chatgpt",
            machine="student",
            surface="terminal_linux",
            project="opt-trading",
            module="memory_bricks",
            summary_short="hello",
            resume_point="next",
            links=["MB-00002"],
        )
        brick.validate()

    def test_create_list_show_status_and_link(self) -> None:
        first = self.create_sample(title="First Brick")
        second = self.create_sample(title="Second Brick", brick_type="reference", status="open", ia="claude")

        rows = list_bricks({"status": "", "type": "", "project": "", "module": "", "machine": "", "ia": "", "surface": "", "tag": ""})
        self.assertEqual(len(rows), 2)
        self.assertIn(first["id"], rows[0])

        before, after = update_status(first["id"], "closed")
        self.assertEqual(before, "resumed")
        self.assertEqual(after, "closed")

        link_bricks(first["id"], second["id"])
        content = show_brick(first["id"])
        self.assertIn(second["id"], content)
        self.assertIn('status: "closed"', content)

    def test_rebuild_export_merge_and_handoff(self) -> None:
        first = self.create_sample(title="First Brick", decisions=["Keep V1 local"], todo=["Write tests"])
        second = self.create_sample(title="Second Brick", brick_type="decision", ia="claude", decisions=["Keep V1 local", "Expose handoff"], todo=["Write docs"], summary_short="Second summary.")

        outputs = rebuild_index()
        self.assertTrue(any(path.endswith("index_short.md") for path in outputs))
        self.assertTrue(any(path.endswith("index_full.json") for path in outputs))

        txt_path = Path(export_bricks([first["id"], second["id"]], "txt"))
        json_path = Path(export_bricks([first["id"], second["id"]], "json"))
        md_path = Path(export_bricks([first["id"], second["id"]], "md"))
        merge_path = Path(merge_bricks([first["id"], second["id"]]))
        handoff_path = Path(handoff_bricks([first["id"], second["id"]], "claude"))

        self.assertTrue(txt_path.is_file())
        self.assertTrue(json_path.is_file())
        self.assertTrue(md_path.is_file())
        self.assertTrue(merge_path.is_file())
        self.assertTrue(handoff_path.is_file())
        self.assertIn("Keep V1 local", merge_path.read_text(encoding="utf-8"))
        self.assertIn("HANDOFF CLAUDE", handoff_path.read_text(encoding="utf-8"))

    def test_cli_end_to_end(self) -> None:
        env = os.environ.copy()
        cmd = [
            "bash",
            str(MODULE_DIR / "scripts" / "cmd.sh"),
            "new",
            "--type",
            "resume_point",
            "--title",
            "CLI Brick",
            "--ia",
            "chatgpt",
            "--machine",
            "student",
            "--surface",
            "terminal_linux",
            "--project",
            "opt-trading",
            "--module",
            "memory_bricks",
            "--status",
            "resumed",
            "--summary-short",
            "CLI summary.",
            "--resume-point",
            "CLI continue.",
        ]
        created = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        self.assertIn("CREATED: MB-00001", created.stdout)

        listed = subprocess.run(["bash", str(MODULE_DIR / "scripts" / "cmd.sh"), "list"], check=True, capture_output=True, text=True, env=env)
        self.assertIn("MB-00001", listed.stdout)


if __name__ == "__main__":
    unittest.main()
