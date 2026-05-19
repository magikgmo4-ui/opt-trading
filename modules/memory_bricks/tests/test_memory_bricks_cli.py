from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CMD_PATH = REPO_ROOT / "modules" / "memory_bricks" / "cmd.sh"


class MemoryBricksCliTests(unittest.TestCase):
    def test_new_link_index_and_status_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_root = Path(temp_dir) / "state"
            payload_path = Path(temp_dir) / "brick.json"
            payload_path.write_text(
                json.dumps(
                    {
                        "title": "First Brick",
                        "type": "decision",
                        "summary_short": "Short summary",
                        "resume_point": "GO_NEXT",
                        "tags": ["alpha"],
                        "decisions": ["keep"],
                        "todo": ["check"],
                    }
                ),
                encoding="utf-8",
            )

            created = self._run(state_root, "new", "--payload-file", str(payload_path))
            self.assertEqual(created["status"], "created")
            self.assertEqual(created["id"], "MB-00001")

            linked = self._run(state_root, "link", "--id", "MB-00001", "--target", "KIL-123")
            self.assertEqual(linked["status"], "linked")

            rebuilt = self._run(state_root, "index", "rebuild")
            self.assertEqual(rebuilt["status"], "rebuilt")
            self.assertTrue((state_root / "index_full.json").exists())
            self.assertTrue((state_root / "index_short.md").exists())

            status = self._run(state_root, "query", "status")
            self.assertTrue(status["root_exists"])
            self.assertTrue(status["bricks_dir"])
            self.assertEqual(status["bricks"], 1)
            self.assertTrue(status["index_full"])
            self.assertTrue(status["index_short"])
            self.assertTrue(status["sequence"])

            brick_payload = json.loads((state_root / "bricks" / "MB-00001.json").read_text(encoding="utf-8"))
            self.assertEqual(brick_payload["links"], ["KIL-123"])

    def test_new_accepts_kil_wrapped_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_root = Path(temp_dir) / "state"
            payload_path = Path(temp_dir) / "wrapped.json"
            payload_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "KIL-XYZ",
                        "capitalization_id": "CAP-XYZ",
                        "brick": {
                            "title": "Wrapped Brick",
                            "type": "decision",
                            "summary_short": "From KIL",
                            "resume_point": "GO_WRAP",
                            "links": ["KIL-XYZ", "CAP-XYZ"],
                        },
                    }
                ),
                encoding="utf-8",
            )

            created = self._run(state_root, "new", "--payload-file", str(payload_path))
            self.assertEqual(created["id"], "MB-00001")
            brick_payload = json.loads((state_root / "bricks" / "MB-00001.json").read_text(encoding="utf-8"))
            self.assertEqual(brick_payload["title"], "Wrapped Brick")
            self.assertEqual(brick_payload["links"], ["KIL-XYZ", "CAP-XYZ"])

    def test_missing_brick_returns_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_root = Path(temp_dir) / "state"
            completed = self._run_raw(state_root, "link", "--id", "MB-99999", "--target", "KIL-404")
            self.assertEqual(completed.returncode, 2)
            payload = json.loads(completed.stderr.strip())
            self.assertEqual(payload["status"], "error")

    def _run(self, state_root: Path, *args: str) -> dict[str, object]:
        completed = self._run_raw(state_root, *args)
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        return json.loads(completed.stdout.strip())

    def _run_raw(self, state_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["MEMORY_BRICKS_STATE_ROOT"] = str(state_root)
        return subprocess.run(
            ["bash", str(CMD_PATH), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
