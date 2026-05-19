#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import time
import json
import hashlib
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
SKIP_STATUSES = {"blocked", "invalid_visual"}

def check_sidecar_status(img_path: Path) -> str | None:
    sidecar = img_path.with_suffix(".json")
    if not sidecar.exists():
        return None
    try:
        meta = json.loads(sidecar.read_text(encoding="utf-8"))
        return meta.get("status")
    except Exception:
        return None

def env(name: str, default: str) -> str:
    v = os.environ.get(name)
    return v if v not in (None, "") else default

def now_iso() -> str:
    # keep timezone naive; logs in local time on host
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def load_state(state_path: Path) -> dict:
    if state_path.exists():
        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            return {"processed": {}}
    return {"processed": {}}

def save_state(state_path: Path, state: dict) -> None:
    safe_mkdir(state_path.parent)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")

def is_file_stable(p: Path, wait_ms: int = 400) -> bool:
    try:
        s1 = p.stat().st_size
        time.sleep(wait_ms / 1000.0)
        s2 = p.stat().st_size
        return s1 == s2 and s2 > 0
    except FileNotFoundError:
        return False

def write_outputs(outbox: Path, stem: str, md: str, raw: str) -> None:
    safe_mkdir(outbox)
    (outbox / f"{stem}.md").write_text(md, encoding="utf-8")
    (outbox / f"{stem}.txt").write_text(raw, encoding="utf-8")

def engine_dummy(image: Path, prompt: str) -> tuple[str, str]:
    raw = f"[dummy] No engine configured. Image={image.name}\nPrompt={prompt}\n"
    md = "\n".join([
        f"# vision_bot result (dummy)",
        f"- image: `{image.name}`",
        f"- time: `{now_iso()}`",
        "",
        "## Output",
        "No engine configured. Set `VISION_BOT_ENGINE` to `ocr` (needs tesseract) or `shell`.",
        "",
        "### Raw",
        "```",
        raw.strip(),
        "```",
        ""
    ])
    return md, raw

def engine_ocr(image: Path, prompt: str) -> tuple[str, str]:
    # Prefer tesseract CLI; no python deps.
    # Note: prompt unused for OCR (kept for interface)
    cmd = ["tesseract", str(image), "stdout"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return engine_dummy(image, prompt)

    raw = (p.stdout or "").strip()
    if not raw:
        raw = (p.stderr or "").strip() or "[ocr] no text extracted"

    md = "\n".join([
        f"# vision_bot result (ocr)",
        f"- image: `{image.name}`",
        f"- time: `{now_iso()}`",
        "",
        "## Extracted text",
        "```",
        raw[:20000],  # guard against huge outputs
        "```",
        ""
    ])
    return md, raw

def engine_shell(image: Path, prompt: str) -> tuple[str, str]:
    tmpl = env("VISION_BOT_SHELL_CMD", "")
    if not tmpl:
        return engine_dummy(image, prompt)

    cmd = tmpl.format(image=str(image), prompt=prompt)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    raw = (p.stdout or "").strip()
    if not raw:
        raw = (p.stderr or "").strip() or f"[shell] command exited {p.returncode} with no output"

    md = "\n".join([
        f"# vision_bot result (shell)",
        f"- image: `{image.name}`",
        f"- time: `{now_iso()}`",
        "",
        "## Output",
        "```",
        raw[:20000],
        "```",
        ""
    ])
    return md, raw

def pick_engine(name: str):
    name = (name or "").strip().lower()
    if name == "ocr":
        return engine_ocr
    if name == "shell":
        return engine_shell
    return engine_dummy

def list_images(inbox: Path) -> list[Path]:
    if not inbox.exists():
        return []
    items = []
    for p in inbox.iterdir():
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            items.append(p)
    items.sort(key=lambda x: x.stat().st_mtime)
    return items

def log_line(log_path: Path, msg: str) -> None:
    safe_mkdir(log_path.parent)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{now_iso()} | {msg}\n")

def process_once() -> int:
    repo_root = Path(__file__).resolve().parents[3]  # .../modules/vision_bot/app/vision_bot.py
    work_dir = Path(env("VISION_BOT_WORKDIR", str(repo_root / "_work" / "vision_bot")))
    inbox = Path(env("VISION_BOT_INBOX", "/srv/sftp/shared_files/shared/vision_inbox"))
    outbox = Path(env("VISION_BOT_OUTBOX", "/srv/sftp/shared_files/shared/vision_outbox"))
    processed = Path(env("VISION_BOT_PROCESSED", "/srv/sftp/shared_files/shared/vision_processed"))
    log_path = Path(env("VISION_BOT_LOG", str(work_dir / "vision_bot.log")))
    state_path = Path(env("VISION_BOT_STATE", str(work_dir / "state.json")))
    engine_name = env("VISION_BOT_ENGINE", "ocr")
    prompt_default = env("VISION_BOT_PROMPT_DEFAULT", "Décris le screenshot et extrait les infos utiles.")
    safe_mkdir(work_dir)
    safe_mkdir(inbox)
    safe_mkdir(outbox)
    safe_mkdir(processed)

    state = load_state(state_path)
    processed_map = state.setdefault("processed", {})

    engine = pick_engine(engine_name)

    imgs = list_images(inbox)
    if not imgs:
        log_line(log_path, "run_once: no images in inbox")
        return 0

    ok = 0
    for img in imgs:
        if not is_file_stable(img):
            log_line(log_path, f"skip unstable: {img.name}")
            continue

        sidecar_status = check_sidecar_status(img)
        if sidecar_status in SKIP_STATUSES:
            log_line(log_path, f"skip {sidecar_status}: {img.name}")
            rejected_dir = processed / "rejected"
            safe_mkdir(rejected_dir)
            try:
                shutil.move(str(img), str(rejected_dir / img.name))
                sidecar = img.with_suffix(".json")
                if sidecar.exists():
                    shutil.move(str(sidecar), str(rejected_dir / sidecar.name))
            except Exception as e:
                log_line(log_path, f"WARN move rejected failed: {img.name} ({e})")
            continue

        h = sha256_file(img)
        if processed_map.get(h):
            log_line(log_path, f"skip already processed: {img.name}")
            # optionally move duplicates to processed
            dup_target = processed / img.name
            try:
                shutil.move(str(img), str(dup_target))
            except Exception:
                pass
            continue

        prompt_path = img.with_suffix(".prompt.txt")
        prompt = prompt_default
        if prompt_path.exists():
            try:
                prompt = prompt_path.read_text(encoding="utf-8").strip() or prompt_default
            except Exception:
                prompt = prompt_default

        log_line(log_path, f"process: {img.name} engine={engine_name}")
        md, raw = engine(img, prompt)

        stem = img.stem
        write_outputs(outbox, stem, md, raw)

        target = processed / img.name
        try:
            shutil.move(str(img), str(target))
        except Exception as e:
            log_line(log_path, f"WARN move failed: {img.name} -> processed ({e})")

        processed_map[h] = {
            "file": img.name,
            "processed_at": now_iso(),
            "engine": engine_name
        }
        save_state(state_path, state)
        ok += 1

    # Cleanup orphaned blocked JSONs (no matching PNG)
    rejected_dir = processed / "rejected"
    for p in inbox.iterdir():
        if not p.is_file() or p.suffix.lower() != ".json":
            continue
        if p.with_suffix(".png").exists():
            continue
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
            if meta.get("status") in SKIP_STATUSES:
                safe_mkdir(rejected_dir)
                shutil.move(str(p), str(rejected_dir / p.name))
                log_line(log_path, f"archive blocked orphan: {p.name}")
        except Exception:
            pass

    log_line(log_path, f"run_once: processed={ok} total_seen={len(imgs)}")
    return 0

def watch_loop() -> int:
    poll = float(env("VISION_BOT_POLL_SEC", "2"))
    log_path = Path(env("VISION_BOT_LOG", "/opt/trading/_work/vision_bot/vision_bot.log"))
    log_line(log_path, f"watch: started poll={poll}s")
    try:
        while True:
            process_once()
            time.sleep(poll)
    except KeyboardInterrupt:
        log_line(log_path, "watch: stopped (KeyboardInterrupt)")
        return 0

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: vision_bot.py run_once|watch", file=sys.stderr)
        return 2
    cmd = argv[1].strip().lower()
    if cmd == "run_once":
        return process_once()
    if cmd == "watch":
        return watch_loop()
    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
