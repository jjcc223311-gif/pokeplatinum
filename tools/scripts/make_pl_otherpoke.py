#!/usr/bin/env python3

import argparse
import json
import pathlib
import subprocess

argparser = argparse.ArgumentParser(
    prog='pl_poke_icon.narc packer',
    description='Packs the archive containing Pokemon icons'
)
argparser.add_argument('-n', '--nitrogfx',
                       required=True,
                       help='Path to nitrogfx executable')
argparser.add_argument('-k', '--narc',
                       required=True,
                       help='Path to narc executable')
argparser.add_argument('-p', '--private-dir',
                       required=True,
                       help='Path to the private directory (where binaries will be made)')
argparser.add_argument('-o', '--output-dir',
                       required=True,
                       help='Path to the output directory (where the NARC will be made)')
argparser.add_argument('-se', '--sprite-entries',
                       required=True, type=int,
                       help='Number of entries to interpret from the list as NCGR-sources')
argparser.add_argument('-pe', '--palette-entries',
                       required=True, type=int,
                       help='Number of entries to interpret from the list as NCLR-sources')
argparser.add_argument('-m', '--mega-forms',
                       required=True,
                       help='Path to mega_forms.json (Mega / Legendary Mega form table)')
argparser.add_argument('-x', '--extra-forms',
                       required=True,
                       help='Path to extra_forms.json (non-Mega forms with appended sprites)')
argparser.add_argument('-d', '--pokemon-dir',
                       required=True,
                       help='Path to res/pokemon (mega_forms.json form directories are relative to it)')
argparser.add_argument('--depfile',
                       required=True,
                       help='Path to write a Makefile-style depfile listing the Mega sprite sources')
argparser.add_argument('files',
                       nargs='+',
                       help='List of files to process in-order')
args = argparser.parse_args()

private_dir = pathlib.Path(args.private_dir)
output_dir = pathlib.Path(args.output_dir)

private_dir.mkdir(parents=True, exist_ok=True)

# Mega / Legendary Mega sprites go after every other member (Substitute is the last numbered
# one), so no vanilla index moves. Each form takes 4 members, in mega_forms.json order:
# back sprite, front sprite, normal palette, shiny palette. speciesproc numbers them the same way.
mega_base = args.sprite_entries + args.palette_entries + 3
mega_dirs = []
# Extra forms first, then Megas: speciesproc numbers them in the same order
with open(args.extra_forms, 'r', encoding='utf-8') as f:
    for entry in json.load(f):
        mega_dirs.append(pathlib.Path(args.pokemon_dir) / entry['dir'])
with open(args.mega_forms, 'r', encoding='utf-8') as f:
    for entry in json.load(f):
        # enum MegaSlot order (forms 29, 28, 30, 31), the same order speciesproc numbers them in
        for key in ('mega_1', 'mega_2', 'legendary_mega_1', 'legendary_mega_2'):
            if entry.get(key):
                mega_dirs.append(pathlib.Path(args.pokemon_dir) / entry[key])

mega_sources = []
for d in mega_dirs:
    mega_sources += [d / 'back.png', d / 'front.png', d / 'normal.pal', d / 'shiny.pal']

# Members left over from a longer Mega list would otherwise still be packed
mega_end = mega_base + len(mega_sources)
for stale in private_dir.glob('pl_otherpoke_*.N*'):
    if int(stale.stem.split('_')[-1]) >= mega_end:
        stale.unlink()

for k, source in enumerate(mega_sources):
    if source.suffix == '.png':
        subprocess.run([args.nitrogfx, source, private_dir / f'pl_otherpoke_{mega_base + k:04}.NCGR',
                        '-encodefronttoback', '-scan'], check=True)
    else:
        subprocess.run([args.nitrogfx, source, private_dir / f'pl_otherpoke_{mega_base + k:04}.NCLR',
                        '-bitdepth', '8', '-nopad', '-comp', '10'], check=True)

with open(args.depfile, 'w', encoding='utf-8') as f:
    deps = [str(p) for p in mega_sources] + [str(pathlib.Path(str(p) + '.key')) for p in mega_sources if p.suffix == '.png' and pathlib.Path(str(p) + '.key').exists()]
    f.write(str(pathlib.Path(args.output_dir) / 'pl_otherpoke.narc') + ': ' + ' '.join(deps) + '\n')

# The first batch of files should all be sprites
for i in range(args.sprite_entries):
    infile = args.files[i]
    target = private_dir / f'pl_otherpoke_{i:04}.NCGR'
    subprocess.run([
        args.nitrogfx,
        infile,
        target,
        '-encodefronttoback',
        '-scan',
    ])

# The next batch of files should all be palettes
for i in range(args.sprite_entries, args.sprite_entries + args.palette_entries):
    infile = args.files[i]
    target = private_dir / f'pl_otherpoke_{i:04}.NCLR'
    subprocess.run([
        args.nitrogfx,
        infile,
        target,
        '-bitdepth', '8',
        '-nopad',
        '-comp', '10'
    ])

# The last five entries are the Substitute sprite and in-battle shadows
sub_back = args.files[-5]
sub_front = args.files[-4]
sub_pal = args.files[-3]
shadows = args.files[-2]
shadows_pal = args.files[-1]
i = args.sprite_entries + args.palette_entries

subprocess.run([
    args.nitrogfx,
    sub_back,
    private_dir / f'pl_otherpoke_{i:04}.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    sub_front,
    private_dir / f'pl_otherpoke_{(i+1):04}.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    sub_pal,
    private_dir / f'pl_otherpoke_{(i+2):04}.NCLR',
    '-bitdepth', '8',
    '-nopad',
    '-comp', '10'
])
subprocess.run([
    args.nitrogfx,
    shadows,
    private_dir / f'pokemon_shadows.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    shadows_pal,
    private_dir / f'pokemon_shadows_pal.NCLR',
    '-bitdepth', '8',
    '-nopad',
    '-comp', '10'
])

subprocess.run([
    args.narc,
    '--create',
    '--index',
    '--file', output_dir / 'pl_otherpoke.narc',
    private_dir
])
