#!/usr/bin/env python3
"""Recolor Nathan (elite_four_flint / npc flint.png) and Hugo (leader_volkner / npc volkner.png).

  Hugo:   red jacket -> yellow, navy hair -> purple
  Nathan: blue jacket -> black, brown hair -> yellow

Pixels are picked by palette index + a row range inside each frame (so navy pants or red shoes that
share an index with the hair / jacket keep their colour). If the result needs more than 15 colours,
the closest colours are merged. Run with a Python that has Pillow, after phase7_sprites.py.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'scripts'))
from phase7_sprites import front_set  # noqa: E402

CLASSES = ROOT / 'res' / 'trainers' / 'classes'
NPC = ROOT / 'res' / 'graphics' / 'field_sprites' / 'npc'

PURPLE = [(49, 24, 74), (82, 41, 115), (115, 57, 156), (156, 90, 206), (189, 140, 230)]
YELLOW_JACKET = [(140, 99, 24), (189, 148, 41), (247, 206, 57), (255, 239, 140)]
YELLOW_HAIR = [(132, 90, 16), (214, 165, 41), (255, 222, 99), (255, 247, 173)]
BLACK = [(24, 24, 32), (41, 41, 49), (57, 57, 66), (82, 82, 90)]


def lum(c):
    return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def ramp_map(pal, indices, ramp):
    """Map the given palette indices onto a colour ramp, keeping their dark-to-light order."""
    order = sorted(indices, key=lambda i: lum(pal[i]))
    n = len(order)
    return {i: ramp[min(len(ramp) - 1, round(k * (len(ramp) - 1) / max(1, n - 1)))] if n > 1 else ramp[len(ramp) // 2]
            for k, i in enumerate(order)}


def recolor(img, frame_h, rules):
    """rules: list of (indices, ramp, y0, y1, x0, x1[, exclude boxes (x0, y0, x1, y1)]); y relative to each
    frame. Returns a new P image."""
    pal = [tuple(img.getpalette()[3 * i:3 * i + 3]) for i in range(16)]
    maps = [(set(r[0]), ramp_map(pal, r[0], r[1]), *r[2:6], r[6] if len(r) > 6 else []) for r in rules]
    w, h = img.size
    src = img.load()
    rgb = {}
    for y in range(h):
        fy = y % frame_h
        for x in range(w):
            i = src[x, y]
            if i == 0:
                continue
            c = pal[i]
            for idx, m, y0, y1, x0, x1, excl in maps:
                if i in idx and y0 <= fy <= y1 and x0 <= x <= x1 \
                        and not any(a <= x <= c and b <= fy <= d for a, b, c, d in excl):
                    c = m[i]
                    break
            rgb[(x, y)] = c
    counts = {}
    for c in rgb.values():
        counts[c] = counts.get(c, 0) + 1
    colours = list(counts)
    remap = {c: c for c in colours}
    while len(colours) > 15:
        best = None
        for a in range(len(colours)):
            for b in range(a + 1, len(colours)):
                ca, cb = colours[a], colours[b]
                d = sum((p - q) ** 2 for p, q in zip(ca, cb)) * min(counts[ca], counts[cb])
                if best is None or d < best[0]:
                    best = (d, ca, cb)
        _, ca, cb = best
        keep, drop = (ca, cb) if counts[ca] >= counts[cb] else (cb, ca)
        counts[keep] += counts.pop(drop)
        colours.remove(drop)
        for k, v in remap.items():
            if v == drop:
                remap[k] = keep
    colours.sort(key=lum)
    index = {c: i + 1 for i, c in enumerate(colours)}
    out = Image.new('P', (w, h), 0)
    flat = [0, 0, 0] + [v for c in colours for v in c]
    out.putpalette(flat + [0] * (48 - len(flat)))  # exactly 16 colours (field textures need it)
    px = out.load()
    for (x, y), c in rgb.items():
        px[x, y] = index[remap[c]]
    return out


def front(cls, rules):
    img = Image.open(CLASSES / cls / 'front.png')
    frame = img.crop((0, 0, 80, 80))
    frame.putpalette(img.getpalette())
    front_set(cls, recolor(frame, 80, rules))


def overworld(name, rules):
    img = Image.open(NPC / f'{name}.png')
    recolor(img, 32, rules).save(NPC / f'{name}.png')


def main():
    # Hugo: front (hair rows 0-24; jacket = sleeve from x 27 + body, minus the face and the shoes)
    front('leader_volkner', [
        ([1, 4, 14], PURPLE, 0, 24, 0, 79),
        ([3, 5, 8], YELLOW_JACKET, 25, 62, 27, 79, [(30, 24, 52, 31)]),
    ])
    overworld('volkner', [
        ([1, 3, 4, 5], PURPLE, 0, 17, 0, 31),
        ([8, 9, 14], YELLOW_JACKET, 18, 26, 0, 31),
    ])
    # Nathan: front (hair rows 0-30; jacket rows 31-52)
    front('elite_four_flint', [
        ([2, 3, 4], YELLOW_HAIR, 0, 30, 0, 79),
        ([8, 9, 10, 11], BLACK, 31, 52, 0, 79),
    ])
    overworld('flint', [
        ([2, 3, 4], YELLOW_HAIR, 0, 17, 0, 31),
        ([10, 11, 12], BLACK, 18, 27, 0, 31),
    ])

    # VS-screen close-ups from the recoloured fronts
    import make_vs_mugshots
    make_vs_mugshots.main()


if __name__ == '__main__':
    main()
