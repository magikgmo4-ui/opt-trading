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
from app.storage.markdown_store import load_brick, load_all_bricks
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

    def run_cli(self, *args, env=None):
        return subprocess.run(
            ["bash", str(MODULE_DIR / "scripts" / "cmd.sh"), *args],
            capture_output=True,
            text=True,
            env=env or os.environ.copy(),
        )

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

    def test_brick_model_rejects_invalid_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid date"):
            BrickModel(
                id="MB-00001",
                title="Test",
                date="not-a-date",
                type="reference",
                status="draft",
                ia="chatgpt",
                machine="student",
                surface="terminal_linux",
                project="opt-trading",
                module="memory_bricks",
                summary_short="hello",
            ).validate()

        with self.assertRaisesRegex(ValueError, "Invalid ia"):
            BrickModel(
                id="MB-00001",
                title="Test",
                date="2026-03-25T10:00:00-04:00",
                type="reference",
                status="draft",
                ia="bad-ia",
                machine="student",
                surface="terminal_linux",
                project="opt-trading",
                module="memory_bricks",
                summary_short="hello",
            ).validate()

        with self.assertRaisesRegex(ValueError, "summary_short cannot be empty"):
            BrickModel(
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
                summary_short="",
            ).validate()

    def test_brick_model_normalizes_lists(self) -> None:
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
            links=[" MB-00002 ", "", "MB-00003"],
            tags=[" test ", "", "memory"],
        )
        self.assertEqual(brick.links, ["MB-00002", "MB-00003"])
        self.assertEqual(brick.tags, ["test", "memory"])

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

    def test_missing_brick_operations_fail_cleanly(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "Brick not found"):
            update_status("MB-99999", "closed")

        existing = self.create_sample(title="Existing Brick")
        with self.assertRaisesRegex(FileNotFoundError, "Brick not found"):
            link_bricks(existing["id"], "MB-99999")

    def test_duplicate_file_and_invalid_frontmatter_are_detected(self) -> None:
        created = self.create_sample(title="Dup Brick")
        first_path = Path(created["file"])
        duplicate_path = first_path.with_name(f"{created['id']}__duplicate.md")
        duplicate_path.write_text(first_path.read_text(encoding="utf-8"), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Multiple brick files found"):
            load_brick(created["id"])

        duplicate_path.unlink()
        first_path.write_text("# no frontmatter\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Markdown file missing frontmatter"):
            load_all_bricks()

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

    def test_export_merge_and_handoff_reject_empty_dataset(self) -> None:
        with self.assertRaisesRegex(ValueError, "No brick ids provided"):
            export_bricks([], "txt")
        with self.assertRaisesRegex(ValueError, "No brick ids provided"):
            merge_bricks([])
        with self.assertRaisesRegex(ValueError, "No brick ids provided"):
            handoff_bricks([], "claude")

    def test_rebuild_index_fails_on_incoherent_dataset(self) -> None:
        self.create_sample(title="Healthy Brick")
        bad_path = Path(os.environ["MEMORY_BRICKS_STATE_ROOT"]) / "bricks" / "MB-99999__bad.md"
        bad_path.write_text(
            "---\nid: \"MB-99999\"\ntitle: \"Bad\"\ndate: \"bad-date\"\ntimezone: \"America/Montreal\"\ntype: \"reference\"\nstatus: \"draft\"\nia: \"chatgpt\"\nmachine: \"student\"\nsurface: \"terminal_linux\"\nproject: \"opt-trading\"\nmodule: \"memory_bricks\"\nsummary_short: \"bad\"\nresume_point: \"\"\nlinks: []\ntags: []\nrepo: \"\"\nbranch: \"\"\npath: \"\"\nsource_ref: []\ncanonical_ref: []\nreal_state_ref: []\nvalidated_by: \"\"\ndecisions: []\ntodo: []\n---\n\n# bad\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "Invalid date"):
            rebuild_index()

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

    def test_query_cli_reads_existing_source_without_writes(self) -> None:
        first = self.create_sample(
            title="LocalCMS Seed",
            summary_short="LocalCMS seed brick.",
            resume_point="Read the persisted LocalCMS dataset here.",
            tags=["localcms", "viewer"],
        )
        second = self.create_sample(
            title="Viewer Contract",
            brick_type="decision",
            status="open",
            ia="claude",
            summary_short="Viewer consumes index_full.json in read-only mode.",
            decisions=["needle-decision"],
            tags=["contract", "readonly"],
        )
        rebuild_index()

        status = self.run_cli("query", "status")
        self.assertEqual(status.returncode, 0)
        self.assertIn(f"ROOT: {os.environ['MEMORY_BRICKS_STATE_ROOT']}", status.stdout)
        self.assertIn("BRICKS: 2", status.stdout)
        self.assertIn("INDEX_FULL: yes", status.stdout)
        self.assertIn("SEQUENCE: yes", status.stdout)

        listed = self.run_cli("query", "list", "--ia", "claude")
        self.assertEqual(listed.returncode, 0)
        self.assertIn(second["id"], listed.stdout)
        self.assertNotIn(first["id"], listed.stdout)

        shown = self.run_cli("query", "show", "--id", first["id"])
        self.assertEqual(shown.returncode, 0)
        self.assertIn("LocalCMS Seed", shown.stdout)

        found = self.run_cli("query", "find", "--text", "needle-decision")
        self.assertEqual(found.returncode, 0)
        self.assertIn(second["id"], found.stdout)

    def test_query_cli_does_not_create_state_dirs(self) -> None:
        root = Path(self.tmpdir.name) / "query-read-only-root"
        os.environ["MEMORY_BRICKS_STATE_ROOT"] = str(root)
        env = os.environ.copy()

        status = self.run_cli("query", "status", env=env)
        self.assertEqual(status.returncode, 0)
        self.assertIn("ROOT_EXISTS: no", status.stdout)
        self.assertFalse(root.exists())

        listed = self.run_cli("query", "list", env=env)
        self.assertEqual(listed.returncode, 0)
        self.assertEqual(listed.stdout, "")
        self.assertFalse(root.exists())

        found = self.run_cli("query", "find", "--text", "localcms", env=env)
        self.assertEqual(found.returncode, 0)
        self.assertEqual(found.stdout, "")
        self.assertFalse(root.exists())

        shown = self.run_cli("query", "show", "--id", "MB-99999", env=env)
        self.assertNotEqual(shown.returncode, 0)
        self.assertIn("ERROR: Brick not found", shown.stderr)
        self.assertFalse(root.exists())

    def test_cli_errors_return_non_zero_with_minimal_message(self) -> None:
        env = os.environ.copy()

        missing = subprocess.run(
            ["bash", str(MODULE_DIR / "scripts" / "cmd.sh"), "show", "--id", "MB-99999"],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("ERROR: Brick not found", missing.stderr)

        invalid_ia = subprocess.run(
            [
                "bash",
                str(MODULE_DIR / "scripts" / "cmd.sh"),
                "new",
                "--type",
                "resume_point",
                "--title",
                "CLI Brick",
                "--ia",
                "bad-ia",
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
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(invalid_ia.returncode, 0)
        self.assertIn("ERROR: Invalid ia: bad-ia", invalid_ia.stderr)


if __name__ == "__main__":
    unittest.main()
