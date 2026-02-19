import time, json, urllib.parse, urllib.request

BASE = "https://api.bitget.com"

def get(path, params=None):
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode(params)
    url = BASE + path + qs
    req = urllib.request.Request(url, headers={"User-Agent":"tv-perf-probe/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    # 1) time
    t = get("/api/v2/public/time")
    print("time:", t)

    # 2) candles (default: BTCUSDT perpetual USDT)
    # Bitget a plusieurs produits: 'USDT-FUTURES' vs spot, etc.
    # Ici on teste futures USDT (mix market) via endpoint v2 mix/market/candles
    # NOTE: paramètres exacts peuvent varier -> on imprime l’erreur si mismatch.
    params = {
        "symbol": "BTCUSDT",
        "productType": "USDT-FUTURES",
        "granularity": "300",  # 5m en secondes, souvent attendu
        "limit": "5"
    }
    try:
        c = get("/api/v2/mix/market/candles", params)
        print("candles:", json.dumps(c)[:800])
    except Exception as e:
        print("candles ERROR:", repr(e))

if __name__ == "__main__":
    main()
