import os
import json
import pytest
import sys
from unittest.mock import patch, MagicMock
from scripts.ai.workers.doc_ops_constraint_check import check_constraints, parse_constraints_from_file

def test_check_constraints_read_only():
    files = ["docs/a.md", "scripts/b.py"]
    violations = check_constraints(files, "READ_ONLY")
    assert violations == files

def test_check_constraints_doc_only_pass():
    files = ["docs/a.md", "docs/index/inbox/test.md"]
    violations = check_constraints(files, "DOC_ONLY")
    assert violations == []

def test_check_constraints_doc_only_fail():
    files = ["docs/a.md", "scripts/b.py"]
    violations = check_constraints(files, "DOC_ONLY")
    assert violations == ["scripts/b.py"]

def test_parse_constraints_from_file_doc_only():
    content = "---\nGO_ID: TEST\nDOC_ONLY: true\n---\n# Title"
    with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=content)))))):
        with patch("os.path.exists", return_value=True):
            constraints = parse_constraints_from_file("dummy.md")
            assert "DOC_ONLY" in constraints
            assert "READ_ONLY" not in constraints

def test_parse_constraints_from_file_read_only():
    content = "---\nREAD_ONLY: true\n---\n"
    with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=content)))))):
        with patch("os.path.exists", return_value=True):
            constraints = parse_constraints_from_file("dummy.md")
            assert "READ_ONLY" in constraints
            assert "DOC_ONLY" not in constraints

def test_parse_constraints_none():
    content = "---\nGO_ID: TEST\n---\n"
    with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=content)))))):
        with patch("os.path.exists", return_value=True):
            constraints = parse_constraints_from_file("dummy.md")
            assert constraints == []

@patch("subprocess.check_output")
def test_main_logic_pass(mock_git, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    # Mock git output: only docs modified
    mock_git.side_effect = [b"docs/a.md\n", b""]
    
    # Force DOC_ONLY mode via args
    with patch("sys.argv", ["script_name", "--mode", "DOC_ONLY"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        captured = capsys.readouterr()
        assert "Result: PASS" in captured.out

@patch("subprocess.check_output")
def test_main_logic_fail(mock_git, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    # Mock git output: script modified
    mock_git.side_effect = [b"scripts/a.py\n", b""]
    
    # Force DOC_ONLY mode via args
    with patch("sys.argv", ["script_name", "--mode", "DOC_ONLY"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Result: FAIL" in captured.out
        assert "scripts/a.py" in captured.out

@patch("subprocess.check_output")
def test_main_logic_json(mock_git, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    mock_git.side_effect = [b"docs/a.md\n", b""]
    
    with patch("sys.argv", ["script_name", "--mode", "DOC_ONLY", "--json"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["status"] == "PASS"
        assert data["mode"] == "DOC_ONLY"

@patch("os.path.exists")
@patch("subprocess.check_output")
def test_main_exit_2_on_missing_requested_file(mock_git, mock_exists, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    # File does not exist
    mock_exists.return_value = False
    
    with patch("sys.argv", ["script_name", "--initial-doc", "missing.md"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 2
        captured = capsys.readouterr()
        assert "Error: Initial project doc not found" in captured.err

@patch("os.path.exists")
@patch("subprocess.check_output")
def test_main_local_doc_detection(mock_git, mock_exists, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    # Mock ./00_INITIAL_PROJECT_DOC.md exists
    mock_exists.side_effect = lambda p: p == "./00_INITIAL_PROJECT_DOC.md"
    mock_git.side_effect = [b"docs/a.md\n", b""]
    
    # Mock content with DOC_ONLY
    content = "---\nDOC_ONLY: true\n---\n"
    with patch("builtins.open", MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=content)))))):
        with patch("sys.argv", ["script_name"]):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0
            captured = capsys.readouterr()
            assert "Mode: DOC_ONLY" in captured.out

@patch("os.path.exists")
@patch("subprocess.check_output")
def test_main_no_mode_detected_pass(mock_git, mock_exists, capsys):
    from scripts.ai.workers.doc_ops_constraint_check import main
    
    # No files exist
    mock_exists.return_value = False
    # Some files modified
    mock_git.side_effect = [b"scripts/a.py\n", b""]
    
    with patch("sys.argv", ["script_name"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        captured = capsys.readouterr()
        assert "Mode: NONE" or "Mode: " in captured.out
        assert "Result: PASS" in captured.out
