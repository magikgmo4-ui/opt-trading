from __future__ import annotations

"""Governance test: safe_rewrite.sh presence and DEV_CONTRACTS documentation.

Verifies that the Windows/Linux mtime safe-rewrite tooling is in place:
1. scripts/safe_rewrite.sh exists and is executable.
2. docs/DEV_CONTRACTS.md exists and documents CONTRACT_01.
3. The script references the bash heredoc pattern.
"""

import os
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]


class TestSafeRewriteContract(unittest.TestCase):

    def test_safe_rewrite_script_exists(self):
        script = _REPO / "scripts" / "safe_rewrite.sh"
        self.assertTrue(script.exists(), f"scripts/safe_rewrite.sh not found at {script}")

    def test_safe_rewrite_script_is_executable(self):
        script = _REPO / "scripts" / "safe_rewrite.sh"
        if script.exists():
            self.assertTrue(os.access(script, os.X_OK), "scripts/safe_rewrite.sh is not executable")

    def test_safe_rewrite_script_documents_heredoc(self):
        script = _REPO / "scripts" / "safe_rewrite.sh"
        if script.exists():
            text = script.read_text(encoding="utf-8")
            self.assertIn("heredoc", text.lower(), "safe_rewrite.sh should mention heredoc pattern")
            self.assertIn("touch", text, "safe_rewrite.sh should run touch to update mtime")
            self.assertIn("__pycache__", text, "safe_rewrite.sh should purge __pycache__")

    def test_dev_contracts_doc_exists(self):
        doc = _REPO / "docs" / "DEV_CONTRACTS.md"
        self.assertTrue(doc.exists(), f"docs/DEV_CONTRACTS.md not found at {doc}")

    def test_dev_contracts_doc_references_contract_01(self):
        doc = _REPO / "docs" / "DEV_CONTRACTS.md"
        if doc.exists():
            text = doc.read_text(encoding="utf-8")
            self.assertIn("CONTRACT_01", text, "DEV_CONTRACTS.md must define CONTRACT_01")
            self.assertIn("safe_rewrite", text.lower(), "DEV_CONTRACTS.md must reference safe_rewrite")
            self.assertIn("mtime", text.lower(), "DEV_CONTRACTS.md must document mtime issue")


if __name__ == "__main__":
    unittest.main()
