from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .models import RawEvent, EnrichedEvent
from .data_provider import get_price_at
from .utils_time import add_minutes
from .event_journal import read_jsonl, existing_ids, ensure_parent_dir


def compute_outcome(
    direction: str, price_at_signal: float, future_price: float
) -> tuple[float, str]:
    if direction == "bullish":
        delta = future_price - price_at_signal
    else:
        delta = price_at_signal - future_price

    outcome = "win" if delta > 0 else "loss"
    return round(delta, 4), outcome


def enrich_event(raw: dict, config: dict) -> EnrichedEvent:
    tz_name = config.get("timezone", "America/Montreal")
    fvg_detected = raw.get("fvg_detected", False)
    direction = raw.get("fvg_direction", "")
    price_signal = raw.get("price_at_signal", 0.0)

    signal_ts_raw = raw.get("signal_ts")
    signal_ts = (
        datetime.fromisoformat(signal_ts_raw) if signal_ts_raw else None
    )

    window_ts_raw = raw.get("window_open_ts")
    window_ts = (
        datetime.fromisoformat(window_ts_raw) if window_ts_raw else None
    )

    fvg_created_raw = raw.get("fvg_created_at")
    fvg_created = (
        datetime.fromisoformat(fvg_created_raw) if fvg_created_raw else None
    )

    enriched = EnrichedEvent(
        event_id=raw.get("event_id", ""),
        version=raw.get("version", "v0"),
        symbol=raw.get("symbol", ""),
        timezone=raw.get("timezone", tz_name),
        window_type=raw.get("window_type", ""),
        window_open_ts=window_ts,
        scope=raw.get("scope", ""),
        weekday=raw.get("weekday", ""),
        ref_open=raw.get("ref_open", 0.0),
        ref_high=raw.get("ref_high", 0.0),
        ref_low=raw.get("ref_low", 0.0),
        ref_close=raw.get("ref_close", 0.0),
        fvg_detected=fvg_detected,
        fvg_direction=direction,
        fvg_top=raw.get("fvg_top", 0.0),
        fvg_bottom=raw.get("fvg_bottom", 0.0),
        fvg_created_at=fvg_created,
        signal_ts=signal_ts,
        price_at_signal=price_signal,
        sweep=raw.get("sweep", False),
        sweep_side=raw.get("sweep_side", "none"),
    )

    if not fvg_detected or not signal_ts:
        return enriched

    ts_30m = add_minutes(signal_ts, 30)
    ts_60m = add_minutes(signal_ts, 60)

    price_30m = get_price_at(raw.get("symbol", ""), ts_30m, config)
    price_60m = get_price_at(raw.get("symbol", ""), ts_60m, config)

    enriched.price_plus_30m = price_30m
    enriched.price_plus_60m = price_60m

    if price_30m is not None:
        delta, outcome = compute_outcome(direction, price_signal, price_30m)
        enriched.delta_30m = delta
        enriched.outcome_30m = outcome

    if price_60m is not None:
        delta, outcome = compute_outcome(direction, price_signal, price_60m)
        enriched.delta_60m = delta
        enriched.outcome_60m = outcome

    return enriched


def sample_pending(
    raw_path: str | Path, enriched_path: str | Path, config: dict
) -> dict:
    raw_entries = read_jsonl(raw_path)
    enriched_ids = existing_ids(enriched_path)

    processed = 0
    appended = 0
    skipped = 0

    for raw in raw_entries:
        eid = raw.get("event_id", "")
        if not eid:
            continue

        processed += 1

        if eid in enriched_ids:
            skipped += 1
            continue

        enriched = enrich_event(raw, config)
        ensure_parent_dir(enriched_path)

        from .event_journal import append_enriched_event
        result = append_enriched_event(enriched, enriched_path)
        if result == "appended":
            appended += 1
        else:
            skipped += 1

    return {"processed": processed, "appended": appended, "skipped": skipped}
