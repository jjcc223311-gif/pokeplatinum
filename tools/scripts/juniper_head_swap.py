#!/usr/bin/env python3
"""Stand-in Juniper action sprites: put Juniper's real head (from her walk sheet, player_f.png)
onto the 9 action sheets that juniper_field_poses.py made by recolouring Dawn, and turn Dawn's
green skirt into Juniper's white lab coat.

Reads the action sheets from commit 79914c67 (the recoloured-Dawn versions), so it can be re-run.
Facing is detected per frame from where the face (skin) sits under the hair.
usage: juniper_head_swap.py [--preview out.png]
"""
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DIR = 'res/graphics/field_sprites/player'
BASE = '79914c67'
SHEETS = ['player_f_bike', 'player_f_fishing', 'player_f_holding_pokeball', 'player_f_pokecenter_heal',
          'player_f_poketch', 'player_f_save', 'player_f_sprayduck', 'player_f_surf', 'player_f_vs_seeker']
# Juniper's standing frames in player_f.png
JUN_FRAME = {'up': 0, 'down': 4, 'left': 8, 'right': 12}

HAIR = [(189, 139, 82), (164, 115, 66), (131, 90, 57), (98, 57, 41), (74, 41, 33)]
SKIN = [(255, 214, 189), (222, 165, 123)]
GREEN = [(57, 99, 74), (82, 148, 98)]
COAT = {(57, 99, 74): (206, 206, 222), (82, 148, 98): (239, 239, 255)}  # skirt -> lab coat


def git_image(path, rev):
    data = subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=ROOT, capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data))


def pal_of(img):
    p = img.getpalette()
    return [tuple(p[3 * i:3 * i + 3]) for i in range(16)]


def nearest(pal, c):
    return min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], c)))


def px(img, x, y):
    return img.getpixel((x, y))


def head_box(frame, pal, hair_cols):
    """Rows/cols of the hair+face block at the top of a 32x32 frame."""
    pts = [(x, y) for y in range(32) for x in range(32)
           if px(frame, x, y) and pal[px(frame, x, y)] in hair_cols]
    if not pts:
        return None
    top = min(y for _, y in pts)
    xs = [x for x, y in pts if y < top + 12]
    return top, sum(xs) / len(xs)


def facing(frame, pal):
    hb = head_box(frame, pal, HAIR)
    top, hx = hb
    skin = [(x, y) for y in range(top, min(32, top + 16)) for x in range(32)
            if px(frame, x, y) and pal[px(frame, x, y)] in SKIN]
    if len(skin) < 6:
        return 'up'
    sx = sum(x for x, _ in skin) / len(skin)
    if sx < hx - 1.5:
        return 'left'
    if sx > hx + 1.5:
        return 'right'
    return 'down'


def main():
    walk = Image.open(ROOT / DIR / 'player_f.png')
    wpal = pal_of(walk)
    jhair = [c for c in wpal if c in [(189, 139, 82), (131, 90, 57), (222, 164, 123), (123, 74, 74)]]
    jun = {}
    for face, k in JUN_FRAME.items():
        fr = walk.crop((0, k * 32, 32, k * 32 + 32))
        top, hx = head_box(fr, wpal, jhair)
        jun[face] = (fr, top, hx)
    HEAD_H = 14  # rows taken from Juniper: hair top to chin
    previews = []
    for name in SHEETS:
        src = git_image(f'{DIR}/{name}.png', BASE)
        pal = pal_of(src)
        out = src.copy()
        for k in range(src.size[1] // 32):
            fr = src.crop((0, k * 32, 32, k * 32 + 32))
            face = facing(fr, pal)
            top, hx = head_box(fr, pal, HAIR)
            jfr, jtop, jhx = jun[face]
            dx, dy = round(hx - jhx), top - jtop
            new = fr.copy()
            # held items next to the head (the VS Seeker): green screen with a brown frame. Keep every
            # pixel in a box around the green so the item stays in front of the new head
            greens = [(x, y) for y in range(32) for x in range(32)
                      if px(fr, x, y) and y < top + HEAD_H - 2 and (
                          pal[px(fr, x, y)] in GREEN
                          or (pal[px(fr, x, y)] == (230, 98, 90) and abs(x - hx) >= 8))]
            keep = set()
            if greens:
                x0, x1 = min(x for x, _ in greens) - 2, max(x for x, _ in greens) + 2
                y0, y1 = min(y for _, y in greens) - 2, max(y for _, y in greens) + 2
                keep = {(x, y) for x in range(max(0, x0), min(32, x1 + 1))
                        for y in range(max(0, y0), min(32, y1 + 1)) if px(fr, x, y)}
            # 1. clear Dawn's hair and face
            # (row by row, only between the leftmost and rightmost hair/face pixel, so hands and
            # held items beside the head keep their outline)
            for y in range(top, min(32, top + HEAD_H)):
                xs = [x for x in range(32) if px(fr, x, y) and (pal[px(fr, x, y)] in HAIR or pal[px(fr, x, y)] in SKIN)]
                if not xs:
                    continue
                for x in range(max(0, min(xs) - 1), min(32, max(xs) + 2)):
                    c = pal[px(fr, x, y)]
                    if (x, y) not in keep and px(fr, x, y) and (c in HAIR or c in SKIN or c == (0, 0, 0)
                                         or c in [(230, 98, 90), (164, 57, 65), (123, 66, 66)]):
                        new.putpixel((x, y), 0)
            # 2. lab coat
            for y in range(32):
                for x in range(32):
                    c = pal[px(new, x, y)]
                    if px(new, x, y) and c in COAT and y >= top + HEAD_H - 2:
                        new.putpixel((x, y), nearest(pal, COAT[c]))
            # 3. Juniper's head
            for y in range(jtop, min(32, jtop + HEAD_H)):
                for x in range(32):
                    v = px(jfr, x, y)
                    tx, ty = x + dx, y + dy
                    if v and 0 <= tx < 32 and 0 <= ty < 32 and (tx, ty) not in keep:
                        new.putpixel((tx, ty), nearest(pal, wpal[v]))
            out.paste(new, (0, k * 32))
            previews.append((name, k, face, fr, new, pal))
        out.save(ROOT / DIR / f'{name}.png')
    if len(sys.argv) > 2 and sys.argv[1] == '--preview':
        from PIL import ImageDraw
        per = 12
        rows = (len(previews) + per - 1) // per
        S = 3
        img = Image.new('RGB', (per * (32 * S + 4), rows * (64 * S + 22)), (120, 160, 120))
        d = ImageDraw.Draw(img)
        for i, (name, k, face, a, b, pal) in enumerate(previews):
            x, y = (i % per) * (32 * S + 4), (i // per) * (64 * S + 22)
            for j, fr in enumerate((a, b)):
                rgba = fr.convert('RGBA')
                rgba.putdata([(0, 0, 0, 0) if v == 0 else (*pal[v], 255) for v in fr.get_flattened_data()])
                rgba = rgba.resize((32 * S, 32 * S), Image.NEAREST)
                img.paste(rgba, (x, y + 12 + j * 32 * S), rgba)
            d.text((x + 1, y), f'{name[9:]}{k} {face[0]}', fill=(0, 0, 0))
        img.save(sys.argv[2])


if __name__ == '__main__':
    main()
