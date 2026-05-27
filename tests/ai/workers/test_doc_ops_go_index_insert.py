import os
import shutil
import tempfile
import unittest
import json
import io
from unittest.mock import patch
from scripts.ai.workers.doc_ops_go_index_insert import (
    validate_go_id,
    parse_initial_doc,
    generate_entry,
    entry_exists_in_index,
    apply_entry,
    main,
)

GOOD_INITIAL_DOC = """---
go_id: GO_TEST_INSERTION_01
doc_type: INITIAL_PROJECT_DOC
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Create a controlled assistant for GO_INDEX.md insertion.

## 6_FINAL_TARGET
A working CLI tool for GO_INDEX.md insertion.

## PARENT_GO_ID
GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
"""

INITIAL_DOC_NO_TARGETS = """---
go_id: GO_NO_TARGET_01
doc_type: INITIAL_PROJECT_DOC
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

## 6_FINAL_TARGET

"""


class TestValidateGoId(unittest.TestCase):
    def test_valid_ids(self):
        for go_id in ["GO_PROJECT_01", "GO_TEST_A_01", "GO_123_45"]:
            self.assertTrue(validate_go_id(go_id)[0])

    def test_invalid_ids(self):
        for go_id in ["go_project_01", "GO_PROJECT", "GO-PROJECT-01", "GO PROJECT 01", "PROJECT_01"]:
            self.assertFalse(validate_go_id(go_id)[0])


class TestParseInitialDoc(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers/GO_TEST_INSERTION_01")
        os.makedirs("docs/chantiers/GO_NO_TARGET_01")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_parse_valid_doc(self):
        path = "docs/chantiers/GO_TEST_INSERTION_01/00_INITIAL_PROJECT_DOC.md"
        with open(path, "w") as f:
            f.write(GOOD_INITIAL_DOC)
        data, err = parse_initial_doc(path)
        self.assertIsNotNone(data)
        self.assertIsNone(err)
        self.assertEqual(data["go_id"], "GO_TEST_INSERTION_01")
        self.assertIn("controlled assistant", data["master_target"])
        self.assertIn("A working CLI tool", data["final_target"])
        self.assertIn("SELECTION_AUTOMATION_PRIORITY_01", data["parent_go_id"])

    def test_parse_no_targets(self):
        path = "docs/chantiers/GO_NO_TARGET_01/00_INITIAL_PROJECT_DOC.md"
        with open(path, "w") as f:
            f.write(INITIAL_DOC_NO_TARGETS)
        data, err = parse_initial_doc(path)
        self.assertIsNotNone(data)
        self.assertEqual(data["master_target"], "")

    def test_missing_file(self):
        path = "docs/chantiers/GO_MISSING_01/00_INITIAL_PROJECT_DOC.md"
        data, err = parse_initial_doc(path)
        self.assertIsNone(data)
        self.assertIsNotNone(err)
        self.assertIn("not found", err)


class TestGenerateEntry(unittest.TestCase):
    def test_entry_contains_go_id(self):
        data = {
            "go_id": "GO_TEST_ENTRY_01",
            "master_target": "A test target",
            "final_target": "A final result",
            "parent_go_id": "",
            "short_title": "A test target",
            "entry_type": "chantier technique",
            "status": "OPEN",
            "updated_at": "2026-05-27",
        }
        entry = generate_entry(data)
        self.assertIn("GO_TEST_ENTRY_01", entry)
        self.assertIn("A test target", entry)
        self.assertIn("OPEN", entry)

    def test_entry_with_parent(self):
        data = {
            "go_id": "GO_CHILD_01",
            "master_target": "Child target",
            "final_target": "",
            "parent_go_id": "GO_PARENT_01",
            "short_title": "Child target",
            "entry_type": "chantier technique / child",
            "status": "ACTIVE",
            "updated_at": "2026-05-27",
        }
        entry = generate_entry(data)
        self.assertIn("GO_CHILD_01", entry)
        self.assertIn("chantier technique / child", entry)


class TestEntryExists(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        self.index_path = "docs/index/GO_INDEX.md"
        os.makedirs("docs/index")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_entry_detected(self):
        content = """# GO_INDEX

## Entrées

### GO_EXISTING_01
- repo : opt-trading
"""
        with open(self.index_path, "w") as f:
            f.write(content)
        self.assertTrue(entry_exists_in_index(self.index_path, "GO_EXISTING_01"))
        self.assertFalse(entry_exists_in_index(self.index_path, "GO_MISSING_01"))

    def test_no_index_file(self):
        self.assertFalse(entry_exists_in_index("nonexistent.md", "GO_ANY_01"))


class TestApplyEntry(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/index")
        self.index_path = "docs/index/GO_INDEX.md"

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_insert_new_entry(self):
        content = """# GO_INDEX

## Entrées

### GO_OTHER_01
- repo : opt-trading
"""
        with open(self.index_path, "w") as f:
            f.write(content)
        entry = "### GO_NEW_01\n- repo : opt-trading\n"
        success, msg = apply_entry(self.index_path, entry, "GO_NEW_01")
        self.assertTrue(success)
        self.assertTrue(entry_exists_in_index(self.index_path, "GO_NEW_01"))

    def test_duplicate_rejected(self):
        content = """# GO_INDEX

## Entrées

### GO_DUP_01
- repo : opt-trading
"""
        with open(self.index_path, "w") as f:
            f.write(content)
        entry = "### GO_DUP_01\n- repo : opt-trading\n"
        success, msg = apply_entry(self.index_path, entry, "GO_DUP_01")
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_missing_index(self):
        success, msg = apply_entry("/tmp/nonexistent/index.md", "### GO_X\n", "GO_X")
        self.assertFalse(success)
        self.assertIn("not found", msg)


class TestMainDryRun(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers/GO_DRY_RUN_TEST_01")
        os.makedirs("docs/index")
        with open("docs/chantiers/GO_DRY_RUN_TEST_01/00_INITIAL_PROJECT_DOC.md", "w") as f:
            f.write(GOOD_INITIAL_DOC.replace("GO_TEST_INSERTION_01", "GO_DRY_RUN_TEST_01"))
        with open("docs/index/GO_INDEX.md", "w") as f:
            f.write("# GO_INDEX\n\n## Entrées\n")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_dry_run_no_modify(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            with patch('sys.argv', [
                'prog', '--go-id', 'GO_DRY_RUN_TEST_01', '--dry-run', '--json'
            ]):
                try:
                    main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)
                output = fake_out.getvalue()
                json_str = output[output.find('{'):]
                data = json.loads(json_str)
                self.assertEqual(data["status"], "PASS")
                self.assertTrue(data["would_change"])
                self.assertFalse(data["duplicate"])
        with open("docs/index/GO_INDEX.md", "r") as f:
            self.assertNotIn("GO_DRY_RUN_TEST_01", f.read())


class TestMainApplyTmpPath(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers/GO_APPLY_TEST_01")
        os.makedirs("docs/index")
        with open("docs/chantiers/GO_APPLY_TEST_01/00_INITIAL_PROJECT_DOC.md", "w") as f:
            f.write(GOOD_INITIAL_DOC.replace("GO_TEST_INSERTION_01", "GO_APPLY_TEST_01"))
        self.tmp_index = os.path.join(self.tmp_root, "tmp_go_index.md")
        with open(self.tmp_index, "w") as f:
            f.write("# GO_INDEX\n\n## Entrées\n")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_apply_modifies_tmp_copy(self):
        with patch('sys.stdout', new=io.StringIO()):
            with patch('sys.argv', [
                'prog', '--go-id', 'GO_APPLY_TEST_01',
                '--index-path', self.tmp_index,
                '--apply',
            ]):
                try:
                    main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)
        with open(self.tmp_index, "r") as f:
            content = f.read()
            self.assertIn("GO_APPLY_TEST_01", content)


class TestMainInvalidId(unittest.TestCase):
    def test_exit_code_1(self):
        with patch('sys.stderr', new=io.StringIO()):
            with patch('sys.argv', ['prog', '--go-id', 'invalid']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)

    def test_exit_code_1_json(self):
        with patch('sys.stdout', new=io.StringIO()):
            with patch('sys.argv', ['prog', '--go-id', 'invalid', '--json']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1)


class TestMainMissingDoc(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers/GO_MISSING_DOC_01")

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_exit_code_2(self):
        with patch('sys.stderr', new=io.StringIO()):
            with patch('sys.argv', ['prog', '--go-id', 'GO_MISSING_DOC_01']):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 2)


class TestMainJsonParseable(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_root)
        os.makedirs("docs/chantiers/GO_JSON_PARSE_01")
        with open("docs/chantiers/GO_JSON_PARSE_01/00_INITIAL_PROJECT_DOC.md", "w") as f:
            f.write(GOOD_INITIAL_DOC.replace("GO_TEST_INSERTION_01", "GO_JSON_PARSE_01"))

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmp_root)

    def test_json_output(self):
        with patch('sys.stdout', new=io.StringIO()):
            with patch('sys.argv', [
                'prog', '--go-id', 'GO_JSON_PARSE_01', '--dry-run', '--json'
            ]):
                try:
                    main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)


if __name__ == "__main__":
    unittest.main()
