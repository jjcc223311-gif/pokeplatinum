#!/usr/bin/env python3
"""Distorted Rift: overworld sprites for the Rift's legendary pool, made from the battle sprites.

Each sprite is a two-frame billboard sheet like the vanilla legendary overworlds (arceus.png,
darkrai.png): frames stacked vertically, 64x64 for big Pokemon and 32x32 for small mythicals.
The front battle sprite is cropped, area-downscaled, reduced to 15 colours, despeckled and
outlined (rebuild_sprite_from_source.py); frame 2 bobs one pixel down.

usage: make_rift_overworlds.py [species...]   (default: the whole pool)
writes res/graphics/field_sprites/pokemon/rift_<species>.png
"""
import sys
from pathlib import Path

from PIL import Image

from rebuild_sprite_from_source import ALPHA_CUT, build_palette, clean, index_frame, outline

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'res/graphics/field_sprites/pokemon'

# species folder -> billboard size. Darkrai and Shaymin use their vanilla overworlds, Arceus too.
POOL = {
    'mewtwo': 64, 'mew': 32, 'raikou': 64, 'entei': 64, 'suicune': 64, 'lugia': 64, 'ho_oh': 64,
    'celebi': 32, 'latias': 64, 'latios': 64, 'kyogre': 64, 'groudon': 64, 'rayquaza': 64,
    'jirachi': 32, 'deoxys': 64, 'manaphy': 32, 'phione': 32, 'victini': 32, 'cobalion': 64,
    'terrakion': 64, 'virizion': 64, 'tornadus': 64, 'thundurus': 64, 'reshiram': 64,
    'zekrom': 64, 'landorus': 64, 'kyurem': 64, 'keldeo': 32, 'meloetta': 32, 'genesect': 64,
}


def battle_front(species):
    d = ROOT / 'res/pokemon' / species
    for gender in ('male', 'female'):
        p = d / f'{gender}_front.png'
        if p.exists():
            im = Image.open(p)
            idx = im.crop((0, 0, 80, 80))
            rgba = idx.convert('RGBA')
            rgba.putdata([(0, 0, 0, 0) if i == 0 else c for i, c in zip(idx.get_flattened_data(), rgba.get_flattened_data())])
            return rgba
    sys.exit(f'error: no front sprite for {species}')


def make(species, size):
    src = battle_front(species)
    src = src.crop(src.getchannel('A').point(lambda a: 255 if a >= ALPHA_CUT else 0).getbbox())
    w, h = src.size
    inner = size - 1  # keep a free row at the top for frame 2's bob
    s = min(inner / w, inner / h)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    big = src.resize((w * 8, h * 8), Image.NEAREST)
    small = big.resize((nw * 2, nh * 2), Image.BOX).resize((nw, nh), Image.LANCZOS)

    frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    frame.paste(small, ((size - nw) // 2, size - 1 - nh))
    colours = build_palette([frame])
    grid = outline(clean(index_frame(frame, colours)), 1)

    pal = [(144, 200, 152)] + colours + [(0, 0, 0)] * (15 - len(colours))
    sheet = Image.new('P', (size, size * 2), 0)
    sheet.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    data = [grid[y][x] for y in range(size) for x in range(size)]
    f1 = Image.new('P', (size, size), 0)
    f1.putdata(data)
    sheet.paste(f1, (0, 0))
    sheet.paste(f1, (0, size + 1))  # frame 2: one pixel lower (the bottom row is always empty)
    sheet.paste(Image.new('P', (size, 1), 0), (0, size))
    sheet.save(OUT / f'rift_{species}.png', bits=4, transparency=0)


def main():
    names = sys.argv[1:] or list(POOL)
    for name in names:
        make(name, POOL[name])
        print(f'rift_{name}.png')


if __name__ == '__main__':
    main()
