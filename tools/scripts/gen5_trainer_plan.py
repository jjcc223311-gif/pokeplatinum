#!/usr/bin/env python3
"""Phase 6: give every trainer team a Gen 1-5 mix (with at least one Gen 5 Pokemon); the ace stays.

usage: gen5_trainer_plan.py [--apply]
  writes tools/gen5_pack/PHASE6_TRAINER_PLAN.md (and with --apply, res/trainers/data/*.json)

Rules (from the spec):
  - ace = highest level (ties: the last one); Barry's ace is his starter line; a team that is only
    its ace is unchanged
  - team size stays; about half of the non-ace Pokemon are replaced (at least one, and one of the
    replacements is always Gen 5); the rest stay as they were
  - replacements fit the trainer class's types, keep the replaced Pokemon's level, held item (unless
    species-specific) and gain level-up moves if the trainer uses custom moves
  - evolution stage from the level (level evolutions at their level, stone / trade / friendship
    evolutions from Lv 30)
  - no legendaries / mythicals; starters and pseudo-legendaries only for strong classes
  - the same trainer (rematches, every Barry battle) always maps an original family to the same
    replacement family, so his Pokemon grow / evolve between battles
  - Gym Leaders after Roark, the Elite Four and the Champion prefer Mega-capable replacements
"""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAINERS = ROOT / 'res' / 'trainers' / 'data'
POKEMON = ROOT / 'res' / 'pokemon'
MAPS = ROOT / 'res' / 'field' / 'maps'
SPECIES = (ROOT / 'generated' / 'species.txt').read_text().split()
SKIP = {'lass_sarah'}  # Phase 1A TEMP TEST trainer (Charizard)

LEGENDARY = set('''ARTICUNO ZAPDOS MOLTRES MEWTWO MEW RAIKOU ENTEI SUICUNE LUGIA HO_OH CELEBI REGIROCK REGICE REGISTEEL
LATIAS LATIOS KYOGRE GROUDON RAYQUAZA JIRACHI DEOXYS UXIE MESPRIT AZELF DIALGA PALKIA HEATRAN REGIGIGAS GIRATINA
CRESSELIA PHIONE MANAPHY DARKRAI SHAYMIN ARCEUS VICTINI COBALION TERRAKION VIRIZION TORNADUS THUNDURUS RESHIRAM
ZEKROM LANDORUS KYUREM KELDEO MELOETTA GENESECT'''.split())
STARTERS = set('''BULBASAUR CHARMANDER SQUIRTLE CHIKORITA CYNDAQUIL TOTODILE TREECKO TORCHIC MUDKIP TURTWIG CHIMCHAR PIPLUP
SNIVY TEPIG OSHAWOTT'''.split())
PSEUDO = set('DRATINI LARVITAR BAGON BELDUM GIBLE DEINO AXEW LARVESTA'.split())
EXCLUDE = set('UNOWN DITTO SMEARGLE SHEDINJA MAGIKARP FEEBAS WURMPLE KRICKETOT BURMY COMBEE SPINDA CASTFORM'.split())
STRONG = {'ACE_TRAINER_FEMALE', 'ACE_TRAINER_MALE', 'ACE_TRAINER_SNOW_FEMALE', 'ACE_TRAINER_SNOW_MALE', 'VETERAN',
          'DRAGON_TAMER', 'CHAMPION_CYNTHIA', 'RIVAL', 'ELITE_FOUR_AARON', 'ELITE_FOUR_BERTHA', 'ELITE_FOUR_FLINT',
          'ELITE_FOUR_LUCIAN', 'FACTORY_HEAD', 'HALL_MATRON', 'ARCADE_STAR', 'CASTLE_VALET', 'TOWER_TYCOON',
          'DP_PLAYER_MALE', 'DP_PLAYER_FEMALE', 'GALACTIC_BOSS'}
MEGA_PREF = {'LEADER_GARDENIA', 'LEADER_FANTINA', 'LEADER_MAYLENE', 'LEADER_WAKE', 'LEADER_BYRON', 'LEADER_CANDICE',
             'LEADER_VOLKNER', 'ELITE_FOUR_AARON', 'ELITE_FOUR_BERTHA', 'ELITE_FOUR_FLINT', 'ELITE_FOUR_LUCIAN',
             'CHAMPION_CYNTHIA'}
SPECIFIC_ITEMS = {'ITEM_LIGHT_BALL', 'ITEM_THICK_CLUB', 'ITEM_LUCKY_PUNCH', 'ITEM_STICK', 'ITEM_METAL_POWDER',
                  'ITEM_QUICK_POWDER', 'ITEM_DEEPSEATOOTH', 'ITEM_DEEPSEASCALE', 'ITEM_SOUL_DEW', 'ITEM_ADAMANT_ORB',
                  'ITEM_LUSTROUS_ORB', 'ITEM_GRISEOUS_ORB'}
ANY = None
THEMES = {
    'ACE_TRAINER_FEMALE': ANY, 'ACE_TRAINER_MALE': ANY, 'VETERAN': ANY, 'RICH_BOY': ANY, 'DOUBLE_TEAM': ANY,
    'ACE_TRAINER_SNOW_FEMALE': ['ICE', 'WATER', 'NORMAL'], 'ACE_TRAINER_SNOW_MALE': ['ICE', 'WATER', 'FIGHTING'],
    'AROMA_LADY': ['GRASS'], 'ARTIST': ['NORMAL', 'PSYCHIC'], 'BATTLE_GIRL': ['FIGHTING'],
    'BEAUTY': ['WATER', 'NORMAL', 'GRASS', 'PSYCHIC', 'FAIRY'], 'BELLE_AND_PA': ['NORMAL', 'FAIRY'],
    'BIRD_KEEPER': ['FLYING'], 'BLACK_BELT': ['FIGHTING'], 'BREEDER_FEMALE': ['NORMAL', 'FAIRY', 'WATER'],
    'BREEDER_MALE': ['NORMAL', 'GRASS', 'FIRE'], 'BUG_CATCHER': ['BUG'], 'CAMERAMAN': ['NORMAL', 'ELECTRIC'],
    'CAMPER': ['GROUND', 'ROCK', 'NORMAL', 'FIRE', 'BUG'], 'CLOWN': ['PSYCHIC', 'NORMAL'],
    'COLLECTOR': ['NORMAL', 'GHOST', 'POISON', 'ROCK'], 'COWGIRL': ['NORMAL', 'GROUND'], 'RANCHER': ['NORMAL', 'GROUND'],
    'CYCLIST_FEMALE': ['NORMAL', 'ELECTRIC', 'FLYING'], 'CYCLIST_MALE': ['NORMAL', 'ELECTRIC', 'FIGHTING'],
    'DRAGON_TAMER': ['DRAGON'], 'FISHERMAN': ['WATER'], 'GENTLEMAN': ['NORMAL', 'FIRE'],
    'GUITARIST': ['ELECTRIC', 'POISON', 'NORMAL'], 'HIKER': ['ROCK', 'GROUND'], 'IDOL': ['NORMAL', 'FAIRY', 'ELECTRIC'],
    'INTERVIEWERS': ['NORMAL', 'ELECTRIC'], 'JOGGER': ['NORMAL', 'FIGHTING'], 'LADY': ['NORMAL', 'FAIRY'],
    'LASS': ['NORMAL', 'GRASS', 'FAIRY'], 'MAID': ['NORMAL', 'PSYCHIC'], 'NINJA_BOY': ['POISON', 'BUG', 'DARK', 'GHOST'],
    'PARASOL_LADY': ['WATER', 'GRASS'], 'PI': ['DARK', 'PSYCHIC'], 'PICNICKER': ['GRASS', 'NORMAL', 'BUG'],
    'POKEFAN_FEMALE': ['NORMAL', 'ELECTRIC', 'FAIRY'], 'POKEFAN_MALE': ['NORMAL', 'ELECTRIC', 'FAIRY'],
    'POKE_KID': ['NORMAL', 'ELECTRIC', 'FAIRY'], 'POLICEMAN': ['NORMAL', 'FIRE', 'FIGHTING'], 'PSYCHIC_FEMALE': ['PSYCHIC'],
    'PSYCHIC_MALE': ['PSYCHIC'], 'RANGER_FEMALE': ['GRASS', 'BUG', 'NORMAL', 'FLYING'],
    'RANGER_MALE': ['GRASS', 'BUG', 'NORMAL', 'FLYING'], 'REPORTER': ['NORMAL', 'ELECTRIC'], 'ROUGHNECK': ['DARK', 'POISON'],
    'RUIN_MANIAC': ['ROCK', 'GROUND'], 'SAILOR': ['WATER', 'FIGHTING'], 'SCHOOL_KID_FEMALE': ['NORMAL', 'GRASS', 'ELECTRIC'],
    'SCHOOL_KID_MALE': ['NORMAL', 'GRASS', 'ELECTRIC'], 'SCIENTIST': ['ELECTRIC', 'POISON', 'STEEL', 'PSYCHIC'],
    'SIS_AND_BRO': ['NORMAL', 'WATER'], 'TWINS': ['NORMAL', 'FAIRY'], 'YOUNG_COUPLE': ['NORMAL', 'FAIRY', 'GRASS'],
    'SKIER_FEMALE': ['ICE'], 'SKIER_MALE': ['ICE'], 'SOCIALITE': ['NORMAL', 'FAIRY', 'PSYCHIC'],
    'SWIMMER_FEMALE': ['WATER'], 'SWIMMER_MALE': ['WATER'], 'TUBER_FEMALE': ['WATER'], 'TUBER_MALE': ['WATER'],
    'WAITER': ['NORMAL', 'FIRE'], 'WAITRESS': ['NORMAL', 'FIRE'], 'WORKER': ['STEEL', 'FIGHTING', 'ROCK', 'ELECTRIC'],
    'YOUNGSTER': ['NORMAL', 'BUG', 'FLYING'],
    'GALACTIC_GRUNT_MALE': ['POISON', 'DARK'], 'GALACTIC_GRUNT_FEMALE': ['POISON', 'DARK'],
    'COMMANDER_MARS': ['NORMAL', 'STEEL', 'PSYCHIC'], 'COMMANDER_JUPITER': ['POISON', 'DARK'],
    'COMMANDER_SATURN': ['POISON', 'FIGHTING'], 'GALACTIC_BOSS': ['DARK', 'ICE', 'FLYING'],
    'LEADER_ROARK': ['ROCK'], 'LEADER_GARDENIA': ['GRASS'], 'LEADER_FANTINA': ['GHOST'], 'LEADER_MAYLENE': ['FIGHTING'],
    'LEADER_WAKE': ['WATER'], 'LEADER_BYRON': ['STEEL'], 'LEADER_CANDICE': ['ICE'], 'LEADER_VOLKNER': ['ELECTRIC'],
    'ELITE_FOUR_AARON': ['BUG'], 'ELITE_FOUR_BERTHA': ['GROUND'], 'ELITE_FOUR_FLINT': ['FIRE'],
    'ELITE_FOUR_LUCIAN': ['PSYCHIC'], 'CHAMPION_CYNTHIA': ['DRAGON', 'GROUND', 'STEEL', 'WATER', 'PSYCHIC', 'FIGHTING'],
    'RIVAL': ANY, 'DP_PLAYER_MALE': ANY, 'DP_PLAYER_FEMALE': ANY, 'TRAINER_CHERYL': ['NORMAL', 'FAIRY'],
    'TRAINER_MIRA': ['PSYCHIC'], 'TRAINER_RILEY': ['FIGHTING', 'STEEL'], 'TRAINER_MARLEY': ['NORMAL', 'FIRE'],
    'TRAINER_BUCK': ['FIRE', 'GROUND'], 'FACTORY_HEAD': ANY, 'HALL_MATRON': ANY, 'ARCADE_STAR': ANY,
    'CASTLE_VALET': ANY, 'TOWER_TYCOON': ANY,
}

_cache = {}


def data(name):
    if name not in _cache:
        _cache[name] = json.loads((POKEMON / name.lower() / 'data.json').read_text())
    return _cache[name]


def dex(name):
    return SPECIES.index('SPECIES_' + name)


def gen(name):
    i = dex(name)
    return 1 if i <= 151 else 2 if i <= 251 else 3 if i <= 386 else 4 if i <= 493 else 5


def base_of(name):
    return data(name)['offspring'][8:]


def stage_for(base, level):
    cur = base
    while True:
        evos = data(cur)['evolutions']
        if not evos:
            return cur
        method, target = evos[0][0], evos[0][-1][8:]
        if method == 'EVO_LEVEL' and level >= evos[0][1]:
            cur = target
        elif method != 'EVO_LEVEL' and level >= 30:
            cur = target
        else:
            return cur


def family(base):
    out, todo = [], [base]
    while todo:
        s = todo.pop()
        out.append(s)
        todo += [e[-1][8:] for e in data(s)['evolutions']]
    return out


MEGA = {e['species'][8:] for e in json.loads((POKEMON / 'mega_forms.json').read_text())}
BASES = []
for c in SPECIES[1:SPECIES.index('SPECIES_EGG')]:
    n = c[8:]
    if base_of(n) == n and n not in LEGENDARY and n not in EXCLUDE and gen(n) != 4:
        BASES.append(n)


def candidates(cls, level, strong):
    theme = THEMES.get(cls, ANY)
    out = []
    for b in BASES:
        if (b in STARTERS or b in PSEUDO) and not strong:
            continue
        s = stage_for(b, level)
        types = {t[5:] for t in data(s)['types']}
        if theme is not ANY and not (types & set(theme)):
            continue
        if level >= 30 and data(s)['evolutions'] and dex(s) == dex(b) and family(b)[1:]:
            pass  # unevolved but its evolution isn't reached by level yet: allowed
        out.append((b, s))
    return out


def rng(*parts):
    return int(hashlib.sha1('|'.join(parts).encode()).hexdigest(), 16)


def level_moves(species, level):
    moves = []
    for lv, m in data(species)['learnset']['by_level']:
        if lv <= level and m not in moves:
            moves.append(m)
    return moves[-4:]


def trainer_locations():
    loc = {}
    for pattern in ('*/events.json', '*/scripts.s'):
        for ev in MAPS.glob(pattern):
            for tr in set(re.findall(r'\b(TRAINER_[A-Z0-9_]+)\b', ev.read_text())):
                loc.setdefault(tr, ev.parent.name)
    return loc


def main():
    write = '--apply' in sys.argv
    locs = trainer_locations()
    rows = []
    mapping = {}  # (trainer key, original family) -> replacement family
    files = sorted(TRAINERS.glob('*.json'), key=lambda f: (max([p['level'] for p in json.loads(f.read_text())['party']] or [0]), f.stem))
    for f in files:
        if f.stem in SKIP:
            continue
        d = json.loads(f.read_text())
        party = d['party']
        cls = d['class'][len('TRAINER_CLASS_'):]
        if len(party) < 2 or cls == 'PLAYER_MALE':
            continue
        key = d['name'] if cls in ('RIVAL', 'DP_PLAYER_MALE', 'DP_PLAYER_FEMALE') else re.sub(r'_rematch.*$|_\d+$', '', f.stem)
        strong = cls in STRONG
        # ace
        if cls == 'RIVAL':
            starters = {s for b in ('TURTWIG', 'CHIMCHAR', 'PIPLUP') for s in family(b)}
            ace = next((i for i, p in enumerate(party) if p['species'][8:] in starters), None)
            if ace is None:
                ace = max(range(len(party)), key=lambda i: (party[i]['level'], i))
        else:
            ace = max(range(len(party)), key=lambda i: (party[i]['level'], i))
        others = [i for i in range(len(party)) if i != ace]
        n_replace = max(1, math.ceil(len(others) / 2))
        # pick which members: deterministic per trainer + original family
        others.sort(key=lambda i: rng(key, base_of(party[i]['species'][8:]), 'pick'))
        chosen = sorted(others[:n_replace])
        team_bases = {base_of(p['species'][8:]) for p in party}
        has_moves = any(p.get('moves') for p in party)
        changed = []
        for idx, i in enumerate(chosen):
            p = party[i]
            orig = p['species'][8:]
            level = p['level']
            want5 = idx % 2 == 0  # the 1st, 3rd, ... replacement is Gen 5, the others Gen 1-3
            mkey = (key, base_of(orig))
            if mkey in mapping:
                b = mapping[mkey]
                s = stage_for(b, level)
                team_bases.add(b)
                party[i] = dict(p, species='SPECIES_' + s, form=0,
                                moves=(level_moves(s, level) or None) if has_moves else None,
                                item=p.get('item') if p.get('item') not in SPECIFIC_ITEMS else None)
                note = ' (was Mega-capable)' if orig in MEGA else ''
                changed.append(f"{orig.title()}{note} → {s.title()} (Gen {gen(s)}), Lv {level}")
                continue
            cands = [c for c in candidates(cls, level, strong) if c[0] not in team_bases]
            pool = [c for c in cands if (gen(c[1]) == 5) == want5]
            if not pool and want5:
                pool = [c for c in candidates(None, level, strong) if gen(c[1]) == 5 and c[0] not in team_bases]
            pool = pool or cands
            if not pool:
                continue
            if cls in MEGA_PREF:
                mp = [c for c in pool if any(s in MEGA for s in family(c[0]))]
                pool = mp or pool
            b, s = pool[rng(key, base_of(orig), 'choose') % len(pool)]
            mapping[mkey] = b
            team_bases.add(b)
            new = {'species': 'SPECIES_' + s, 'form': 0, 'level': level,
                   'item': p.get('item') if p.get('item') not in SPECIFIC_ITEMS else None,
                   'moves': (level_moves(s, level) or None) if has_moves else None,
                   'iv_scale': p.get('iv_scale', 0), 'ball_seal': p.get('ball_seal', 0)}
            for k in p:
                if k not in new:
                    new[k] = p[k]
            party[i] = new
            note = ' (was Mega-capable)' if orig in MEGA else ''
            changed.append(f"{orig.title()}{note} → {s.title()} (Gen {gen(s)}), Lv {level}")
        if changed and not any(gen(party[i]['species'][8:]) == 5 for i in range(len(party))):
            # still no Gen 5 (all replacements came from earlier mappings): add one more replacement
            rest = [i for i in others if i not in chosen]
            i = (rest or chosen)[0]
            p = party[i]
            level = p['level']
            pool = [c for c in candidates(cls, level, strong) if gen(c[1]) == 5 and c[0] not in team_bases] or \
                   [c for c in candidates(None, level, strong) if gen(c[1]) == 5 and c[0] not in team_bases]
            b, s = pool[rng(key, base_of(p['species'][8:]), 'choose') % len(pool)]
            mapping[(key, base_of(p['species'][8:]))] = b
            orig = p['species'][8:]
            party[i] = dict(p, species='SPECIES_' + s, form=0,
                            moves=(level_moves(s, level) or None) if has_moves else None)
            changed.append(f"{orig.title()} → {s.title()} (Gen 5), Lv {level}")
        if changed:
            rows.append((locs.get('TRAINER_' + f.stem.upper(), '-'), f"{d['name']} ({cls.replace('_', ' ').title()})", f.stem, changed))
            if write:
                f.write_text(json.dumps(d, indent=4, ensure_ascii=False) + '\n')
    out = ['# Phase 6: trainer teams', '', 'Ace kept; about half of the other Pokémon replaced; every changed team has a Gen 5 Pokémon.',
           'Single-Pokémon teams are unchanged. Lass Sarah (Route 204, Phase 1A TEMP TEST) is skipped.', '',
           '| Location | Trainer | File | Replaced → replacement |', '|---|---|---|---|']
    for loc, name, stem, ch in sorted(rows):
        out.append(f'| {loc} | {name} | {stem} | ' + '<br>'.join(ch) + ' |')
    (ROOT / 'tools' / 'gen5_pack' / 'PHASE6_TRAINER_PLAN.md').write_text('\n'.join(out) + '\n')
    print(len(rows), 'trainers changed', '(applied)' if write else '(plan only)')


if __name__ == '__main__':
    main()
