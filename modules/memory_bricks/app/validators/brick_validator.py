from __future__ import annotations

from app.schemas.brick_schema import BrickModel


def validate_brick(brick: BrickModel) -> None:
    brick.validate()
