from pathlib import Path

from tools.why_lint_static_validator.why_lint_static_validator import (
    DocScanFormatError,
    parse_fixture_markdown,
    render_doc_scan_text_report,
    render_text_report,
    run_doc_scan,
    run_validation,
    validate_fixture,
)


VALID_SNIPPET = """rule_id: "MINIMAL_RULE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
"""


def _fixture_doc(
    fixture_id: str = "VALID_MINIMAL_RULE_01",
    snippet: str = VALID_SNIPPET,
    expected_verdict: str = "PASS_RULE_STATIC_VALIDATION",
    expected_error_code: str = "(none)",
) -> str:
    return f"""### {fixture_id}

- **fixture_id**: {fixture_id}
- **category**: A - Test fixture
- **purpose**: Local unit test fixture.
- **expected_verdict**: {expected_verdict}
- **expected_error_code**: {expected_error_code}
- **related_validator_rule**: rule_schema_test
- **related_warning_family**: WHY_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: The test controls the expected verdict.

```yaml
{snippet}```
"""


def _validate(markdown: str):
    fixture = parse_fixture_markdown(markdown)[0]
    return validate_fixture(fixture)


def _write(tmp_path: Path, markdown: str) -> Path:
    path = tmp_path / "fixtures.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def _why_lint_parent(tmp_path: Path) -> Path:
    root = (
        tmp_path
        / "docs"
        / "chantiers"
        / "GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01"
    )
    root.mkdir(parents=True)
    return root


def _valid_doc() -> str:
    return """# Sample WHY lint document

## 1_MASTER_TARGET

Target.

## 6_FINAL_TARGET

FINAL_TARGET: produce a bounded document.

## 12_INVARIANTS

- read-only

## 17_RESUME_POINT

Resume here.

## WHY

This document exists for testing.
"""


def test_extracts_fixtures_and_fenced_snippets() -> None:
    markdown = _fixture_doc("VALID_MINIMAL_RULE_01") + "\n" + _fixture_doc("VALID_WHY_GAP_RULE_01")

    fixtures = parse_fixture_markdown(markdown)

    assert [fixture.fixture_id for fixture in fixtures] == [
        "VALID_MINIMAL_RULE_01",
        "VALID_WHY_GAP_RULE_01",
    ]
    assert fixtures[0].policy["rule_id"] == "MINIMAL_RULE_001"
    assert fixtures[0].fenced_policy_snippet.strip().startswith('rule_id: "MINIMAL_RULE_001"')


def test_valid_fixture_passes_static_validation() -> None:
    result = _validate(_fixture_doc())

    assert result.observed_verdict == "PASS_RULE_STATIC_VALIDATION"
    assert result.observed_error_code is None
    assert result.matched is True


def test_missing_rule_id_fails_schema() -> None:
    snippet = VALID_SNIPPET.replace('rule_id: "MINIMAL_RULE_001"\n', "")
    result = _validate(
        _fixture_doc(
            "FAIL_MISSING_RULE_ID_01",
            snippet,
            "FAIL_SCHEMA_MISSING_FIELD",
            "ERR_SCHEMA_MISSING_RULE_ID",
        )
    )

    assert result.observed_verdict == "FAIL_SCHEMA_MISSING_FIELD"
    assert result.observed_error_code == "ERR_SCHEMA_MISSING_RULE_ID"
    assert result.matched is True


def test_unknown_warning_family_fails() -> None:
    snippet = VALID_SNIPPET.replace('family: "WHY_GAP"', 'family: "EXECUTE_SHELL"')
    result = _validate(
        _fixture_doc(
            "FAIL_UNKNOWN_WARNING_FAMILY_01",
            snippet,
            "FAIL_UNKNOWN_WARNING_FAMILY",
            "ERR_UNKNOWN_FAMILY_EXECUTE_SHELL",
        )
    )

    assert result.observed_verdict == "FAIL_UNKNOWN_WARNING_FAMILY"
    assert result.matched is True


def test_missing_gate_fails_gate_binding() -> None:
    snippet = VALID_SNIPPET.replace('gate_required: "REVIEW_REQUIRED"\n', "")
    result = _validate(
        _fixture_doc(
            "FAIL_MISSING_GATE_BINDING_01",
            snippet,
            "FAIL_GATE_BINDING",
            "ERR_GATE_MISSING_BINDING",
        )
    )

    assert result.observed_verdict == "FAIL_GATE_BINDING"
    assert result.matched is True


def test_missing_trace_fails_trace_binding() -> None:
    snippet = VALID_SNIPPET.replace("trace_required: true\n", "")
    result = _validate(
        _fixture_doc(
            "FAIL_MISSING_TRACE_01",
            snippet,
            "FAIL_TRACE_BINDING",
            "ERR_TRACE_REQUIRED_MISSING",
        )
    )

    assert result.observed_verdict == "FAIL_TRACE_BINDING"
    assert result.matched is True


def test_missing_eval_fails_eval_binding() -> None:
    snippet = VALID_SNIPPET.replace("eval_required: false\n", "")
    result = _validate(
        _fixture_doc(
            "FAIL_MISSING_EVAL_01",
            snippet,
            "FAIL_EVAL_BINDING",
            "ERR_EVAL_REQUIRED_MISSING",
        )
    )

    assert result.observed_verdict == "FAIL_EVAL_BINDING"
    assert result.matched is True


def test_autofix_true_fails() -> None:
    snippet = VALID_SNIPPET.replace("autofix_allowed: false", "autofix_allowed: true")
    result = _validate(
        _fixture_doc("FAIL_AUTOFIX_ENABLED_01", snippet, "FAIL_AUTOFIX_ENABLED", "ERR_AUTOFIX_ENABLED")
    )

    assert result.observed_verdict == "FAIL_AUTOFIX_ENABLED"
    assert result.matched is True


def test_runtime_binding_true_fails() -> None:
    snippet = VALID_SNIPPET.replace("runtime_binding: false", "runtime_binding: true")
    result = _validate(
        _fixture_doc(
            "FAIL_RUNTIME_BINDING_ENABLED_01",
            snippet,
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_RUNTIME_BINDING_ENABLED",
        )
    )

    assert result.observed_verdict == "FAIL_RUNTIME_BINDING_ENABLED"
    assert result.matched is True


def test_can_fail_ci_true_fails() -> None:
    snippet = VALID_SNIPPET.replace("can_fail_ci: false", "can_fail_ci: true")
    result = _validate(
        _fixture_doc(
            "FAIL_CI_BLOCKING_ENABLED_01",
            snippet,
            "FAIL_CI_BLOCKING_ENABLED",
            "ERR_CI_BLOCKING_ENABLED",
        )
    )

    assert result.observed_verdict == "FAIL_CI_BLOCKING_ENABLED"
    assert result.matched is True


def test_axis_authority_drift_fails() -> None:
    snippet = """rule_id: "LINT_AUTHORIZES_RUNTIME_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "WHY Lint"
affected_axis:
  - "OpenClaw Central"
gate_required: "GATE_RUNTIME"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/why_lint/rule_drift.md"
  - "L5"
  - "Lint rule attempts to grant execution permission"
lint_action: "GRANT_EXECUTION_PERMISSION"
"""
    result = _validate(
        _fixture_doc(
            "FAIL_WHY_LINT_AUTHORIZES_RUNTIME_01",
            snippet,
            "FAIL_AXIS_AUTHORITY_DRIFT",
            "ERR_AUTHORITY_DRIFT_LINT_RUNTIME",
        )
    )

    assert result.observed_verdict == "FAIL_AXIS_AUTHORITY_DRIFT"
    assert result.matched is True


def test_fake_secret_like_placeholder_fails() -> None:
    snippet = VALID_SNIPPET.replace('"docs/source/example.md"', '"FAKE_SECRET_DO_NOT_USE"')
    result = _validate(
        _fixture_doc("FAIL_SECRET_LIKE_FIELD_01", snippet, "FAIL_SECRET_RISK", "ERR_SECRET_LIKE_FIELD")
    )

    assert result.observed_verdict == "FAIL_SECRET_RISK"
    assert result.matched is True


def test_global_pass_report_exit_code_zero(tmp_path: Path) -> None:
    markdown = _fixture_doc("VALID_MINIMAL_RULE_01") + "\n" + _fixture_doc(
        "FAIL_UNKNOWN_WARNING_FAMILY_01",
        VALID_SNIPPET.replace('family: "WHY_GAP"', 'family: "EXECUTE_SHELL"'),
        "FAIL_UNKNOWN_WARNING_FAMILY",
        "ERR_UNKNOWN_FAMILY_EXECUTE_SHELL",
    )
    report = run_validation(_write(tmp_path, markdown))

    assert report.exit_code == 0
    assert report.status == "PASS"
    assert "status: PASS" in render_text_report(report)


def test_global_fail_report_exit_code_one(tmp_path: Path) -> None:
    report = run_validation(
        _write(
            tmp_path,
            _fixture_doc(
                "VALID_WITH_WRONG_EXPECTED_VERDICT_01",
                VALID_SNIPPET,
                "FAIL_UNKNOWN_RULE",
                "ERR_UNKNOWN_RULE_ID_ZZ_999",
            ),
        )
    )

    assert report.exit_code == 1
    assert report.status == "FAIL_VERDICT_MISMATCH"
    assert report.mismatched_fixtures == 1


def test_repository_fixture_corpus_matches_expected() -> None:
    repo_root = Path(__file__).parents[2]
    corpus = (
        repo_root
        / "docs"
        / "chantiers"
        / "GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01"
        / "GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md"
    )

    report = run_validation(corpus)

    assert report.exit_code == 0
    assert report.total_fixtures == 40


def test_doc_scan_parent_folder_passes_without_findings(tmp_path: Path) -> None:
    root = _why_lint_parent(tmp_path)
    (root / "SPEC_SAMPLE.md").write_text(_valid_doc(), encoding="utf-8")
    (root / "GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md").write_text(
        "# fixtures are skipped", encoding="utf-8"
    )

    report = run_doc_scan(root)

    assert report.exit_code == 0
    assert report.status == "PASS"
    assert len(report.scanned_files) == 1
    assert len(report.skipped_files) == 1
    assert len(report.findings) == 0
    assert "status: PASS" in render_doc_scan_text_report(report)


def test_doc_scan_reports_missing_required_markers(tmp_path: Path) -> None:
    root = _why_lint_parent(tmp_path)
    (root / "INCOMPLETE.md").write_text("# Incomplete\n\n## WHY\n\nReason only.\n", encoding="utf-8")

    report = run_doc_scan(root)

    assert report.exit_code == 1
    assert report.status == "FINDINGS_PRESENT"
    finding_ids = {finding.finding_id for finding in report.findings}
    assert "MISSING_FINAL_TARGET" in finding_ids
    assert "MISSING_INVARIANTS" in finding_ids
    assert "MISSING_RESUME_POINT" in finding_ids


def test_doc_scan_rejects_out_of_scope_root(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "chantiers" / "OTHER_GO"
    root.mkdir(parents=True)

    try:
        run_doc_scan(root)
    except DocScanFormatError as exc:
        assert "V1 scan root must end with" in str(exc)
    else:  # pragma: no cover - defensive branch.
        raise AssertionError("expected DocScanFormatError")


def test_doc_scan_reports_forbidden_runtime_implications(tmp_path: Path) -> None:
    root = _why_lint_parent(tmp_path)
    (root / "BAD_RUNTIME.md").write_text(_valid_doc() + "\nruntime_binding: true\n", encoding="utf-8")

    report = run_doc_scan(root)

    assert report.exit_code == 1
    assert any(finding.finding_id == "RUNTIME_BINDING_ENABLED" for finding in report.findings)


def test_doc_scan_reports_unexpected_secret_like_risk(tmp_path: Path) -> None:
    root = _why_lint_parent(tmp_path)
    (root / "SECRET_RISK.md").write_text(
        _valid_doc() + "\napi_key = abcdefghijklmnopqrstuvwxyz123456\n", encoding="utf-8"
    )

    report = run_doc_scan(root)

    assert report.exit_code == 3
    assert report.status == "FAIL_SECRET_RISK"
    assert any(finding.verdict == "FAIL_SECRET_RISK" for finding in report.findings)
