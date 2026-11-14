#!/usr/bin/env python3
"""
Generates the Legendary button art for the battle move menu (src/battle/battle_subscreen.c).

Output: src/battle/legendary_button_gfx.h, containing
  - sLegendaryButtonTiles:     9x6 tiles (72x48 px, 4bpp), row-major
  - sLegendaryButtonPalettes:  [normal, active, disabled] 16-color BG palettes

The art is a gold plate with a rough, rocky stone border. To use your own art instead, draw a
72x48 4bpp indexed image with the same palette layout (see PALETTE below) and convert it to the
same tile order, or edit draw_button() here and re-run:

    python3 tools/scripts/gen_legendary_button.py
"""

import random
import struct
import zlib
from pathlib import Path

W, H = 72, 48  # 9 x 6 tiles

# Palette layout (index: role)
#   0 transparent | 1 white sparkle | 2-4 stone dark/mid/light | 5 stone outline
#   6-11 gold light -> dark | 12 gold highlight
STONE = [(9, 8, 7), (14, 12, 10), (19, 17, 14)]
STONE_OUTLINE = (4, 3, 3)
GOLD = [(31, 30, 18), (31, 27, 8), (29, 23, 3), (25, 18, 1), (20, 13, 1), (14, 9, 1)]
GOLD_HIGHLIGHT = (31, 31, 26)


def palette(gold, stone, outline, highlight, white=(31, 31, 31)):
    cols = [(0, 0, 0), white] + stone + [outline] + gold + [highlight] + [(0, 0, 0)] * 3
    return cols


def brighten(c, amt):
    return tuple(min(31, round(v + (31 - v) * amt)) for v in c)


def grey(c):
    g = round(0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])
    g = round(g * 0.75 + 4)
    return (g, g, g)


PALETTES = {
    'normal': palette(GOLD, STONE, STONE_OUTLINE, GOLD_HIGHLIGHT),
    'active': palette([brighten(c, 0.35) for c in GOLD], [brighten(c, 0.15) for c in STONE], STONE_OUTLINE, (31, 31, 31)),
    'disabled': palette([grey(c) for c in GOLD], [grey(c) for c in STONE], grey(STONE_OUTLINE), grey(GOLD_HIGHLIGHT), grey((31, 31, 31))),
}


def draw_button():
    rnd = random.Random(1234)
    px = [[0] * W for _ in range(H)]

    # Irregular outer edge: each row/column is inset by 0-2 px, corners rounded off
    def inside_outer(x, y):
        r = 6
        cx = min(max(x, r), W - 1 - r)
        cy = min(max(y, r), H - 1 - r)
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

    rough_left = [rnd.choice([0, 0, 1, 1, 2]) for _ in range(H)]
    rough_right = [rnd.choice([0, 0, 1, 1, 2]) for _ in range(H)]
    rough_top = [rnd.choice([0, 0, 1, 1, 2]) for _ in range(W)]
    rough_bot = [rnd.choice([0, 0, 1, 1, 2]) for _ in range(W)]

    border = 5
    for y in range(H):
        for x in range(W):
            if not inside_outer(x, y):
                continue
            if x < rough_left[y] or x > W - 1 - rough_right[y] or y < rough_top[x] or y > H - 1 - rough_bot[x]:
                continue

            depth = min(x - rough_left[y], W - 1 - rough_right[y] - x, y - rough_top[x], H - 1 - rough_bot[x] - y)
            inner_jag = (x * 7 + y * 13) % 3 == 0  # makes the stone/gold boundary rough too
            if depth < border + (1 if inner_jag else 0):
                if depth == 0:
                    px[y][x] = 5  # outline
                else:
                    px[y][x] = rnd.choice([2, 2, 3, 3, 3, 4])  # rocky texture
            else:
                # Gold plate: vertical gradient, light at the top
                gy = (y - border) / max(1, (H - 2 * border - 1))
                idx = 6 + min(5, int(gy * 6))
                px[y][x] = idx

    # Stone "cracks": short dark streaks
    for _ in range(14):
        x, y = rnd.randrange(W), rnd.randrange(H)
        for _ in range(3):
            if 0 <= x < W and 0 <= y < H and px[y][x] in (3, 4):
                px[y][x] = 2
            x += rnd.choice([-1, 0, 1])
            y += rnd.choice([-1, 0, 1])

    # Light catching the top of the stones
    for x in range(W):
        for y in range(H):
            if px[y][x] in (2, 3, 4):
                if y > 0 and px[y - 1][x] in (0, 5):
                    px[y][x] = 4
                break

    # Gold highlight band and a few sparkles
    for x in range(border + 2, W - border - 2):
        y = border + 2
        if px[y][x] in range(6, 12):
            px[y][x] = 12
    for _ in range(6):
        x = rnd.randrange(border + 3, W - border - 3)
        y = rnd.randrange(border + 3, H - border - 3)
        if px[y][x] in range(6, 12):
            px[y][x] = 1

    return px


def to_tiles(px):
    tiles = []
    for ty in range(H // 8):
        for tx in range(W // 8):
            tile = bytearray()
            for y in range(8):
                for x in range(0, 8, 2):
                    lo = px[ty * 8 + y][tx * 8 + x]
                    hi = px[ty * 8 + y][tx * 8 + x + 1]
                    tile.append(lo | (hi << 4))
            tiles.append(bytes(tile))
    return tiles


def rgb555(c):
    return c[0] | (c[1] << 5) | (c[2] << 10)


def write_preview_png(path, px, pal):
    raw = b''.join(b'\0' + bytes(row) for row in px)
    out = b'\x89PNG\r\n\x1a\n'

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)

    out += chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 3, 0, 0, 0))
    out += chunk(b'PLTE', b''.join(bytes((r * 255 // 31, g * 255 // 31, b * 255 // 31)) for r, g, b in pal))
    out += chunk(b'tRNS', b'\0')
    out += chunk(b'IDAT', zlib.compress(raw, 9))
    out += chunk(b'IEND', b'')
    Path(path).write_bytes(out)


def main():
    root = Path(__file__).resolve().parents[2]
    px = draw_button()
    tiles = to_tiles(px)

    lines = [
        '// Generated by tools/scripts/gen_legendary_button.py -- do not edit by hand.',
        '// Legendary button art: 9x6 tiles (72x48 px), 4bpp, row-major.',
        '',
        '#define LEGENDARY_BUTTON_TILES_W 9',
        '#define LEGENDARY_BUTTON_TILES_H 6',
        '',
        'static const u8 sLegendaryButtonTiles[LEGENDARY_BUTTON_TILES_W * LEGENDARY_BUTTON_TILES_H][32] = {',
    ]
    for t in tiles:
        lines.append('    { ' + ', '.join('0x%02X' % b for b in t) + ' },')
    lines += ['};', '', '// [0] normal, [1] active (Legendary set), [2] disabled (greyed out)',
              'static const u16 sLegendaryButtonPalettes[3][16] = {']
    for name in ('normal', 'active', 'disabled'):
        lines.append('    { ' + ', '.join('0x%04X' % rgb555(c) for c in PALETTES[name]) + ' }, // ' + name)
    lines += ['};', '']

    (root / 'src/battle/legendary_button_gfx.h').write_text('\n'.join(lines))
    write_preview_png(root / 'tools/scripts/legendary_button_preview.png', px, PALETTES['normal'])
    print('wrote src/battle/legendary_button_gfx.h and tools/scripts/legendary_button_preview.png')


if __name__ == '__main__':
    main()
