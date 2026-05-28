from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

try:
    from pydantic import BaseModel, Field  # type: ignore
except ImportError:
    _REQUIRED = object()

    @dataclass(frozen=True)
    class _FieldSpec:
        default: Any = _REQUIRED
        default_factory: Callable[[], Any] | None = None

    def Field(  # type: ignore[misc]
        default: Any = _REQUIRED,
        *,
        default_factory: Callable[[], Any] | None = None,
        **_: Any,
    ) -> _FieldSpec:
        return _FieldSpec(default=default, default_factory=default_factory)

    class BaseModel:
        def __init__(self, **kwargs: Any) -> None:
            annotations = getattr(self.__class__, "__annotations__", {})
            for name in annotations:
                if name in kwargs:
                    value = kwargs[name]
                else:
                    spec = getattr(self.__class__, name, _REQUIRED)
                    if isinstance(spec, _FieldSpec):
                        if spec.default_factory is not None:
                            value = spec.default_factory()
                        elif spec.default is not _REQUIRED:
                            value = spec.default
                        else:
                            raise TypeError(f"Missing required field: {name}")
                    elif spec is not _REQUIRED:
                        value = spec
                    else:
                        raise TypeError(f"Missing required field: {name}")
                setattr(self, name, value)

        def model_dump(self) -> dict[str, Any]:
            annotations = getattr(self.__class__, "__annotations__", {})
            return {name: getattr(self, name) for name in annotations}
