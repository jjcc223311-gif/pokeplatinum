#!/usr/bin/env python3
"""Add the Gen 5 alternate forms to res/pokemon/<species>/forms/<name>/ and res/pokemon/extra_forms.json.

Sprites come from tools/gen5_pack/pokemon_sprites/sheets/{normal,shiny}/{front,back}/<dex>-<Name>-<Form>.png.
Forms with their own stats / types / abilities get a data.json (copied from the base species with
those fields replaced); cosmetic forms only get sprites ("has_data": false).
usage: add_gen5_forms.py   (run with a Python that has Pillow)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'scripts'))
from import_gen5_species import copy_sheet, write_pal  # noqa: E402

POKEMON = ROOT / 'res' / 'pokemon'
SHEETS = ROOT / 'tools' / 'gen5_pack' / 'pokemon_sprites' / 'sheets'


def stats(hp, atk, df, spe, spa, spd):
    return {'hp': hp, 'attack': atk, 'defense': df, 'speed': spe, 'special_attack': spa, 'special_defense': spd}


# (species dir, form number, folder, sheet name, data overrides or None for a cosmetic form)
FORMS = [
    ('basculin', 1, 'blue_striped', '550-Basculin-Blue-Striped',
     {'abilities': ['ABILITY_ROCK_HEAD', 'ABILITY_ADAPTABILITY']}),
    ('darmanitan', 1, 'zen', '555-Darmanitan-Zen',
     {'base_stats': stats(105, 30, 105, 55, 140, 105), 'types': ['TYPE_FIRE', 'TYPE_PSYCHIC']}),
    ('deerling', 1, 'summer', '585-Deerling-Summer', None),
    ('deerling', 2, 'autumn', '585-Deerling-Autumn', None),
    ('deerling', 3, 'winter', '585-Deerling-Winter', None),
    ('sawsbuck', 1, 'summer', '586-Sawsbuck-Summer', None),
    ('sawsbuck', 2, 'autumn', '586-Sawsbuck-Autumn', None),
    ('sawsbuck', 3, 'winter', '586-Sawsbuck-Winter', None),
    ('tornadus', 1, 'therian', '641-Tornadus-Therian',
     {'base_stats': stats(79, 100, 80, 121, 110, 90), 'types': ['TYPE_FLYING', 'TYPE_FLYING'],
      'abilities': ['ABILITY_REGENERATOR', 'ABILITY_NONE']}),
    ('thundurus', 1, 'therian', '642-Thundurus-Therian',
     {'base_stats': stats(79, 105, 70, 101, 145, 80), 'types': ['TYPE_ELECTRIC', 'TYPE_FLYING'],
      'abilities': ['ABILITY_VOLT_ABSORB', 'ABILITY_NONE']}),
    ('landorus', 1, 'therian', '645-Landorus-Therian',
     {'base_stats': stats(89, 145, 90, 91, 105, 80), 'types': ['TYPE_GROUND', 'TYPE_FLYING'],
      'abilities': ['ABILITY_INTIMIDATE', 'ABILITY_NONE']}),
    ('keldeo', 1, 'resolute', '647-Keldeo-Resolute', None),
    ('meloetta', 1, 'pirouette', '648-Meloetta-Pirouette',
     {'base_stats': stats(100, 128, 90, 128, 77, 77), 'types': ['TYPE_NORMAL', 'TYPE_FIGHTING']}),
    ('genesect', 1, 'douse_drive', '649-Genesect-Douse-Drive', None),
    ('genesect', 2, 'shock_drive', '649-Genesect-Shock-Drive', None),
    ('genesect', 3, 'burn_drive', '649-Genesect-Burn-Drive', None),
    ('genesect', 4, 'chill_drive', '649-Genesect-Chill-Drive', None),
]

# Abilities given to the base form (Darmanitan's second slot = Zen Mode, so Zen Forme is reachable)
BASE_ABILITY_CHANGES = {'darmanitan': ['ABILITY_SHEER_FORCE', 'ABILITY_ZEN_MODE']}


def form_data(species, overrides):
    base = json.loads((POKEMON / species / 'data.json').read_text())
    out = {}
    for k, v in base.items():
        out[k] = v
        if k == 'learnset':
            break
    out['evolutions'] = []
    out.update(overrides)
    return out


def main():
    extra_path = POKEMON / 'extra_forms.json'
    extra = json.loads(extra_path.read_text())
    have = {(e['species'], e['form']) for e in extra}
    for species, form, folder, sheet, overrides in FORMS:
        d = POKEMON / species / 'forms' / folder
        d.mkdir(parents=True, exist_ok=True)
        for face in ('front', 'back'):
            pal = copy_sheet(SHEETS / 'normal' / face / f'{sheet}.png', d / f'{face}.png')
            if face == 'front':
                write_pal(d / 'normal.pal', pal)
        for face in ('front', 'back'):  # scan keys, as for Kyurem's forms
            key = POKEMON / species / f'male_{face}.png.key'
            (d / f'{face}.png.key').write_bytes(key.read_bytes())
        shiny = copy_sheet(SHEETS / 'shiny' / 'front' / f'{sheet}.png', d / '_shiny_tmp.png')
        (d / '_shiny_tmp.png').unlink()
        write_pal(d / 'shiny.pal', shiny)
        if overrides is not None:
            data = form_data(species, overrides)
            (d / 'data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')
        key = (f'SPECIES_{species.upper()}', form)
        if key not in have:
            extra.append({'species': key[0], 'form': form, 'dir': f'{species}/forms/{folder}',
                          'has_data': overrides is not None})
            have.add(key)
        print(f'{species} form {form} ({folder}) {"data + sprites" if overrides else "sprites"}')
    extra_path.write_text(json.dumps(extra, indent=4) + '\n')

    for species, abilities in BASE_ABILITY_CHANGES.items():
        p = POKEMON / species / 'data.json'
        data = json.loads(p.read_text())
        data['abilities'] = abilities
        p.write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
