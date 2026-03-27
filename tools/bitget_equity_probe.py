#!/usr/bin/env python3
"""
Probe minimal lecture equity Bitget (USDT-FUTURES + COIN-FUTURES).
Lecture seule, pas d'ordre.
Utilise modules.auth.bitget_credentials pour le chargement des credentials.
"""
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
from typing import Any, Dict, Optional

sys.path.insert(0, "/opt/trading")
from modules.auth.bitget_credentials import load_credentials, DEFAULT_PROFILE

BASE = "https://api.bitget.com"

PRODUCT_TYPES = {
    "USDTM_LONG": "USDT-FUTURES",
    "COINM_SHORT": "COIN-FUTURES",
}


def _sign(timestamp: str, method: str, path: str, body: str, secret: str) -> str:
    prehash = f"{timestamp}{method}{path}{body}"
    return hmac.new(secret.encode(), prehash.encode(), hashlib.sha256).hexdigest()


def _get_private(path: str, creds: Dict[str, str]) -> Dict[str, Any]:
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    body = ""
    signature = _sign(timestamp, method, path, body, creds["secret_key"])

    url = BASE + path
    req = urllib.request.Request(url, method=method, headers={
        "ACCESS-KEY": creds["api_key"],
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": creds["passphrase"],
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_accounts(creds: Dict[str, str], product_type: str) -> list:
    path = f"/api/v2/mix/account/accounts?productType={product_type}"
    data = _get_private(path, creds)
    if data.get("code") != "00000":
        raise RuntimeError(f"Bitget error: code={data.get('code')} msg={data.get('msg')}")
    return data.get("data") or []


def extract_equity(accounts: list) -> Dict[str, Any]:
    """Extract usdtEquity (or available) from account list."""
    result = {}
    for acct in accounts:
        margin_coin = acct.get("marginCoin", "")
        equity = acct.get("usdtEquity") or acct.get("available") or "0"
        result[margin_coin] = float(equity)
    return result


def main():
    profile = os.environ.get("BITGET_PROFILE", DEFAULT_PROFILE)
    status, creds = load_credentials(profile)

    if status == "missing":
        print(f"STATUS: credentials missing (profile={profile})")
        print(f"REQUIRED: BITGET_{profile.upper()}_API_KEY, BITGET_{profile.upper()}_SECRET_KEY, BITGET_{profile.upper()}_PASSPHRASE")
        sys.exit(1)
    if status == "incomplete":
        print(f"STATUS: credentials incomplete (profile={profile})")
        print("Some fields are set but not all three required fields")
        sys.exit(1)

    print(f"STATUS: credentials ok (profile={profile})")
    assert creds is not None
    results = {}

    for engine, product_type in PRODUCT_TYPES.items():
        try:
            accounts = fetch_accounts(creds, product_type)
            equity = extract_equity(accounts)
            results[engine] = {"product_type": product_type, "equity": equity, "ok": True}
            print(f"  [{engine}] product={product_type} equity={equity}")
        except Exception as e:
            results[engine] = {"product_type": product_type, "error": str(e), "ok": False}
            print(f"  [{engine}] ERROR: {e}")

    print(json.dumps(results, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
