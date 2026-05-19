from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.rules import SurfaceRule, matches_any, propose_name


@dataclass
class Finding:
    surface: str
    path: str
    current_name: str
    proposed_name: str
    reason: str


def _iter_direct_children(root: Path, entry_kind: str) -> Iterable[Path]:
    if not root.exists():
        return []
    entries = []
    for entry in sorted(root.iterdir()):
        if entry_kind == "dir" and entry.is_dir():
            entries.append(entry)
        elif entry_kind == "file" and entry.is_file():
            entries.append(entry)
    return entries


def _iter_chantier_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    entries = []
    for go_dir in sorted(root.iterdir()):
        if not go_dir.is_dir():
            continue
        for item in sorted(go_dir.iterdir()):
            if item.is_file():
                entries.append(item)
    return entries


def _iter_module_scripts(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    entries = []
    for module_dir in sorted(root.iterdir()):
        if not module_dir.is_dir():
            continue
        for item in sorted(module_dir.iterdir()):
            if item.is_file() and item.suffix in {".sh", ".py"}:
                entries.append(item)
    return entries


def _iter_branches(repo_root: Path) -> Iterable[str]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(repo_root), "for-each-ref", "--format=%(refname:short)", "refs/heads"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def _is_exception(rel_path: str, name: str, exceptions: dict) -> bool:
    if rel_path in exceptions.get("paths", []):
        return True
    if name in exceptions.get("names", []):
        return True
    return False


def scan_repo(repo_root: Path, surfaces: list[SurfaceRule], exceptions: dict) -> list[Finding]:
    findings: list[Finding] = []

    for surface in surfaces:
        root = repo_root / surface.root

        if surface.selector == "direct_children":
            items = _iter_direct_children(root, surface.entry_kind)
            for item in items:
                rel_path = str(item.relative_to(repo_root))
                name = item.name
                if _is_exception(rel_path, name, exceptions):
                    continue
                if not matches_any(surface.patterns, name):
                    findings.append(
                        Finding(
                            surface=surface.name,
                            path=rel_path,
                            current_name=name,
                            proposed_name=propose_name(surface, name),
                            reason=surface.description,
                        )
                    )

        elif surface.selector == "chantier_files":
            items = _iter_chantier_files(root)
            for item in items:
                rel_path = str(item.relative_to(repo_root))
                name = item.name
                if _is_exception(rel_path, name, exceptions):
                    continue
                if not matches_any(surface.patterns, name):
                    findings.append(
                        Finding(
                            surface=surface.name,
                            path=rel_path,
                            current_name=name,
                            proposed_name=propose_name(surface, name),
                            reason=surface.description,
                        )
                    )

        elif surface.selector == "module_scripts":
            items = _iter_module_scripts(root)
            for item in items:
                rel_path = str(item.relative_to(repo_root))
                name = item.name
                if _is_exception(rel_path, name, exceptions):
                    continue
                if not matches_any(surface.patterns, name):
                    findings.append(
                        Finding(
                            surface=surface.name,
                            path=rel_path,
                            current_name=name,
                            proposed_name=propose_name(surface, name),
                            reason=surface.description,
                        )
                    )

        elif surface.selector == "branches":
            items = _iter_branches(repo_root)
            for name in items:
                if _is_exception(f"branch:{name}", name, exceptions):
                    continue
                if not matches_any(surface.patterns, name):
                    findings.append(
                        Finding(
                            surface=surface.name,
                            path=f"branch:{name}",
                            current_name=name,
                            proposed_name=propose_name(surface, name),
                            reason=surface.description,
                        )
                    )

    return findings
