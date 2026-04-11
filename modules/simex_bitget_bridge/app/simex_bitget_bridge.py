import os
import time
import datetime
import requests

CONTRACT_VERSION = "SIMEX_UNITS_V1"
BITGET_HOST = "api.bitget.com"
BITGET_CANDLES_URL = "https://api.bitget.com/api/v2/mix/market/candles"


class BitgetUpstreamDataError(RuntimeError):
    def __init__(self, failure_class: str, detail: str):
        super().__init__(detail)
        self.failure_class = failure_class
        self.detail = detail


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


def _compact_text(value, max_len: int = 240) -> str:
    text = " ".join(str(value).split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


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


def classify_bitget_request_failure(exc: requests.exceptions.RequestException) -> str:
    text = _compact_text(exc, max_len=400).lower()

    if (
        "temporary failure in name resolution" in text
        or "failed to resolve" in text
        or "nameresolutionerror" in text
        or "getaddrinfo" in text
    ):
        return "NF_DNS_RESOLUTION"

    if (
        "handshake operation timed out" in text
        or ("ssl" in text and "timed out" in text)
        or "_ssl.c" in text
    ):
        return "NF_TLS_HANDSHAKE_TIMEOUT"

    if "read timed out" in text or "readtimeouterror" in text or "readtimeout" in text:
        return "NF_HTTP_READ_TIMEOUT"

    if "connect timed out" in text or "connecttimeout" in text:
        return "NF_HTTP_CONNECT_TIMEOUT"

    if isinstance(exc, requests.exceptions.Timeout):
        return "NF_HTTP_TIMEOUT"

    if isinstance(exc, requests.exceptions.ConnectionError):
        return "NF_CONNECTION"

    return "NF_UPSTREAM_UNKNOWN"


def log_upstream_failure(failure_class: str, detail) -> None:
    print(
        "upstream_failure: "
        f"class={failure_class} "
        f"host={BITGET_HOST} "
        f"symbol={SYMBOL} "
        f"product_type={PRODUCT_TYPE} "
        f"granularity_sec={GRANULARITY_SEC} "
        f"detail={_compact_text(detail)}"
    )


def log_bitget_request_failure(exc: requests.exceptions.RequestException) -> None:
    failure_class = classify_bitget_request_failure(exc)
    log_upstream_failure(failure_class, exc)



def bitget_candles(symbol: str):
    params = {
        "symbol": symbol,
        "productType": PRODUCT_TYPE,
        "granularity": str(GRANULARITY_SEC),
        "limit": str(LIMIT),
    }
    r = requests.get(BITGET_CANDLES_URL, params=params, timeout=20)
    r.raise_for_status()
    j = r.json()
    if isinstance(j, dict) and j.get("code") not in (None, "00000", 0):
        raise RuntimeError(f"Bitget error code={j.get('code')} msg={j.get('msg')}")
    data = (j.get("data") or [])
    if len(data) < 3:
        raise BitgetUpstreamDataError(
            "NF_INSUFFICIENT_CANDLES",
            f"Not enough candles: received={len(data)} need=3 requested_limit={LIMIT}",
        )
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
    try:
        candles = bitget_candles(SYMBOL)
    except requests.exceptions.RequestException as exc:
        log_bitget_request_failure(exc)
        return
    except BitgetUpstreamDataError as exc:
        log_upstream_failure(exc.failure_class, exc.detail)
        return

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
