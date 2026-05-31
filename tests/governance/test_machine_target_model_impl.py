from pathlib import Path

import yaml

from modules.modules_registry_reader.app.modules_registry_reader import ModulesRegistry


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_REGISTRY_PATH = REPO_ROOT / "registry" / "modules_registry.yaml"
ALLOWED_PLACEMENT_MODES = {
    "single_host",
    "operator_entry",
    "cross_host_facade",
    "portable_tool",
    "compatibility_shim",
}
DEFERRED_ANY_ALLOWLIST = set()


def load_modules_registry():
    return yaml.safe_load(MODULES_REGISTRY_PATH.read_text(encoding="utf-8"))


def test_modules_registry_entries_keep_machine_target():
    modules = load_modules_registry()

    for module in modules:
        assert "machine_target" in module, module.get("module_name")
        assert module["machine_target"], module.get("module_name")


def test_placement_mode_is_optional_but_constrained_when_present():
    modules = load_modules_registry()

    for module in modules:
        if "placement_mode" in module:
            assert module["placement_mode"] in ALLOWED_PLACEMENT_MODES, module.get("module_name")


def test_machine_target_any_requires_placement_mode_or_deferred_allowlist():
    modules = load_modules_registry()

    for module in modules:
        if module.get("machine_target") != "any":
            continue

        module_name = module.get("module_name")
        placement_mode = module.get("placement_mode")

        assert placement_mode == "portable_tool" or placement_mode == "cross_host_facade" or module_name in DEFERRED_ANY_ALLOWLIST, module_name


def test_modules_registry_reader_lists_placement_mode(capsys):
    registry = ModulesRegistry()

    registry.list_modules()
    captured = capsys.readouterr()

    assert "PLACEMENT" in captured.out
    assert "validated_prompt_factory" in captured.out
    assert "portable_tool" in captured.out
