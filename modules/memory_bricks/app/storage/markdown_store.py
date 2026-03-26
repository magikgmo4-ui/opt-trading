from __future__ import annotations

from pathlib import Path

from app.core.frontmatter import parse_frontmatter
from app.core.paths import get_bricks_dir
from app.schemas.brick_schema import BrickModel


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("Markdown file missing frontmatter")
    _, rest = text.split("---\n", 1)
    front, body = rest.split("\n---\n", 1)
    return parse_frontmatter(front), body.strip()

def save_brick(brick: BrickModel, content: str, slug: str) -> Path:
    out = get_bricks_dir() / f"{brick.id}__{slug}.md"
    out.write_text(content, encoding="utf-8")
    return out

def _find_path(brick_id: str) -> Path:
    matches = sorted(get_bricks_dir().glob(f"{brick_id}__*.md"))
    if not matches:
        raise FileNotFoundError(f"Brick not found: {brick_id}")
    if len(matches) > 1:
        raise ValueError(f"Multiple brick files found for {brick_id}")
    return matches[0]

def load_brick_text(brick_id: str) -> str:
    return _find_path(brick_id).read_text(encoding="utf-8")

def load_brick(brick_id: str) -> BrickModel:
    text = load_brick_text(brick_id)
    data, _ = _split_frontmatter(text)
    brick = BrickModel(**data)
    brick.validate()
    return brick

def overwrite_brick(brick: BrickModel, content: str) -> None:
    path = _find_path(brick.id)
    path.write_text(content, encoding="utf-8")

def load_all_bricks() -> list[BrickModel]:
    bricks = []
    for path in sorted(get_bricks_dir().glob("MB-*.md")):
        data, _ = _split_frontmatter(path.read_text(encoding="utf-8"))
        brick = BrickModel(**data)
        brick.validate()
        bricks.append(brick)
    return sorted(bricks, key=lambda brick: (brick.date, brick.id))

def load_bricks_by_ids(ids: list[str]) -> list[BrickModel]:
    unique_ids: list[str] = []
    for brick_id in ids:
        normalized = brick_id.strip()
        if normalized and normalized not in unique_ids:
            unique_ids.append(normalized)
    return [load_brick(brick_id) for brick_id in unique_ids]
