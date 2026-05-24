import os
import shutil
import tempfile
import unittest
import json
import io
from unittest.mock import patch
from scripts.ai.workers.doc_ops_create_chantier import validate_go_id, create_chantier, main

class TestDocOpsCreateChantier(unittest.TestCase):
    def test_validate_go_id(self):
        self.assertTrue(validate_go_id("GO_PROJECT_01")[0])
        self.assertTrue(validate_go_id("GO_PROJECT_A_01")[0])
        self.assertTrue(validate_go_id("GO_123_45")[0])

        self.assertFalse(validate_go_id("go_project_01")[0])
        self.assertFalse(validate_go_id("GO_PROJECT")[0])
        self.assertFalse(validate_go_id("GO-PROJECT-01")[0])
        self.assertFalse(validate_go_id("GO PROJECT 01")[0])
        self.assertFalse(validate_go_id("PROJECT_01")[0])

class TestCreateChantierIntegrated(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers")
        os.makedirs("docs/index/inbox")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_integrated_creation(self):
        go_id = "GO_TEST_PROJECT_01"
        success, result = create_chantier(go_id, "Test Summary", create_inbox=True)

        self.assertTrue(success)
        self.assertTrue(os.path.exists(f"docs/chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md"))
        self.assertTrue(os.path.exists(f"docs/index/inbox/{go_id}.md"))

        with open(f"docs/chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md", "r") as f:
            content = f.read()
            self.assertIn(go_id, content)
            self.assertIn("Test Summary", content)

    def test_dry_run_no_write(self):
        go_id = "GO_DRY_RUN_01"
        success, result = create_chantier(go_id, "Dry Run", create_inbox=True, dry_run=True)

        self.assertTrue(success)
        self.assertFalse(os.path.exists(f"docs/chantiers/{go_id}"))
        self.assertFalse(os.path.exists(f"docs/index/inbox/{go_id}.md"))

    def test_conflict_without_force_fails(self):
        go_id = "GO_CONFLICT_01"
        os.makedirs(f"docs/chantiers/{go_id}")
        doc_path = f"docs/chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md"
        with open(doc_path, "w") as f:
            f.write("OLD CONTENT")

        # Should fail without force
        success, result = create_chantier(go_id, "New", force=False)
        self.assertFalse(success)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("Conflict" in e for e in result["errors"]))

        with open(doc_path, "r") as f:
            self.assertEqual(f.read(), "OLD CONTENT")

    def test_force_overwrite(self):
        go_id = "GO_OVERWRITE_01"
        os.makedirs(f"docs/chantiers/{go_id}")
        doc_path = f"docs/chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md"
        with open(doc_path, "w") as f:
            f.write("OLD CONTENT")

        # Should overwrite with force
        success, result = create_chantier(go_id, "New", force=True)
        self.assertTrue(success)
        self.assertIn(doc_path, result["created_files"])

        with open(doc_path, "r") as f:
            self.assertIn("New", f.read())

    def test_json_output_parseable(self):
        go_id = "GO_JSON_01"
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            with patch('sys.argv', ['prog', '--go-id', go_id, '--json', '--dry-run']):
                try:
                    main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)

                output = fake_out.getvalue()
                # Find the JSON part (ignore possible non-JSON print lines if any)
                json_str = output[output.find('{'):]
                data = json.loads(json_str)
                self.assertEqual(data["go_id"], go_id)
                self.assertEqual(data["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
