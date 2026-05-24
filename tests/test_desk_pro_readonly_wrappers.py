import json
from pathlib import Path

from modules.desk_pro.desk_snapshot_adapter import (
    normalize_desk_snapshot_v1,
    read_desk_snapshot_v1,
    validate_desk_snapshot_v1,
)
from modules.desk_pro.visual_context_adapter import (
    normalize_visual_context_v1,
    read_visual_context_v1,
    validate_visual_context_v1,
)


FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestDeskProReadonlyWrappers:
    def test_desk_snapshot_normalize_validate(self):
        raw = _load("desk_snapshot_minimal.json")
        v1 = normalize_desk_snapshot_v1(raw)
        ok, errors = validate_desk_snapshot_v1(v1)
        assert ok is True
        assert errors == []

    def test_desk_snapshot_read_is_readonly(self, tmp_path: Path):
        raw = _load("desk_snapshot_minimal.json")
        p = tmp_path / "desk_snapshot.json"
        p.write_text(json.dumps(raw), encoding="utf-8")
        v1 = read_desk_snapshot_v1(p)
        assert v1 is not None
        ok, errors = validate_desk_snapshot_v1(v1)
        assert ok is True
        assert errors == []

    def test_visual_context_normalize_validate(self):
        raw = _load("visual_context_v1_minimal.json")
        v1 = normalize_visual_context_v1(raw)
        ok, errors = validate_visual_context_v1(v1)
        assert ok is True
        assert errors == []

    def test_visual_context_read_is_readonly(self, tmp_path: Path):
        raw = _load("visual_context_v1_minimal.json")
        p = tmp_path / "visual_context.json"
        p.write_text(json.dumps(raw), encoding="utf-8")
        v1 = read_visual_context_v1(p)
        assert v1 is not None
        ok, errors = validate_visual_context_v1(v1)
        assert ok is True
        assert errors == []

