#!/usr/bin/env python3
"""Rebuild every Mega / Legendary Mega sprite that has a high-resolution source render.

For each form in import_mega_pack.py's MEGA_DATA / LEGENDARY_DATA whose pack folder has a
matching 04_Source_Sheets/<folder>/ (front.png + back.png, or front_back.png), the form's
front.png, back.png, normal.pal and shiny.pal are rebuilt with rebuild_sprite_from_source.py.
The previous files are first copied to tools/mega_pack/_lowres_backup/<species>/<form>/
(only once, so the backup always holds the original pack sprites).

Forms without a source render (the Radical Red pack, the five-Mega pack) are listed and left
alone.

usage: rebuild_mega_sprites.py [names...]   (default: every form)
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

from import_mega_pack import LEGENDARY_DATA, MEGA_DATA, POKEMON, find_pack_folder, make_shiny, read_jasc, write_jasc
from rebuild_sprite_from_source import enlarge_pixel_art, indexed_frame_rgba, rebuild_mode as rebuild

ROOT = Path(__file__).resolve().parents[2]
BACKUP = ROOT / 'tools/mega_pack/_lowres_backup'
UNSCALED = ROOT / 'tools/mega_pack/_unscaled_backup'  # the 64 px packs' original sprites


def source_images(pack_folder):
    src = pack_folder.parent.parent / '04_Source_Sheets' / pack_folder.name
    if (src / 'front.png').exists() and (src / 'back.png').exists():
        return Image.open(src / 'front.png'), Image.open(src / 'back.png')
    if (src / 'front_back.png').exists():
        return Image.open(src / 'front_back.png'), None
    return None


def rebuild_form(species, folder, front, back, enlarge=False):
    species_dir = POKEMON / species
    dst = species_dir / 'forms' / folder
    backup = BACKUP / species / folder
    if not backup.exists():
        backup.mkdir(parents=True)
        for name in ('front.png', 'back.png', 'normal.pal', 'shiny.pal'):
            if (dst / name).exists():
                shutil.copyfile(dst / name, backup / name)

    images, pal = enlarge_pixel_art(front, back, species_dir) if enlarge else rebuild(front, back, species_dir)
    for face, img in images.items():
        img.save(dst / f'{face}.png', bits=4, transparency=0)
    write_jasc(dst / 'normal.pal', pal)
    write_jasc(dst / 'shiny.pal', make_shiny(pal, read_jasc(species_dir / 'normal.pal'), read_jasc(species_dir / 'shiny.pal')))


def main():
    names = set(sys.argv[1:])
    skipped = []
    for kind, table in (('mega', MEGA_DATA), ('legendary', LEGENDARY_DATA)):
        for name, forms in table.items():
            if names and name not in names:
                continue
            for number, suffix, *_ in forms:
                folder = f'{kind}_{number}'
                sources = source_images(find_pack_folder(name, suffix))
                if sources is None:
                    # Native 64 px pixel art: enlarge it (Scale2x x2 + mode reduction) to fill the
                    # frame like a Gen 4 sprite, from the untouched original
                    orig = UNSCALED / name.lower() / folder
                    if not (orig / 'front.png').exists():
                        orig = BACKUP / name.lower() / folder
                    if not (orig / 'front.png').exists():
                        orig = POKEMON / name.lower() / 'forms' / folder
                    rebuild_form(name.lower(), folder, indexed_frame_rgba(orig / 'front.png'),
                                 indexed_frame_rgba(orig / 'back.png'), enlarge=True)
                    skipped.append(f'{name} {folder} ({suffix}): enlarged from {orig.relative_to(ROOT)}')
                    continue
                rebuild_form(name.lower(), folder, *sources)
                print(f'{name} {folder}: rebuilt')

    if skipped:
        print('\nno source render (native pixel art, enlarged):')
        for s in skipped:
            print('  ' + s)


if __name__ == '__main__':
    main()
