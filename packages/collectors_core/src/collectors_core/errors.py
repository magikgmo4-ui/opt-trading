from __future__ import annotations

from dataclasses import dataclass, field


class CollectorsCoreError(Exception):
    pass


class ConfigurationError(CollectorsCoreError):
    pass


class ValidationError(CollectorsCoreError):
    pass


@dataclass
class HttpRequestError(CollectorsCoreError):
    message: str
    status_code: int | None = None
    body: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    url: str | None = None

    def __str__(self) -> str:
        if self.status_code is None:
            return self.message
        return f"{self.message} (status={self.status_code})"
