from modules.webhook.paper_guards import evaluate_paper_test_runtime_guards


VALID_ENV = {
    "RUNNER_MODE": "PAPER",
    "SIMULATION_MODE": "true",
    "TRADE_ALLOWED": "false",
    "LEDGER_PATH": "/data/ledger_paper.json",
}


def test_paper_guards_pass_with_required_env_and_paper_adapter():
    result = evaluate_paper_test_runtime_guards(
        env=VALID_ENV,
        active_engine=None,
        adapter_names=["paper"],
    )

    assert result["ok"] is True
    assert result["reasons"] == []


def test_paper_guards_fail_when_required_flags_are_missing():
    result = evaluate_paper_test_runtime_guards(
        env={},
        active_engine=None,
        adapter_names=["paper"],
    )

    assert result["ok"] is False
    assert any("runner_mode" in reason for reason in result["reasons"])
    assert any("simulation_mode" in reason for reason in result["reasons"])
    assert any("trade_allowed" in reason for reason in result["reasons"])
    assert any("ledger_path" in reason for reason in result["reasons"])


def test_paper_guards_fail_when_trade_allowed_is_true():
    env = {**VALID_ENV, "TRADE_ALLOWED": "true"}

    result = evaluate_paper_test_runtime_guards(
        env=env,
        active_engine=None,
        adapter_names=["paper"],
    )

    assert result["ok"] is False
    assert result["guards"]["trade_allowed"]["ok"] is False


def test_paper_guards_fail_when_active_engine_is_aggressive():
    result = evaluate_paper_test_runtime_guards(
        env=VALID_ENV,
        active_engine="COINM_SHORT",
        adapter_names=["paper"],
    )

    assert result["ok"] is False
    assert result["guards"]["active_engine"]["ok"] is False


def test_paper_guards_fail_when_ledger_points_to_live_file():
    env = {**VALID_ENV, "LEDGER_PATH": "/data/ledger_live.json"}

    result = evaluate_paper_test_runtime_guards(
        env=env,
        active_engine=None,
        adapter_names=["paper"],
    )

    assert result["ok"] is False
    assert result["guards"]["ledger_path"]["ok"] is False


def test_paper_guards_fail_when_paper_adapter_is_missing():
    result = evaluate_paper_test_runtime_guards(
        env=VALID_ENV,
        active_engine=None,
        adapter_names=["live"],
    )

    assert result["ok"] is False
    assert result["guards"]["paper_adapter"]["ok"] is False
