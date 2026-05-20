#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_PATH = PROJECT_ROOT / "data" / "telemetry" / "telegram_send.jsonl"


def _parse_utc_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def _percentile(sorted_vals: list[int], p: float) -> int | None:
    if not sorted_vals:
        return None
    if p <= 0:
        return sorted_vals[0]
    if p >= 100:
        return sorted_vals[-1]
    idx = (len(sorted_vals) - 1) * (p / 100.0)
    lo = int(idx)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = idx - lo
    return int(round(sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac))


@dataclass(frozen=True)
class Record:
    timestamp: datetime
    source: str
    ok: bool
    duration_ms: int


def _load_records(path: Path, since: datetime | None, until: datetime | None) -> list[Record]:
    if not path.exists():
        return []
    out: list[Record] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _parse_utc_iso(str(raw.get("timestamp", "")))
            if ts is None:
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            try:
                duration_ms = int(raw.get("duration_ms", 0))
            except Exception:
                continue
            out.append(
                Record(
                    timestamp=ts,
                    source=str(raw.get("source", "")),
                    ok=bool(raw.get("ok", False)),
                    duration_ms=duration_ms,
                )
            )
    return out


def _summarize(records: list[Record]) -> dict[str, Any]:
    durations_all = sorted(r.duration_ms for r in records)
    durations_ok = sorted(r.duration_ms for r in records if r.ok)
    by_source: dict[str, list[Record]] = {}
    for r in records:
        by_source.setdefault(r.source or "unknown", []).append(r)

    def stats(vals: list[int]) -> dict[str, Any]:
        if not vals:
            return {"count": 0}
        return {
            "count": len(vals),
            "min_ms": vals[0],
            "p50_ms": _percentile(vals, 50),
            "p90_ms": _percentile(vals, 90),
            "p95_ms": _percentile(vals, 95),
            "p99_ms": _percentile(vals, 99),
            "max_ms": vals[-1],
        }

    sources_out: dict[str, Any] = {}
    for src, recs in sorted(by_source.items(), key=lambda kv: kv[0]):
        src_durations = sorted(r.duration_ms for r in recs)
        src_ok = sum(1 for r in recs if r.ok)
        sources_out[src] = {
            "count": len(recs),
            "ok_count": src_ok,
            "ok_rate": (src_ok / len(recs)) if recs else 0.0,
            "latency_ms": stats(src_durations),
        }

    ok_count = sum(1 for r in records if r.ok)
    return {
        "count": len(records),
        "ok_count": ok_count,
        "ok_rate": (ok_count / len(records)) if records else 0.0,
        "latency_ms_all": stats(durations_all),
        "latency_ms_ok": stats(durations_ok),
        "by_source": sources_out,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Telegram send latency backtest from JSONL telemetry logs")
    p.add_argument("--path", help="Path to telegram_send.jsonl (defaults to env TELEGRAM_LATENCY_LOG_PATH or repo data path)")
    p.add_argument("--since", help="Filter since ISO-8601 UTC timestamp (inclusive)")
    p.add_argument("--until", help="Filter until ISO-8601 UTC timestamp (inclusive)")
    args = p.parse_args()

    path = Path(args.path) if args.path else Path(os.getenv("TELEGRAM_LATENCY_LOG_PATH", str(DEFAULT_LOG_PATH)))
    since = _parse_utc_iso(args.since) if args.since else None
    until = _parse_utc_iso(args.until) if args.until else None
    records = _load_records(path, since=since, until=until)
    summary = {"path": str(path), "since": args.since or "", "until": args.until or "", "summary": _summarize(records)}
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
