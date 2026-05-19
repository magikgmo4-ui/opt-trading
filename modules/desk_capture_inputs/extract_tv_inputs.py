#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

from modules.desk_common.paths import (
    INPUTS_DIR,
    SNAPSHOT_LATEST_JSON,
    TV_INPUTS_HISTORY_JSONL,
    TV_INPUTS_LATEST_JSON,
)

def eprint(*a: Any) -> None:
    print(*a, file=sys.stderr, flush=True)

def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)

def append_jsonl(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def b64_data_uri(img_path: Path) -> str:
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    ext = img_path.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"

def extract_json_from_text(text: str) -> Optional[dict]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None

def call_openai_vision(prompt: str, img_path: Path) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return {"_error": "OPENAI_API_KEY missing"}

    base_url = os.environ.get("OPENAI_API_BASE", "https://api.openai.com").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    timeout = int(os.environ.get("TIMEOUT_SEC", "90"))
    max_tokens = int(os.environ.get("MAX_TOKENS", "500"))

    url = f"{base_url}/v1/chat/completions"
    data_uri = b64_data_uri(img_path)

    payload = {
        "model": model,
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    j = json.loads(body)
    try:
        return {"_raw": j, "_text": j["choices"][0]["message"]["content"]}
    except Exception:
        return {"_raw": j, "_error": "unexpected_openai_response"}

def build_prompt(symbol: str, tf: str, max_levels: int) -> str:
    return (
        "Tu analyses UNE capture TradingView (un seul graphique). "
        "Réponds UNIQUEMENT en JSON valide (pas de markdown, pas de texte autour).\n"
        f"Contexte: symbol={symbol}, tf={tf}.\n"
        "Règles: si une valeur est illisible -> null. N'invente pas.\n"
        "Schéma JSON attendu:\n"
        "{"
        "\n  \"symbol\": str,"
        "\n  \"tf\": str,"
        "\n  \"price\": number|null,"
        "\n  \"change_abs\": number|null,"
        "\n  \"change_pct\": number|null,"
        "\n  \"volume_last\": number|null,"
        "\n  \"rsi\": number|null,"
        "\n  \"ema_bias\": \"above\"|\"below\"|\"mixed\"|null,"
        "\n  \"structure\": \"bull\"|\"bear\"|\"range\"|null,"
        f"\n  \"support\": number[] ,            // max {max_levels} niveaux"
        f"\n  \"resistance\": number[]           // max {max_levels} niveaux"
        "\n}"
    )

def main() -> int:
    tf_default = os.environ.get("TF_DEFAULT", "H1")
    max_levels = int(os.environ.get("MAX_LEVELS", "2"))
    merge_back = os.environ.get("MERGE_BACK_TO_SNAPSHOTS", "1").strip() == "1"

    if not SNAPSHOT_LATEST_JSON.exists():
        eprint(f"ERROR: missing {SNAPSHOT_LATEST_JSON}")
        return 2

    latest = read_json(SNAPSHOT_LATEST_JSON)
    if not isinstance(latest, dict) or not latest:
        eprint("ERROR: latest.json empty")
        return 3

    results: Dict[str, Any] = {}
    ts_run = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    for sym, rec in latest.items():
        img = Path(rec.get("path", ""))
        tf = rec.get("tf") or tf_default

        if not img.exists():
            results[sym] = {"symbol": sym, "tf": tf, "_error": f"missing_image:{img}"}
            continue

        prompt = build_prompt(sym, tf, max_levels)
        r = call_openai_vision(prompt, img)

        if "_error" in r:
            results[sym] = {"symbol": sym, "tf": tf, "snapshot_ts": rec.get("snapshot_ts"), "image_path": str(img), "tv": None, "_error": r["_error"]}
            continue

        parsed = extract_json_from_text(r.get("_text", ""))
        if not parsed:
            results[sym] = {"symbol": sym, "tf": tf, "snapshot_ts": rec.get("snapshot_ts"), "image_path": str(img), "tv": None, "_error": "json_parse_failed"}
            continue

        support = parsed.get("support") or []
        resistance = parsed.get("resistance") or []
        if not isinstance(support, list): support = []
        if not isinstance(resistance, list): resistance = []

        tv = {
            "price": parsed.get("price"),
            "change_abs": parsed.get("change_abs"),
            "change_pct": parsed.get("change_pct"),
            "volume_last": parsed.get("volume_last"),
            "rsi": parsed.get("rsi"),
            "ema_bias": parsed.get("ema_bias"),
            "structure": parsed.get("structure"),
            "support": support[:max_levels],
            "resistance": resistance[:max_levels],
        }

        results[sym] = {
            "symbol": sym,
            "tf": tf,
            "snapshot_ts": rec.get("snapshot_ts"),
            "image_path": str(img),
            "tv": tv,
        }

    out = {"ts_run": ts_run, "source": "snapshots.latest.json", "items": results}

    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(TV_INPUTS_LATEST_JSON, out)
    append_jsonl(TV_INPUTS_HISTORY_JSONL, out)

    if merge_back:
        for sym, rec in latest.items():
            item = results.get(sym)
            if isinstance(item, dict) and "tv" in item:
                rec["tv_inputs"] = item["tv"]
        write_json(SNAPSHOT_LATEST_JSON, latest)

    print(json.dumps({"ok": True, "out": str(TV_INPUTS_LATEST_JSON), "merged": merge_back, "symbols": list(results.keys())}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
