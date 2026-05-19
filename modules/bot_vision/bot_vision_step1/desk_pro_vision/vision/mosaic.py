from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image

def build_mosaic_2x2(img_paths: List[Path], out_path: Path) -> None:
    # Expect 4 images
    if len(img_paths) != 4:
        raise ValueError(f"Expected 4 images, got {len(img_paths)}")

    imgs = [Image.open(p).convert("RGB") for p in img_paths]
    w = max(i.width for i in imgs)
    h = max(i.height for i in imgs)

    # normalize sizes
    norm = []
    for im in imgs:
        if im.size != (w, h):
            norm.append(im.resize((w, h)))
        else:
            norm.append(im)

    canvas = Image.new("RGB", (w*2, h*2), (255, 255, 255))
    canvas.paste(norm[0], (0, 0))
    canvas.paste(norm[1], (w, 0))
    canvas.paste(norm[2], (0, h))
    canvas.paste(norm[3], (w, h))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, format="PNG")
