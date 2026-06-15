"""
Voice Operator — Freshness Model
GO_VOICE_OPERATOR_STALE_DATA_GUARDS_01

Classifies data freshness for voice responses.
Prevents ambiguity: "0.0" is never presented as a live price.
"""
from enum import Enum
from datetime import datetime, timezone


class FreshnessState(str, Enum):
    LIVE = "LIVE"
    STALE = "STALE"
    MARKET_CLOSED = "MARKET_CLOSED"
    UNKNOWN = "UNKNOWN"
    NO_DATA = "NO_DATA"


def classify_freshness(
    price: float | None = None,
    source_quality: str | None = None,
    source: str | None = None,
    data_age_minutes: int | None = None,
    generated_at: str | None = None,
    pipeline_state: str | None = None,
) -> dict:
    """Classify data freshness for voice operator display.

    Returns a dict with freshness_state, badge info, and spoken context,
    intended to be injected into the /voice/query response.
    """
    # NO_DATA: no price at all
    if price is None or price == 0:
        if source_quality in ("unavailable", None):
            return {
                "freshness_state": FreshnessState.NO_DATA,
                "badge": "NO DATA",
                "css_class": "freshness-no-data",
                "spoken": "aucune donnee disponible",
                "warning": "Aucune quote recue. Verifier les sources.",
            }
        if data_age_minutes and data_age_minutes > 720:
            return {
                "freshness_state": FreshnessState.STALE,
                "badge": "MARKET CLOSED",
                "css_class": "freshness-stale",
                "spoken": "marche ferme. aucune donnee temps reel.",
                "warning": "Derniere donnee valide: marche ferme ou source stale.",
            }
        return {
            "freshness_state": FreshnessState.MARKET_CLOSED,
            "badge": "MARKET CLOSED",
            "css_class": "freshness-stale",
            "spoken": "marche ferme. donnees non temps reel.",
            "warning": "Marche ferme. Les prix affiches peuvent dater de la derniere session.",
        }

    # LIVE: recent quote, good source
    if source_quality in ("direct", "delayed") and (source or "").lower() not in ("unknown", "stale", ""):
        age_hint = f" (il y a {data_age_minutes}min)" if data_age_minutes and data_age_minutes < 60 else ""
        return {
            "freshness_state": FreshnessState.LIVE,
            "badge": "LIVE",
            "css_class": "freshness-live",
            "spoken": f"donnee live{age_hint}",
            "warning": None,
        }

    # STALE: old data
    if data_age_minutes and data_age_minutes > 60:
        return {
            "freshness_state": FreshnessState.STALE,
            "badge": f"STALE ({data_age_minutes}min)",
            "css_class": "freshness-stale",
            "spoken": f"donnee stale, agee de {data_age_minutes} minutes",
            "warning": f"Donnee agee de {data_age_minutes} minutes. Peut ne pas refleter le marche actuel.",
        }

    # UNKNOWN: source present but quality uncertain
    if pipeline_state == "degraded" or source_quality == "unknown":
        return {
            "freshness_state": FreshnessState.UNKNOWN,
            "badge": "QUALITY UNKNOWN",
            "css_class": "freshness-unknown",
            "spoken": "qualite de la source indeterminee",
            "warning": "Qualite de la source indeterminee. Donnees potentiellement non fiables.",
        }

    # Default: LIVE but conservative
    return {
        "freshness_state": FreshnessState.UNKNOWN,
        "badge": "UNKNOWN",
        "css_class": "freshness-unknown",
        "spoken": "fraicheur indeterminee",
        "warning": None,
    }


def compute_age_minutes(generated_at: str | None) -> int | None:
    """Compute age in minutes from an ISO timestamp."""
    if not generated_at:
        return None
    try:
        ts = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - ts).total_seconds()
        return int(age / 60)
    except Exception:
        return None
