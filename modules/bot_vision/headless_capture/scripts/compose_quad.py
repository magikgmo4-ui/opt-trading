#!/usr/bin/env python3
"""
compose_quad — Stitch 4 individual captures into a 2x2 dashboard image.

Used by run_vision_pipeline.py when screen_type == DASHBOARD_MACRO
and layout == quad. Takes 4 images with matching dashboard_id and
composes them into a single 1920x1080 viewport image that can be
fed to bot_vision_step2 in CROP_MODE=quad.

Usage:
  python3 scripts/compose_quad.py \\
    --top-left    /path/to/01.png \\
    --top-right   /path/to/02.png \\
    --bottom-left /path/to/03.png \\
    --bottom-right /path/to/04.png \\
    --output      /path/to/composite.png

The output dimensions are forced to VIEWPORT_SIZE (1920x1080).
Each quadrant is resized to 960x540 and arranged in the 2x2 grid.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

VIEWPORT_W = 1920
VIEWPORT_H = 1080
QUAD_W = VIEWPORT_W // 2
QUAD_H = VIEWPORT_H // 2


def _resize_fill(img: Image.Image, w: int, h: int) -> Image.Image:
    """Resize image to cover target dimensions, center-crop to exact size."""
    scale = max(w / img.width, h / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return resized.crop((left, top, left + w, top + h))


def compose_quad(
    top_left: Path,
    top_right: Path,
    bottom_left: Path,
    bottom_right: Path,
    output: Path,
) -> Path:
    if Image is None:
        raise RuntimeError("Pillow not installed. pip install Pillow")

    canvas = Image.new("RGB", (VIEWPORT_W, VIEWPORT_H), color=(0, 0, 0))

    slots = [
        (top_left, 0, 0),
        (top_right, QUAD_W, 0),
        (bottom_left, 0, QUAD_H),
        (bottom_right, QUAD_W, QUAD_H),
    ]

    for slot_path, x, y in slots:
        if not slot_path.exists():
            raise FileNotFoundError(f"Missing quadrant image: {slot_path}")
        img = Image.open(slot_path).convert("RGB")
        fitted = _resize_fill(img, QUAD_W, QUAD_H)
        canvas.paste(fitted, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(output), format="PNG", optimize=True)
    print(f"OK: composite -> {output} ({VIEWPORT_W}x{VIEWPORT_H})")
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description="Compose 4 captures into 2x2 dashboard")
    ap.add_argument("--top-left", required=True, type=Path)
    ap.add_argument("--top-right", required=True, type=Path)
    ap.add_argument("--bottom-left", required=True, type=Path)
    ap.add_argument("--bottom-right", required=True, type=Path)
    ap.add_argument("--output", "-o", required=True, type=Path)
    args = ap.parse_args()

    try:
        compose_quad(
            args.top_left,
            args.top_right,
            args.bottom_left,
            args.bottom_right,
            args.output,
        )
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
