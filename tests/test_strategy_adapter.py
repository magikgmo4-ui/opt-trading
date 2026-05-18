"""
Tests for modules/strategy/adapter.py

Run: pytest tests/test_strategy_adapter.py -q
"""

from modules.strategy.adapter import (
    validate_strategy_id,
    get_known_ids,
    lookup_strategy,
    get_all_entries,
)

KNOWN_IDS = {
    "SMC_ICT_CHOCH_BOS_RETEST",
    "xau_session_open_v1",
    "COINM_SHORT",
    "USDTM_LONG",
    "GOLD_CFD_LONG",
    "range_strategy_v1",
    "btc_coinm_accumulation",
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
        assert len(get_known_ids()) == 7


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
        assert len(entries) == 7

    def test_all_known(self):
        ids = {e.strategy_id for e in get_all_entries()}
        assert ids == KNOWN_IDS


class TestIdempotent:
    def test_cache_consistent(self):
        assert get_known_ids() == get_known_ids()
        assert get_all_entries() == get_all_entries()
