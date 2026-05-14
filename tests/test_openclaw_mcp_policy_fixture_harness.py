import json
import subprocess
import sys
import textwrap
from pathlib import Path

from modules.governance.openclaw_mcp_policy_validator.fixture_harness import (
    BLOCKED_WITH_REASON,
    PASS_FIXTURE_HARNESS,
    run_fixture_harness,
)


REAL_CORPUS = Path(
    "docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01"
)


def test_real_markdown_fixture_corpus_passes():
    report = run_fixture_harness(REAL_CORPUS)
    assert report.verdict == PASS_FIXTURE_HARNESS
    assert report.total_fixtures == 37
    assert report.pass_count == 37
    assert report.fail_count == 0


def test_cli_outputs_deterministic_json_for_real_corpus():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "modules.governance.openclaw_mcp_policy_validator.fixture_harness",
            str(REAL_CORPUS),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["verdict"] == PASS_FIXTURE_HARNESS
    assert payload["total_fixtures"] == 37
    assert payload["fail_count"] == 0


def test_missing_snippet_blocks(tmp_path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md").write_text(
        textwrap.dedent(
            """
            | fixture_id | file | category | expected_verdict | expected_error_code | related_rule | related_gate | related_trace | related_eval |
            |---|---|---|---|---|---|---|---|---|
            | `MISSING_SNIPPET_01` | `01_FIXTURES.md` | invalid | `FAIL_POLICY` | `ERR_POLICY_PARSE` | parse | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (corpus / "01_FIXTURES.md").write_text(
        textwrap.dedent(
            """
            # Fixture

            ```text
            fixture_id: MISSING_SNIPPET_01
            expected_verdict: FAIL_POLICY
            expected_error_code: ERR_POLICY_PARSE
            ```
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    report = run_fixture_harness(corpus)
    assert report.verdict == BLOCKED_WITH_REASON
    assert report.blocked_reasons


def test_ambiguous_duplicate_fixture_blocks(tmp_path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md").write_text(
        textwrap.dedent(
            """
            | fixture_id | file | category | expected_verdict | expected_error_code | related_rule | related_gate | related_trace | related_eval |
            |---|---|---|---|---|---|---|---|---|
            | `DUPLICATE_01` | `01_FIXTURES.md` | invalid | `FAIL_POLICY` | `ERR_POLICY_PARSE` | parse | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    block = textwrap.dedent(
        """
        ```text
        fixture_id: DUPLICATE_01
        expected_verdict: FAIL_POLICY
        expected_error_code: ERR_POLICY_PARSE
        policy_snippet:
          policy:
            id: DUPLICATE
        ```
        """
    ).strip()
    (corpus / "01_FIXTURES.md").write_text(f"{block}\n\n{block}\n", encoding="utf-8")
    report = run_fixture_harness(corpus)
    assert report.verdict == BLOCKED_WITH_REASON
    assert report.blocked_reasons
