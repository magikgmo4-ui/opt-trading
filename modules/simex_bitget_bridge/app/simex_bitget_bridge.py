import os
import time
import datetime
import requests

CONTRACT_VERSION = "SIMEX_UNITS_V1"


def _env_first(*names: str, default: str):
    for name in names:
        value = os.getenv(name)
        if value not in (None, ""):
            return value
    return default


def _env_str(*names: str, default: str) -> str:
    return str(_env_first(*names, default=default))


def _env_int(*names: str, default: int) -> int:
    return int(_env_first(*names, default=str(default)))


def _env_float(*names: str, default: float) -> float:
    return float(_env_first(*names, default=str(default)))


SYMBOL = _env_str("SIMEX_SYMBOL", default="XAUUSDT")
PRODUCT_TYPE = _env_str("SIMEX_PRODUCT_TYPE", default="USDT-FUTURES")
GRANULARITY_SEC = _env_int("SIMEX_GRANULARITY_SEC", "SIMEX_GRANULARITY", default=300)
LIMIT = _env_int("SIMEX_LIMIT", default=3)

# unités de prix absolues (compat legacy conservée pour SIMEX_TOL)
TOL_PRICE_ABS = _env_float("SIMEX_TOL_PRICE_ABS", "SIMEX_TOL", default=0.5)
STOP_OFFSET_PRICE_ABS = _env_float("SIMEX_STOP_OFFSET_PRICE_ABS", default=5.0)
TARGET_OFFSET_PRICE_ABS = _env_float("SIMEX_TARGET_OFFSET_PRICE_ABS", default=2.0)

# quantité scalaire consommée par Perf (pnl = delta_prix * qty)
QTY_UNITS = _env_float("SIMEX_QTY_UNITS", default=0.1)
RISK_USD = _env_float("SIMEX_RISK_USD", default=0.5)

PERF_EVENT = _env_str("SIMEX_PERF_EVENT", default="http://127.0.0.1:8010/perf/event")
ENGINE = _env_str("SIMEX_ENGINE", default="BITGET_SM_LITE")

LEGACY_ENV_BRIDGE = {
    "SIMEX_GRANULARITY": os.getenv("SIMEX_GRANULARITY_SEC") in (None, "") and os.getenv("SIMEX_GRANULARITY") not in (None, ""),
    "SIMEX_TOL": os.getenv("SIMEX_TOL_PRICE_ABS") in (None, "") and os.getenv("SIMEX_TOL") not in (None, ""),
}


def bitget_candles(symbol: str):
    url = "https://api.bitget.com/api/v2/mix/market/candles"
    params = {
        "symbol": symbol,
        "productType": PRODUCT_TYPE,
        "granularity": str(GRANULARITY_SEC),
        "limit": str(LIMIT),
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    j = r.json()
    if isinstance(j, dict) and j.get("code") not in (None, "00000", 0):
        raise RuntimeError(f"Bitget error code={j.get('code')} msg={j.get('msg')}")
    data = (j.get("data") or [])
    if len(data) < 3:
        raise RuntimeError(f"Not enough candles: {len(data)} (need 3)")
    return sorted(data, key=lambda x: int(x[0]))


def perf_post(payload: dict):
    r = requests.post(PERF_EVENT, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def runtime_units_meta() -> dict:
    return {
        "contract_version": CONTRACT_VERSION,
        "units": {
            "granularity": "seconds",
            "tolerance": "absolute_price",
            "stop_offset": "absolute_price",
            "target_offset": "absolute_price",
            "qty": "perf_qty_units",
            "risk": "usd",
        },
        "normalization": {
            "granularity_sec": GRANULARITY_SEC,
            "tol_price_abs": TOL_PRICE_ABS,
            "stop_offset_price_abs": STOP_OFFSET_PRICE_ABS,
            "target_offset_price_abs": TARGET_OFFSET_PRICE_ABS,
            "qty_units": QTY_UNITS,
            "risk_usd": RISK_USD,
        },
        "legacy_env_bridge": LEGACY_ENV_BRIDGE,
    }


def main():
    candles = bitget_candles(SYMBOL)
    a, b, c = candles[-3], candles[-2], candles[-1]

    a_low = float(a[3])
    b_low = float(b[3])
    c_close = float(c[4])
    b_open = float(b[1])
    last_ts = int(c[0])

    print("a_low:", a_low, "b_low:", b_low, "c_close:", c_close, "ts_ms:", last_ts)

    sweep = b_low <= a_low + TOL_PRICE_ABS
    reclaim = c_close > a_low
    confirm = c_close > b_open

    if not (sweep and reclaim and confirm):
        print(
            "signal: NO "
            f"(sweep={sweep} reclaim={reclaim} confirm={confirm} "
            f"tol_price_abs={TOL_PRICE_ABS})"
        )
        return

    print("signal: YES (SWEEP+RECLAIM tol) -> OPEN then CLOSE")
    trade_id = "T_BITGET_SM_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    entry = c_close

    open_payload = {
        "type": "OPEN",
        "trade_id": trade_id,
        "engine": ENGINE,
        "symbol": SYMBOL,
        "side": "LONG",
        "entry": entry,
        "stop": entry - STOP_OFFSET_PRICE_ABS,
        "qty": QTY_UNITS,
        "risk_usd": RISK_USD,
        "meta": {
            "rule": "sweep+reclaim_tol",
            "origin": "simex_bitget_bridge",
            "product_type": PRODUCT_TYPE,
            "a_low": a_low,
            "b_low": b_low,
            "ts_ms": last_ts,
            **runtime_units_meta(),
        },
    }
    print("perf_open:", perf_post(open_payload))

    time.sleep(10)

    close_payload = {
        "type": "CLOSE",
        "trade_id": trade_id,
        "exit": entry + TARGET_OFFSET_PRICE_ABS,
        "meta": {
            "note": "auto close 10s",
            **runtime_units_meta(),
        },
    }
    print("perf_close:", perf_post(close_payload))


if __name__ == "__main__":
    main()
