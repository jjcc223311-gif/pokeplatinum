#!/usr/bin/env python3
"""Tables for the Legendary Pokédex (forms page, Mega / Types / Abilities sections).

Writes:
  include/data/legdex_tables.h     extra forms (forms page), Mega list, type chart, ability holders
  res/text/legdex_sections.json    the sections' text, plus a label for every extra form
Re-run after changing species abilities, forms, Megas or the type chart.
usage: make_legdex_tables.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POKEMON = ROOT / 'res' / 'pokemon'

SPECIES = [l.strip() for l in (ROOT / 'generated' / 'species.txt').read_text().splitlines()]
ABILITIES = [l.strip() for l in (ROOT / 'generated' / 'abilities.txt').read_text().splitlines()]
TYPES = [l.strip() for l in (ROOT / 'generated' / 'pokemon_types.txt').read_text().splitlines()]
NATDEX = 649
MEGA_FORMS = [('mega_1', 'FORM_MEGA_1'), ('mega_2', 'FORM_MEGA_2'),
              ('legendary_mega_1', 'FORM_LEGENDARY_MEGA_1'), ('legendary_mega_2', 'FORM_LEGENDARY_MEGA_2')]

# Forms page: (species, [(form, label), ...]) for species shown with the generic "forms" layout
TYPE_LABELS = ['NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL', None,
               'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK', None, 'LIGHT']
EXTRA_FORMS = [
    ('CASTFORM', [(0, 'NORMAL FORM'), (1, 'SUNNY FORM'), (2, 'RAINY FORM'), (3, 'SNOWY FORM')]),
    ('CHERRIM', [(0, 'OVERCAST FORM'), (1, 'SUNSHINE FORM')]),
    ('DIALGA', [(0, 'NORMAL FORME'), (1, 'ORIGIN FORME')]),
    ('PALKIA', [(0, 'NORMAL FORME'), (1, 'ORIGIN FORME')]),
    ('ARCEUS', [(t, f'{n} TYPE') for t, n in enumerate(TYPE_LABELS) if n]),
    ('BASCULIN', [(0, 'RED-STRIPED'), (1, 'BLUE-STRIPED')]),
    ('DARMANITAN', [(0, 'STANDARD MODE'), (1, 'ZEN MODE')]),
    ('DEERLING', [(0, 'SPRING FORM'), (1, 'SUMMER FORM'), (2, 'AUTUMN FORM'), (3, 'WINTER FORM')]),
    ('SAWSBUCK', [(0, 'SPRING FORM'), (1, 'SUMMER FORM'), (2, 'AUTUMN FORM'), (3, 'WINTER FORM')]),
    ('TORNADUS', [(0, 'INCARNATE FORME'), (1, 'THERIAN FORME')]),
    ('THUNDURUS', [(0, 'INCARNATE FORME'), (1, 'THERIAN FORME')]),
    ('LANDORUS', [(0, 'INCARNATE FORME'), (1, 'THERIAN FORME')]),
    ('KYUREM', [(0, 'KYUREM'), (1, 'BLACK KYUREM'), (2, 'WHITE KYUREM')]),
    ('KELDEO', [(0, 'ORDINARY FORM'), (1, 'RESOLUTE FORM')]),
    ('MELOETTA', [(0, 'ARIA FORME'), (1, 'PIROUETTE FORME')]),
    ('GENESECT', [(0, 'NO DRIVE'), (1, 'DOUSE DRIVE'), (2, 'SHOCK DRIVE'), (3, 'BURN DRIVE'), (4, 'CHILL DRIVE')]),
]

# Text of the sections. (id suffix, text)
UI = [
    ('Title', 'LEGENDARY POKéDEX'),
    ('TabPokemon', 'POKéMON'),
    ('TabMega', 'MEGA'),
    ('TabTypes', 'TYPES'),
    ('TabAbilities', 'ABILITIES'),
    ('PokemonList', 'POKéMON LIST'),
    ('HomeInfo', ['Every Pokémon from BULBASAUR to\n', 'GENESECT, with all of their forms,\n',
                  'in your father’s order.']),
    ('HomeOpen', 'Press A to open the Pokémon list.'),
    ('HomeSections', ['Press L or R for the Mega Evolution,\n', 'Type and Ability sections.']),
    ('HomeCountSpecies', 'Pokémon: '),
    ('HomeCountMegas', 'Megas: '),
    ('HomeCountTypes', 'Types: '),
    ('HomeCountAbilities', 'Abilities: '),
    ('FooterHome', 'L/R: Section  A: Open  B: Exit'),
    ('FooterList', 'L/R: Section  +: Move  B: Exit'),
    ('FooterAbilities', 'L/R: Section  A: More  B: Exit'),
    ('MegaPrefix', 'MEGA '),
    ('LegendaryPrefix', 'LEG. MEGA '),
    ('LegendaryTitlePrefix', 'LEGENDARY MEGA '),
    ('SecondSuffix', ' 2'),
    ('Unknown', '???'),
    ('NotCaught', ['Catch this Pokémon to see\n', 'its Mega Evolution.']),
    ('Type', 'Type'),
    ('BaseStats', 'Base stats'),
    ('StatHP', 'HP'),
    ('StatAtk', 'Atk'),
    ('StatDef', 'Def'),
    ('StatSpA', 'SpA'),
    ('StatSpD', 'SpD'),
    ('StatSpe', 'Spe'),
    ('StatTotal', 'Total'),
    ('Ability', 'Ability'),
    ('HowToGet', 'How to get'),
    ('HowMega1', ['Mega Ring. Press MEGA in battle.']),
    ('HowMega2', ['Mega Ring, holding a Mega Rock.']),
    ('HowLegendary1', ['Legend Necklace. Press LEGENDARY.']),
    ('HowLegendary2', ['Legend Necklace, holding a Mega Rock.']),
    ('Attacking', 'ATTACKING'),
    ('Defending', 'DEFENDING'),
    ('SuperEffective', 'x2  '),
    ('NotVeryEffective', 'x0.5  '),
    ('NoEffect', 'x0  '),
    ('None', '-'),
    ('Separator', ', '),
    ('HoldersTitle', 'Pokémon with this Ability:'),
    ('NoHolders', 'No Pokémon have this Ability.'),
    ('MoreHolders', '(A: more)'),
    ('SuffixMega1', ' (MEGA)'),
    ('SuffixMega2', ' (MEGA 2)'),
    ('SuffixLegendary1', ' (LEG. MEGA)'),
    ('SuffixLegendary2', ' (LEG. MEGA 2)'),
    ('OpenParen', ' ('),
    ('CloseParen', ')'),
]


def species_dir(const):
    return const.replace('SPECIES_', '').lower()


def label_id(text):
    return 'LegDexSections_Text_Form' + re.sub(r'[^A-Za-z0-9]', '', text.title())


def main():
    messages = [{'id': f'LegDexSections_Text_{k}', 'en_US': v} for k, v in UI]
    labels = {}
    for _, forms in EXTRA_FORMS:
        for _, text in forms:
            if text not in labels:
                labels[text] = label_id(text)
                messages.append({'id': labels[text], 'en_US': text})
    bank = {'key': 47103, 'messages': messages}
    (ROOT / 'res' / 'text' / 'legdex_sections.json').write_text(json.dumps(bank, indent=2, ensure_ascii=False) + '\n')

    out = ['#ifndef POKEPLATINUM_DATA_LEGDEX_TABLES_H', '#define POKEPLATINUM_DATA_LEGDEX_TABLES_H', '',
           '// Generated by tools/scripts/make_legdex_tables.py: data for the Legendary Pokédex.', '',
           '#include "constants/battle.h"', '#include "constants/forms.h"', '#include "constants/species.h"',
           '#include "generated/abilities.h"', '#include "generated/pokemon_types.h"', '',
           '#include "res/text/bank/legdex_sections.h"', '',
           'typedef struct LegDexForm {', '    u16 species;', '    u8 form;', '    u16 label; // legdex_sections entry', '} LegDexForm;', '',
           'typedef struct LegDexSpeciesForm {', '    u16 species;', '    u8 form;', '} LegDexSpeciesForm;', '']

    # Extra forms (forms page)
    out.append('// Forms page: species shown with every form listed here, in this order')
    out.append('static const LegDexForm sLegDexExtraForms[] = {')
    for sp, forms in EXTRA_FORMS:
        for form, text in forms:
            out.append(f'    {{ SPECIES_{sp}, {form}, {labels[text]} }},')
    out += ['};', '']

    # Megas, in National Dex order
    megas = []
    for row in json.loads((POKEMON / 'mega_forms.json').read_text()):
        for key, form in MEGA_FORMS:
            if key in row:
                megas.append((SPECIES.index(row['species']), row['species'], form, row[key]))
    megas.sort(key=lambda m: (m[0], [f for _, f in MEGA_FORMS].index(m[2])))
    out.append('// Mega section: every Mega / Legendary Mega, in National Dex order')
    out.append('static const LegDexSpeciesForm sLegDexMegas[] = {')
    out += [f'    {{ {sp}, {form} }},' for _, sp, form, _ in megas]
    out += ['};', '']

    # Type chart
    src = (ROOT / 'src' / 'battle' / 'battle_lib.c').read_text()
    table = src[src.index('static const u8 sTypeMatchupMultipliers[][3] = {'):]
    table = table[:table.index('};')]
    chart = re.findall(r'\{\s*(TYPE_[A-Z]+),\s*(TYPE_[A-Z]+),\s*(TYPE_MULTI_[A-Z_]+)\s*\}', table)
    out.append('// Types section: copy of the battle type chart (attacking type, defending type, multiplier x10)')
    out.append('static const u8 sLegDexTypeChart[][3] = {')
    out += [f'    {{ {a}, {d}, {m} }},' for a, d, m in chart]
    out += ['};', '']

    # Ability holders
    holders = {a: [] for a in ABILITIES}
    for i, const in enumerate(SPECIES[1:NATDEX + 1], start=1):
        base = json.loads((POKEMON / species_dir(const) / 'data.json').read_text())['abilities']
        for a in dict.fromkeys(base):
            if a != 'ABILITY_NONE':
                holders[a].append((i, const, '0'))
        for row in json.loads((POKEMON / 'extra_forms.json').read_text()):
            if row['species'] == const and row['has_data']:
                fa = json.loads((POKEMON / row['dir'] / 'data.json').read_text())['abilities']
                for a in dict.fromkeys(fa):
                    if a != 'ABILITY_NONE' and a not in base:
                        holders[a].append((i, const, str(row['form'])))
    for i, const, form, d in megas:
        fa = json.loads((POKEMON / d / 'data.json').read_text())['abilities']
        for a in dict.fromkeys(fa):
            if a != 'ABILITY_NONE':
                holders[a].append((i, const, form))
    out.append('// Abilities section: who has each Ability (base forms, forms with other Abilities, Megas)')
    out.append('static const LegDexSpeciesForm sLegDexAbilityHolders[] = {')
    starts, n = [], 0
    for a in ABILITIES:
        starts.append(n)
        for _, const, form in sorted(holders[a], key=lambda h: h[0]):
            out.append(f'    {{ {const}, {form} }}, // {a}')
            n += 1
    starts.append(n)
    out += ['};', '', f'#define LEGDEX_NUM_ABILITIES {len(ABILITIES)}', '',
            '// sLegDexAbilityHolders[sLegDexAbilityHolderStart[a] .. sLegDexAbilityHolderStart[a + 1] - 1]',
            'static const u16 sLegDexAbilityHolderStart[LEGDEX_NUM_ABILITIES + 1] = {']
    out += [f'    {s},' for s in starts]
    out += ['};', '', '#endif // POKEPLATINUM_DATA_LEGDEX_TABLES_H', '']
    (ROOT / 'include' / 'data' / 'legdex_tables.h').write_text('\n'.join(out))
    print(f'{len(megas)} Megas, {len(chart)} type chart entries, {n} ability holders, {len(labels)} form labels')


if __name__ == '__main__':
    main()
