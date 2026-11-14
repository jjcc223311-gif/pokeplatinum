#!/usr/bin/env python3
"""Placeholder footprints for the Gen 5 species: each copies the footprint (picture, size, type and
whether it has one) of the vanilla Pokémon (#1-493) with the same body shape and the closest height.
usage: set_gen5_footprints.py
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POKEMON = ROOT / 'res' / 'pokemon'


def main():
    species = [l.strip().replace('SPECIES_', '').lower() for l in (ROOT / 'generated' / 'species.txt').read_text().splitlines()]
    vanilla = []
    for name in species[1:494]:
        d = json.loads((POKEMON / name / 'data.json').read_text())
        vanilla.append((name, d['pokedex_data']['body_shape'], d['pokedex_data']['height_inches'], d['footprint']))
    report = []
    for name in species[494:650]:
        p = POKEMON / name / 'data.json'
        d = json.loads(p.read_text())
        shape, height = d['pokedex_data']['body_shape'], d['pokedex_data']['height_inches']
        same = [v for v in vanilla if v[1] == shape] or vanilla
        src, _, _, footprint = min(same, key=lambda v: (abs(v[2] - height), v[0]))
        d['footprint'] = dict(footprint)
        shutil.copyfile(POKEMON / src / 'footprint.png', POKEMON / name / 'footprint.png')
        p.write_text(json.dumps(d, indent=4, ensure_ascii=False) + '\n')
        report.append(f'{name}: {src}')
    out = ROOT / 'tools' / 'gen5_pack' / 'gen5_footprints.txt'
    out.write_text('Placeholder footprints (Gen 5 species: copied from)\n' + '\n'.join(report) + '\n')
    print(len(report), 'footprints;', out)


if __name__ == '__main__':
    main()
