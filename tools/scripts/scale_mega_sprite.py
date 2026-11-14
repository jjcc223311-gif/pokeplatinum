#!/usr/bin/env python3
"""Scale a 160x80 two-frame indexed Pokemon sprite up (nearest neighbour, palette kept).

The Mega packs draw everything inside a 64x64 box, so Megas looked smaller than the
vanilla 80x80 sprites. Fronts keep their bottom (feet) row; backs are also raised.

Usage: scale_mega_sprite.py front|back <in.png> <out.png>
"""
import sys
from PIL import Image

MAX_SCALE = 1.2   # "slightly bigger"
BACK_RAISE = 4    # back sprites sit this many pixels higher


def scale(face, img):
    assert img.mode == 'P' and img.size == (160, 80)
    frame = img.crop((0, 0, 80, 80))
    box = frame.getbbox()  # index 0 is transparent
    if box is None:
        return img
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    bottom = y1  # exclusive
    if face == 'back':
        bottom = max(h, bottom - BACK_RAISE)
    s = min(MAX_SCALE, 80 / w, bottom / h)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    part = frame.crop(box).resize((nw, nh), Image.NEAREST)
    cx = (x0 + x1) / 2
    nx = int(round(cx - nw / 2))
    nx = min(max(nx, 0), 80 - nw)
    ny = bottom - nh
    out = Image.new('P', (160, 80), 0)
    out.putpalette(img.getpalette())
    for fx in (0, 80):
        out.paste(part, (nx + fx, ny))
    if 'transparency' in img.info:
        out.info['transparency'] = img.info['transparency']
    return out


if __name__ == '__main__':
    face, src, dst = sys.argv[1:4]
    im = Image.open(src)
    out = scale(face, im)
    out.save(dst, bits=4, **({'transparency': im.info['transparency']} if 'transparency' in im.info else {}))
