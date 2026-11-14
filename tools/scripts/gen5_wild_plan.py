#!/usr/bin/env python3
"""Phase 5: mix Gen 5 and more Gen 1-3 Pokemon into the wild encounter tables.

usage: gen5_wild_plan.py            -> writes the approval table tools/gen5_pack/PHASE5_WILD_PLAN.md
       gen5_wild_plan.py --apply    -> applies it to res/field/maps/*/encounters.json

Rules: every original species keeps at least one slot; a new species takes over a slot whose
species also appears in another slot; it keeps that slot's level and rate; the evolution stage is
picked from the level (level evolutions at their level, stone / trade / friendship evolutions only
from Lv 45, i.e. post-game areas). Time-of-day, swarm, radar and dual-slot overrides are untouched.
Slot rates: land 20,20,10,10,10,10,5,5,4,4,1,1 (slots 3-4 are replaced by morning/day/night
Pokemon, 1-2 by swarms, 9-10 by GBA dual-slot, so new Pokemon use slots 5-8 and 11-12);
surf / rods 60,30,5,4,1.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / 'res' / 'field' / 'maps'
POKEMON = ROOT / 'res' / 'pokemon'

LAND_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
WATER_RATES = [60, 30, 5, 4, 1]
GEN5 = range(494, 650)
SPECIES = (ROOT / 'generated' / 'species.txt').read_text().split()

# (maps, kind, family base, why).  kind: land / rare (1% land slot) / surf / good / super
ROUTE_201_ORIGINAL = ['STARLY', 'BIDOOF', 'STARLY', 'KRICKETOT', 'STARLY', 'BIDOOF', 'STARLY', 'BIDOOF', 'STARLY', 'BIDOOF', 'STARLY', 'BIDOOF']
LAKE_FISH = ['twinleaf_town', 'lake_verity', 'lake_verity_low_water', 'route_203', 'route_204_south', 'route_204_north', 'route_208', 'route_209', 'route_212_north', 'route_214', 'eterna_city', 'celestic_town', 'lake_valor', 'lake_acuity', 'sendoff_spring', 'route_205_north', 'route_210_north']
SEA = ['route_205_south', 'valley_windworks_outside', 'fuego_ironworks_outside', 'route_212_south', 'route_213', 'route_218', 'route_219', 'route_220', 'route_221', 'pastoria_city', 'canalave_city', 'iron_island', 'sunyshore_city']
LATE_SEA = ['route_222', 'route_223', 'route_224', 'route_226', 'route_230', 'pokemon_league']
MARSH = [f'great_marsh_{i}' for i in range(1, 7)]
CHATEAU = [p.name for p in MAPS.iterdir() if p.name.startswith('old_chateau')]
LOST_TOWER = [p.name for p in MAPS.iterdir() if p.name.startswith('route_209_lost_tower')]
TURNBACK_LOW = [p.name for p in MAPS.iterdir() if re.match(r'turnback_cave_(entrance|pillar_1_)', p.name)]
TURNBACK_MID = [p.name for p in MAPS.iterdir() if p.name.startswith('turnback_cave_pillar_2_')]
TURNBACK_HIGH = [p.name for p in MAPS.iterdir() if re.match(r'turnback_cave_(pillar_3_|pillar_room|giratina)', p.name)]
IRON = [p.name for p in MAPS.iterdir() if p.name.startswith('iron_island_')]
CORONET_LOW = ['mt_coronet_1f_north_room_1', 'mt_coronet_1f_south']
CORONET_HIGH = ['mt_coronet_1f_north_room_2', 'mt_coronet_1f_tunnel_room', 'mt_coronet_2f', 'mt_coronet_3f', 'mt_coronet_4f_room_3',
                'mt_coronet_4f_rooms_1_and_2', 'mt_coronet_5f', 'mt_coronet_6f', 'mt_coronet_b1f']
TEMPLE = [p.name for p in MAPS.iterdir() if p.name.startswith('snowpoint_temple')]
VROAD = [p.name for p in MAPS.iterdir() if p.name.startswith('victory_road')]
VROAD_LATE = ['victory_road_1f_room_1', 'victory_road_1f_room_2', 'victory_road_1f_room_3']

PLAN = [
    (['route_201'], 'land', 'PATRAT', 'starting route: common Normal-type scout like Bidoof'),
    (['route_201'], 'land', 'PIDGEY', 'starting route: early bird like Starly'),
    (['lake_verity', 'lake_verity_low_water'], 'land', 'PATRAT', 'lakeside grass next to Route 201'),
    (['lake_verity', 'lake_verity_low_water'], 'land', 'SENTRET', 'small Normal-type of early grass'),
    (['route_202'], 'land', 'LILLIPUP', 'early grass: puppy alongside Shinx'),
    (['route_202'], 'land', 'ZIGZAGOON', 'early grass: common Normal-type'),
    (['route_203'], 'land', 'PURRLOIN', 'early grass: sneaky Dark cat'),
    (['route_203'], 'land', 'POOCHYENA', 'early grass: Dark dog'),
    (['route_204_south'], 'land', 'SEWADDLE', 'grassy route before the forest: Bug/Grass'),
    (['route_204_south'], 'land', 'CATERPIE', 'Bug for the Bug-heavy grass'),
    (['route_204_north'], 'land', 'VENIPEDE', 'Bug/Poison near the woods'),
    (['route_204_north'], 'land', 'WEEDLE', 'Bug/Poison like Wurmple'),
    (['oreburgh_gate_1f', 'oreburgh_gate_b1f', 'ravaged_path'], 'land', 'WOOBAT', 'cave bat like Zubat'),
    (['oreburgh_gate_1f', 'oreburgh_gate_b1f', 'ravaged_path'], 'land', 'WHISMUR', 'echoing caves'),
    (['oreburgh_mine_b1f', 'oreburgh_mine_b2f'], 'land', 'ROGGENROLA', 'coal mine: Rock-type'),
    (['oreburgh_mine_b1f', 'oreburgh_mine_b2f'], 'land', 'ARON', 'mine: eats iron ore'),
    (['route_207'], 'land', 'ROGGENROLA', 'rocky slope like Geodude'),
    (['route_207'], 'land', 'SANDSHREW', 'dry rocky ground'),
    (['valley_windworks_outside'], 'land', 'EMOLGA', 'windworks: Electric glider'),
    (['valley_windworks_outside'], 'land', 'VOLTORB', 'power plant Electric-type'),
    (['route_205_south'], 'land', 'BLITZLE', 'meadow by the windworks: Electric like Pachirisu'),
    (['route_205_south'], 'land', 'ELECTRIKE', 'Electric of the open meadow'),
    (['route_205_north'], 'land', 'COTTONEE', 'flowery north meadow: Grass'),
    (['route_205_north'], 'land', 'ODDISH', 'Grass near the forest'),
    (['eterna_forest'], 'land', 'SEWADDLE', 'Bug/Grass forest'),
    (['eterna_forest'], 'land', 'KARRABLAST', 'forest Bug'),
    (['eterna_forest'], 'land', 'PARAS', 'Bug/Grass mushroom bug of dark forests'),
    (['wayward_cave_1f', 'wayward_cave_b1f'], 'land', 'DRILBUR', 'digging Ground-type cave'),
    (['wayward_cave_1f', 'wayward_cave_b1f'], 'land', 'ARON', 'cave Steel/Rock'),
    (['route_206'], 'land', 'DRILBUR', 'rocky cycling road'),
    (['route_206'], 'land', 'SANDSHREW', 'rocky cycling road'),
    (CORONET_LOW, 'land', 'WOOBAT', 'mountain cave bat'),
    (CORONET_LOW, 'land', 'ROGGENROLA', 'mountain cave Rock'),
    (['route_211_west'], 'land', 'TIMBURR', 'mountain trail Fighting like Machop'),
    (['route_211_west'], 'land', 'MAKUHITA', 'mountain trail Fighting'),
    (['route_211_east'], 'land', 'TIMBURR', 'mountain trail Fighting'),
    (['route_211_east'], 'land', 'MAKUHITA', 'mountain trail Fighting'),
    (['old_chateau'] + CHATEAU, 'land', 'LITWICK', 'haunted mansion: candle ghost'),
    (['old_chateau'] + CHATEAU, 'land', 'YAMASK', 'haunted mansion: Ghost'),
    (['old_chateau'] + CHATEAU, 'land', 'SHUPPET', 'haunted mansion: Ghost'),
    (['route_208'], 'land', 'PETILIL', 'flower route: Grass'),
    (['route_208'], 'land', 'HOPPIP', 'flower route: Grass/Flying'),
    (['route_209'], 'land', 'MUNNA', 'peaceful route: Psychic like Ralts'),
    (['route_209'], 'land', 'SNUBBULL', 'route with Chansey: Normal/Fairy'),
    (LOST_TOWER, 'land', 'LITWICK', 'grave tower: Ghost'),
    (LOST_TOWER, 'land', 'SHUPPET', 'grave tower: Ghost'),
    (['route_210_south'], 'land', 'DEERLING', 'tall-grass route'),
    (['route_210_south'], 'land', 'DODUO', 'tall-grass route'),
    (['route_210_north'], 'land', 'MIENFOO', 'foggy mountain: Fighting like Meditite'),
    (['route_210_north'], 'land', 'NATU', 'foggy mountain bird'),
    (['route_215'], 'land', 'PIDOVE', 'rainy route: Normal/Flying like Staravia'),
    (['route_215'], 'land', 'HOPPIP', 'rainy grass'),
    (['route_212_north'], 'land', 'TYMPOLE', 'rainy route: Water tadpole'),
    (['route_212_north'], 'land', 'LOTAD', 'rainy route: Water/Grass'),
    (['route_212_south'], 'land', 'STUNFISK', 'swampy route'),
    (['route_212_south'], 'land', 'POLIWAG', 'swampy route'),
    (MARSH, 'land', 'TYMPOLE', 'marsh: Water/Ground'),
    (MARSH, 'land', 'STUNFISK', 'marsh: flat Ground/Electric fish'),
    (MARSH, 'land', 'LOTAD', 'marsh: Water/Grass'),
    (['route_213'], 'land', 'DUCKLETT', 'beach: Water bird like Wingull'),
    (['route_213'], 'land', 'KRABBY', 'beach crab'),
    (['route_214'], 'land', 'SANDILE', 'dry rocky route like Rhyhorn'),
    (['route_214'], 'land', 'TRAPINCH', 'dry sandy ground'),
    (['ruin_maniac_cave_long', 'ruin_maniac_cave_short', 'maniac_tunnel'], 'land', 'DRILBUR', 'freshly dug tunnel'),
    (['ruin_maniac_cave_long', 'ruin_maniac_cave_short', 'maniac_tunnel'], 'land', 'SANDSHREW', 'freshly dug tunnel'),
    (['valor_lakefront'], 'land', 'MINCCINO', 'lakefront resort area'),
    (['valor_lakefront'], 'land', 'SKITTY', 'lakefront resort area'),
    (['trophy_garden'], 'land', 'AUDINO', "mansion garden"),
    (['trophy_garden'], 'land', 'PLUSLE', 'mansion garden: small Electric like Pichu'),
    (['fuego_ironworks_outside'], 'land', 'KLINK', 'ironworks: gears'),
    (['fuego_ironworks_outside'], 'land', 'SLUGMA', 'ironworks furnaces'),
    (TURNBACK_LOW, 'land', 'GOLETT', 'ancient cave: Ground/Ghost'),
    (TURNBACK_LOW, 'land', 'SABLEYE', 'dark cave Ghost'),
    (TURNBACK_MID, 'land', 'GOLETT', 'ancient cave: Ground/Ghost'),
    (TURNBACK_MID, 'land', 'YAMASK', 'ancient cave: Ghost'),
    (TURNBACK_HIGH, 'land', 'YAMASK', 'ancient cave: Ghost'),
    (TURNBACK_HIGH, 'land', 'SHUPPET', 'ancient cave: Ghost'),
    (['route_218'], 'land', 'DUCKLETT', 'seaside route'),
    (['route_218'], 'land', 'KRABBY', 'seaside route'),
    (['route_221'], 'land', 'DEERLING', 'grassy route'),
    (['route_221'], 'land', 'SPINDA', 'grassy route'),
    (IRON, 'land', 'DURANT', 'iron mine: Bug/Steel'),
    (IRON, 'land', 'KLINK', 'iron mine: Steel gears'),
    (IRON, 'rare', 'BELDUM', 'optional island: rare pseudo-legendary'),
    (CORONET_HIGH, 'land', 'ROGGENROLA', 'deep mountain caves: Rock'),
    (CORONET_HIGH, 'land', 'ARON', 'deep mountain caves'),
    (['mt_coronet_outside_north', 'mt_coronet_outside_south'], 'land', 'CUBCHOO', 'snowy mountainside'),
    (['mt_coronet_outside_north', 'mt_coronet_outside_south'], 'land', 'SNORUNT', 'snowy mountainside'),
    (['route_216'], 'land', 'CUBCHOO', 'snow route'),
    (['route_216'], 'land', 'SNORUNT', 'snow route'),
    (['route_217'], 'land', 'VANILLITE', 'blizzard route'),
    (['route_217'], 'land', 'SPHEAL', 'blizzard route'),
    (['acuity_lakefront'], 'land', 'CRYOGONAL', 'icy lakefront'),
    (['acuity_lakefront'], 'land', 'DELIBIRD', 'icy lakefront'),
    (['lake_acuity'], 'land', 'VANILLITE', 'frozen lake'),
    (['lake_acuity'], 'land', 'SPHEAL', 'frozen lake'),
    (['lake_valor'], 'land', 'DUCKLETT', 'lake bird'),
    (['lake_valor'], 'land', 'PIDGEY', 'lake bird'),
    (['sendoff_spring'], 'land', 'GOLETT', 'spring by Turnback Cave'),
    (['sendoff_spring'], 'land', 'MISDREAVUS', 'spring by Turnback Cave'),
    (['route_222'], 'land', 'BLITZLE', 'Electric seaside route like Luxio'),
    (['route_222'], 'land', 'ELECTRIKE', 'Electric seaside route'),
    (TEMPLE, 'land', 'CRYOGONAL', 'ice temple'),
    (TEMPLE, 'land', 'SNORUNT', 'ice temple'),
    (VROAD, 'land', 'DRILBUR', 'Victory Road: Ground/Steel'),
    (VROAD, 'land', 'ROGGENROLA', 'Victory Road: Rock'),
    (VROAD, 'rare', 'AXEW', 'late area: rare Dragon'),
    (VROAD_LATE, 'rare', 'DEINO', 'post-game rooms: rare pseudo-legendary'),
    (['victory_road_1f', 'victory_road_2f', 'victory_road_b1f'], 'rare', 'BAGON', 'late area: rare pseudo-legendary'),
    (['route_224'], 'land', 'PETILIL', 'flower route'),
    (['route_224'], 'land', 'ODDISH', 'flower route'),
    (['route_224'], 'rare', 'BULBASAUR', 'post-game: rare starter'),
    (['route_225'], 'land', 'RUFFLET', 'mountain route: bird of prey like Fearow'),
    (['route_225'], 'land', 'MANKEY', 'mountain route: Fighting'),
    (['route_225'], 'rare', 'LARVITAR', 'post-game: rare pseudo-legendary'),
    (['route_226'], 'land', 'VULLABY', 'cliff route: vulture'),
    (['route_226'], 'land', 'MANKEY', 'cliff route: Fighting'),
    (['route_226'], 'rare', 'OSHAWOTT', 'post-game coast: rare starter'),
    (['route_227', 'stark_mountain_outside'], 'land', 'DARUMAKA', 'volcano: Fire'),
    (['route_227', 'stark_mountain_outside'], 'land', 'TORKOAL', 'volcano: Fire'),
    (['route_227'], 'rare', 'TEPIG', 'post-game volcano: rare starter'),
    (['stark_mountain_outside'], 'rare', 'CHARMANDER', 'post-game volcano: rare starter'),
    (['stark_mountain_room_1', 'stark_mountain_room_2'], 'land', 'HEATMOR', 'volcano cave: Fire'),
    (['stark_mountain_room_1', 'stark_mountain_room_2'], 'land', 'NUMEL', 'volcano cave: Fire/Ground'),
    (['stark_mountain_room_1', 'stark_mountain_room_2'], 'rare', 'LARVESTA', 'post-game volcano: rare Bug/Fire'),
    (['route_228'], 'land', 'SANDILE', 'desert'),
    (['route_228'], 'land', 'TRAPINCH', 'desert'),
    (['route_228'], 'rare', 'MARACTUS', 'desert cactus'),
    (['route_229'], 'land', 'SEWADDLE', 'bug forest'),
    (['route_229'], 'land', 'JOLTIK', 'bug forest'),
    (['route_229'], 'land', 'HERACROSS', 'bug forest'),
    (['route_229'], 'rare', 'SNIVY', 'post-game forest: rare starter'),
    (['route_230'], 'land', 'DUCKLETT', 'sea route'),
    (['route_230'], 'land', 'KRABBY', 'sea route'),
    (['route_230'], 'rare', 'SQUIRTLE', 'post-game sea: rare starter'),
    # surfing
    (LAKE_FISH, 'surf', 'BASCULIN', 'freshwater: Basculin'),
    (LAKE_FISH, 'surf', 'MARILL', 'freshwater'),
    (MARSH + ['route_212_south'], 'surf', 'TYMPOLE', 'marsh water'),
    (MARSH, 'surf', 'LOTAD', 'marsh water'),
    (SEA, 'surf', 'FRILLISH', 'sea: jellyfish like Tentacool'),
    (SEA, 'surf', 'HORSEA', 'sea'),
    (LATE_SEA, 'surf', 'ALOMOMOLA', 'open sea'),
    (LATE_SEA, 'surf', 'FRILLISH', 'open sea'),
    (['route_229', 'route_227', 'route_228'], 'surf', 'BASCULIN', 'freshwater'),
    # fishing
    (LAKE_FISH + MARSH + ['oreburgh_gate_b1f', 'ravaged_path', 'mt_coronet_1f_south', 'mt_coronet_b1f'], 'good', 'BASCULIN', 'freshwater fish'),
    (SEA + LATE_SEA, 'good', 'FRILLISH', 'sea fishing'),
    (LAKE_FISH + MARSH, 'super', 'CORPHISH', 'freshwater'),
    (SEA, 'super', 'TYNAMO', 'sea: EleFish'),
    (LATE_SEA, 'super', 'TYNAMO', 'sea: EleFish'),
    (LATE_SEA, 'super', 'CLAMPERL', 'deep sea'),
]


def species_data(name):
    return json.loads((POKEMON / name.lower() / 'data.json').read_text())


def stage_for(base, level):
    cur = base
    while True:
        evos = species_data(cur)['evolutions']
        if not evos:
            return cur
        method = evos[0][0]
        target = evos[0][-1][8:]
        if method == 'EVO_LEVEL' and level >= evos[0][1]:
            cur = target
        elif method not in ('EVO_LEVEL',) and method != 'EVO_NONE' and level >= 45:
            cur = target
        else:
            return cur


def gen_of(name):
    i = SPECIES.index('SPECIES_' + name)
    return 1 if i <= 151 else 2 if i <= 251 else 3 if i <= 386 else 4 if i <= 493 else 5


def apply(write):
    rows = []
    tables = {}
    used = {}  # (map, table) -> set of slots already replaced
    for maps, kind, base, why in PLAN:
        for m in maps:
            f = MAPS / m / 'encounters.json'
            if not f.exists():
                continue
            d = tables.setdefault(m, json.loads(f.read_text()))
            if m == 'route_201':  # undo the Phase 2 Snivy / Tepig / Oshawott test first
                for i, s in enumerate(ROUTE_201_ORIGINAL):
                    if i not in used.get((m, 'land'), set()):
                        d['land_encounters'][i]['species'] = 'SPECIES_' + s
            if kind in ('land', 'rare'):
                if not d['land_rate']:
                    continue
                enc = d['land_encounters']
                prefs = [10, 11] if kind == 'rare' else [4, 5, 6, 7, 8, 9]
                rates = LAND_RATES
                lvl = lambda e: e['level']
                key = (m, 'land')
            else:
                tname = {'surf': 'surf', 'good': 'good_rod', 'super': 'super_rod'}[kind]
                if not d[f'{tname}_rate']:
                    continue
                enc = d[f'{tname}_encounters']
                prefs = [2, 3, 4, 1]
                rates = WATER_RATES
                lvl = lambda e: e['level_min']
                key = (m, tname)
            taken = used.setdefault(key, set())
            slot = None
            for s in prefs:
                if s in taken:
                    continue
                sp = enc[s]['species']
                if sp == 'SPECIES_NONE':
                    continue
                others = [e['species'] for i, e in enumerate(enc) if i != s and i not in taken]
                if sp in others:
                    slot = s
                    break
            if slot is None:
                rows.append((m, kind, base, '-', '-', '-', 'SKIPPED: no free slot without removing an original'))
                continue
            taken.add(slot)
            level = lvl(enc[slot])
            name = stage_for(base, level)
            old = enc[slot]['species'][8:]
            enc[slot]['species'] = 'SPECIES_' + name
            lv = f"{enc[slot]['level']}" if 'level' in enc[slot] else f"{enc[slot]['level_min']}-{enc[slot]['level_max']}"
            rows.append((m, kind, name, gen_of(name), lv, f'{rates[slot]}% (was {old})', why))
    if write:
        for m, d in tables.items():
            (MAPS / m / 'encounters.json').write_text(json.dumps(d, indent=4) + '\n')
    return rows


def main():
    write = '--apply' in sys.argv
    rows = apply(write)
    # group identical rows over sub-maps for the table
    groups = {}
    for m, kind, name, g, lv, rate, why in rows:
        k = (kind, name, g, lv, rate, why, re.sub(r'(_\d+|_room.*|_b?\d+f.*|_(north|south|east|west|corridor|dining_area|side_rooms|entrance|left_room|right_room|pillar.*))$', '', m))
        groups.setdefault(k, []).append(m)
    out = ['# Phase 5: wild encounter plan', '', 'Each new Pokémon replaces one slot whose Pokémon also has another slot in that table,',
           'so every original Pokémon stays. Level = the replaced slot\'s level; rate = that slot\'s rate.', '',
           '| Area | Encounter | Pokémon added (gen) | Level | Rate | Why it fits |', '|---|---|---|---|---|---|']
    skipped = sorted({(k[6], k[1].title(), k[0]) for k in groups if k[5].startswith('SKIPPED')})
    groups = {k: v for k, v in groups.items() if not k[5].startswith('SKIPPED')}
    for (kind, name, g, lv, rate, why, area), ms in sorted(groups.items(), key=lambda x: (x[1][0], x[0][0])):
        where = ms[0] if len(ms) == 1 else f'{area} ({len(ms)} maps)'
        label = {'land': 'grass / cave', 'rare': 'grass / cave (rare slot)', 'surf': 'surfing', 'good': 'Good Rod', 'super': 'Super Rod'}[kind]
        out.append(f"| {where} | {label} | {name.title()} (Gen {g}) | {lv} | {rate} | {why} |")
    out += ['', '## Not added (every slot in that table is the only slot of an original Pokémon)', '']
    out += [f'- {a}: {n} ({k})' for a, n, k in skipped]
    (ROOT / 'tools' / 'gen5_pack' / 'PHASE5_WILD_PLAN.md').write_text('\n'.join(out) + '\n')
    print(len(rows), 'changes;', sum('SKIPPED' in r[-1] for r in rows), 'skipped', '(applied)' if write else '(plan only)')


if __name__ == '__main__':
    main()
