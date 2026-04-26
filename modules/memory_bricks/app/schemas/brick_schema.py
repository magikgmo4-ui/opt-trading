from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import re
from typing import Any

from app.core.constants import ALLOWED_IAS, ALLOWED_STATUSES, ALLOWED_TYPES, DEFAULT_MODULE, DEFAULT_PROJECT, DEFAULT_TIMEZONE


BRICK_ID_RE = re.compile(r"^MB-[0-9]{5}$")


@dataclass
class BrickModel:
    id: str
    title: str
    date: str
    timezone: str = DEFAULT_TIMEZONE
    type: str = "reference"
    status: str = "draft"
    ia: str = "generic"
    machine: str = ""
    surface: str = ""
    project: str = ""
    module: str = "memory_bricks"
    summary_short: str = ""
    resume_point: str = ""
    links: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    repo: str = ""
    branch: str = ""
    path: str = ""
    source_ref: list[Any] = field(default_factory=list)
    canonical_ref: list[Any] = field(default_factory=list)
    real_state_ref: list[Any] = field(default_factory=list)
    validated_by: str = ""
    decisions: list[str] = field(default_factory=list)
    todo: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.id = str(self.id).strip()
        self.title = str(self.title).strip()
        self.date = str(self.date).strip()
        self.timezone = str(self.timezone or DEFAULT_TIMEZONE).strip() or DEFAULT_TIMEZONE
        self.type = str(self.type).strip()
        self.status = str(self.status).strip()
        self.ia = str(self.ia).strip()
        self.machine = str(self.machine).strip()
        self.surface = str(self.surface).strip()
        self.project = str(self.project or DEFAULT_PROJECT).strip() or DEFAULT_PROJECT
        self.module = str(self.module or DEFAULT_MODULE).strip() or DEFAULT_MODULE
        self.summary_short = str(self.summary_short).strip()
        self.resume_point = str(self.resume_point).strip()
        self.repo = str(self.repo).strip()
        self.branch = str(self.branch).strip()
        self.path = str(self.path).strip()
        self.validated_by = str(self.validated_by).strip()
        self.links = _string_list(self.links)
        self.tags = _string_list(self.tags)
        self.source_ref = _string_list(self.source_ref)
        self.canonical_ref = _string_list(self.canonical_ref)
        self.real_state_ref = _string_list(self.real_state_ref)
        self.decisions = _string_list(self.decisions)
        self.todo = _string_list(self.todo)

    def validate(self) -> None:
        if not BRICK_ID_RE.fullmatch(self.id):
            raise ValueError(f"Invalid brick id: {self.id}")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        try:
            datetime.fromisoformat(self.date)
        except ValueError as exc:
            raise ValueError(f"Invalid date: {self.date}") from exc
        if self.type not in ALLOWED_TYPES:
            raise ValueError(f"Invalid type: {self.type}")
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {self.status}")
        if self.ia and self.ia not in ALLOWED_IAS:
            raise ValueError(f"Invalid ia: {self.ia}")
        if not self.machine:
            raise ValueError("machine cannot be empty")
        if not self.surface:
            raise ValueError("surface cannot be empty")
        if not self.project:
            raise ValueError("project cannot be empty")
        if not self.module:
            raise ValueError("module cannot be empty")
        if not self.summary_short.strip():
            raise ValueError("summary_short cannot be empty")
        if len(set(self.links)) != len(self.links):
            raise ValueError("links cannot contain duplicates")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _string_list(values: list[Any] | tuple[Any, ...] | None) -> list[str]:
    if values is None:
        return []
    if not isinstance(values, (list, tuple)):
        raise ValueError("Expected a list value")
    return [str(value).strip() for value in values if str(value).strip()]
