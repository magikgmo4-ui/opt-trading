# PSEUDOCODE PACK — MIMO OPEN OBSERVER V0

## app/config.py
```python
def load_config(config_path=None):
    path = resolve_default_or_custom_config(config_path)
    raw = read_yaml(path)
    assert raw["symbol"] == "XAUUSD"
    assert raw["timezone"] == "America/Montreal"
    assert raw["windows"]["open_1800"]["enabled"] is True
    assert raw["scope"]["type"] == "M1x5"
    assert raw["sampling"]["horizons_minutes"] == [30, 60]
    return raw
```

## app/models.py
```python
@dataclass
class Bar:
    ts_open: datetime
    ts_close: datetime
    open: float
    high: float
    low: float
    close: float
    timeframe: str = "M1"

@dataclass
class RawEvent:
    ...

@dataclass
class EnrichedEvent(RawEvent):
    price_plus_30m: float | None = None
    price_plus_60m: float | None = None
    delta_30m: float | None = None
    delta_60m: float | None = None
    outcome_30m: str | None = None
    outcome_60m: str | None = None
```

## app/data_provider.py
```python
def get_m1_bars(symbol, start_ts, end_ts, config):
    mode = config["provider"]["mode"]
    if mode == "fixture":
        rows = load_fixture_rows(symbol, start_ts, end_ts, config)
        bars = [row_to_bar(x) for x in rows]
        return sort_and_filter(bars, start_ts, end_ts)
    raise NotImplementedError("provider mode not yet implemented")

def get_price_at(symbol, ts, config):
    bars = get_m1_bars(symbol, floor_to_minute(ts), ceil_to_minute(ts), config)
    if not bars:
        return None
    return bars[0].close
```

## app/utils_time.py
```python
def is_active_weekday(dt_local):
    return dt_local.weekday_name in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

def build_window_ts(date_value, tz_name, hour=18, minute=0):
    return localized_datetime(date_value, tz_name, hour, minute)

def add_minutes(ts, minutes):
    return ts + timedelta(minutes=minutes)
```

## app/window_detector.py
```python
def find_first_fvg(bars):
    triplets = [(0,1,2), (1,2,3), (2,3,4)]
    for a,b,c in triplets:
        b1, b2, b3 = bars[a], bars[b], bars[c]
        if b3.low > b1.high:
            return {"direction": "bullish", "top": b3.low, "bottom": b1.high, "signal_bar_index": c, "signal_ts": b3.ts_close, "price_at_signal": b3.close}
        if b3.high < b1.low:
            return {"direction": "bearish", "top": b1.low, "bottom": b3.high, "signal_bar_index": c, "signal_ts": b3.ts_close, "price_at_signal": b3.close}
    return None

def compute_sweep(bars, signal_bar_index):
    ref_high = bars[0].high
    ref_low = bars[0].low
    sweep_high = any(bar.high > ref_high for bar in bars[:signal_bar_index+1])
    sweep_low = any(bar.low < ref_low for bar in bars[:signal_bar_index+1])
    if sweep_high and sweep_low:
        return True, "both"
    if sweep_high:
        return True, "high"
    if sweep_low:
        return True, "low"
    return False, "none"
```

## app/event_journal.py
```python
def read_jsonl(path): ...
def existing_ids(path): ...
def append_raw_event(event, path): ...
def append_enriched_event(event, path): ...
```

## app/outcome_sampler.py
```python
def compute_outcome(direction, price_at_signal, future_price): ...
def enrich_event(raw_event, config, provider): ...
def sample_pending(raw_path, enriched_path, config, provider): ...
```

## app/stats_builder.py
```python
def build_stats(enriched_events): ...
def write_reports(stats, reports_dir): ...
```

## app/runner_detect.py
```python
def main(argv):
    cfg = load_config()
    provider = build_provider(cfg)
    dispatch_detect_command(argv, cfg, provider)
```

## app/runner_sample.py
```python
def main(argv):
    cfg = load_config()
    provider = build_provider(cfg)
    sample_pending(...)
```

## app/runner_stats.py
```python
def main(argv):
    cfg = load_config()
    rows = read_jsonl(cfg["paths"]["enriched_events"])
    stats = build_stats(rows)
    write_reports(...)
```
