#!/usr/bin/env python3
from __future__ import annotations
import base64, datetime as dt, json, os, re, sys, time, traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
except Exception:
    Image = None

import urllib.parse
import urllib.request

def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")

def load_env_file(env_path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env

def cfg() -> Dict[str, str]:
    env_path = Path("/opt/trading/modules/bot_vision_step2/config/bot_vision.env")
    fe = load_env_file(env_path)
    def g(k: str, d: str="") -> str:
        return os.environ.get(k) or fe.get(k) or d
    return {
        "TELEGRAM_BOT_TOKEN": g("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": g("TELEGRAM_CHAT_ID"),
        # Optional allowlist: comma-separated chat ids. If empty, allow all.
        # Example: ALLOWED_CHAT_ID=-5177632039
        "ALLOWED_CHAT_ID": g("ALLOWED_CHAT_ID"),
        "OPENAI_API_KEY": g("OPENAI_API_KEY"),
        "OPENAI_MODEL": g("OPENAI_MODEL", "gpt-4.1-mini"),
        "VISION_INBOX": g("VISION_INBOX", "/srv/sftp/shared_files/shared/vision_inbox"),
        "VISION_PROCESSED": g("VISION_PROCESSED", "/srv/sftp/shared_files/shared/vision_processed"),
        "VISION_OUTBOX": g("VISION_OUTBOX", "/srv/sftp/shared_files/shared/vision_outbox"),
        "DESKPRO_VISION_DIR": g("DESKPRO_VISION_DIR", "/opt/trading/data/deskpro/vision"),
        "WORKDIR": g("WORKDIR", "/opt/trading/_work/bot_vision_step2"),
        "MAX_W": g("MAX_W", "1280"),
        "MAX_H": g("MAX_H", "720"),
        "JPEG_QUALITY": g("JPEG_QUALITY", "75"),
        "CROP_MODE": g("CROP_MODE", "quad"),
        "ANALYZE_MODE": g("ANALYZE_MODE", "single"),
        "ENABLE_SENDER_TIMER": g("ENABLE_SENDER_TIMER", "0"),
        "SENDER_EVERY_MIN": g("SENDER_EVERY_MIN", "10"),
        "ENABLE_PRUNE_TIMER": g("ENABLE_PRUNE_TIMER", "1"),
        "PRUNE_KEEP_DAYS": g("PRUNE_KEEP_DAYS", "7"),
    }

def parse_allowed_chat_ids(raw: str) -> Optional[set[str]]:
    raw = (raw or "").strip()
    if not raw:
        return None  # allow all
    out: set[str] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        out.add(part)
    return out or None

def is_allowed_chat(c: Dict[str, str], chat_id: str) -> bool:
    allowed = parse_allowed_chat_ids(c.get("ALLOWED_CHAT_ID", ""))
    if allowed is None:
        return True
    return str(chat_id).strip() in allowed

def ensure_dirs(c: Dict[str, str], strict: bool=True) -> None:
    """Ensure required directories exist.

    - strict=True: raise if we cannot create a required directory (runtime requirement on admin-trading).
    - strict=False: warn and continue if a path is not creatable (e.g., student machine without /srv/sftp mount).
    """
    for k in ["VISION_INBOX","VISION_PROCESSED","VISION_OUTBOX","DESKPRO_VISION_DIR","WORKDIR"]:
        p = Path(c[k])
        try:
            p.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            if strict:
                raise
            print(f"WARN: cannot create {p} ({e}); skipping (expected on machines without /srv/sftp).")
        except FileNotFoundError as e:
            # Can happen when an intermediate path cannot be created (e.g., /srv/sftp on non-admin machines).
            if strict:
                raise
            print(f"WARN: cannot create {p} ({e}); skipping (expected on machines without /srv/sftp).")

def list_images(folder: Path) -> List[Path]:
    exts = {".png",".jpg",".jpeg",".webp"}
    imgs = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts]
    imgs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return imgs

def latest_screenshot(c: Dict[str, str]) -> Path:
    proc = Path(c["VISION_PROCESSED"])
    inbox = Path(c["VISION_INBOX"])
    cand = list_images(proc)
    if not cand:
        cand = list_images(inbox)
    if not cand:
        raise RuntimeError("No screenshots found in processed or inbox.")
    return cand[0]

def resize_to_jpeg(src: Path, dst: Path, max_w: int, max_h: int, q: int) -> Tuple[int,int]:
    if Image is None:
        raise RuntimeError("Pillow not installed. Run install_service.sh to install deps.")
    im = Image.open(str(src)).convert("RGB")
    w,h = im.size
    scale = min(max_w / w, max_h / h, 1.0)
    nw, nh = int(w*scale), int(h*scale)
    if (nw,nh) != (w,h):
        im = im.resize((nw,nh))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(str(dst), format="JPEG", quality=q, optimize=True)
    return nw, nh

def crop_quadrants(jpg_path: Path, out_dir: Path) -> List[Path]:
    if Image is None:
        raise RuntimeError("Pillow not installed.")
    im = Image.open(str(jpg_path)).convert("RGB")
    w,h = im.size
    midx, midy = w//2, h//2
    boxes = [
        (0,0,midx,midy),
        (midx,0,w,midy),
        (0,midy,midx,h),
        (midx,midy,w,h),
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for i,b in enumerate(boxes, start=1):
        p = out_dir / f"{i:02d}.jpg"
        im.crop(b).save(str(p), format="JPEG", quality=85, optimize=True)
        out.append(p)
    return out

def data_url(path: Path) -> str:
    mime = "image/jpeg" if path.suffix.lower() in [".jpg",".jpeg"] else "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"

def call_openai(c: Dict[str, str], images: List[Path]) -> Dict[str, Any]:
    api_key = c.get("OPENAI_API_KEY","")
    if not api_key or api_key == "REPLACE_ME":
        raise RuntimeError("OPENAI_API_KEY not set in bot_vision.env")
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        raise RuntimeError("openai python package not installed. Run install_service.sh") from e
    client = OpenAI(api_key=api_key)
    model = c.get("OPENAI_MODEL","gpt-4.1-mini")

    prompt = (
        "Tu es un assistant d'analyse de marché (trading). L'image montre un dashboard avec 4 graphiques (grille 2x2).\n"
        "Objectif: donner une lecture RAPIDE, actionnable et structurée, en FRANÇAIS.\n\n"
        "Contraintes:\n"
        "- Ne devine pas: si un symbole/timeframe n'est pas lisible, indique 'inconnu'.\n"
        "- Utilise le vocabulaire: tendance, structure (HH/HL/LH/LL), zones clés (S/R), scénario, invalidation.\n"
        "- 6 à 12 lignes max par graphique.\n\n"
        "Format de sortie EXACT:\n"
        "A) Résumé global (3 bullets max)\n"
        "B) Chart 1 (haut-gauche): ...\n"
        "C) Chart 2 (haut-droit): ...\n"
        "D) Chart 3 (bas-gauche): ...\n"
        "E) Chart 4 (bas-droit): ...\n"
        "F) DeskPro (JSON compact sur 1 bloc) avec clés: run_id, charts[{slot,bias,structure,supports,resistances,plan,invalidation}]\n"
    )

    content: List[Dict[str, Any]] = [{"type":"input_text","text":prompt}]
    for p in images:
        content.append({"type":"input_image","image_url":data_url(p)})

    resp = client.responses.create(model=model, input=[{"role":"user","content":content}])
    txt = getattr(resp, "output_text", "") or ""
    return {"model": model, "output_text": txt}

def extract_json(text: str) -> Dict[str, Any]:
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            return {}
    m = re.search(r"(\{[\s\S]*\})", text)
    if m:
        blob = m.group(1)
        last = blob.rfind("}")
        blob = blob[:last+1] if last != -1 else blob
        try:
            return json.loads(blob)
        except Exception:
            return {}
    return {}

# --- Telegram (stdlib) ---
def tg_api(c: Dict[str, str], method: str, params: Dict[str, Any], files: Optional[Dict[str, Path]]=None) -> Dict[str, Any]:
    token = c.get("TELEGRAM_BOT_TOKEN","")
    if not token or token == "REPLACE_ME":
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in bot_vision.env")
    url = f"https://api.telegram.org/bot{token}/{method}"
    if files:
        boundary = "----botvisionboundary"
        body = b""
        for k,v in params.items():
            body += (f"--{boundary}\r\n").encode()
            body += (f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n').encode("utf-8")
        for field, path in files.items():
            data = path.read_bytes()
            body += (f"--{boundary}\r\n").encode()
            body += (f'Content-Disposition: form-data; name="{field}"; filename="{path.name}"\r\n').encode()
            body += b"Content-Type: application/octet-stream\r\n\r\n" + data + b"\r\n"
        body += (f"--{boundary}--\r\n").encode()
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            raise RuntimeError(f"Telegram {method} HTTP {getattr(e,'code', '?')}: {body[:500]}") from e
    data = urllib.parse.urlencode({k:str(v) for k,v in params.items() if v is not None}).encode("utf-8")
    try:
        with urllib.request.urlopen(url, data=data, timeout=90) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise RuntimeError(f"Telegram {method} HTTP {getattr(e,'code', '?')}: {body[:500]}") from e

def tg_send_message(c: Dict[str, str], chat_id: str, text: str, reply_markup: Optional[Dict[str, Any]]=None) -> None:
    # Telegram hard limit is 4096 chars for sendMessage; keep margin.
    max_len = int(c.get("TG_MAX_LEN", "3500") or "3500")
    if text is None:
        text = ""
    if len(text) > max_len:
        text = text[: max(0, max_len - 20)] + "\n…(trunc)"
    params: Dict[str, Any] = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    tg_api(c, "sendMessage", params)

def tg_send_photo(c: Dict[str, str], chat_id: str, photo: Path, caption: str="", reply_markup: Optional[Dict[str, Any]]=None) -> None:
    params: Dict[str, Any] = {"chat_id": chat_id, "caption": caption}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    tg_api(c, "sendPhoto", params, files={"photo": photo})

def tg_answer_cb(c: Dict[str, str], cbid: str, text: str="OK") -> None:
    tg_api(c, "answerCallbackQuery", {"callback_query_id": cbid, "text": text})

def make_run_dir(base_dir: Path) -> Tuple[str, Path]:
    run_id = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = base_dir / "runs" / run_id
    (run_dir / "charts").mkdir(parents=True, exist_ok=True)
    return run_id, run_dir

def analyze_latest(chat_id_override: Optional[str]=None) -> Dict[str, Any]:
    c = cfg(); ensure_dirs(c)
    base_dir = Path(c["DESKPRO_VISION_DIR"])
    run_id, run_dir = make_run_dir(base_dir)
    charts_dir = run_dir / "charts"
    log_path = run_dir / "vision.log.jsonl"
    outbox = Path(c["VISION_OUTBOX"])

    def log(event: str, **fields: Any) -> None:
        rec = {"ts": now_iso(), "run_id": run_id, "event": event, **fields}
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    log("start")

    src = latest_screenshot(c)
    log("source", path=str(src))

    # Resize once (cheap)
    max_w = int(c["MAX_W"]); max_h = int(c["MAX_H"]); q = int(c["JPEG_QUALITY"])
    resized = charts_dir / "dashboard.jpg"
    w,h = resize_to_jpeg(src, resized, max_w, max_h, q)
    log("resized", w=w, h=h, path=str(resized))

    crops: List[Path] = []
    if c["CROP_MODE"] == "quad":
        crops = crop_quadrants(resized, charts_dir)
        log("cropped", files=[p.name for p in crops])

    # OpenAI analyze
    mode = c["ANALYZE_MODE"]
    images_for_ai = [resized] if mode == "single" else (crops if crops else [resized])
    oa = call_openai(c, images_for_ai)
    text_out = oa.get("output_text","")
    signals = extract_json(text_out)

    # Artifacts
    summary = {
        "run_id": run_id,
        "ts": now_iso(),
        "model": oa.get("model"),
        "source_screenshot": str(src),
        "files": {
            "dashboard": str(resized.relative_to(run_dir)),
            "charts": [str(p.relative_to(run_dir)) for p in crops],
        },
        "analysis_text": text_out,
        "signals": signals,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "analysis.txt").write_text(text_out, encoding="utf-8")
    md = "# bot_vision analysis\n\n" + text_out.strip() + "\n"
    (run_dir / "analysis.md").write_text(md, encoding="utf-8")

    # latest symlink
    latest = base_dir / "latest"
    try:
        if latest.exists() or latest.is_symlink():
            latest.unlink()
        latest.symlink_to(run_dir, target_is_directory=True)
    except Exception:
        (base_dir / "latest_path.txt").write_text(str(run_dir), encoding="utf-8")

    # Mirror to vision_outbox (you asked .txt/.md after analyze)
    stub = f"analyze_{run_id}"
    (outbox / f"{stub}.txt").write_text(text_out, encoding="utf-8")
    (outbox / f"{stub}.md").write_text(md, encoding="utf-8")

    log("done")

    # Optional Telegram notify
    if chat_id_override:
        target = chat_id_override.strip()
    else:
        target = ""
        try:
            from shared.telegram_channels import get_chat_id
            target = get_chat_id("push")
        except Exception:
            target = (c.get("TELEGRAM_CHAT_ID") or "").strip()
    if target:
        c["TELEGRAM_CHAT_ID"] = target
        try:
            kb = {"inline_keyboard":[
                [{"text":"Send all (4 charts)", "callback_data": f"sendall:{run_id}"}],
            ]}
            caption = text_out.strip()
            if len(caption) > 900:
                caption = caption[:900] + "…"
            tg_send_photo(c, target, resized, caption=caption, reply_markup=kb)
            if len(text_out) > 3200:
                tg_send_message(c, target, text_out[:3200] + "\n…(truncated)…")
            else:
                tg_send_message(c, target, text_out)
            log("telegram_sent", chat_id=target)
        except Exception as e:
            log("telegram_error", err=str(e))

    return {"run_id": run_id, "run_dir": str(run_dir), "dashboard": str(resized), "charts": [str(p) for p in crops]}

def send_latest_to_telegram() -> None:
    c = cfg(); ensure_dirs(c)
    try:
        from shared.telegram_channels import get_chat_id
        target = get_chat_id("push")
    except Exception:
        target = (c.get("TELEGRAM_CHAT_ID") or "").strip()
    if not target:
        raise RuntimeError("TELEGRAM_CHAT_ID must be set for scheduled sending.")
    c["TELEGRAM_CHAT_ID"] = target
    src = latest_screenshot(c)

    state_path = Path(c["WORKDIR"]) / "sender_state.json"
    prev = {}
    if state_path.exists():
        try:
            prev = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            prev = {}
    key = f"{src.name}:{int(src.stat().st_mtime)}"
    if prev.get("last_key") == key:
        return

    max_w = int(c["MAX_W"]); max_h = int(c["MAX_H"]); q = int(c["JPEG_QUALITY"])
    tmp = Path(c["WORKDIR"]) / "latest_send.jpg"
    resize_to_jpeg(src, tmp, max_w, max_h, q)
    tg_send_photo(c, target, tmp, caption=src.name)

    state_path.write_text(json.dumps({"last_key": key, "ts": now_iso()}, ensure_ascii=False, indent=2), encoding="utf-8")

def prune_old() -> None:
    c = cfg(); ensure_dirs(c)
    keep_days = int(c.get("PRUNE_KEEP_DAYS","7") or "7")
    cutoff = time.time() - keep_days*86400

    for folder_key in ["VISION_PROCESSED","VISION_OUTBOX"]:
        folder = Path(c[folder_key])
        for p in folder.iterdir():
            if not p.is_file():
                continue
            if p.name.startswith("_") or p.name.endswith(".json"):
                continue
            try:
                if p.stat().st_mtime < cutoff:
                    p.unlink()
            except Exception:
                pass

def serve() -> None:
    c = cfg(); ensure_dirs(c)
    offset = 0
    allowed = (c.get("ALLOWED_CHAT_ID") or "").strip()
    print("bot_vision_step2 telegram serve: started", flush=True)
    if allowed:
        print(f"bot_vision_step2 allowlist enabled: {allowed}", flush=True)
    while True:
        try:
            r = tg_api(c, "getUpdates", {"timeout": 50, "offset": offset})
            if not r.get("ok"):
                time.sleep(2); continue
            for upd in r.get("result", []):
                offset = max(offset, int(upd.get("update_id", 0)) + 1)

                msg = upd.get("message") or {}
                if msg:
                    text = (msg.get("text") or "").strip()
                    chat_id = str((msg.get("chat") or {}).get("id") or "")
                    if not chat_id:
                        continue

                    # Hard gate: ignore chats not in allowlist (prevents 400s from random/private chats)
                    if not is_allowed_chat(c, chat_id):
                        continue

                    target = (c.get("TELEGRAM_CHAT_ID") or chat_id).strip()

                    # ── Command Center dispatch ──
                    if text.startswith("/") and not text.startswith("/chatid"):
                        try:
                            _root = str(Path(__file__).resolve().parents[3])
                            if _root not in sys.path:
                                sys.path.insert(0, _root)
                            from modules.telegram_command_center.app.commands import dispatch
                            resp, ch, action = dispatch(text, chat_id=chat_id)
                            if resp:
                                if ch and ch != chat_id:
                                    from shared.telegram_channels import send_to_channel
                                    send_to_channel(ch, resp, source=f"cmd:{text.split()[0]}")
                                else:
                                    tg_send_message(c, chat_id, resp)
                            if action and action.get("kind") == "send_photo_channel":
                                try:
                                    from shared.telegram_channels import get_chat_id
                                    target_photo_chat = get_chat_id(str(action.get("channel") or "push"))
                                    if not target_photo_chat:
                                        raise RuntimeError("target photo channel is not configured")
                                    tg_send_photo(
                                        c,
                                        target_photo_chat,
                                        Path(str(action["photo_path"])),
                                        caption=str(action.get("caption") or ""),
                                    )
                                except Exception as photo_exc:
                                    tg_send_message(c, chat_id, f"Snapshot send failed: {photo_exc}")
                        except Exception as exc:
                            print(f"WARN: command dispatch failed: {exc}", flush=True)
                        continue

                    if text.startswith("/chatid"):
                        try:
                            tg_send_message(c, target, f"chat_id={chat_id}")
                        except Exception as e:
                            print(f"WARN: /chatid send failed: {e}", flush=True)
                        continue
                cb = upd.get("callback_query") or {}
                if cb:
                    cbid = cb.get("id") or ""
                    data = (cb.get("data") or "").strip()
                    msg = cb.get("message") or {}
                    chat_id = str((msg.get("chat") or {}).get("id") or "")
                    target = (c.get("TELEGRAM_CHAT_ID") or chat_id).strip()

                    if not chat_id or not is_allowed_chat(c, chat_id):
                        # Ignore callbacks from other chats.
                        continue

                    if data.startswith("sendall:"):
                        run_id = data.split(":",1)[1]
                        charts_dir = Path(c["DESKPRO_VISION_DIR"]) / "runs" / run_id / "charts"
                        files = [charts_dir / f"{i:02d}.jpg" for i in range(1,5)]
                        sent = 0
                        for f in files:
                            if f.exists():
                                try:
                                    tg_send_photo(c, target, f, caption=f.name)
                                except Exception as e:
                                    print(f"WARN: sendall photo failed: {e}", flush=True)
                                sent += 1
                        try:
                            tg_answer_cb(c, cbid, f"Sent {sent}.")
                        except Exception as e:
                            print(f"WARN: answerCallbackQuery failed: {e}", flush=True)
                    else:
                        if cbid:
                            try:
                                tg_answer_cb(c, cbid, "OK")
                            except Exception as e:
                                print(f"WARN: answerCallbackQuery failed: {e}", flush=True)

        except Exception:
            traceback.print_exc()
            time.sleep(3)

def sanity() -> int:
    c = cfg()
    print("=== bot_vision_step2 sanity ===")
    print(now_iso())
    for k in ["VISION_INBOX","VISION_PROCESSED","VISION_OUTBOX","DESKPRO_VISION_DIR","WORKDIR","MAX_W","MAX_H","CROP_MODE","ANALYZE_MODE"]:
        print(f"{k}={c[k]}")
    ensure_dirs(c, strict=False)
    if Image is None:
        print("WARN: Pillow missing (install_service.sh will install).")
    if not c.get("TELEGRAM_BOT_TOKEN") or c["TELEGRAM_BOT_TOKEN"] == "REPLACE_ME":
        print("WARN: TELEGRAM_BOT_TOKEN not set yet.")
    if not c.get("OPENAI_API_KEY") or c["OPENAI_API_KEY"] == "REPLACE_ME":
        print("WARN: OPENAI_API_KEY not set yet.")
    print("PASS")
    return 0

def usage() -> None:
    print("Usage:")
    print("  bot_vision_step2.py sanity")
    print("  bot_vision_step2.py analyze_latest")
    print("  bot_vision_step2.py send_latest")
    print("  bot_vision_step2.py prune_old")
    print("  bot_vision_step2.py serve")
    sys.exit(2)

def main() -> None:
    if len(sys.argv) < 2:
        usage()
    cmd = sys.argv[1]
    if cmd == "sanity":
        raise SystemExit(sanity())
    if cmd == "analyze_latest":
        res = analyze_latest()
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if cmd == "send_latest":
        send_latest_to_telegram()
        return
    if cmd == "prune_old":
        prune_old()
        return
    if cmd == "serve":
        serve()
        return
    usage()

if __name__ == "__main__":
    main()
