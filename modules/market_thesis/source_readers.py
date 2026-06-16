"""
Source readers — PR2.

Reads raw data from all existing sources and normalizes them
into structured records for the context aggregator.

Design principles:
- Never crash on missing/invalid sources
- Ignore malformed JSONL lines, record errors
- Normalize symbol names and event aliases
- Preserve source, timestamp, freshness for every record
- All functions accept an optional symbol filter
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (
    SOURCES,
    normalize_event_alias,
    normalize_symbol,
    source_path_for_symbol,
)
from .source_status import SourceStatus, evaluate_freshness


# ── Internal record types ──────────────────────────────────────────────────

@dataclass
class NormalizedEvent:
    """A single normalized event from any source."""

    source: str
    symbol: str
    event_type: str            # normalized alias
    direction: str             # BUY / SELL / NEUTRAL / MONITOR_ONLY
    price: Optional[float] = None
    volume: Optional[float] = None
    timeframe: Optional[str] = None
    ts: Optional[datetime] = None
    confidence: Optional[float] = None
    raw_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedMetrics:
    """Normalized market metrics for a symbol."""

    source: str
    symbol: str
    ts: Optional[datetime] = None
    price: Optional[float] = None
    open_interest: Optional[float] = None
    funding_rate: Optional[float] = None
    volume_24h: Optional[float] = None
    long_short_ratio: Optional[float] = None
    liquidations_long: Optional[float] = None
    liquidations_short: Optional[float] = None
    price_change_24h_pct: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedSetup:
    """Normalized technical setup from multitf_setup_score."""

    source: str
    symbol: str
    setup_id: str
    direction: str
    setup_type: str
    grade: str
    score: int = 0
    probability_pct: float = 0.0
    confidence_pct: float = 0.0
    entry_zone: List[float] = field(default_factory=list)
    invalidation: Optional[float] = None
    targets: List[float] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedVision:
    """Normalized vision/coinglass context."""

    source: str
    symbol: str
    ts: Optional[datetime] = None
    support_levels: List[float] = field(default_factory=list)
    resistance_levels: List[float] = field(default_factory=list)
    analysis_summary: Optional[str] = None
    coinglass_detections: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ── JSONL reader ───────────────────────────────────────────────────────────

def _read_jsonl(
    path: Path | None,
    symbol: Optional[str] = None,
    status: Optional[SourceStatus] = None,
) -> List[Dict[str, Any]]:
    """Read a JSONL file, returning valid records.

    Invalid lines are skipped and counted in status.errors.
    Returns empty list if file missing or unreadable.
    """
    if path is None or not path.exists():
        return []

    records: List[Dict[str, Any]] = []
    try:
        with open(path, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                    if status:
                        status.records_valid += 1
                except json.JSONDecodeError:
                    if status:
                        if not status.error_message:
                            status.error_message = f"Invalid JSONL line {line_num}"
                        else:
                            status.error_message += f", line {line_num}"
                except Exception as exc:
                    if status:
                        if not status.error_message:
                            status.error_message = f"Line {line_num}: {exc}"
    except (OSError, IOError) as exc:
        if status:
            status.state = "error"
            status.error_message = str(exc)
        return []

    if status:
        status.records_count = len(records)

    # Filter by symbol if requested
    if symbol:
        filtered = []
        for rec in records:
            raw_sym = rec.get("symbol", rec.get("pair", rec.get("ticker", "")))
            if normalize_symbol(raw_sym) == symbol:
                filtered.append(rec)
        if status:
            status.records_filtered = len(records) - len(filtered)
        return filtered

    return records


# ── Source-specific readers ────────────────────────────────────────────────

def read_events_jsonl(
    symbol: Optional[str] = None,
) -> tuple[List[NormalizedEvent], SourceStatus]:
    """Read webhook events from state/events.jsonl."""
    path = SOURCES.get("events_jsonl")
    status = SourceStatus(
        name="Webhook Events",
        contract="webhook_event.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return [], status

    freshness = evaluate_freshness(path)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    raw = _read_jsonl(path, symbol, status)
    events: List[NormalizedEvent] = []

    for rec in raw:
        try:
            evt = NormalizedEvent(
                source="webhook",
                symbol=normalize_symbol(rec.get("symbol", "")),
                event_type=normalize_event_alias(rec.get("signal", rec.get("event", ""))),
                direction=rec.get("signal", rec.get("direction", "NEUTRAL")),
                price=rec.get("price"),
                volume=rec.get("qty"),
                timeframe=rec.get("tf"),
                ts=_parse_ts(rec.get("_ts")),
                confidence=None,
                raw_reason=rec.get("reason"),
                metadata={"engine": rec.get("engine"), "tp": rec.get("tp"), "sl": rec.get("sl")},
            )
            events.append(evt)
        except Exception as exc:
            if status.error_message:
                status.error_message += f"; record error: {exc}"
            else:
                status.error_message = f"Record error: {exc}"

    return events, status


def read_events_cdp_jsonl(
    symbol: Optional[str] = None,
) -> tuple[List[NormalizedEvent], SourceStatus]:
    """Read CDP events from state/events_cdp.jsonl."""
    path = SOURCES.get("events_cdp_jsonl")
    status = SourceStatus(
        name="CDP Events",
        contract="signal_event.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return [], status

    freshness = evaluate_freshness(path)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    raw = _read_jsonl(path, symbol, status)
    events: List[NormalizedEvent] = []

    for rec in raw:
        try:
            evt = NormalizedEvent(
                source="cdp",
                symbol=normalize_symbol(rec.get("symbol", "")),
                event_type=normalize_event_alias(rec.get("event", rec.get("signal", ""))),
                direction="MONITOR_ONLY",
                price=rec.get("price"),
                volume=rec.get("volume"),
                timeframe=rec.get("timeframe", rec.get("tf")),
                ts=_parse_ts(rec.get("timestamp") or rec.get("_ts") or rec.get("ts")),
                confidence=rec.get("confidence"),
                raw_reason=None,
                metadata={"flags": rec.get("flags", {})},
            )
            events.append(evt)
        except Exception:
            pass

    return events, status


def read_market_metrics(
    symbol: str,
) -> tuple[Optional[NormalizedMetrics], SourceStatus]:
    """Read market_metrics.v1 for a given canonical symbol."""
    path = source_path_for_symbol("market_metrics", symbol)
    status = SourceStatus(
        name="Market Metrics",
        contract="market_metrics.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return None, status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return None, status

    status.records_count = 1
    status.records_valid = 1

    # Timestamp from payload
    data_ts = _parse_ts(raw.get("metrics_ts") or raw.get("produced_at") or raw.get("as_of"))
    freshness = evaluate_freshness(path, data_ts)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    metrics_raw = raw.get("metrics", {})
    norm = NormalizedMetrics(
        source="market_metrics",
        symbol=symbol,
        ts=data_ts,
        price=raw.get("last_price") or metrics_raw.get("price"),
        open_interest=metrics_raw.get("open_interest"),
        funding_rate=metrics_raw.get("funding_rate"),
        volume_24h=metrics_raw.get("volume_futures") or metrics_raw.get("volume_24h"),
        long_short_ratio=metrics_raw.get("long_short_ratio"),
        liquidations_long=metrics_raw.get("liquidations_long"),
        liquidations_short=metrics_raw.get("liquidations_short"),
        price_change_24h_pct=metrics_raw.get("price_change_24h_pct"),
        metadata={"freshness_state": raw.get("freshness_state"), "provider": raw.get("provider_id")},
    )
    return norm, status


def read_multitf_analysis(
    symbol: str,
) -> tuple[Optional[Dict[str, Any]], SourceStatus]:
    """Read multitf_analysis_input.v1 for a given canonical symbol."""
    path = source_path_for_symbol("multitf_analysis", symbol)
    status = SourceStatus(
        name="Multi-TF Analysis",
        contract="multitf_analysis_input.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return None, status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return None, status

    status.records_count = 1
    status.records_valid = 1

    data_ts = _parse_ts(raw.get("as_of"))
    freshness = evaluate_freshness(path, data_ts)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    return raw, status


def read_multitf_scores(
    symbol: str,
) -> tuple[List[NormalizedSetup], SourceStatus]:
    """Read multitf_setup_score.v1 for a given canonical symbol."""
    path = source_path_for_symbol("multitf_scores", symbol)
    status = SourceStatus(
        name="Multi-TF Scores",
        contract="multitf_setup_score.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return [], status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return [], status

    status.records_count = 1
    status.records_valid = 1

    data_ts = _parse_ts(raw.get("as_of"))
    freshness = evaluate_freshness(path, data_ts)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    setups: List[NormalizedSetup] = []
    for s in raw.get("setups", []):
        setups.append(NormalizedSetup(
            source="multitf_scores",
            symbol=symbol,
            setup_id=s.get("setup_id", ""),
            direction=s.get("direction", "monitor_only"),
            setup_type=s.get("setup_type", ""),
            grade=s.get("grade", "REJECT"),
            score=s.get("score", 0),
            probability_pct=s.get("probability_pct", 0.0),
            confidence_pct=s.get("confidence_pct", 0.0),
            entry_zone=s.get("entry_zone", []),
            invalidation=s.get("invalidation"),
            targets=s.get("targets", []),
            reasons=s.get("reason", []),
            metadata={
                "bias": raw.get("bias"),
                "missing": s.get("missing", []),
                "score_breakdown": s.get("score_breakdown", {}),
            },
        ))
    return setups, status


def read_vision_coinglass(
    symbol: Optional[str] = None,
) -> tuple[Optional[NormalizedVision], SourceStatus]:
    """Read vision_context.coinglass.v1 (single global file, filtered by symbol)."""
    path = SOURCES.get("vision_coinglass")
    status = SourceStatus(
        name="Vision Coinglass",
        contract="vision_context.coinglass.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return None, status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return None, status

    status.records_count = 1
    status.records_valid = 1

    raw_sym = raw.get("symbol", "")
    canon_sym = normalize_symbol(raw_sym)

    if symbol and canon_sym != symbol:
        status.records_filtered = 1
        status.records_valid = 0
        return None, status

    data_ts = _parse_ts(raw.get("analysis_ts") or raw.get("screenshot_ts"))
    freshness = evaluate_freshness(path, data_ts)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    return NormalizedVision(
        source="vision_coinglass",
        symbol=canon_sym,
        ts=data_ts,
        coinglass_detections=raw.get("detections", []),
        metadata={"screen_type": raw.get("screen_type"), "slug": raw.get("coinglass_slug")},
    ), status


def read_vision_analysis(
    symbol: str,
) -> tuple[Optional[NormalizedVision], SourceStatus]:
    """Read vision_analysis.v1 from DC views for a given symbol."""
    path = source_path_for_symbol("vision_analysis_dc", symbol)
    status = SourceStatus(
        name="Vision Analysis",
        contract="vision_analysis.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return None, status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return None, status

    status.records_count = 1
    status.records_valid = 1

    data_ts = _parse_ts(raw.get("analysis_ts") or raw.get("as_of"))
    freshness = evaluate_freshness(path, data_ts)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    signals = raw.get("signals", [])
    supports = [s.get("value") for s in signals if s.get("type") == "support_level" and isinstance(s.get("value"), (int, float))]
    resistances = [s.get("value") for s in signals if s.get("type") == "resistance_level" and isinstance(s.get("value"), (int, float))]

    return NormalizedVision(
        source="vision_analysis",
        symbol=symbol,
        ts=data_ts,
        support_levels=sorted(supports),
        resistance_levels=sorted(resistances),
        analysis_summary=raw.get("analysis_summary"),
        metadata={"capture_id": raw.get("capture_id"), "timeframe": raw.get("timeframe")},
    ), status


def read_telegram_signals(
    symbol: Optional[str] = None,
) -> tuple[List[NormalizedEvent], SourceStatus]:
    """Read telegram signal files from data/telegram_screener/signals/."""
    base = SOURCES.get("telegram_screener")
    status = SourceStatus(
        name="Telegram Signals",
        contract="telegram_signal.v1",
        path=str(base) if base else None,
    )

    if base is None or not base.exists():
        status.state = "missing"
        return [], status

    # Find the newest file to gauge freshness
    try:
        files = sorted(
            [f for f in base.iterdir() if f.suffix == ".json"],
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
    except OSError as exc:
        status.state = "error"
        status.error_message = str(exc)
        return [], status

    if not files:
        status.state = "missing"
        return [], status

    # Overall freshness from newest file
    newest = files[0]
    freshness = evaluate_freshness(newest)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    events: List[NormalizedEvent] = []
    for f in files:
        try:
            rec = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        status.records_count += 1

        raw_pair = rec.get("pair", "")
        canon = normalize_symbol(raw_pair)
        if symbol and canon != symbol:
            status.records_filtered += 1
            continue

        status.records_valid += 1

        try:
            ts = _parse_ts(rec.get("parsed_at") or rec.get("produced_at"))
            evt = NormalizedEvent(
                source="telegram",
                symbol=canon,
                event_type=rec.get("signal_type", "trade"),
                direction=rec.get("direction", "NEUTRAL"),
                price=rec.get("entry_price"),
                timeframe=None,
                ts=ts,
                confidence=_confidence_to_float(rec.get("confidence")),
                raw_reason=rec.get("summary") or rec.get("raw_text", "")[:200],
                metadata={
                    "channel": rec.get("channel"),
                    "channel_priority": rec.get("channel_priority"),
                    "tps": rec.get("tps", []),
                    "sl": rec.get("sl"),
                },
            )
            events.append(evt)
        except Exception:
            status.records_valid -= 1

    return events, status


def read_telegram_signals_dc(
    symbol: Optional[str] = None,
) -> tuple[List[NormalizedEvent], SourceStatus]:
    """Read telegram_signals.v1 from DC views for a given symbol."""
    path = source_path_for_symbol("telegram_signals_dc", symbol) if symbol else None
    status = SourceStatus(
        name="Telegram Signals DC",
        contract="telegram_signals.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return [], status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return [], status

    status.records_count = 1
    status.records_valid = 1

    freshness = evaluate_freshness(path)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    events: List[NormalizedEvent] = []
    # The DC format may be a list or an object with signals[]
    signals_list = raw if isinstance(raw, list) else raw.get("signals", raw.get("items", []))
    for s in signals_list if isinstance(signals_list, list) else [signals_list]:
        try:
            evt = NormalizedEvent(
                source="telegram_dc",
                symbol=normalize_symbol(s.get("pair", s.get("symbol", ""))),
                event_type=s.get("signal_type", "signal"),
                direction=s.get("direction", "NEUTRAL"),
                price=s.get("entry_price", s.get("price")),
                ts=_parse_ts(s.get("timestamp") or s.get("ts") or s.get("parsed_at")),
                confidence=_confidence_to_float(s.get("confidence")),
                raw_reason=s.get("summary", ""),
                metadata={"channel": s.get("channel")},
            )
            events.append(evt)
        except Exception:
            pass

    return events, status


def read_signal_event_dc(
    symbol: str,
) -> tuple[List[NormalizedEvent], SourceStatus]:
    """Read signal_event.v1 from DC views for a given symbol."""
    path = source_path_for_symbol("signal_event", symbol)
    status = SourceStatus(
        name="Signal Events DC",
        contract="signal_event.v1",
        path=str(path) if path else None,
    )

    if path is None or not path.exists():
        status.state = "missing"
        return [], status

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        status.state = "error"
        status.error_message = str(exc)
        return [], status

    status.records_count = 1
    status.records_valid = 1

    freshness = evaluate_freshness(path)
    status.state = freshness["state"]
    status.age_minutes = freshness["age_minutes"]

    events: List[NormalizedEvent] = []
    items = raw if isinstance(raw, list) else raw.get("events", [])
    for rec in items if isinstance(items, list) else [items]:
        try:
            evt = NormalizedEvent(
                source="signal_event_dc",
                symbol=normalize_symbol(rec.get("symbol", "")),
                event_type=normalize_event_alias(rec.get("event", rec.get("signal", ""))),
                direction=rec.get("direction", rec.get("signal", "MONITOR_ONLY")),
                price=rec.get("price"),
                volume=rec.get("volume") or rec.get("qty"),
                timeframe=rec.get("timeframe", rec.get("tf")),
                ts=_parse_ts(rec.get("timestamp") or rec.get("written_at") or rec.get("_ts")),
                confidence=rec.get("confidence"),
                raw_reason=rec.get("reason"),
                metadata={"flags": rec.get("flags", {}), "source": rec.get("source")},
            )
            events.append(evt)
        except Exception:
            pass

    return events, status


# ── Helpers ────────────────────────────────────────────────────────────────

def _parse_ts(value: Any) -> Optional[datetime]:
    """Parse a timestamp from string or numeric epoch."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        # Try ISO 8601 formats
        for fmt in [
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]:
            try:
                dt = datetime.strptime(value, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        # Try fromisoformat as last resort
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass
    return None


def _confidence_to_float(val: Any) -> Optional[float]:
    """Convert confidence strings (LOW/MEDIUM/HIGH) to 0.0-1.0."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val) if isinstance(val, int) or val <= 1.0 else float(val) / 100.0
    mapping = {"LOW": 0.33, "MEDIUM": 0.66, "HIGH": 1.0, "UNKNOWN": 0.0}
    return mapping.get(str(val).upper())
