#!/usr/bin/env python3
"""Import Gen 5 species (#494-649) into res/pokemon/<species>/ from the packs in tools/gen5_pack/.

usage: import_gen5_species.py <first dex no> <last dex no> [--force]
       (run with a Python that has Pillow + openpyxl)

Sources (Phase 3 rule: the spreadsheet is the source of truth):
  - spreadsheet  tools/gen5_pack/spreadsheet/Unova_Pokemon_Stats_and_Abilities.xlsx
                 name, types, base stats, abilities, evolutions, learnsets
  - Black 2      tools/gen5_pack/items_and_moves/original_archives/*.narc
                 catch rate, EXP yield, EV yield, held items, gender ratio, hatch cycles,
                 friendship, growth rate, egg groups, colour, height, weight
  - sprites      tools/gen5_pack/pokemon_sprites/sheets/{normal,shiny}/{front,back}/
  - cries        tools/gen5_pack/audio/gen5_cries/wav/
Placeholders (marked, listed in the report): party icon (shrunk front sprite), no footprint,
Pokedex entry text, abilities/moves that don't exist yet.

Writes a report of everything filled in / skipped to tools/gen5_pack/import_report_<a>_<b>.txt
"""
import shutil
import json
import math
import re
import struct
import sys
import wave
from pathlib import Path

import openpyxl
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'tools' / 'gen5_pack'
POKEMON = ROOT / 'res' / 'pokemon'
SHEET = PACK / 'spreadsheet' / 'Unova_Pokemon_Stats_and_Abilities.xlsx'
NARCS = PACK / 'items_and_moves' / 'original_archives'

# Pokedex categories (Black 2)
CATEGORIES = {
    'Victini': 'Victory',
    'Snivy': 'Grass Snake',
    'Servine': 'Grass Snake',
    'Serperior': 'Regal',
    'Tepig': 'Fire Pig',
    'Pignite': 'Fire Pig',
    'Emboar': 'Mega Fire Pig',
    'Oshawott': 'Sea Otter',
    'Dewott': 'Discipline',
    'Samurott': 'Formidable',
    'Patrat': 'Scout',
    'Watchog': 'Lookout',
    'Lillipup': 'Puppy',
    'Herdier': 'Loyal Dog',
    'Stoutland': 'Big-Hearted',
    'Purrloin': 'Devious',
    'Liepard': 'Cruel',
    'Pansage': 'Grass Monkey',
    'Simisage': 'Thorn Monkey',
    'Pansear': 'High Temp',
    'Simisear': 'Ember',
    'Panpour': 'Spray',
    'Simipour': 'Geyser',
    'Munna': 'Dream Eater',
    'Musharna': 'Drowsing',
    'Pidove': 'Tiny Pigeon',
    'Tranquill': 'Wild Pigeon',
    'Unfezant': 'Proud',
    'Blitzle': 'Electrified',
    'Zebstrika': 'Thunderbolt',
    'Roggenrola': 'Mantle',
    'Boldore': 'Ore',
    'Gigalith': 'Compressed',
    'Woobat': 'Bat',
    'Swoobat': 'Courting',
    'Drilbur': 'Mole',
    'Excadrill': 'Subterrene',
    'Audino': 'Hearing',
    'Timburr': 'Muscular',
    'Gurdurr': 'Muscular',
    'Conkeldurr': 'Muscular',
    'Tympole': 'Tadpole',
    'Palpitoad': 'Vibration',
    'Seismitoad': 'Vibration',
    'Throh': 'Judo',
    'Sawk': 'Karate',
    'Sewaddle': 'Sewing',
    'Swadloon': 'Leaf-Wrapped',
    'Leavanny': 'Nurturing',
    'Venipede': 'Centipede',
    'Whirlipede': 'Curlipede',
    'Scolipede': 'Megapede',
    'Cottonee': 'Cotton Puff',
    'Whimsicott': 'Windveiled',
    'Petilil': 'Bulb',
    'Lilligant': 'Flowering',
    'Basculin': 'Hostile',
    'Sandile': 'Desert Croc',
    'Krokorok': 'Desert Croc',
    'Krookodile': 'Intimidation',
    'Darumaka': 'Zen Charm',
    'Darmanitan': 'Blazing',
    'Maractus': 'Cactus',
    'Dwebble': 'Rock Inn',
    'Crustle': 'Stone Home',
    'Scraggy': 'Shedding',
    'Scrafty': 'Hoodlum',
    'Sigilyph': 'Avianoid',
    'Yamask': 'Spirit',
    'Cofagrigus': 'Coffin',
    'Tirtouga': 'Prototurtle',
    'Carracosta': 'Prototurtle',
    'Archen': 'First Bird',
    'Archeops': 'First Bird',
    'Trubbish': 'Trash Bag',
    'Garbodor': 'Trash Heap',
    'Zorua': 'Tricky Fox',
    'Zoroark': 'Illusion Fox',
    'Minccino': 'Chinchilla',
    'Cinccino': 'Scarf',
    'Gothita': 'Fixation',
    'Gothorita': 'Manipulate',
    'Gothitelle': 'Astral Body',
    'Solosis': 'Cell',
    'Duosion': 'Mitosis',
    'Reuniclus': 'Multiplying',
    'Ducklett': 'Water Bird',
    'Swanna': 'White Bird',
    'Vanillite': 'Fresh Snow',
    'Vanillish': 'Icy Snow',
    'Vanilluxe': 'Snowstorm',
    'Deerling': 'Season',
    'Sawsbuck': 'Season',
    'Emolga': 'Sky Squirrel',
    'Karrablast': 'Clamping',
    'Escavalier': 'Cavalry',
    'Foongus': 'Mushroom',
    'Amoonguss': 'Mushroom',
    'Frillish': 'Floating',
    'Jellicent': 'Floating',
    'Alomomola': 'Caring',
    'Joltik': 'Attaching',
    'Galvantula': 'EleSpider',
    'Ferroseed': 'Thorn Seed',
    'Ferrothorn': 'Thorn Pod',
    'Klink': 'Gear',
    'Klang': 'Gear',
    'Klinklang': 'Gear',
    'Tynamo': 'EleFish',
    'Eelektrik': 'EleFish',
    'Eelektross': 'EleFish',
    'Elgyem': 'Cerebral',
    'Beheeyem': 'Cerebral',
    'Litwick': 'Candle',
    'Lampent': 'Lamp',
    'Chandelure': 'Luring',
    'Axew': 'Tusk',
    'Fraxure': 'Axe Jaw',
    'Haxorus': 'Axe Jaw',
    'Cubchoo': 'Chill',
    'Beartic': 'Freezing',
    'Cryogonal': 'Crystallizing',
    'Shelmet': 'Snail',
    'Accelgor': 'Shell Out',
    'Stunfisk': 'Trap',
    'Mienfoo': 'Martial Arts',
    'Mienshao': 'Martial Arts',
    'Druddigon': 'Cave',
    'Golett': 'Automaton',
    'Golurk': 'Automaton',
    'Pawniard': 'Sharp Blade',
    'Bisharp': 'Sword Blade',
    'Bouffalant': 'Bash Buffalo',
    'Rufflet': 'Eaglet',
    'Braviary': 'Valiant',
    'Vullaby': 'Diapered',
    'Mandibuzz': 'Bone Vulture',
    'Heatmor': 'Anteater',
    'Durant': 'Iron Ant',
    'Deino': 'Irate',
    'Zweilous': 'Hostile',
    'Hydreigon': 'Brutal',
    'Larvesta': 'Torch',
    'Volcarona': 'Sun',
    'Cobalion': 'Iron Will',
    'Terrakion': 'Cavern',
    'Virizion': 'Grassland',
    'Tornadus': 'Cyclone',
    'Thundurus': 'Bolt Strike',
    'Reshiram': 'Vast White',
    'Zekrom': 'Deep Black',
    'Landorus': 'Abundance',
    'Kyurem': 'Boundary',
    'Keldeo': 'Colt',
    'Meloetta': 'Melody',
    'Genesect': 'Paleozoic',
}

# Body shapes (not in the Black 2 personal data; approximate)
BODY_SHAPES = {
    'Victini': 'SHAPE_BIPEDAL_TAILED',
    'Snivy': 'SHAPE_BIPEDAL_TAILED',
    'Servine': 'SHAPE_BIPEDAL_TAILED',
    'Serperior': 'SHAPE_SERPENTINE',
    'Tepig': 'SHAPE_QUADRUPED',
    'Pignite': 'SHAPE_BIPEDAL_TAILED',
    'Emboar': 'SHAPE_BIPEDAL_TAILED',
    'Oshawott': 'SHAPE_BIPEDAL_TAILED',
    'Dewott': 'SHAPE_BIPEDAL_TAILED',
    'Samurott': 'SHAPE_QUADRUPED',
    'Patrat': 'SHAPE_BIPEDAL_TAILED',
    'Watchog': 'SHAPE_BIPEDAL_TAILED',
    'Lillipup': 'SHAPE_QUADRUPED',
    'Herdier': 'SHAPE_QUADRUPED',
    'Stoutland': 'SHAPE_QUADRUPED',
    'Purrloin': 'SHAPE_QUADRUPED',
    'Liepard': 'SHAPE_QUADRUPED',
    'Pansage': 'SHAPE_BIPEDAL_TAILED',
    'Simisage': 'SHAPE_BIPEDAL_TAILED',
    'Pansear': 'SHAPE_BIPEDAL_TAILED',
    'Simisear': 'SHAPE_BIPEDAL_TAILED',
    'Panpour': 'SHAPE_BIPEDAL_TAILED',
    'Simipour': 'SHAPE_BIPEDAL_TAILED',
    'Munna': 'SHAPE_QUADRUPED',
    'Musharna': 'SHAPE_SERPENTINE',
    'Pidove': 'SHAPE_WINGED',
    'Tranquill': 'SHAPE_WINGED',
    'Unfezant': 'SHAPE_WINGED',
    'Blitzle': 'SHAPE_QUADRUPED',
    'Zebstrika': 'SHAPE_QUADRUPED',
    'Roggenrola': 'SHAPE_HEAD_LEGS',
    'Boldore': 'SHAPE_HEAD_LEGS',
    'Gigalith': 'SHAPE_HEAD_LEGS',
    'Woobat': 'SHAPE_WINGED',
    'Swoobat': 'SHAPE_WINGED',
    'Drilbur': 'SHAPE_BIPEDAL_TAILED',
    'Excadrill': 'SHAPE_BIPEDAL_TAILLESS',
    'Audino': 'SHAPE_BIPEDAL_TAILLESS',
    'Timburr': 'SHAPE_BIPEDAL_TAILLESS',
    'Gurdurr': 'SHAPE_BIPEDAL_TAILLESS',
    'Conkeldurr': 'SHAPE_BIPEDAL_TAILLESS',
    'Tympole': 'SHAPE_HEAD_BASE',
    'Palpitoad': 'SHAPE_QUADRUPED',
    'Seismitoad': 'SHAPE_BIPEDAL_TAILLESS',
    'Throh': 'SHAPE_BIPEDAL_TAILLESS',
    'Sawk': 'SHAPE_BIPEDAL_TAILLESS',
    'Sewaddle': 'SHAPE_INSECTOID',
    'Swadloon': 'SHAPE_HEAD_BASE',
    'Leavanny': 'SHAPE_INSECTOID',
    'Venipede': 'SHAPE_INSECTOID',
    'Whirlipede': 'SHAPE_HEAD_BASE',
    'Scolipede': 'SHAPE_INSECTOID',
    'Cottonee': 'SHAPE_HEAD',
    'Whimsicott': 'SHAPE_BIPEDAL_TAILLESS',
    'Petilil': 'SHAPE_HEAD_LEGS',
    'Lilligant': 'SHAPE_BIPEDAL_TAILLESS',
    'Basculin': 'SHAPE_FINS',
    'Sandile': 'SHAPE_QUADRUPED',
    'Krokorok': 'SHAPE_BIPEDAL_TAILED',
    'Krookodile': 'SHAPE_BIPEDAL_TAILED',
    'Darumaka': 'SHAPE_HEAD_LEGS',
    'Darmanitan': 'SHAPE_QUADRUPED',
    'Maractus': 'SHAPE_BIPEDAL_TAILLESS',
    'Dwebble': 'SHAPE_INSECTOID',
    'Crustle': 'SHAPE_INSECTOID',
    'Scraggy': 'SHAPE_BIPEDAL_TAILED',
    'Scrafty': 'SHAPE_BIPEDAL_TAILED',
    'Sigilyph': 'SHAPE_WINGED',
    'Yamask': 'SHAPE_HEAD_ARMS',
    'Cofagrigus': 'SHAPE_HEAD_ARMS',
    'Tirtouga': 'SHAPE_FINS',
    'Carracosta': 'SHAPE_BIPEDAL_TAILED',
    'Archen': 'SHAPE_WINGED',
    'Archeops': 'SHAPE_WINGED',
    'Trubbish': 'SHAPE_HEAD_ARMS',
    'Garbodor': 'SHAPE_BIPEDAL_TAILLESS',
    'Zorua': 'SHAPE_QUADRUPED',
    'Zoroark': 'SHAPE_BIPEDAL_TAILED',
    'Minccino': 'SHAPE_QUADRUPED',
    'Cinccino': 'SHAPE_QUADRUPED',
    'Gothita': 'SHAPE_BIPEDAL_TAILLESS',
    'Gothorita': 'SHAPE_BIPEDAL_TAILLESS',
    'Gothitelle': 'SHAPE_BIPEDAL_TAILLESS',
    'Solosis': 'SHAPE_HEAD',
    'Duosion': 'SHAPE_HEAD',
    'Reuniclus': 'SHAPE_HEAD_ARMS',
    'Ducklett': 'SHAPE_WINGED',
    'Swanna': 'SHAPE_WINGED',
    'Vanillite': 'SHAPE_HEAD_BASE',
    'Vanillish': 'SHAPE_HEAD_BASE',
    'Vanilluxe': 'SHAPE_MULTI_BODY',
    'Deerling': 'SHAPE_QUADRUPED',
    'Sawsbuck': 'SHAPE_QUADRUPED',
    'Emolga': 'SHAPE_WINGED',
    'Karrablast': 'SHAPE_INSECTOID',
    'Escavalier': 'SHAPE_BIPEDAL_TAILLESS',
    'Foongus': 'SHAPE_HEAD_ARMS',
    'Amoonguss': 'SHAPE_HEAD_ARMS',
    'Frillish': 'SHAPE_TENTACLES',
    'Jellicent': 'SHAPE_TENTACLES',
    'Alomomola': 'SHAPE_FINS',
    'Joltik': 'SHAPE_INSECTOID',
    'Galvantula': 'SHAPE_INSECTOID',
    'Ferroseed': 'SHAPE_HEAD',
    'Ferrothorn': 'SHAPE_TENTACLES',
    'Klink': 'SHAPE_MULTI_BODY',
    'Klang': 'SHAPE_MULTI_BODY',
    'Klinklang': 'SHAPE_MULTI_BODY',
    'Tynamo': 'SHAPE_FINS',
    'Eelektrik': 'SHAPE_FINS',
    'Eelektross': 'SHAPE_FINS',
    'Elgyem': 'SHAPE_BIPEDAL_TAILLESS',
    'Beheeyem': 'SHAPE_BIPEDAL_TAILLESS',
    'Litwick': 'SHAPE_HEAD_BASE',
    'Lampent': 'SHAPE_HEAD_ARMS',
    'Chandelure': 'SHAPE_HEAD_ARMS',
    'Axew': 'SHAPE_BIPEDAL_TAILED',
    'Fraxure': 'SHAPE_BIPEDAL_TAILED',
    'Haxorus': 'SHAPE_BIPEDAL_TAILED',
    'Cubchoo': 'SHAPE_BIPEDAL_TAILLESS',
    'Beartic': 'SHAPE_QUADRUPED',
    'Cryogonal': 'SHAPE_HEAD',
    'Shelmet': 'SHAPE_HEAD_BASE',
    'Accelgor': 'SHAPE_BIPEDAL_TAILLESS',
    'Stunfisk': 'SHAPE_FINS',
    'Mienfoo': 'SHAPE_BIPEDAL_TAILED',
    'Mienshao': 'SHAPE_BIPEDAL_TAILED',
    'Druddigon': 'SHAPE_BIPEDAL_TAILED',
    'Golett': 'SHAPE_BIPEDAL_TAILLESS',
    'Golurk': 'SHAPE_BIPEDAL_TAILLESS',
    'Pawniard': 'SHAPE_BIPEDAL_TAILLESS',
    'Bisharp': 'SHAPE_BIPEDAL_TAILLESS',
    'Bouffalant': 'SHAPE_QUADRUPED',
    'Rufflet': 'SHAPE_WINGED',
    'Braviary': 'SHAPE_WINGED',
    'Vullaby': 'SHAPE_WINGED',
    'Mandibuzz': 'SHAPE_WINGED',
    'Heatmor': 'SHAPE_BIPEDAL_TAILED',
    'Durant': 'SHAPE_INSECTOID',
    'Deino': 'SHAPE_QUADRUPED',
    'Zweilous': 'SHAPE_QUADRUPED',
    'Hydreigon': 'SHAPE_MULTI_WINGED',
    'Larvesta': 'SHAPE_INSECTOID',
    'Volcarona': 'SHAPE_MULTI_WINGED',
    'Cobalion': 'SHAPE_QUADRUPED',
    'Terrakion': 'SHAPE_QUADRUPED',
    'Virizion': 'SHAPE_QUADRUPED',
    'Tornadus': 'SHAPE_HEAD_ARMS',
    'Thundurus': 'SHAPE_HEAD_ARMS',
    'Reshiram': 'SHAPE_BIPEDAL_TAILED',
    'Zekrom': 'SHAPE_BIPEDAL_TAILED',
    'Landorus': 'SHAPE_HEAD_ARMS',
    'Kyurem': 'SHAPE_BIPEDAL_TAILED',
    'Keldeo': 'SHAPE_QUADRUPED',
    'Meloetta': 'SHAPE_BIPEDAL_TAILLESS',
    'Genesect': 'SHAPE_BIPEDAL_TAILED',
}

# Abilities that don't exist yet (Phase 4): temporary stand-ins
ABILITY_STANDINS = {
    'Victory Star': 'ABILITY_COMPOUND_EYES',  # Victory Star = +10% accuracy for the side
    'Healer': 'ABILITY_NATURAL_CURE',         # both cure status
    'Regenerator': 'ABILITY_NATURAL_CURE',    # both trigger on switching out
    'Sheer Force': 'ABILITY_GUTS',            # attack boost
    'Mummy': 'ABILITY_PRESSURE',              # placeholder (contact effect needs new code)
    'Illusion': 'ABILITY_PRESSURE',           # placeholder (Illusion needs big new code)
    'Defeatist': 'ABILITY_NONE',              # a drawback ability: none until Phase 4
    'Iron Barbs': 'ABILITY_ROUGH_SKIN',       # identical effect
    'Big Pecks': 'ABILITY_KEEN_EYE',          # both block one stat drop
    'Overcoat': 'ABILITY_MAGIC_GUARD',        # both stop weather damage
    'Turboblaze': 'ABILITY_MOLD_BREAKER',     # identical effect (message differs)
    'Teravolt': 'ABILITY_MOLD_BREAKER',       # identical effect (message differs)
    'Justified': 'ABILITY_STEADFAST',         # stat boost triggered by the opponent
    'Prankster': 'ABILITY_PRESSURE',          # placeholder (priority change needs new code)
}

# --------------------------------------------------------------------------------------------

def narc_members(path):
    d = path.read_bytes()
    off = struct.unpack_from('<H', d, 12)[0]
    size, count = struct.unpack_from('<II', d, off + 4)
    entries = [struct.unpack_from('<II', d, off + 12 + 8 * i) for i in range(count)]
    off += size
    off += struct.unpack_from('<I', d, off + 4)[0]
    base = off + 8
    return [d[base + s:base + e] for s, e in entries]


GROWTH = ['EXP_RATE_MEDIUM_FAST', 'EXP_RATE_ERRATIC', 'EXP_RATE_FLUCTUATING', 'EXP_RATE_MEDIUM_SLOW',
          'EXP_RATE_FAST', 'EXP_RATE_SLOW']
EGG = ['EGG_GROUP_NONE', 'EGG_GROUP_MONSTER', 'EGG_GROUP_WATER_1', 'EGG_GROUP_BUG', 'EGG_GROUP_FLYING',
       'EGG_GROUP_FIELD', 'EGG_GROUP_FAIRY', 'EGG_GROUP_GRASS', 'EGG_GROUP_HUMAN_LIKE', 'EGG_GROUP_WATER_3',
       'EGG_GROUP_MINERAL', 'EGG_GROUP_AMORPHOUS', 'EGG_GROUP_WATER_2', 'EGG_GROUP_DITTO', 'EGG_GROUP_DRAGON',
       'EGG_GROUP_UNDISCOVERED']
COLORS = ['MON_COLOR_RED', 'MON_COLOR_BLUE', 'MON_COLOR_YELLOW', 'MON_COLOR_GREEN', 'MON_COLOR_BLACK',
          'MON_COLOR_BROWN', 'MON_COLOR_PURPLE', 'MON_COLOR_GRAY', 'MON_COLOR_WHITE', 'MON_COLOR_PINK']
GENDER = {0: 'GENDER_RATIO_MALE_ONLY', 31: 'GENDER_RATIO_FEMALE_12_5', 63: 'GENDER_RATIO_FEMALE_25',
          127: 'GENDER_RATIO_FEMALE_50', 191: 'GENDER_RATIO_FEMALE_75', 223: 'GENDER_RATIO_FEMALE_87_5',
          254: 'GENDER_RATIO_FEMALE_ONLY', 255: 'GENDER_RATIO_NO_GENDER'}


def b2_personal(records, dex):
    rec = records[dex]
    ev = struct.unpack_from('<H', rec, 10)[0]
    items = struct.unpack_from('<3H', rec, 12)
    gender, hatch, friend, growth, eg1, eg2 = struct.unpack_from('<6B', rec, 18)
    flee = rec[27]
    base_exp, height, weight = struct.unpack_from('<3H', rec, 0x22)
    keys = ['hp', 'attack', 'defense', 'speed', 'special_attack', 'special_defense']
    return dict(catch_rate=rec[8], evs={k: (ev >> (2 * i)) & 3 for i, k in enumerate(keys)}, items=items,
                gender=gender, hatch=hatch, friendship=friend, growth=GROWTH[growth],
                egg_groups=[EGG[eg1], EGG[eg2]], flee=flee, color=COLORS[rec[0x21] & 0x3F],
                base_exp=base_exp, height_dm=height, weight_hg=weight)


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper().replace('É', 'E').replace('♀', 'F').replace('♂', 'M'))


def load_constants(path, prefix):
    out = {}
    for line in (ROOT / 'generated' / path).read_text().splitlines():
        c = line.split('=')[0].strip()
        if c.startswith(prefix):
            out[norm(c[len(prefix):])] = c
    return out


# Spreadsheet names whose spelling differs from the decomp's constant (after removing punctuation)
MOVE_ALIASES = {'FEINTATTACK': 'MOVE_FAINT_ATTACK', 'HIGHJUMPKICK': 'MOVE_HI_JUMP_KICK',
                'SMELLINGSALTS': 'MOVE_SMELLING_SALT', 'VISEGRIP': 'MOVE_VICE_GRIP'}


def nearest_vanilla(height_dm, vanilla):
    return min(vanilla, key=lambda v: (abs(v[1] - height_dm), v[0]))[2]


def make_icon(front_sheet, out_path):
    """Placeholder party icon: front sprite shrunk into 32x32, mapped onto the closest shared icon palette."""
    lines = (POKEMON / '.shared' / 'pl_poke_icon.pal').read_text().splitlines()[3:]
    pals = [[tuple(map(int, l.split())) for l in lines[16 * p:16 * p + 16]] for p in range(3)]
    src = Image.open(front_sheet)
    frame = src.crop((0, 0, 80, 80))
    rgba = frame.convert('RGBA')
    px = rgba.load()
    fp = frame.load()
    for y in range(80):
        for x in range(80):
            if fp[x, y] == 0:
                px[x, y] = (0, 0, 0, 0)
    bbox = rgba.getbbox()
    crop = rgba.crop(bbox)
    scale = min(28 / crop.width, 28 / crop.height, 1.0)
    small = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.NEAREST)

    def dist(a, b):
        return sum((x - y) ** 2 for x, y in zip(a, b))

    best = None
    for p, pal in enumerate(pals):
        err = 0
        for c in small.get_flattened_data():
            if c[3] >= 128:
                err += min(dist(c[:3], pal[i]) for i in range(1, 16))
        if best is None or err < best[0]:
            best = (err, p)
    p = best[1]
    pal = pals[p]
    icon = Image.new('P', (32, 64), 0)
    flat = []
    for c in pal:
        flat += list(c)
    icon.putpalette(flat)
    for frame_no, dy in enumerate((0, 1)):
        ox = (32 - small.width) // 2
        oy = 32 * frame_no + (31 - small.height) - dy
        for y in range(small.height):
            for x in range(small.width):
                c = small.getpixel((x, y))
                if c[3] >= 128:
                    idx = min(range(1, 16), key=lambda i: dist(c[:3], pal[i]))
                    icon.putpixel((ox + x, oy + y), idx)
    # dark outline (palette index 15) around the silhouette
    for f in range(2):
        base = icon.copy()
        for y in range(32 * f, 32 * f + 32):
            for x in range(32):
                if base.getpixel((x, y)) == 0 and any(
                        0 <= x + a < 32 and 32 * f <= y + b < 32 * f + 32 and base.getpixel((x + a, y + b)) not in (0, 15)
                        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    icon.putpixel((x, y), 15)
    icon.save(out_path)
    return p


def write_pal(path, palette):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for i in range(16):
            r, g, b = palette[3 * i:3 * i + 3]
            f.write(f'{r} {g} {b}\n')


def copy_sheet(src, dst):
    im = Image.open(src)
    assert im.mode == 'P' and im.size == (160, 80), (src, im.mode, im.size)
    out = Image.new('P', im.size)
    pal = (im.getpalette() + [0] * 48)[:48]
    out.putpalette(pal)
    out.putdata(list(im.get_flattened_data()))
    out.save(dst)
    return pal


def empty_rows_below(png):
    im = Image.open(png).crop((0, 0, 80, 80))
    px = im.load()
    rows = [y for y in range(80) if any(px[x, y] != 0 for x in range(80))]
    return 79 - max(rows) if rows else 0


def convert_cry(src, dst):
    with wave.open(str(src)) as w:
        ch, width, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        data = w.readframes(n)
    assert ch == 1
    if width == 1:
        data = b''.join(struct.pack('<h', (b - 128) << 8) for b in data)
    with wave.open(str(dst), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data)


def main():
    first, last = int(sys.argv[1]), int(sys.argv[2])
    force = '--force' in sys.argv
    report = []
    log = report.append

    wb = openpyxl.load_workbook(SHEET, read_only=True, data_only=True)
    dex_rows = [r for r in list(wb['Pokédex'].iter_rows(values_only=True))[5:] if isinstance(r[0], int)]
    learn_rows = [r for r in list(wb['Learnsets'].iter_rows(values_only=True))[5:] if isinstance(r[0], int)]
    records = narc_members(NARCS / 'species_parameters_and_machine_tutor_flags.narc')

    moves = load_constants('moves.txt', 'MOVE_')
    abilities = load_constants('abilities.txt', 'ABILITY_')
    types = load_constants('pokemon_types.txt', 'TYPE_')
    tm_by_move = {}
    for f in sorted((ROOT / 'res' / 'items' / 'data').glob('[th]m[0-9]*.json')):
        mv = json.loads(f.read_text()).get('teachesMove')
        if mv:
            tm_by_move[mv] = f.stem.upper()
    tutor_moves = {t['move'] for t in json.loads((POKEMON / 'move_tutors.json').read_text())}
    species_consts = (ROOT / 'generated' / 'species.txt').read_text().split()
    items_map = load_constants('items.txt', 'ITEM_')
    import csv
    with open(PACK / 'items_and_moves' / 'items' / 'items.csv', encoding='utf-8-sig') as f:
        b2_item_names = {int(r['id']): r['name'] for r in csv.DictReader(f)}

    vanilla = []
    for c in species_consts[1:494]:
        d = json.loads((POKEMON / c[8:].lower() / 'data.json').read_text())
        h = round(d['pokedex_data']['height_inches'] * 0.254)
        vanilla.append((species_consts.index(c), h, c[8:].lower()))

    def move_const(name):
        k = norm(name)
        if k in MOVE_ALIASES:
            assert MOVE_ALIASES[k] in moves.values(), MOVE_ALIASES[k]
            return MOVE_ALIASES[k]
        return moves.get(k)

    for dex in range(first, last + 1):
        rows = [r for r in dex_rows if r[0] == dex]
        base = rows[0]
        name = base[1]
        stem = norm(name).lower()
        const = f'SPECIES_{norm(name)}'
        d = POKEMON / stem
        if d.exists() and not force:
            log(f'{name}: already exists, skipped')
            continue
        d.mkdir(exist_ok=True)
        log(f'== #{dex} {name} ({const})')

        b2 = b2_personal(records, dex)
        hp, atk, de, spa, spd, spe = base[4:10]
        tlist = [types.get(norm(t)) for t in base[3].split(' / ')]
        if len(tlist) == 1:
            tlist.append(tlist[0])

        abil, missing = [], []
        for a in base[11:13]:
            if not a:
                continue
            real = abilities.get(norm(a))
            c = real or ABILITY_STANDINS.get(a)
            if c is None:
                missing.append(a)
            elif real is None:
                log(f'  ability "{a}" does not exist yet -> stand-in {c} (Phase 4)')
            abil.append(c)
        valid = [c for c in abil if c]
        if not valid and base[13] and abilities.get(norm(base[13])):
            valid = [abilities[norm(base[13])]]  # nothing usable: fall back to the Hidden Ability
        for a in missing:
            log(f'  ability "{a}" does not exist yet -> stand-in {valid[0] if valid else "ABILITY_NONE"} (Phase 4)')
        abil = [c or (valid[0] if valid else 'ABILITY_NONE') for c in abil]
        if len(abil) == 2 and abil[0] == abil[1]:
            abil[1] = 'ABILITY_NONE'
        while len(abil) < 2:
            abil.append('ABILITY_NONE')
        if base[13]:
            log(f'  hidden ability "{base[13]}" not used (Platinum has no Hidden Abilities)')

        by_level, by_tm, by_tutor, egg = [], [], [], []
        for r in learn_rows:
            if r[0] != dex or (r[2] and len(rows) > 1 and r[2] != rows[0][2]):
                continue
            method, level, tm, mv = r[3], r[4], r[5], r[6]
            c = move_const(mv)
            if c is None:
                log(f'  {method} move "{mv}" does not exist yet -> skipped')
                continue
            if method == 'Level up':
                by_level.append([int(level), c])
            elif method in ('TM', 'HM'):
                t = tm_by_move.get(c)
                if t is None and c in tutor_moves:
                    if c not in by_tutor:
                        by_tutor.append(c)  # e.g. Dive: an HM in Black 2, a tutor move in Platinum
                elif t is None:
                    log(f'  {tm} {mv}: not a Platinum TM/HM -> skipped')
                elif t not in by_tm:
                    by_tm.append(t)
            elif method == 'Move Tutor':
                if c in tutor_moves:
                    if c not in by_tutor:
                        by_tutor.append(c)
                elif t := tm_by_move.get(c):
                    if t not in by_tm:
                        by_tm.append(t)
                else:
                    log(f'  tutor move {mv}: not a Platinum tutor/TM move -> skipped')
            elif method == 'Egg Move':
                egg.append(c)
        by_level.sort(key=lambda x: x[0])
        by_tm.sort(key=lambda t: (t[0] == 'H', int(t[2:])))

        evolutions = []
        if base[15]:
            target = f'SPECIES_{norm(base[15])}'
            req = base[17] or ''
            stone = re.match(r'Use an? (.+)$', req)
            if target not in species_consts:
                log(f'  evolution to {base[15]} ({req}): target not added yet -> skipped')
            elif req == 'Level up' and base[16]:
                evolutions.append(['EVO_LEVEL', int(base[16]), target])
            elif stone and items_map.get(norm(stone.group(1))):
                evolutions.append(['EVO_USE_ITEM', items_map[norm(stone.group(1))], target])
            elif req == 'Level up with high friendship':
                evolutions.append(['EVO_LEVEL_HAPPINESS', target])
            elif req == 'Trade':
                evolutions.append(['EVO_TRADE', target])
            elif (m := re.match(r'Trade for (\w+)', req)) and f'SPECIES_{norm(m.group(1))}' in species_consts:
                # Karrablast / Shelmet: level up with the other in the party (like Mantyke + Remoraid)
                evolutions.append(['EVO_LEVEL_SPECIES_IN_PARTY', f'SPECIES_{norm(m.group(1))}', target])
                log(f'  evolution: level up with {m.group(1)} in the party (replaces the Black 2 trade)')
            else:
                log(f'  EVOLUTION NEEDS A DECISION: {base[15]} ({req}) -> skipped')

        offspring = const
        if base[14]:
            prev = base[14]
            while True:
                pr = [r for r in dex_rows if r[1] == prev]
                if pr and pr[0][14]:
                    prev = pr[0][14]
                else:
                    break
            offspring = f'SPECIES_{norm(prev)}'

        # sprites
        sheets = PACK / 'pokemon_sprites' / 'sheets'
        stem_png = f'{dex}-{name}.png'
        gendered = not (sheets / 'normal' / 'front' / stem_png).exists() and (sheets / 'normal' / 'front' / f'{dex}-{name}-Male.png').exists()
        if not gendered and not (sheets / 'normal' / 'front' / stem_png).exists():
            # species with alternate forms: the base species uses the first form row's art
            form = (base[2] or '').replace(' Forme', '').replace(' Form', '').replace(' Mode', '').replace(' ', '-')
            cands = sorted((sheets / 'normal' / 'front').glob(f'{dex}-{name}-*.png'))
            pick = [c for c in cands if form and c.stem.endswith(form)] or [c for c in cands if c.stem.split('-', 2)[-1] in ('Spring', 'Normal', 'No-Drive', 'Ordinary')] or cands
            stem_png = pick[0].name
            log(f'  base form art: {stem_png} (other forms not added yet)')
        if gendered:
            stem_png = f'{dex}-{name}-Male.png'
            fem_png = f'{dex}-{name}-Female.png'
            copy_sheet(sheets / 'normal' / 'front' / fem_png, d / 'female_front.png')
            copy_sheet(sheets / 'normal' / 'back' / fem_png, d / 'female_back.png')
            log('  separate female sprites')
        normal_pal = copy_sheet(sheets / 'normal' / 'front' / stem_png, d / 'male_front.png')
        copy_sheet(sheets / 'normal' / 'back' / stem_png, d / 'male_back.png')
        # the game loads the female slot for every female mon; like vanilla, species that
        # can be female without a visual difference get copies of the male sprites
        can_be_female = GENDER[b2['gender']] not in ('GENDER_RATIO_MALE_ONLY', 'GENDER_RATIO_NO_GENDER')
        has_female = gendered or can_be_female
        if has_female and not gendered:
            shutil.copy(d / 'male_front.png', d / 'female_front.png')
            shutil.copy(d / 'male_back.png', d / 'female_back.png')
        shiny_pal = Image.open(sheets / 'shiny' / 'front' / stem_png).getpalette()[:48]
        write_pal(d / 'normal.pal', normal_pal)
        write_pal(d / 'shiny.pal', (shiny_pal + [0] * 48)[:48])

        template = nearest_vanilla(b2['height_dm'], vanilla)
        tdata = json.loads((POKEMON / template / 'data.json').read_text())
        tsprite = json.loads((POKEMON / template / 'sprite_data.json').read_text())
        sprite = json.loads(json.dumps(tsprite))
        fy, by = empty_rows_below(d / 'male_front.png'), empty_rows_below(d / 'male_back.png')
        ffy, fby = (empty_rows_below(d / 'female_front.png'), empty_rows_below(d / 'female_back.png')) if has_female else (fy, by)
        sprite['front']['y_offset'] = {'female': ffy, 'male': fy}
        sprite['back']['y_offset'] = {'female': fby, 'male': by}
        hm = b2['height_dm'] / 10
        sprite['shadow']['size'] = 'SHADOW_SIZE_SMALL' if hm < 1.0 else 'SHADOW_SIZE_MEDIUM' if hm < 2.0 else 'SHADOW_SIZE_LARGE'
        sprite['shadow']['x_offset'] = 0
        (d / 'sprite_data.json').write_text(json.dumps(sprite, indent=4, ensure_ascii=False) + '\n')
        # nitrogfx needs the 4-byte encryption seed next to each sprite; any seed works, the game
        # reads it back from the encoded data
        for f in ('male_front.png', 'male_back.png') + (('female_front.png', 'female_back.png') if has_female else ()):
            (d / f'{f}.key').write_bytes((POKEMON / 'charmander' / f'male_{f.split("_")[1]}.key').read_bytes())
        log(f'  sprite animation, Pokedex scale/position copied from {template} (similar height)')

        icon_pal = make_icon(sheets / 'normal' / 'front' / stem_png, d / 'icon.png')
        log('  PLACEHOLDER party icon (shrunk front sprite)')
        (POKEMON / 'anorith' / 'footprint.png').read_bytes()
        (d / 'footprint.png').write_bytes((POKEMON / 'anorith' / 'footprint.png').read_bytes())

        cry = PACK / 'audio' / 'gen5_cries' / 'wav' / f'{dex}_{name.lower()}.wav'
        convert_cry(cry, d / 'cry.wav')
        (d / 'cry.txt').write_text((POKEMON / 'bulbasaur' / 'cry.txt').read_text())

        items = []
        for iid in b2['items'][:2]:
            if iid == 0:
                items.append('ITEM_NONE')
                continue
            c = items_map.get(norm(b2_item_names.get(iid, '')))
            if c is None:
                log(f'  wild held item {b2_item_names.get(iid, iid)} does not exist in Platinum -> ITEM_NONE')
            items.append(c or 'ITEM_NONE')

        en_name = name.upper()
        cat = CATEGORIES.get(name, 'Unova') + ' Pokémon'
        entry = ['Pokédex data for this Pokémon\n', 'has not been added yet.']
        langs = {}
        for lang in ('en', 'fr', 'de', 'it', 'es', 'jp'):
            langs[lang] = {'name': en_name, 'category': cat, 'entry_text': entry}
        pdex = {k: v for k, v in tdata['pokedex_data'].items() if k not in ('en', 'fr', 'de', 'it', 'es', 'jp')}
        pdex['height_inches'] = round(b2['height_dm'] / 0.254)
        pdex['weight_pounds'] = round(b2['weight_hg'] * 0.220462, 1)
        pdex['body_shape'] = BODY_SHAPES.get(name, tdata['pokedex_data']['body_shape'])
        pdex.update(langs)

        data = {
            'base_stats': {'hp': hp, 'attack': atk, 'defense': de, 'speed': spe, 'special_attack': spa, 'special_defense': spd},
            'types': tlist,
            'catch_rate': b2['catch_rate'],
            'base_exp_reward': min(b2['base_exp'], 255),
            'ev_yields': b2['evs'],
            'held_items': {'common': items[0], 'rare': items[1]},
            'gender_ratio': GENDER[b2['gender']],
            'hatch_cycles': b2['hatch'],
            'base_friendship': b2['friendship'],
            'exp_rate': b2['growth'],
            'egg_groups': b2['egg_groups'],
            'abilities': abil[:2],
            'safari_flee_rate': 0,
            'body_color': b2['color'],
            'flip_sprite': False,
            'icon_palette': icon_pal,
            'learnset': {'by_level': by_level, 'by_tm': by_tm, 'by_tutor': by_tutor, 'egg_moves': egg},
            'evolutions': evolutions,
            'offspring': offspring,
            'footprint': {'has': False, 'size': 'FOOTPRINT_SMALL', 'type': 'FOOTPRINT_TYPE_SILENT'},
            'pokedex_data': pdex,
            'catching_show': {'pal_park_land_area': 'PAL_PARK_AREA_LAND_NONE', 'pal_park_water_area': 'PAL_PARK_AREA_WATER_NONE',
                              'catching_points': 0, 'rarity': 0, 'unused': 0},
        }
        if b2['base_exp'] > 255:
            log(f'  base EXP {b2["base_exp"]} > 255 (Platinum limit) -> 255')
        (d / 'data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')
        fem = "pokegra_files += files('female_back.png')\n" if has_female else ''
        fem2 = "pokegra_files += files('female_front.png')\n" if has_female else ''
        (d / 'meson.build').write_text(
            "species_data_files += files('data.json', 'sprite_data.json')\n\n"
            "poke_icon_files += files('icon.png')\n\n"
            + fem + "pokegra_files += files('male_back.png')\n"
            + fem2 + "pokegra_files += files('male_front.png')\n\n"
            "pokefoot_files += files('footprint.png')\n")
        log('  PLACEHOLDER Pokedex entry text and foreign names (English); no footprint')

    out = PACK / f'import_report_{first}_{last}.txt'
    out.write_text('\n'.join(report) + '\n')
    print('\n'.join(report))


if __name__ == '__main__':
    main()
