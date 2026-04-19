from __future__ import annotations

CAMPAIGN_STATUSES = {
    "DRAFT",
    "FRAMED",
    "QUESTIONED",
    "ANSWERED",
    "EVALUATED",
    "COMPARED",
    "CAPITALIZATION_PENDING",
    "CAPITALIZED",
    "EXPORTED",
    "CLOSED",
    "BLOCKED",
    "REJECTED",
}

FRAMING_STATUSES = {
    "TO_FRAME",
    "IN_AUDIT",
    "FRAME_ACCEPTED",
    "FRAME_REWORK",
    "FRAME_REJECTED",
}

RESPONSE_STATUSES = {
    "CAPTURED_RAW",
    "NORMALIZED",
    "INVALID_FORMAT",
    "READY_FOR_EVAL",
}

EVALUATION_STATUSES = {
    "NOT_EVALUATED",
    "EVAL_IN_PROGRESS",
    "EVAL_COMPLETE",
    "EVAL_BIASED_SUSPECTED",
    "EVAL_REJECTED",
}

CAPITALIZATION_STATUSES = {
    "NOT_ELIGIBLE",
    "CANDIDATE_LAB",
    "CANDIDATE_STANDARD",
    "CANDIDATE_STRICT",
    "PROMOTED_LAB",
    "PROMOTED_STANDARD",
    "PROMOTED_STRICT",
    "PROMOTION_REJECTED",
}

VERDICTS = {"ACCEPT", "ACCEPT_WITH_NOTES", "REJECT"}
CERTAINTY_LEVELS = {"ETABLI", "A_CONFIRMER", "HYPOTHESE"}

REQUIRED_POLICIES = ("framing", "evaluation", "promotion")


def require_fields(payload: dict[str, object], fields: tuple[str, ...], context: str) -> None:
    missing = [field for field in fields if not payload.get(field)]
    if missing:
        from .errors import ValidationError

        raise ValidationError(f"Missing required {context} fields: {', '.join(missing)}")
