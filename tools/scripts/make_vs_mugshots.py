#!/usr/bin/env python3
"""VS-screen close-ups (mugshot.png, 96x64) for the replaced trainers, made from their battle sprites.

Vanilla close-ups are a tight head-and-shoulders crop at roughly 2.5x. This crops the head (found from
the sprite's top rows), enlarges it with Scale2x twice (pixel-art upscaling that keeps outlines sharp
and smooths diagonals), shrinks it to 96x64 and maps every pixel back onto the sprite's own 16-colour
palette, so the result has the same colours and outline as the battle sprite.
usage: make_vs_mugshots.py [preview_dir]   (run with a Python that has Pillow, after the sprite scripts)
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CLASSES = ROOT / 'res' / 'trainers' / 'classes'

# class: (crop width in sprite pixels, extra rows above the hair, horizontal nudge)
TRAINERS = {
    'leader_volkner': (46, 1, 5),      # Hugo (tall hair: wider crop, away from the Poké Ball hand)
    'elite_four_flint': (40, 1, 0),    # Nathan
    'elite_four_aaron': (40, 1, 0),    # Beatrice
    'leader_candice': (40, 1, 0),      # Dawn
}
OUT_W, OUT_H = 96, 64


def scale2x(px, w, h):
    """EPX / Scale2x on a 2D list of palette indices."""
    out = [[0] * (2 * w) for _ in range(2 * h)]
    for y in range(h):
        for x in range(w):
            p = px[y][x]
            a = px[y - 1][x] if y > 0 else p
            b = px[y][x + 1] if x < w - 1 else p
            c = px[y][x - 1] if x > 0 else p
            d = px[y + 1][x] if y < h - 1 else p
            e0 = c if (c == a and c != d and a != b) else p
            e1 = a if (a == b and a != c and b != d) else p
            e2 = c if (d == c and d != b and c != a) else p
            e3 = b if (b == d and b != a and d != c) else p
            out[2 * y][2 * x], out[2 * y][2 * x + 1] = e0, e1
            out[2 * y + 1][2 * x], out[2 * y + 1][2 * x + 1] = e2, e3
    return out


def make(cls, crop_w, above, nudge):
    front = Image.open(CLASSES / cls / 'front.png')
    pal = (front.getpalette() + [0] * 48)[:48]
    frame = front.crop((0, 0, 80, 80))
    src = frame.load()

    rows = [y for y in range(80) if any(src[x, y] for x in range(80))]
    top = rows[0]
    # head centre: mean x of the opaque pixels in the first 14 rows
    xs = [x for y in range(top, top + 14) for x in range(80) if src[x, y]]
    cx = sum(xs) // len(xs) + nudge
    crop_h = crop_w * OUT_H // OUT_W
    x0 = max(0, min(80 - crop_w, cx - crop_w // 2))
    y0 = max(0, top - above)
    px = [[src[x, y] if y < 80 else 0 for x in range(x0, x0 + crop_w)] for y in range(y0, y0 + crop_h)]

    big = scale2x(px, crop_w, crop_h)
    big = scale2x(big, 2 * crop_w, 2 * crop_h)
    bw, bh = 4 * crop_w, 4 * crop_h

    # shrink to 96x64 by nearest sampling of the 4x image (keeps the palette, no blending)
    mug = Image.new('P', (OUT_W, OUT_H), 0)
    mug.putpalette(pal + [0] * (768 - 48))
    out = mug.load()
    for y in range(OUT_H):
        for x in range(OUT_W):
            out[x, y] = big[min(bh - 1, (2 * y + 1) * bh // (2 * OUT_H))][min(bw - 1, (2 * x + 1) * bw // (2 * OUT_W))]
    mug.save(CLASSES / cls / 'mugshot.png')
    return mug


def main():
    preview = Path(sys.argv[1]) if len(sys.argv) > 1 and __name__ == "__main__" else None
    mugs = [make(cls, *args) for cls, args in TRAINERS.items()]
    if preview:
        sheet = Image.new('RGB', (len(mugs) * 200, 136), (255, 0, 255))
        for i, m in enumerate(mugs):
            rgb = m.convert('RGB')
            bg = Image.new('RGB', m.size, (120, 200, 120))
            mask = m.point(lambda v: 255 if v else 0).convert('L') if False else Image.frombytes('L', m.size, bytes(255 if v else 0 for v in m.tobytes()))
            bg.paste(rgb, (0, 0), mask)
            sheet.paste(bg.resize((192, 128), Image.NEAREST), (200 * i, 0))
        sheet.save(preview / 'vs_mugshots_preview.png')


if __name__ == '__main__':
    main()
