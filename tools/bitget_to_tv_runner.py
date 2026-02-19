import os, json, time, urllib.request
import sys
sys.path.insert(0, "/opt/trading/tools")
from datetime import datetime, timezone
from bitget_feed import fetch_candles_usdt_futures

TV_URL = os.environ.get("TV_WEBHOOK_URL", "http://127.0.0.1:8000/tv")
KEY = os.environ.get("TV_WEBHOOK_KEY", "")
STATE = "/opt/trading/tmp/bitget_tv_state.json"


PERF_URL = os.environ.get("PERF_URL", "http://127.0.0.1:8010")

def _http_json(url: str, method: str = "GET", payload: dict | None = None, timeout: int = 15):
    import json as _json, urllib.request as _ur
    data = None
    headers = {"User-Agent":"bitget-runner/1.0"}
    if payload is not None:
        data = _json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = _ur.Request(url, data=data, headers=headers, method=method)
    with _ur.urlopen(req, timeout=timeout) as r:
        return _json.loads(r.read().decode("utf-8"))

def perf_find_open(engine: str, symbol: str):
    d = _http_json(f"{PERF_URL}/perf/open")
    for t in d.get("open", []):
        if t.get("engine") == engine and t.get("symbol") == symbol and t.get("status") == "OPEN":
            return t
    return None

def perf_close(trade_id: str, exit_price: float):
    return _http_json(f"{PERF_URL}/perf/event", method="POST", payload={
        "type": "CLOSE",
        "trade_id": trade_id,
        "exit": float(exit_price)
    })

DRY_RUN = os.environ.get("DRY_RUN", "1") == "1"
FORCE_SIGNAL = (os.environ.get("FORCE_SIGNAL") or "").strip().upper()

def iso_from_ms(ts_ms: int) -> str:
    return datetime.fromtimestamp(ts_ms/1000, tz=timezone.utc).isoformat()

def post(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TV_URL,
        data=body,
        headers={"Content-Type":"application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def load_state():
    try:
        with open(STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, sort_keys=True)

def main():
    if not KEY:
        raise SystemExit("Missing TV_WEBHOOK_KEY in env")

    symbol = os.environ.get("BITGET_SYMBOL", "BTCUSDT")
    tf_sec = int(os.environ.get("BITGET_TF_SEC", "300"))
    poll_s = int(os.environ.get("BITGET_POLL_S", "5"))

    engine = os.environ.get("TV_ENGINE", "_TEST_BITGET_BTCUSDT_M5")
    st = load_state()
    last_ts = st.get("last_ts_ms")

    print(f"RUNNER start symbol={symbol} tf_sec={tf_sec} poll_s={poll_s} engine={engine} DRY_RUN={DRY_RUN}")

    while True:
        try:
            print(f"fetching candles: symbol={{SYMBOL}} tf_sec={{TF_SEC}} ...")
            try:
                cs = fetch_candles_usdt_futures(SYMBOL, TF_SEC, limit=3)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"[{datetime.now().isoformat()}] fetch ERROR: {e!r}")
                time.sleep(poll_s)
                continue
            print(f"got candles: {len(cs) if cs else 0}")

            last = cs[-1]
            ts_ms = last.ts_ms

            if last_ts != ts_ms:
                # Placeholder signal (à remplacer par SMC):
                signal = "BUY" if last.c >= last.o else "SELL"
                if FORCE_SIGNAL in ("BUY","SELL"):
                    signal = FORCE_SIGNAL

                sl = (last.c - 10) if signal == "BUY" else (last.c + 10)

                payload = {
                    "key": KEY,
                    "engine": engine,
                    "signal": signal,
                    "symbol": symbol,
                    "tf": str(tf_sec//60),
                    "price": float(last.c),
                    "sl": float(sl),
                    "tp": None,
                    "reason": f"bitget bar-close ts={ts_ms}",
                    "_ts": iso_from_ms(ts_ms),
                }

                if DRY_RUN:
                    print(f"[{datetime.now().isoformat()}] DRY_RUN payload={json.dumps(payload)[:300]}")
                else:
                    resp = post(payload)
                    print(f"[{datetime.now().isoformat()}] sent {signal} {symbol} close={last.c} ts={ts_ms} resp={resp}")

                last_ts = ts_ms
                st["last_ts_ms"] = ts_ms
                save_state(st)

            time.sleep(poll_s)

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ERROR: {e!r}")
            time.sleep(max(5, poll_s))

if __name__ == "__main__":
    main()
