import sys
import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.derivatives_collector import DerivativesCollector

def test_adapter(source_name, expected_exchange):
    print(f"--- Testing {expected_exchange} Flow ---")
    config = {
        "DATA_SOURCE": source_name,
        "SYMBOLS": ["BTCUSDT", "ETHUSDT"],
        "OUTPUT_FORMAT": "json",
        "OUTPUT_DIR": PROJECT_ROOT / "data" / "derivatives" / "test_output"
    }
    collector = DerivativesCollector(config)
    
    data = collector.run()
    
    assert data is not None, f"Data for {expected_exchange} should not be None"
    assert len(data) == 2, f"Data for {expected_exchange} should contain 2 elements"
    
    expected_keys = [
        "symbol", "exchange", "timestamp", "open_interest",
        "funding_rate", "long_short_ratio", "liquidations_long",
        "liquidations_short", "volume_futures"
    ]
    
    for row in data:
        assert row["symbol"] in ["BTCUSDT", "ETHUSDT"], f"Unexpected symbol: {row['symbol']}"
        assert row["exchange"] == expected_exchange, f"Exchange should be {expected_exchange}"
        
        for key in expected_keys:
            assert key in row, f"Missing key in output contract: {key}"
            
        # Specific assertions
        if expected_exchange == "BINANCE":
            assert row["open_interest"] is not None and row["open_interest"] > 0
        elif expected_exchange == "BITGET":
            # Volume is the most reliable fallback metric to be not None on Bitget V2
            assert row["volume_futures"] is not None
        elif expected_exchange == "MOCK":
            assert row["open_interest"] is not None
            
    print(f"[PASS] {expected_exchange} flow\n")

from modules.derivatives_collector.app.derivatives_collector import BaseAdapter, DerivativesRow

class ExplodingMockAdapter(BaseAdapter):
    def _collect_symbol(self, symbol, batch_timestamp):
        if symbol == "BOMB":
            raise ValueError("Intentional crash for testing")
        elif symbol == "DICT":
            return {"symbol": "DICT", "error": "I am a raw dictionary, not a dataclass!"}
        return DerivativesRow(symbol=symbol, exchange="MOCK", timestamp=batch_timestamp)

def test_fail_open():
    print("--- Testing Fail-Open Hardening ---")
    adapter = ExplodingMockAdapter("MOCK")
    # Batch query where 2 elements are corrupt 
    data = adapter.collect(["BTCUSDT", "BOMB", "ETHUSDT", "DICT"])
    assert len(data) == 4, f"Fail-open should return 4 rows for 4 symbols, got {len(data)}"
    assert data[0]["symbol"] == "BTCUSDT"
    assert data[1]["symbol"] == "BOMB"
    assert "Intentional crash" in data[1]["error"]
    assert data[2]["symbol"] == "ETHUSDT"
    assert data[3]["symbol"] == "DICT"
    assert "Invalid return type" in data[3]["error"]
    print("[PASS] Fail-Open architecture\n")

def test_sidecar_metadata():
    print("--- Testing Sidecar Metadata ---")
    config = {
        "DATA_SOURCE": "mock",
        "SYMBOLS": ["BTCUSDT", "ETHUSDT", "FAIL"],
        "OUTPUT_FORMAT": "json",
        "OUTPUT_DIR": PROJECT_ROOT / "data" / "derivatives" / "test_output"
    }
    collector = DerivativesCollector(config)
    
    # Clean output dir
    if config["OUTPUT_DIR"].exists():
        for f in config["OUTPUT_DIR"].glob("derivatives_*"):
            f.unlink()
            
    data = collector.run()
    
    # Find created files
    json_files = list(config["OUTPUT_DIR"].glob("*.json"))
    meta_files = [f for f in json_files if f.suffix == ".json" and f.name.endswith(".meta.json")]
    primary_files = [f for f in json_files if f not in meta_files]
    
    assert len(primary_files) == 1, "Should have 1 primary JSON file"
    assert len(meta_files) == 1, "Should have 1 sidecar meta file"
    
    with open(meta_files[0], "r") as f:
        meta = json.load(f)
        
    assert meta["meta_schema_version"] == 1
    assert meta["stats"]["requested"] == 3
    assert meta["stats"]["succeeded"] == 3 # Mock succeeds even if symbol is FAIL
    print("[PASS] Sidecar Metadata architecture\n")

if __name__ == "__main__":
    try:
        test_adapter("mock", "MOCK")
        test_adapter("binance", "BINANCE")
        test_adapter("bitget", "BITGET")
        test_fail_open()
        test_sidecar_metadata()
        print("[SUCCESS] All multi-adapter smoke tests passed.")
        sys.exit(0)
    except AssertionError as e:
        print(f"[FAIL] Smoke test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        sys.exit(1)
