import json
import tempfile
from pathlib import Path

from modules.data_center.storage.manifest_writer import write_manifest


def test_write_manifest_creates_file():
    td = Path(tempfile.mkdtemp())
    prod_dir = td / "producer_a"
    prod_dir.mkdir(parents=True)

    result = write_manifest(prod_dir, "test_producer", "market_metrics.v1")

    assert result == prod_dir / "manifest.json"
    assert result.exists()


def test_write_manifest_content():
    td = Path(tempfile.mkdtemp())
    prod_dir = td / "producer_a"
    prod_dir.mkdir(parents=True)

    write_manifest(prod_dir, "test_producer", "market_metrics.v1", status="ok")
    data = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8"))

    assert data["producer_id"] == "test_producer"
    assert data["schema"] == "market_metrics.v1"
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_write_manifest_with_extra():
    td = Path(tempfile.mkdtemp())
    prod_dir = td / "producer_a"
    prod_dir.mkdir(parents=True)

    write_manifest(
        prod_dir,
        "test_producer",
        "funding.v1",
        status="degraded",
        extra={"reason": "partial_data"},
    )
    data = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8"))

    assert data["extra"]["reason"] == "partial_data"


def test_write_manifest_with_root():
    td = Path(tempfile.mkdtemp())
    prod_dir = Path("data/data_center/test")
    prod_path = td / prod_dir
    prod_path.mkdir(parents=True)

    result = write_manifest(prod_dir, "test", "oi.v1", root=td)

    assert result == prod_path / "manifest.json"
    assert result.exists()


def test_write_manifest_custom_status():
    td = Path(tempfile.mkdtemp())
    prod_dir = td / "producer_b"
    prod_dir.mkdir(parents=True)

    write_manifest(prod_dir, "err_producer", "liquidations.v1", status="error")
    data = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8"))

    assert data["status"] == "error"


def test_write_manifest_overwrites():
    td = Path(tempfile.mkdtemp())
    prod_dir = td / "producer_a"
    prod_dir.mkdir(parents=True)

    write_manifest(prod_dir, "test", "schema.v1", status="ok")
    write_manifest(prod_dir, "test", "schema.v1", status="degraded")
    data = json.loads((prod_dir / "manifest.json").read_text(encoding="utf-8"))

    assert data["status"] == "degraded"
