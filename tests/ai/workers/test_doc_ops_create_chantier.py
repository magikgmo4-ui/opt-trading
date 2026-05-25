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
        os.makedirs("docs/templates/doc_ops")

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
                # Find the JSON part
                json_str = output[output.find('{'):]
                data = json.loads(json_str)
                self.assertEqual(data["go_id"], go_id)
                self.assertEqual(data["status"], "PASS")

    def test_external_template_v1(self):
        # Create external templates
        with open("docs/templates/doc_ops/chantier_initial_project_doc_v1.md", "w") as f:
            f.write("EXTERNAL DOC {go_id}")
        with open("docs/templates/doc_ops/inbox_entry_v1.md", "w") as f:
            f.write("EXTERNAL INBOX {go_id}")

        go_id = "GO_TEMPLATE_V1_01"
        success, result = create_chantier(go_id, "Summary", template_version="v1", create_inbox=True)

        self.assertTrue(success)
        self.assertIn("loaded:", result["info"]["doc_template_status"])

        with open(f"docs/chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md", "r") as f:
            self.assertEqual(f.read(), f"EXTERNAL DOC {go_id}")
        with open(f"docs/index/inbox/{go_id}.md", "r") as f:
            self.assertEqual(f.read(), f"EXTERNAL INBOX {go_id}")

    def test_missing_template_version_fails(self):
        go_id = "GO_MISSING_TEMPLATE_01"
        success, result = create_chantier(go_id, "Summary", template_version="v999")

        self.assertFalse(success)
        self.assertEqual(result.get("exit_code"), 2)
        self.assertTrue(any("not found" in e for e in result["errors"]))

    def test_main_exit_code_2_on_missing_template(self):
        go_id = "GO_EXIT_2_01"
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with patch('sys.argv', ['prog', '--go-id', go_id, '--template-version', 'v999']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 2)
                self.assertIn("not found", fake_err.getvalue())

if __name__ == "__main__":
    unittest.main()
