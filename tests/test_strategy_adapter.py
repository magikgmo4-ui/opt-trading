"""
Tests for modules/strategy/adapter.py

Run: pytest tests/test_strategy_adapter.py -q
"""

import logging

from modules.strategy.adapter import (
    validate_strategy_id,
    get_known_ids,
    lookup_strategy,
    get_all_entries,
    build_unknown_strategy_warning_payload,
    log_unknown_strategy_id_warning,
)

KNOWN_IDS = {
    "SMC_ICT_CHOCH_BOS_RETEST",
    "xau_session_open_v1",
    "COINM_SHORT",
    "USDTM_LONG",
    "GOLD_CFD_LONG",
    "range_strategy_v1",
    "btc_coinm_accumulation",
    "DCA_ON_FEAR_SOLID_STOCKS",
    "e2e_dry_run",
}


class TestValidateStrategyId:
    def test_known_xau(self):
        assert validate_strategy_id("xau_session_open_v1") is True

    def test_known_coinm(self):
        assert validate_strategy_id("COINM_SHORT") is True

    def test_unknown(self):
        assert validate_strategy_id("unknown_strategy") is False

    def test_empty(self):
        assert validate_strategy_id("") is False


class TestGetKnownIds:
    def test_exact_set(self):
        assert get_known_ids() == KNOWN_IDS

    def test_count(self):
        assert len(get_known_ids()) == 9


class TestLookupStrategy:
    def test_found(self):
        entry = lookup_strategy("xau_session_open_v1")
        assert entry is not None
        assert entry.strategy_id == "xau_session_open_v1"
        assert entry.version == "v0.1.0"
        assert entry.lifecycle == "CANDIDATE"

    def test_not_found(self):
        assert lookup_strategy("nonexistent") is None

    def test_coinm_short(self):
        entry = lookup_strategy("COINM_SHORT")
        assert entry is not None
        assert entry.strategy_id == "COINM_SHORT"


class TestGetAllEntries:
    def test_count(self):
        entries = get_all_entries()
        assert len(entries) == 9

    def test_all_known(self):
        ids = {e.strategy_id for e in get_all_entries()}
        assert ids == KNOWN_IDS


class TestIdempotent:
    def test_cache_consistent(self):
        assert get_known_ids() == get_known_ids()
        assert get_all_entries() == get_all_entries()


class TestUnknownStrategyWarningPayload:
    def test_all_canonical_keys_present(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        for key in ("event", "metric", "strategy_id", "source", "mode", "runtime_action", "registry_known"):
            assert key in p

    def test_event_value(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        assert p["event"] == "STRATEGY_ID_UNKNOWN"

    def test_metric_value(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        assert p["metric"] == "strategy_id.unknown.warning"

    def test_mode_warning_only(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        assert p["mode"] == "warning_only"

    def test_runtime_action_continue(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        assert p["runtime_action"] == "continue"

    def test_registry_known_false(self):
        p = build_unknown_strategy_warning_payload("bad_id", "test_surface")
        assert p["registry_known"] is False

    def test_strategy_id_passthrough(self):
        p = build_unknown_strategy_warning_payload("my_unknown_id", "s")
        assert p["strategy_id"] == "my_unknown_id"

    def test_source_passthrough(self):
        p = build_unknown_strategy_warning_payload("x", "signal_router")
        assert p["source"] == "signal_router"

    def test_validate_strategy_id_unchanged_known(self):
        assert validate_strategy_id("xau_session_open_v1") is True

    def test_validate_strategy_id_unchanged_unknown(self):
        assert validate_strategy_id("nonexistent_after_helper") is False


class TestLogUnknownStrategyIdWarning:
    def test_emits_warning_level(self, caplog):
        with caplog.at_level(logging.WARNING, logger="strategy.observability"):
            log_unknown_strategy_id_warning("some_bad_id", "test_surface")
        assert any(r.levelno == logging.WARNING for r in caplog.records)

    def test_emits_event_key(self, caplog):
        with caplog.at_level(logging.WARNING, logger="strategy.observability"):
            log_unknown_strategy_id_warning("some_bad_id", "test_surface")
        assert any("STRATEGY_ID_UNKNOWN" in r.message for r in caplog.records)

    def test_emits_strategy_id(self, caplog):
        with caplog.at_level(logging.WARNING, logger="strategy.observability"):
            log_unknown_strategy_id_warning("my_specific_unknown", "test_surface")
        assert any("my_specific_unknown" in r.message for r in caplog.records)

    def test_emits_source(self, caplog):
        with caplog.at_level(logging.WARNING, logger="strategy.observability"):
            log_unknown_strategy_id_warning("bad_id", "signal_router")
        assert any("signal_router" in r.message for r in caplog.records)

    def test_does_not_raise(self):
        log_unknown_strategy_id_warning("", "empty_id_test")
        log_unknown_strategy_id_warning("some_id", "")
