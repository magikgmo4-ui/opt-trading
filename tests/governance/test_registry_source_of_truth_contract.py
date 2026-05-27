import json
import tempfile
from pathlib import Path

import pytest

from modules.machines_registry_reader.app.machines_registry_reader import MachinesRegistry
from modules.modules_registry_reader.app.modules_registry_reader import ModulesRegistry
from modules.registry_meta_reader.app.registry_meta_reader import MetaRegistry
from modules.ui_registry_msi.app.ui_registry_msi import UIRegistry
from modules.wrappers_registry_reader.app.wrappers_registry_reader import WrappersRegistry


def test_central_readers_report_canonical_source():
    registries = [
        ModulesRegistry(),
        MachinesRegistry(),
        WrappersRegistry(),
        MetaRegistry(),
        UIRegistry(),
    ]

    for registry in registries:
        assert registry.source_file is not None
        assert registry.source_kind == "central"
        assert registry.is_canonical_source is True


def test_ui_registry_uses_seed_as_explicit_fallback(monkeypatch, capsys):
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        missing_central = td_path / "ui_surfaces_registry.yaml"
        seed = td_path / "ui_registry_seed.json"
        seed.write_text(
            json.dumps([
                {
                    "surface_name": "seed_only",
                    "machine_target": "student",
                    "category": "ui/test",
                    "status": "ready",
                    "actions": "cmd-seed_only",
                }
            ]),
            encoding="utf-8",
        )

        monkeypatch.setattr(
            "modules.ui_registry_msi.app.ui_registry_msi.CENTRAL_REGISTRY_FILE",
            missing_central,
        )
        monkeypatch.setattr(
            "modules.ui_registry_msi.app.ui_registry_msi.SEED_FILE",
            seed,
        )

        registry = UIRegistry()

        assert registry.source_file == seed
        assert registry.source_kind == "fallback_seed"
        assert registry.is_canonical_source is False
        assert registry.surfaces[0]["surface_name"] == "seed_only"

        captured = capsys.readouterr()
        assert "fallback seed" in captured.err


def test_ui_registry_fails_without_central_or_seed(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        missing_central = td_path / "ui_surfaces_registry.yaml"
        missing_seed = td_path / "ui_registry_seed.json"

        monkeypatch.setattr(
            "modules.ui_registry_msi.app.ui_registry_msi.CENTRAL_REGISTRY_FILE",
            missing_central,
        )
        monkeypatch.setattr(
            "modules.ui_registry_msi.app.ui_registry_msi.SEED_FILE",
            missing_seed,
        )

        with pytest.raises(SystemExit):
            UIRegistry()
