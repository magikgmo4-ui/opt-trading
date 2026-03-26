from __future__ import annotations

from app.core.clock import now_iso
from app.core.id_sequence import next_brick_id
from app.core.slugify import slugify
from app.renderers.brick_renderer import render_brick
from app.schemas.brick_schema import BrickModel
from app.storage.markdown_store import save_brick


def create_brick(
    brick_type: str,
    title: str,
    ia: str,
    machine: str,
    surface: str,
    project: str,
    module_name: str,
    status: str,
    summary_short: str = "",
    resume_point: str = "",
    tags: list[str] | None = None,
    repo: str = "",
    branch: str = "",
    path: str = "",
    decisions: list[str] | None = None,
    todo: list[str] | None = None,
    source_ref: list[str] | None = None,
    canonical_ref: list[str] | None = None,
    real_state_ref: list[str] | None = None,
    validated_by: str = "",
) -> dict[str, str]:
    brick_id = next_brick_id()
    brick = BrickModel(
        id=brick_id,
        title=title,
        date=now_iso(),
        type=brick_type,
        status=status,
        ia=ia,
        machine=machine,
        surface=surface,
        project=project,
        module=module_name,
        summary_short=summary_short or f"{title} — {status}",
        resume_point=resume_point,
        tags=tags or [],
        repo=repo,
        branch=branch,
        path=path,
        decisions=decisions or [],
        todo=todo or [],
        source_ref=source_ref or [],
        canonical_ref=canonical_ref or [],
        real_state_ref=real_state_ref or [],
        validated_by=validated_by,
    )
    brick.validate()
    content = render_brick(brick)
    saved = save_brick(brick, content, slugify(title))
    return {"id": brick_id, "file": str(saved)}
