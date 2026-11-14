#!/usr/bin/env python3
"""Install an 8x-upscaled 256x256 item icon preview as res/items/icons/<name>.png + .pal.

usage: install_item_icon.py <preview.png> <name>
The preview's corner colour becomes palette index 0 (transparent). Max 15 other colours.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def main():
    src, name = Image.open(sys.argv[1]).convert('RGB'), sys.argv[2]
    scale = src.width // 32
    bg = src.getpixel((0, 0))
    px = [[src.getpixel((scale * x + scale // 2, scale * y + scale // 2)) for x in range(32)] for y in range(32)]
    colours = sorted({c for row in px for c in row} - {bg})
    assert len(colours) <= 15, f'{len(colours)} colours'
    pal = [bg] + colours + [(0, 0, 0)] * (15 - len(colours))
    out = Image.new('P', (32, 32), 0)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    out.putdata([0 if c == bg else pal.index(c) for row in px for c in row])
    out.save(ROOT / 'res' / 'items' / 'icons' / f'{name}.png')
    lines = ['JASC-PAL', '0100', '256'] + [f'{r} {g} {b}' for r, g, b in pal] + ['0 0 0'] * 240
    (ROOT / 'res' / 'items' / 'icons' / f'{name}.pal').write_text('\r\n'.join(lines) + '\r\n')


if __name__ == '__main__':
    main()
