import time
import datetime
import requests

SYMBOL = "XAUUSDT"
PRODUCT_TYPE = "USDT-FUTURES"
GRANULARITY = "300"   # 5m
LIMIT = "3"

# tolérance pour capter micro-sweeps/touches (ajuste 0.3–0.8 si besoin)
TOL = 0.5

PERF_EVENT = "http://127.0.0.1:8010/perf/event"

def bitget_candles(symbol: str):
    url = "https://api.bitget.com/api/v2/mix/market/candles"
    params = {
        "symbol": symbol,
        "productType": PRODUCT_TYPE,
        "granularity": GRANULARITY,
        "limit": LIMIT,
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

def main():
    candles = bitget_candles(SYMBOL)
    a, b, c = candles[-3], candles[-2], candles[-1]  # a=older, b=sweep, c=reclaim

    a_low = float(a[3])
    b_low = float(b[3])
    c_close = float(c[4])
    b_open = float(b[1])
    last_ts = int(c[0])

    print("a_low:", a_low, "b_low:", b_low, "c_close:", c_close, "ts_ms:", last_ts)

    # Sweep tolérant: b_low doit toucher / passer sous (a_low + tol)
    sweep = (b_low <= a_low + TOL)
    reclaim = (c_close > a_low)
    confirm = (c_close > b_open)

    if not (sweep and reclaim and confirm):
        print(f"signal: NO (sweep={sweep} reclaim={reclaim} confirm={confirm} tol={TOL})")
        return

    print("signal: YES (SWEEP+RECLAIM tol) -> OPEN then CLOSE")
    trade_id = "T_BITGET_SM_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    entry = c_close

    open_payload = {
        "type": "OPEN",
        "trade_id": trade_id,
        "engine": "BITGET_SM_LITE",
        "symbol": SYMBOL,
        "side": "LONG",
        "entry": entry,
        "stop": entry - 5.0,
        "qty": 0.1,
        "risk_usd": 0.5,
        "meta": {
            "rule": "sweep+reclaim_tol",
            "tol": TOL,
            "a_low": a_low,
            "b_low": b_low,
            "ts_ms": last_ts
        },
    }
    print("perf_open:", perf_post(open_payload))

    time.sleep(10)

    close_payload = {
        "type": "CLOSE",
        "trade_id": trade_id,
        "exit": entry + 2.0,
        "meta": {"note": "auto close 10s"},
    }
    print("perf_close:", perf_post(close_payload))

if __name__ == "__main__":
    main()
