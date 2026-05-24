from pathlib import Path
import pytest
from modules.data_center.layout import (
    ensure_data_center_dirs,
    get_producer_dir,
    load_consumers_registry,
    load_producers_registry,
)


def test_layout_creates_derivatives_producer(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    prod = base / "derivatives" / "derivatives_collector__bitget"
    assert (prod / "raw").is_dir()
    assert (prod / "normalized").is_dir()
    assert (prod / "cache" / "by_symbol").is_dir()


def test_layout_creates_binance_producer(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    prod = base / "derivatives" / "derivatives_collector__binance"
    assert prod.is_dir()
    assert (prod / "raw").is_dir()


def test_layout_creates_spot_producer(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    prod = base / "spot" / "collector_binance_spot"
    assert (prod / "raw").is_dir()
    assert (prod / "normalized").is_dir()


def test_layout_creates_registry_dir(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    assert (base / "_registry").is_dir()


def test_layout_creates_append_files(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    prod = base / "derivatives" / "derivatives_collector__bitget"
    assert (prod / "events.jsonl").exists()
    assert (prod / "errors.jsonl").exists()


def test_layout_idempotent(tmp_path):
    ensure_data_center_dirs(tmp_path)
    ensure_data_center_dirs(tmp_path)
    assert (tmp_path / "data" / "data_center" / "_registry").is_dir()


def test_get_producer_dir(tmp_path):
    path = get_producer_dir("derivatives", "derivatives_collector__bitget", tmp_path)
    assert path == tmp_path / "data" / "data_center" / "derivatives" / "derivatives_collector__bitget"


def test_load_producers_registry():
    reg = load_producers_registry()
    assert reg["registry_version"] == "v1"
    ids = [p["producer_id"] for p in reg["producers"]]
    assert "derivatives_collector__bitget" in ids
    assert "derivatives_collector__binance" in ids
    assert "collector_binance_spot" in ids


def test_load_consumers_registry():
    reg = load_consumers_registry()
    assert reg["registry_version"] == "v1"
    ids = [c["consumer_id"] for c in reg["consumers"]]
    assert "desk_pro__market_metrics" in ids
    assert "perf_engine__replay_context" in ids


def test_producers_have_required_fields():
    reg = load_producers_registry()
    required = {"producer_id", "family", "contract_class", "schema_version", "output_path_root", "coverage_status"}
    for p in reg["producers"]:
        assert required <= p.keys(), f"producer {p.get('producer_id')} missing fields"


def test_consumers_have_required_fields():
    reg = load_consumers_registry()
    required = {"consumer_id", "surface", "read_path", "access_pattern", "fallback", "implementation_status"}
    for c in reg["consumers"]:
        assert required <= c.keys(), f"consumer {c.get('consumer_id')} missing fields"


def test_layout_creates_views_history_dir(tmp_path):
    base = ensure_data_center_dirs(tmp_path)
    assert (base / "views" / "market_metrics" / "history").is_dir()
