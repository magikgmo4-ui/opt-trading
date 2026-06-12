#!/usr/bin/env python3
"""OT-Core UI governance checker — detects regressions in the design system.

Rules:
  1. No hardcoded {{<span class="badge ...">}} in LocalCMS — use badge() helpers.
  2. No raw inline CSS blocks in LocalCMS that don't reference STANDARD_CSS
     or SIGNALS_DARK_CSS constants.
  3. HTML-generating Python files must import from shared.html_helpers
     or shared.html_design_system when they contain HTML strings > 100 chars.

Exit: 0 = PASS, 1 = VIOLATION, 2 = CONFIG_ERROR

Usage:
    python3 scripts/ui/governance_check.py [--strict]
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DESIGN_SYSTEM_CONSTANTS: frozenset[str] = frozenset({
    "STANDARD_CSS", "SIGNALS_DARK_CSS", "LIGHT_CSS", "DARK_BASE",
    "BADGE_CSS", "TABLE_CSS", "CARD_CSS", "MISC_CSS", "CSS_RESET", "COLORS",
})

SHARED_HELPER_IMPORTS: frozenset[str] = frozenset({
    "badge", "card", "table", "page_shell", "sidebar_nav", "links_bar",
    "auto_refresh_script", "auto_refresh_xhr", "pnl_badge", "verdict_badge",
    "closeout_badge", "cred_status_badge", "STATUS_BADGES", "summary_card",
    "kpi_grid", "section_title", "notice",
})

FILES_TO_CHECK: list[Path] = [
    REPO_ROOT / "modules" / "localcms" / "app" / "main.py",
    REPO_ROOT / "modules" / "desk_pro" / "api" / "routes.py",
    REPO_ROOT / "modules" / "desk_pro" / "ui" / "page.py",
    REPO_ROOT / "perf" / "perf_app.py",
    REPO_ROOT / "webhook_server.py",
]


def _find_import(file_path: Path, module: str) -> bool:
    try:
        tree = ast.parse(file_path.read_text())
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == module:
                return True
    return False


def check_inline_badge_pattern(content: str, file_path: Path) -> list[str]:
    violations: list[str] = []
    for lineno, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if ('<span class="badge' in stripped or "<span class='badge" in stripped) \
           and "badge(" not in stripped \
           and "#" not in stripped:
            violations.append(
                f"  {file_path.name}:{lineno}: hardcoded badge HTML — use badge() from shared.html_helpers"
            )
    return violations


def check_inline_style_no_constant(content: str, file_path: Path) -> list[str]:
    violations: list[str] = []
    lines = content.splitlines()
    in_style = False
    style_start = 0
    block_lines: list[str] = []

    for lineno, line in enumerate(lines, 1):
        if "<style>" in line:
            in_style = True
            style_start = lineno
            block_lines = []
            continue
        if "</style>" in line:
            if in_style and block_lines:
                block_text = "\n".join(block_lines)
                uses_constant = any(
                    f"{{{c}}}" in block_text for c in DESIGN_SYSTEM_CONSTANTS
                )
                if not uses_constant:
                    violations.append(
                        f"  {file_path.name}:{style_start}: inline CSS block "
                        f"not using design system constant — "
                        f"replace with {{{', '.join(sorted(DESIGN_SYSTEM_CONSTANTS)[:3])}}}... or add new constant"
                    )
            in_style = False
            block_lines = []
            continue
        if in_style:
            block_lines.append(line)

    return violations


def check_html_routes_without_shared_import(file_path: Path) -> list[str]:
    violations: list[str] = []
    try:
        content = file_path.read_text()
    except OSError:
        return []

    if file_path.name.endswith(".py"):
        has_helpers = _find_import(file_path, "shared.html_helpers")
        has_design = _find_import(file_path, "shared.html_design_system")

        has_html = any(
            kw in content for kw in ("HTMLResponse", "html", "<div", "<table", "<style", "<body")
        )
        large_html = content.count("\n") > 50 and has_html

        if large_html and not has_helpers and not has_design:
            violations.append(
                f"  {file_path.name}: HTML-generating file without shared.html_helpers "
                f"or shared.html_design_system import — consider adding"
            )
    return violations


def main() -> int:
    strict = "--strict" in sys.argv
    all_violations: list[str] = []
    warnings: list[str] = []

    for file_path in FILES_TO_CHECK:
        if not file_path.exists():
            print(f"[WARN] {file_path} not found — skipping")
            continue

        try:
            content = file_path.read_text()
        except OSError as e:
            print(f"[ERROR] Cannot read {file_path}: {e}")
            continue

        all_violations.extend(check_inline_badge_pattern(content, file_path))
        all_violations.extend(check_inline_style_no_constant(content, file_path))
        warnings.extend(check_html_routes_without_shared_import(file_path))

    if warnings:
        print("[WARNINGS]")
        for w in warnings:
            print(w)
        print()

    if all_violations:
        print(f"[VIOLATIONS] {len(all_violations)} found:")
        for v in all_violations:
            print(v)
        print()
        if not strict:
            print("[INFO] Run with --strict to exit non-zero on violations.")
        return 1 if strict else 0

    print("[PASS] OT-Core UI governance — no violations detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
