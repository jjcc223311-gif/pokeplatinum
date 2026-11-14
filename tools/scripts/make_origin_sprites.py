#!/usr/bin/env python3
"""Origin Forme Dialga / Palkia battle sprites: recolours of the vanilla Dialga / Palkia sprites.

The vanilla sprites are hand-drawn pixel art; these keep every pixel (both animation frames,
front and back) and only replace the palette with an Origin Forme colour scheme:
  Dialga: dark indigo / steel body, glowing cyan lines, silver plating, blue diamond, red eyes
  Palkia: pearly white body, deep violet stripes, pink pearls, red eyes
shiny.pal is generated from the species' own normal -> shiny change (import_mega_pack.make_shiny).

usage: make_origin_sprites.py [--preview out.png]
writes res/pokemon/{dialga,palkia}/forms/origin/{front,back}.png(.key), normal.pal, shiny.pal
"""
import argparse
import shutil
from pathlib import Path

from PIL import Image

from import_mega_pack import make_shiny, read_jasc, write_jasc

ROOT = Path(__file__).resolve().parents[2]

# index -> new colour (indexes not listed keep the vanilla colour)
ORIGIN = {
    'dialga': {
        1: (120, 232, 248),   # light blue highlight -> cyan glow
        2: (72, 152, 208),    # mid blue -> steel blue
        4: (64, 216, 248),    # bright blue -> bright cyan
        5: (56, 88, 160),     # blue -> deep blue
        6: (48, 64, 128),     # deeper blue -> indigo
        7: (32, 40, 96),      # navy -> dark indigo
        8: (16, 24, 64),      # dark navy -> near-black indigo
        10: (232, 240, 248),  # very pale -> silver white
        11: (184, 200, 224),  # grey-blue -> silver
        12: (136, 152, 184),  # steel -> dark silver
        13: (88, 96, 136),    # dark steel -> slate
        15: (64, 96, 160),    # steel blue -> deep steel blue
    },
    'palkia': {
        1: (248, 248, 255),   # body highlight -> pearl white
        2: (232, 224, 248),   # body -> pale pearl lavender
        3: (200, 168, 232),   # lilac -> soft violet
        4: (168, 80, 216),    # purple stripe -> vivid violet
        5: (176, 160, 208),   # grey-purple shade -> lavender shade
        6: (112, 40, 160),    # dark purple -> deep violet
        10: (240, 240, 252),  # pale -> white
        11: (208, 208, 232),  # light grey -> pale lavender grey
    },
}


def recolour(species):
    base = ROOT / 'res/pokemon' / species
    dst = base / 'forms/origin'
    pal = read_jasc(base / 'normal.pal')
    for i, c in ORIGIN[species].items():
        pal[i] = tuple((v >> 3) << 3 | (v >> 5) for v in c)

    for face in ('front', 'back'):
        src = base / f'male_{face}.png'
        img = Image.open(src)
        img.putpalette([v for c in pal for v in c] + [0] * (768 - len(pal) * 3))
        img.save(dst / f'{face}.png', bits=4, transparency=0)
        shutil.copyfile(Path(str(src) + '.key'), dst / f'{face}.png.key')

    write_jasc(dst / 'normal.pal', pal)
    write_jasc(dst / 'shiny.pal', make_shiny(pal, read_jasc(base / 'normal.pal'), read_jasc(base / 'shiny.pal')))
    return dst


def main():
    argp = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argp.add_argument('--preview')
    args = argp.parse_args()

    tiles = []
    for species in ORIGIN:
        dst = recolour(species)
        for face in ('front', 'back'):
            im = Image.open(dst / f'{face}.png').convert('RGBA')
            tiles.append(im)

    if args.preview:
        sheet = Image.new('RGB', (160 * 2 + 8, 80 * 2 + 8), (200, 220, 200))
        for k, im in enumerate(tiles):
            sheet.paste(im.crop((0, 0, 160, 80)).convert('RGB'), ((k % 2) * 168, (k // 2) * 88))
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(args.preview)


if __name__ == '__main__':
    main()
