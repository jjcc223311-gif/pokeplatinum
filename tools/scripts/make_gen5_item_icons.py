#!/usr/bin/env python3
"""Draw item icons for the Reveal Glass and Genesect's four Drives (res/items/icons/*.png + .pal).

Writes 8x previews to <out_dir> when given. usage: make_gen5_item_icons.py [out_dir]  (Pillow)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
ICONS = ROOT / 'res' / 'items' / 'icons'
BG = (180, 180, 180)
OUTLINE = (41, 41, 49)


def save(name, img, out_dir):
    colours = sorted({c for c in img.get_flattened_data()} - {BG})
    assert len(colours) <= 15, (name, len(colours))
    pal = [BG] + colours + [(0, 0, 0)] * (15 - len(colours))
    out = Image.new('P', (32, 32), 0)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    out.putdata([pal.index(c) for c in img.get_flattened_data()])
    out.save(ICONS / f'{name}.png')
    lines = ['JASC-PAL', '0100', '256'] + [f'{r} {g} {b}' for r, g, b in pal] + ['0 0 0'] * 240
    (ICONS / f'{name}.pal').write_text('\r\n'.join(lines) + '\r\n')
    if out_dir:
        img.resize((256, 256), Image.NEAREST).save(Path(out_dir) / f'{name}_preview.png')


def drive(main, light, dark):
    img = Image.new('RGB', (32, 32), BG)
    d = ImageDraw.Draw(img)
    # cartridge body (grey metal) with a coloured label and a notch
    d.rectangle((7, 5, 24, 27), fill=(150, 156, 172), outline=OUTLINE)
    d.rectangle((8, 6, 23, 8), fill=(198, 205, 222))
    d.rectangle((9, 10, 22, 22), fill=main, outline=dark)
    d.rectangle((10, 11, 21, 12), fill=light)
    d.line((10, 21, 21, 21), fill=dark)
    for x in (10, 13, 16, 19):  # contacts
        d.rectangle((x, 24, x + 1, 26), fill=(222, 189, 74))
    d.rectangle((12, 15, 19, 17), fill=light)
    return img


def reveal_glass():
    img = Image.new('RGB', (32, 32), BG)
    d = ImageDraw.Draw(img)
    gold, gold_d, purple, purple_l = (230, 189, 74), (156, 115, 33), (115, 74, 164), (189, 156, 230)
    d.rectangle((14, 21, 17, 29), fill=gold, outline=OUTLINE)  # handle
    d.ellipse((5, 2, 26, 23), fill=gold, outline=OUTLINE)
    d.ellipse((7, 4, 24, 21), fill=gold_d)
    d.ellipse((8, 5, 23, 20), fill=purple)
    d.ellipse((10, 7, 17, 13), fill=purple_l)
    d.point([(11, 8), (12, 8), (11, 9)], fill=(255, 255, 255))
    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None
    save('reveal_glass', reveal_glass(), out_dir)
    save('douse_drive', drive((57, 123, 230), (139, 189, 255), (24, 66, 156)), out_dir)
    save('shock_drive', drive((246, 205, 41), (255, 238, 148), (180, 139, 16)), out_dir)
    save('burn_drive', drive((222, 57, 49), (255, 139, 115), (148, 24, 24)), out_dir)
    save('chill_drive', drive((222, 238, 246), (255, 255, 255), (139, 172, 197)), out_dir)


if __name__ == '__main__':
    main()
