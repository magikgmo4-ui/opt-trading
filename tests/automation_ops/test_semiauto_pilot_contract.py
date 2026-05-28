"""Tests for the semi-auto pilot handoff contract and runner."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from modules.automation_ops.semiauto_pilot import handoff_contract, stop_conditions
from modules.automation_ops.semiauto_pilot.pilot_runner import run


# ---------------------------------------------------------------------------
# handoff_contract
# ---------------------------------------------------------------------------

def _valid() -> dict:
    return {
        "run_id": "pilot_abc12345",
        "go_id": "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01",
        "parent_go_id": "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01",
        "mode": "dry_run",
        "input_prompt_path": "/tmp/prompt.txt",
        "actions_planned": ["read prompt"],
        "actions_executed": [],
        "stop_conditions": [],
        "human_gate_required": True,
        "verdict": "PASS_DRY_RUN",
        "next_go": "",
    }


def test_valid_contract_passes():
    handoff_contract.validate(_valid())


def test_missing_field_raises():
    c = _valid()
    del c["verdict"]
    with pytest.raises(handoff_contract.ContractError, match="missing fields"):
        handoff_contract.validate(c)


def test_human_gate_required_true():
    c = _valid()
    c["human_gate_required"] = False
    with pytest.raises(handoff_contract.ContractError, match="human_gate_required"):
        handoff_contract.validate(c)


def test_mode_must_be_dry_run():
    c = _valid()
    c["mode"] = "live"
    with pytest.raises(handoff_contract.ContractError, match="mode must be"):
        handoff_contract.validate(c)


def test_empty_verdict_rejected():
    c = _valid()
    c["verdict"] = ""
    with pytest.raises(handoff_contract.ContractError, match="verdict"):
        handoff_contract.validate(c)


def test_actions_planned_must_be_list():
    c = _valid()
    c["actions_planned"] = "not a list"
    with pytest.raises(handoff_contract.ContractError, match="actions_planned"):
        handoff_contract.validate(c)


def test_build_empty_is_valid_after_verdict():
    c = handoff_contract.build_empty(
        run_id="r1",
        go_id="GO_TEST",
        parent_go_id="GO_PARENT",
        input_prompt_path="/tmp/p.txt",
    )
    c["verdict"] = "PASS_DRY_RUN"
    handoff_contract.validate(c)


# ---------------------------------------------------------------------------
# stop_conditions
# ---------------------------------------------------------------------------

def test_no_stop_conditions_passes():
    c = _valid()
    stop_conditions.check(c)


def test_triggered_condition_raises():
    c = _valid()
    c["stop_conditions"] = [{"name": "test_trigger", "triggered": True}]
    with pytest.raises(stop_conditions.StopConditionTriggered, match="test_trigger"):
        stop_conditions.check(c)


def test_untriggered_condition_passes():
    c = _valid()
    c["stop_conditions"] = [{"name": "test_trigger", "triggered": False}]
    stop_conditions.check(c)


def test_wrong_mode_triggers_stop():
    c = _valid()
    c["mode"] = "live"
    with pytest.raises(stop_conditions.StopConditionTriggered, match="mode_not_dry_run"):
        stop_conditions.check(c)


def test_human_gate_false_triggers_stop():
    c = _valid()
    c["human_gate_required"] = False
    with pytest.raises(stop_conditions.StopConditionTriggered, match="human_gate_disabled"):
        stop_conditions.check(c)


# ---------------------------------------------------------------------------
# pilot_runner integration
# ---------------------------------------------------------------------------

def _write_prompt(tmp_path: Path, content: str = "run pilot") -> Path:
    p = tmp_path / "prompt.txt"
    p.write_text(content)
    return p


def test_runner_pass_dry_run(tmp_path):
    prompt = _write_prompt(tmp_path)
    rc = run(prompt, base_dir=tmp_path / "artifacts")
    assert rc == 0


def test_runner_missing_prompt_returns_3(tmp_path):
    rc = run(tmp_path / "nonexistent.txt", base_dir=tmp_path / "artifacts")
    assert rc == 3


def test_runner_stop_condition_returns_2(tmp_path):
    payload = json.dumps({"stop_conditions": [{"name": "forced_stop", "triggered": True}]})
    prompt = _write_prompt(tmp_path, payload)
    rc = run(prompt, base_dir=tmp_path / "artifacts")
    assert rc == 2


def test_runner_writes_proof_json(tmp_path):
    prompt = _write_prompt(tmp_path)
    artifacts = tmp_path / "artifacts"
    run(prompt, base_dir=artifacts)
    proofs = list(artifacts.rglob("proof.json"))
    assert len(proofs) == 1
    data = json.loads(proofs[0].read_text())
    assert data["verdict"] == "PASS_DRY_RUN"
    assert data["human_gate_required"] is True
    assert data["mode"] == "dry_run"


def test_runner_writes_markdown_summary(tmp_path):
    prompt = _write_prompt(tmp_path)
    artifacts = tmp_path / "artifacts"
    run(prompt, base_dir=artifacts)
    summaries = list(artifacts.rglob("proof_summary.md"))
    assert len(summaries) == 1
    text = summaries[0].read_text()
    assert "PASS_DRY_RUN" in text
