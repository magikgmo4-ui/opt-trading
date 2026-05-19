from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SurfaceRule:
    name: str
    selector: str
    root: str
    entry_kind: str
    patterns: tuple[str, ...]
    proposal_style: str
    description: str


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_rules(config_dir: Path) -> tuple[list[SurfaceRule], dict]:
    raw_rules = load_json(config_dir / "naming_rules.json")
    exceptions = load_json(config_dir / "exceptions.json")
    surfaces: list[SurfaceRule] = []
    for item in raw_rules["surfaces"]:
        surfaces.append(
            SurfaceRule(
                name=item["name"],
                selector=item["selector"],
                root=item["root"],
                entry_kind=item["entry_kind"],
                patterns=tuple(item["patterns"]),
                proposal_style=item["proposal_style"],
                description=item["description"],
            )
        )
    return surfaces, exceptions


def matches_any(patterns: Iterable[str], value: str) -> bool:
    return any(re.fullmatch(pattern, value) is not None for pattern in patterns)


def to_upper_snake(stem: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    return stem.upper()


def to_lower_snake(stem: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    return stem.lower()


def to_ordered_lower_snake(filename: str) -> str:
    name, dot, ext = filename.partition(".")
    match = re.match(r"^(?P<prefix>\d{2}[A-Z]?_)?(?P<body>.*)$", name)
    prefix = match.group("prefix") or ""
    body = match.group("body")
    body = to_lower_snake(body)
    if prefix and not body:
        body = "unnamed"
    candidate = f"{prefix}{body}".strip("_")
    return f"{candidate}.{ext}" if dot else candidate


def to_branch_name(name: str) -> str:
    if "/" not in name:
        return f"chore/{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')}"
    family, slug = name.split("/", 1)
    family = family.lower()
    slug = re.sub(r"[^a-z0-9/]+", "-", slug.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"{family}/{slug}"


def to_go_canonical_placeholder(current_name: str) -> str:
    stem = to_upper_snake(current_name)
    if stem.startswith("GO_"):
        return f"{stem}__MANUAL_REVIEW_REQUIRED"
    return "GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>__MANUAL_REVIEW_REQUIRED"


def propose_name(surface: SurfaceRule, current_name: str) -> str:
    if surface.proposal_style == "go_canonical":
        return to_go_canonical_placeholder(current_name)
    if surface.proposal_style == "upper_snake":
        stem, dot, ext = current_name.partition(".")
        out = to_upper_snake(stem)
        return f"{out}.{ext.lower()}" if dot else out
    if surface.proposal_style == "lower_snake":
        stem, dot, ext = current_name.partition(".")
        out = to_lower_snake(stem)
        return f"{out}.{ext.lower()}" if dot else out
    if surface.proposal_style == "ordered_lower_snake":
        return to_ordered_lower_snake(current_name)
    if surface.proposal_style == "branch_kebab":
        return to_branch_name(current_name)
    return current_name
