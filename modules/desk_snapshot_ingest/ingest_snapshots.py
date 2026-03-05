#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

IMG_EXTS = {".png", ".jpg", ".jpeg"}

FILENAME_RE = re.compile(
    r"^(?P<symbol>.+?)_(?P<tf>[A-Za-z0-9]+)_(?P<date>\d{8})_(?P<time>\d{6})",
    re.IGNORECASE,
)

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def load_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"WARN: failed to read json {path}: {e}", file=sys.stderr)
        return None

def atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)

def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def parse_from_filename(name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    m = FILENAME_RE.match(Path(name).stem)
    if not m:
        return None, None, None
    symbol = m.group("symbol")
    tf = m.group("tf")
    d = m.group("date")
    t = m.group("time")
    ts = f"{d[0:4]}-{d[4:6]}-{d[6:8]}T{t[0:2]}:{t[2:4]}:{t[4:6]}"
    return symbol, tf, ts

def iter_images(inbox: Path):
    if not inbox.exists():
        return
    for p in sorted(inbox.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            yield p

def ingest_once(
    inbox_dir: Path,
    dest_dir: Path,
    index_file: Path,
    history_file: Path,
    processed_dir: Path,
    mode: str,
    dry_run: bool,
) -> Dict[str, Any]:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    dest_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    latest = load_json(index_file) or {}
    processed_count = 0
    items = []

    for img in iter_images(inbox_dir):
        sidecar = img.with_suffix(".json")
        meta = load_json(sidecar) or {}

        symbol = meta.get("symbol")
        tf = meta.get("tf")
        snapshot_ts = meta.get("ts")

        if not symbol or not tf or not snapshot_ts:
            ps, ptf, pts = parse_from_filename(img.name)
            symbol = symbol or ps or "UNKNOWN"
            tf = tf or ptf or "UNK"
            snapshot_ts = snapshot_ts or pts or now_iso()

        symbol = str(symbol).strip()
        tf = str(tf).strip()

        dest_sub = dest_dir / symbol
        dest_sub.mkdir(parents=True, exist_ok=True)
        dest_img = dest_sub / img.name
        dest_meta = dest_sub / sidecar.name

        action = {
            "ts": now_iso(),
            "event": "ingest",
            "symbol": symbol,
            "tf": tf,
            "src_img": str(img),
            "dst_img": str(dest_img),
            "parsed_snapshot_ts": snapshot_ts,
            "mode": mode,
            "meta": meta if meta else None,
        }

        if not dry_run:
            if mode == "copy":
                shutil.copy2(img, dest_img)
                if sidecar.exists():
                    shutil.copy2(sidecar, dest_meta)
                # move originals to processed to avoid reprocessing
                shutil.move(str(img), str(processed_dir / img.name))
                if sidecar.exists():
                    shutil.move(str(sidecar), str(processed_dir / sidecar.name))
            else:
                shutil.move(str(img), str(dest_img))
                if sidecar.exists():
                    shutil.move(str(sidecar), str(dest_meta))

            latest[symbol] = {
                "symbol": symbol,
                "tf": tf,
                "snapshot_ts": snapshot_ts,
                "path": str(dest_img),
                "ingested_at": action["ts"],
                "source": meta.get("source") if meta else None,
                "host": meta.get("host") if meta else None,
            }
            append_jsonl(history_file, action)

        items.append(action)
        processed_count += 1

    if not dry_run:
        atomic_write_json(index_file, latest)

    return {
        "ok": True,
        "processed": processed_count,
        "index_file": str(index_file),
        "history_file": str(history_file),
        "sample": items[:5],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox", default=os.getenv("INBOX_DIR", "/srv/sftp/shared_files/shared/inbox"))
    ap.add_argument("--dest", default=os.getenv("DEST_DIR", "/opt/trading/desk/snapshots"))
    ap.add_argument("--index", default=os.getenv("INDEX_FILE", "/opt/trading/desk/snapshots/latest.json"))
    ap.add_argument("--history", default=os.getenv("HISTORY_FILE", "/opt/trading/desk/snapshots/history.jsonl"))
    ap.add_argument("--processed", default=os.getenv("PROCESSED_DIR", "/srv/sftp/shared_files/shared/inbox/_processed"))
    ap.add_argument("--mode", default=os.getenv("INGEST_MODE", "move"), choices=["move", "copy"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=int, default=3)
    args = ap.parse_args()

    inbox = Path(args.inbox)
    dest = Path(args.dest)
    indexf = Path(args.index)
    histf = Path(args.history)
    processed = Path(args.processed)

    if not args.watch:
        res = ingest_once(inbox, dest, indexf, histf, processed, args.mode, args.dry_run)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    print(f"[watch] inbox={inbox} interval={args.interval}s mode={args.mode}")
    while True:
        try:
            res = ingest_once(inbox, dest, indexf, histf, processed, args.mode, False)
            if res.get("processed", 0) > 0:
                print(f"[watch] processed={res['processed']} index={indexf}")
        except KeyboardInterrupt:
            print("\n[watch] stopped")
            return 0
        except Exception as e:
            print(f"[watch] ERROR: {e}", file=sys.stderr)
        time.sleep(max(1, args.interval))

if __name__ == "__main__":
    raise SystemExit(main())
