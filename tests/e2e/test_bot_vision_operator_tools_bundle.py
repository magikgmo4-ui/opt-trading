from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_operator_tools_bundle_files_exist():
    expected = [
        PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_runtime_real_preflight.py",
        PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_canonical_checkout.py",
        PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_runtime_stabilize.py",
        PROJECT_ROOT / "docs" / "chantiers" / "GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01" / "00_CADRAGE.md",
        PROJECT_ROOT / "docs" / "chantiers" / "GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01" / "01_USAGE.md",
    ]
    for path in expected:
        assert path.exists(), f"Missing bundle file: {path}"


def test_operator_tools_bundle_usage_mentions_all_three_scripts():
    usage = (
        PROJECT_ROOT
        / "docs"
        / "chantiers"
        / "GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01"
        / "01_USAGE.md"
    ).read_text(encoding="utf-8")
    assert "bot_vision_runtime_real_preflight.py" in usage
    assert "bot_vision_admin_trading_canonical_checkout.py" in usage
    assert "bot_vision_admin_trading_runtime_stabilize.py" in usage
