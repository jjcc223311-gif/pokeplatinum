#!/usr/bin/env python3
"""Import Mega forms from the sprite packs in tools/mega_pack/ into res/pokemon.

For each requested species this:
  - copies the pack's 160x80 indexed front/back PNGs to res/pokemon/<species>/forms/mega_<N>/
    (the same files existing forms use, e.g. res/pokemon/deoxys/forms/attack/),
  - reuses the base species' .key files (the game reads the sprite seed from the data itself),
  - writes normal.pal from the PNGs' shared 16-colour palette,
  - generates shiny.pal from the species' own normal -> shiny colour changes (see make_shiny),
  - writes data.json (the base species' data with the Mega's stats, types and ability),
  - adds / updates the species' row in res/pokemon/mega_forms.json.

Usage: import_mega_pack.py Lucario Charizard ...   (names as in MEGA_DATA)
Needs Pillow. tools/mega_pack/ is git-ignored; unzip the packs there first.
"""
import argparse
import colorsys
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

from scale_mega_sprite import scale as scale_sprite  # packs draw in 64x64; scale up to match vanilla

ROOT = Path(__file__).resolve().parents[2]
PACK_DIRS = [
    ROOT / 'tools/mega_pack/main/Platinum_Mega_Sprite_Pack/03_Indexed_PNG',
    ROOT / 'tools/mega_pack/five/Platinum_Five_Mega_Sprite_Pack/03_Indexed_PNG',
]
# A suffix written 'mega18:Mega' only looks in this pack (Steelix-Mega is in two packs)
NAMED_PACKS = {
    'mega18': ROOT / 'tools/mega_pack/mega18/Platinum_18_Mega_Sprite_Pack/03_Indexed_PNG',
    'mega21': ROOT / 'tools/mega_pack/mega21/Platinum_21_Mega_Expansion_Pack/03_Indexed_PNG',
    'leg24': ROOT / 'tools/mega_pack/legendary24/Platinum_24_Legendary_Mega_Sprite_Pack_v4/03_Indexed_PNG',
}
POKEMON = ROOT / 'res/pokemon'
MEGA_TABLE = POKEMON / 'mega_forms.json'

# name: [(form number, pack folder suffix, types, (hp, atk, def, spa, spd, spe), ability), ...]
# Mega 1 = form 29 (folder mega_1), Mega 2 = form 28 (folder mega_2).
# Abilities marked "stand-in" in the TODO list replace Mega abilities that don't exist in Gen 4.
# The 18-Mega pack's forms use this mod's own abilities (Mind Sanctuary ... Prismatic Armor).
MEGA_DATA = {
    'Abomasnow': [(1, 'Mega', ('GRASS', 'ICE'), (90, 132, 105, 132, 105, 60), 'SNOW_WARNING')],
    'Banette': [(1, 'Mega', ('GHOST', 'NORMAL'), (64, 165, 75, 93, 83, 75), 'INSOMNIA')],
    'Kingler': [(1, 'Mega', ('WATER', 'STEEL'), (55, 150, 130, 50, 75, 110), 'HYPER_CUTTER')],
    'Aerodactyl': [(1, 'Mega', ('ROCK', 'FLYING'), (80, 135, 85, 70, 95, 150), 'ROCK_HEAD')],
    'Aggron': [(1, 'Mega', ('STEEL',), (70, 140, 230, 60, 80, 50), 'FILTER')],
    'Alakazam': [(1, 'Mega', ('PSYCHIC', 'LIGHT'), (55, 50, 65, 175, 105, 150), 'TRACE')],
    'Altaria': [(1, 'Mega', ('DRAGON', 'FAIRY'), (85, 110, 110, 110, 105, 80), 'CLOUD_NINE')],
    'Beedrill': [(1, 'Mega', ('BUG', 'POISON'), (65, 150, 40, 15, 80, 145), 'ADAPTABILITY')],
    'Blastoise': [(1, 'Mega', ('WATER',), (79, 103, 120, 135, 115, 78), 'TORRENT')],
    'Blaziken': [(1, 'Mega', ('FIRE', 'FIGHTING'), (80, 160, 80, 130, 80, 100), 'SPEED_BOOST')],
    'Butterfree': [(1, 'Mega', ('BUG', 'FLYING'), (60, 45, 100, 140, 100, 80), 'COMPOUND_EYES')],
    'Camerupt': [(1, 'Mega', ('FIRE', 'GROUND'), (90, 100, 110, 145, 115, 20), 'SOLID_ROCK')],
    'Charizard': [
        (1, 'Mega-X', ('FIRE', 'DRAGON'), (78, 130, 111, 130, 85, 100), 'BLAZE'),
        (2, 'Mega-Y', ('FIRE', 'LIGHT'), (78, 104, 78, 159, 115, 100), 'DROUGHT'),
    ],
    'Gardevoir': [(1, 'Mega', ('FAIRY', 'LIGHT'), (68, 85, 65, 165, 135, 100), 'TRACE')],
    'Gengar': [(1, 'Mega', ('GHOST', 'POISON'), (60, 65, 80, 170, 95, 130), 'SHADOW_TAG')],
    'Glalie': [(1, 'Mega', ('ICE',), (80, 135, 80, 105, 80, 100), 'ICE_BODY')],
    'Gyarados': [(1, 'Mega', ('WATER', 'DARK'), (95, 155, 109, 70, 130, 81), 'MOLD_BREAKER')],
    'Heracross': [(1, 'Mega', ('BUG', 'FIGHTING'), (80, 185, 115, 40, 105, 75), 'SKILL_LINK')],
    'Kangaskhan': [(1, 'Mega', ('NORMAL',), (105, 125, 100, 60, 100, 100), 'SCRAPPY')],
    'Lapras': [(1, 'Mega', ('WATER', 'DRAGON'), (130, 105, 90, 115, 105, 70), 'WATER_ABSORB')],
    'Latias': [(1, 'Mega', ('DRAGON', 'LIGHT'), (80, 100, 120, 140, 150, 110), 'LEVITATE')],
    'Latios': [(1, 'Mega', ('DRAGON', 'LIGHT'), (80, 130, 100, 160, 120, 110), 'LEVITATE')],
    'Lopunny': [(1, 'Mega', ('FIGHTING', 'LIGHT'), (65, 136, 94, 54, 96, 135), 'SCRAPPY')],
    'Lucario': [
        (1, 'Mega', ('FIGHTING', 'LIGHT'), (70, 145, 88, 140, 70, 112), 'ADAPTABILITY'),
        (2, 'mega18:2', ('FIGHTING', 'LIGHT'), (70, 190, 110, 180, 105, 150), 'AURA_OVERDRIVE'),
    ],
    'Machamp': [
        (1, 'Mega', ('FIGHTING', 'LIGHT'), (90, 145, 110, 65, 115, 75), 'NO_GUARD'),
        (2, 'mega18:2', ('FIGHTING', 'LIGHT'), (90, 220, 150, 65, 140, 125), 'TITANS_GRIP'),
    ],
    'Manectric': [(1, 'Mega', ('ELECTRIC',), (70, 75, 80, 135, 80, 135), 'INTIMIDATE')],
    'Mawile': [(1, 'Mega', ('STEEL', 'FAIRY'), (50, 105, 125, 55, 95, 50), 'HUGE_POWER')],
    'Medicham': [(1, 'Mega', ('FIGHTING', 'PSYCHIC'), (60, 100, 85, 80, 85, 100), 'PURE_POWER')],
    'Metagross': [(1, 'Mega', ('STEEL', 'PSYCHIC'), (80, 145, 150, 105, 110, 110), 'CLEAR_BODY')],
    'Mewtwo': [
        (1, 'Mega-X', ('PSYCHIC', 'FIGHTING'), (106, 190, 100, 154, 100, 130), 'STEADFAST'),
        (2, 'Mega-Y', ('PSYCHIC', 'LIGHT'), (106, 150, 70, 194, 120, 140), 'INSOMNIA'),
    ],
    'Pidgeot': [(1, 'Mega', ('NORMAL', 'FLYING'), (83, 80, 80, 135, 80, 121), 'NO_GUARD')],
    'Pinsir': [(1, 'Mega', ('BUG', 'FLYING'), (65, 155, 120, 65, 90, 105), 'MOLD_BREAKER')],
    'Rayquaza': [(1, 'Mega', ('DRAGON', 'FLYING'), (105, 180, 100, 180, 100, 115), 'AIR_LOCK')],
    'Sableye': [(1, 'Mega', ('DARK', 'GHOST'), (50, 85, 125, 85, 115, 20), 'STALL')],
    'Salamence': [(1, 'Mega', ('DRAGON', 'FLYING'), (95, 145, 130, 120, 90, 120), 'INTIMIDATE')],
    'Sceptile': [(1, 'Mega', ('GRASS', 'DRAGON'), (70, 135, 75, 110, 85, 145), 'TECHNICIAN')],
    'Scizor': [(1, 'Mega', ('BUG', 'STEEL'), (70, 150, 140, 65, 100, 75), 'TECHNICIAN')],
    'Sharpedo': [(1, 'Mega', ('WATER', 'DARK'), (70, 140, 70, 110, 65, 105), 'ROUGH_SKIN')],
    'Slowbro': [(1, 'Mega', ('WATER', 'PSYCHIC'), (95, 75, 180, 130, 80, 30), 'SHELL_ARMOR')],
    'Snorlax': [(1, 'Mega', ('NORMAL', 'GRASS'), (160, 160, 85, 80, 125, 30), 'THICK_FAT')],
    'Steelix': [
        (1, 'Mega', ('STEEL', 'GROUND'), (75, 125, 230, 55, 95, 30), 'HEATPROOF'),
        (2, 'mega18:Mega', ('GROUND', 'ELECTRIC'), (75, 180, 250, 55, 180, 40), 'PRISMATIC_ARMOR'),
    ],
    'Swampert': [(1, 'Mega', ('WATER', 'GROUND'), (100, 150, 110, 95, 110, 70), 'SWIFT_SWIM')],
    'Tyranitar': [(1, 'Mega', ('ROCK', 'DARK'), (100, 164, 150, 95, 120, 71), 'SAND_STREAM')],
    'Uxie': [(1, 'mega18:Mega', ('ELECTRIC', 'LIGHT'), (75, 75, 200, 120, 200, 120), 'MIND_SANCTUARY')],
    'Mesprit': [(1, 'mega18:Mega', ('FAIRY', 'LIGHT'), (80, 140, 135, 150, 135, 150), 'HEARTLINK')],
    'Azelf': [(1, 'mega18:Mega', ('WATER', 'LIGHT'), (75, 165, 100, 165, 100, 190), 'WILL_IGNITION')],
    'Arceus': [(1, 'mega18:Mega', ('LIGHT',), (120, 145, 135, 155, 135, 145), 'DIVINE_EDICT')],
    'Electivire': [(1, 'mega18:Mega', ('ELECTRIC', 'LIGHT'), (75, 200, 120, 120, 110, 165), 'LIVE_WIRE')],
    'Roserade': [(1, 'mega18:Mega', ('GRASS', 'LIGHT'), (60, 95, 110, 200, 150, 165), 'THORN_BLOOM')],
    'Lumineon': [(1, 'mega18:Mega', ('WATER', 'LIGHT'), (69, 90, 130, 185, 150, 156), 'PRISM_TIDE')],
    'Cresselia': [(1, 'mega18:Mega', ('PSYCHIC', 'LIGHT'), (120, 70, 180, 135, 185, 100), 'LUNAR_REFUGE')],
    'Palkia': [(1, 'mega18:Mega', ('WATER', 'LIGHT'), (90, 140, 125, 210, 135, 125), 'SPATIAL_RUPTURE')],
    'Giratina': [(1, 'mega18:Mega', ('GHOST', 'LIGHT'), (150, 160, 150, 160, 135, 75), 'DISTORTION_VEIL')],
    'Dialga': [(1, 'mega18:Mega', ('STEEL', 'LIGHT'), (100, 145, 175, 200, 135, 75), 'TIME_SOVEREIGN')],
    'Infernape': [(1, 'mega18:Mega', ('FIGHTING', 'LIGHT'), (76, 180, 105, 180, 105, 159), 'BLAZING_MIND')],
    'Empoleon': [(1, 'mega18:Mega', ('ELECTRIC', 'STEEL'), (84, 115, 160, 195, 160, 86), 'ROYAL_AEGIS')],
    'Torterra': [(1, 'mega18:Mega', ('GRASS', 'LIGHT'), (95, 190, 200, 85, 160, 70), 'WORLDROOT')],
    'Luxray': [(1, 'mega18:Mega', ('ELECTRIC', 'LIGHT'), (80, 200, 110, 135, 105, 160), 'PREDATOR_VOLT')],
    'Venusaur': [(1, 'Mega', ('GRASS', 'LIGHT'), (80, 100, 123, 122, 120, 80), 'THICK_FAT')],
    # 21-Mega pack (replaces the older Ampharos / Absol / Houndoom / Gallade / Garchomp Megas).
    # Stand-in abilities until the real ones are built (see MEGA_TODO.md).
    'Raichu': [
        (1, 'mega21:Mega-X', ('ELECTRIC',), (60, 135, 95, 90, 95, 110), 'ELECTRIC_SURGE'),
        (2, 'mega21:Mega-Y', ('ELECTRIC', 'LIGHT'), (60, 100, 55, 160, 80, 130), 'NO_GUARD'),
    ],
    'Ampharos': [(1, 'mega21:Mega', ('LIGHT', 'DRAGON'), (90, 95, 105, 165, 110, 45), 'MOLD_BREAKER')],
    'Houndoom': [(1, 'mega21:Mega', ('DARK', 'FIRE'), (75, 90, 90, 140, 90, 115), 'SOLAR_POWER')],
    'Milotic': [(1, 'mega21:Mega', ('FAIRY', 'LIGHT'), (95, 70, 130, 160, 180, 95), 'PEARL_RADIANCE')],
    'Absol': [
        (1, 'mega21:Mega', ('DARK',), (65, 150, 60, 115, 60, 115), 'MAGIC_BOUNCE'),
        (2, 'mega21:Mega-Z', ('DARK', 'GHOST'), (65, 154, 60, 75, 60, 151), 'SHARPNESS'),
    ],
    'Bastiodon': [(1, 'mega21:Mega', ('LIGHT', 'STEEL'), (60, 110, 230, 70, 215, 40), 'FILTER')],
    'Floatzel': [(1, 'mega21:Mega', ('WATER', 'LIGHT'), (85, 165, 90, 110, 80, 160), 'TIDE_RUSH')],
    'Mismagius': [(1, 'mega21:Mega', ('GHOST', 'FAIRY'), (60, 75, 100, 185, 150, 145), 'HEXWEAVER')],
    'Purugly': [(1, 'mega21:Mega', ('NORMAL', 'FAIRY'), (71, 154, 110, 85, 100, 155), 'SILK_SWIPE')],
    'Skuntank': [(1, 'mega21:Mega', ('POISON', 'DARK'), (103, 152, 105, 115, 110, 115), 'FUME_CLOUD')],
    'Garchomp': [
        (1, 'mega21:Mega', ('DRAGON', 'GROUND'), (108, 170, 115, 120, 95, 92), 'SAND_FORCE'),
        (2, 'mega21:Mega-Z', ('DRAGON', 'FIRE'), (108, 130, 85, 141, 85, 151), 'LEVITATE'),
    ],
    'Drapion': [(1, 'mega21:Mega', ('POISON', 'DARK'), (70, 150, 165, 80, 125, 130), 'AMBUSH_FANGS')],
    'Toxicroak': [(1, 'mega21:Mega', ('POISON', 'FIGHTING'), (83, 166, 100, 120, 100, 131), 'TOXIC_FISTS')],
    'Weavile': [(1, 'mega21:Mega', ('DARK', 'ICE'), (70, 185, 95, 65, 120, 175), 'WINTER_CHASE')],
    'Rhyperior': [(1, 'mega21:Mega', ('GROUND', 'ROCK'), (115, 200, 180, 70, 130, 55), 'STONE_ENGINE')],
    'Magmortar': [(1, 'mega21:Mega', ('FIRE', 'DARK'), (75, 135, 105, 205, 130, 90), 'FURNACE_SPARK')],
    'Gallade': [(1, 'mega21:Mega', ('PSYCHIC', 'FIGHTING'), (68, 165, 95, 65, 115, 110), 'INNER_FOCUS')],
    'Froslass': [(1, 'mega21:Mega', ('LIGHT', 'GHOST'), (70, 80, 70, 140, 100, 120), 'RIME_CALLER')],
}


# Legendary Megas (Legendary button): form 30 = Legendary Mega 1 (folder legendary_1, table key
# legendary_mega_1). Same tuple layout as MEGA_DATA. Stand-in abilities until Stage 8.
LEGENDARY_DATA = {
    'Floatzel': [(1, 'leg24:Legendary-Mega', ('WATER', 'LIGHT'), (115, 170, 105, 100, 105, 185), 'WAKE_RUNNER')],
    'Electivire': [(1, 'leg24:Legendary-Mega', ('ELECTRIC', 'LIGHT'), (105, 185, 120, 130, 120, 140), 'CROSSWIRE')],
    'Gallade': [(1, 'leg24:Legendary-Mega', ('PSYCHIC', 'FIGHTING'), (100, 190, 130, 90, 150, 140), 'ROYAL_PARRY')],
    'Magmortar': [(1, 'leg24:Legendary-Mega', ('FIRE', 'DARK'), (110, 130, 110, 200, 140, 105), 'CANNON_SALVO')],
    'Mismagius': [(1, 'leg24:Legendary-Mega', ('GHOST', 'FAIRY'), (100, 85, 105, 175, 155, 160), 'MOONLIT_HEX')],
    'Bastiodon': [(1, 'leg24:Legendary-Mega', ('LIGHT', 'STEEL'), (125, 100, 220, 75, 205, 55), 'FOSSIL_CITADEL')],
    'Froslass': [(1, 'leg24:Legendary-Mega', ('LIGHT', 'GHOST'), (95, 100, 100, 180, 135, 175), 'PALE_MIRAGE')],
    'Drapion': [(1, 'leg24:Legendary-Mega', ('POISON', 'DARK'), (105, 170, 165, 85, 115, 140), 'VENOM_LEVERAGE')],
    'Rhyperior': [(1, 'leg24:Legendary-Mega', ('GROUND', 'ROCK'), (140, 195, 200, 85, 120, 50), 'SEISMIC_BREAKER')],
    'Garchomp': [(1, 'leg24:Legendary-Mega', ('DRAGON', 'GROUND'), (125, 200, 140, 125, 110, 120), 'DUNE_PURSUIT')],
    'Giratina': [(1, 'leg24:Legendary-Mega', ('GHOST', 'LIGHT'), (175, 145, 140, 145, 130, 90), 'DISTORTION_GATE')],
    'Palkia': [(1, 'leg24:Legendary-Mega', ('WATER', 'LIGHT'), (110, 145, 125, 190, 130, 125), 'RIFT_PIERCE')],
    'Dialga': [(1, 'leg24:Legendary-Mega', ('STEEL', 'LIGHT'), (125, 135, 155, 190, 125, 95), 'TIME_LOCK')],
    'Infernape': [(1, 'leg24:Legendary-Mega', ('FIGHTING', 'LIGHT'), (105, 165, 105, 165, 105, 155), 'EMPEROR_MANTLE')],
    'Empoleon': [(1, 'leg24:Legendary-Mega', ('ELECTRIC', 'STEEL'), (110, 115, 140, 175, 155, 95), 'ROYAL_INSULATE')],
    'Torterra': [(1, 'leg24:Legendary-Mega', ('GRASS', 'LIGHT'), (135, 175, 175, 110, 135, 60), 'LIVING_TERRACE')],
    'Luxray': [(1, 'leg24:Legendary-Mega', ('ELECTRIC', 'LIGHT'), (110, 190, 125, 110, 115, 145), 'GILDED_CLAWS')],
    'Lucario': [(1, 'leg24:Legendary-Mega', ('FIGHTING', 'LIGHT'), (100, 175, 110, 175, 105, 145), 'AURA_CONVERGE')],
    'Blastoise': [(1, 'leg24:Legendary-Mega', ('WATER',), (110, 130, 155, 170, 145, 85), 'SIEGE_RESERVOIR')],
    'Gengar': [(1, 'leg24:Legendary-Mega', ('GHOST', 'POISON'), (95, 95, 110, 195, 125, 185), 'THIRD_EYE_CURSE')],
    'Ampharos': [(1, 'leg24:Legendary-Mega', ('LIGHT', 'DRAGON'), (125, 115, 130, 195, 155, 70), 'RUBY_CONDUIT')],
    'Absol': [(1, 'leg24:Legendary-Mega', ('DARK',), (100, 190, 100, 145, 105, 150), 'OMEN_WINGS')],
    'Houndoom': [(1, 'leg24:Legendary-Mega', ('DARK', 'FIRE'), (105, 115, 110, 190, 120, 155), 'AZURE_WILDFIRE')],
    'Milotic': [(1, 'leg24:Legendary-Mega', ('FAIRY', 'LIGHT'), (135, 85, 125, 160, 180, 105), 'PRISMATIC_GRACE')],
}

def find_pack_folder(name, suffix):
    packs = PACK_DIRS
    if ':' in suffix:
        pack_name, suffix = suffix.split(':')
        packs = [NAMED_PACKS[pack_name]]
    for pack in packs:
        hits = sorted(pack.glob(f'*_{name}-{suffix}'))
        if hits:
            return hits[0]
    sys.exit(f'error: no pack folder for {name}-{suffix}')


def read_jasc(path):
    lines = path.read_text().split()
    count = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i * 3:6 + i * 3]) for i in range(count)]


def write_jasc(path, colours):
    with open(path, 'w', newline='\r\n') as f:
        f.write(f'JASC-PAL\n0100\n{len(colours)}\n')
        for c in colours:
            f.write(f'{c[0]} {c[1]} {c[2]}\n')


def to_ds(c):
    # DS colours are 5 bits per channel: keep the values the pack already uses (multiples of 8ish)
    return tuple(max(0, min(255, (v >> 3) << 3 | (v >> 5))) for v in c)


def make_shiny(mega_colours, base_normal, base_shiny):
    """Recolour the Mega the way the species' own shiny recolours its normal form.

    For each Mega colour, find the closest colour in the base species' normal palette (by
    distance in RGB) and apply that colour's normal -> shiny change to it: the hue shift, and
    the saturation / value ratios. So areas that are e.g. orange on Charizard (black when shiny)
    change the same way on the Mega, while colours the base form doesn't have only take on the
    nearest colour's change. Index 0 (transparency) is kept."""
    pairs = [(n, s) for n, s in zip(base_normal[1:], base_shiny[1:]) if n != s]
    if not pairs:  # the species' shiny only changes colours the Mega lacks: keep a copy
        pairs = list(zip(base_normal[1:], base_shiny[1:]))

    out = [mega_colours[0]]
    for c in mega_colours[1:]:
        n, s = min(pairs, key=lambda p: sum((a - b) ** 2 for a, b in zip(p[0], c)))
        hn, sn, vn = colorsys.rgb_to_hsv(*(v / 255 for v in n))
        hs, ss, vs = colorsys.rgb_to_hsv(*(v / 255 for v in s))
        h, sat, val = colorsys.rgb_to_hsv(*(v / 255 for v in c))
        if sn < 0.2:
            # A greyish base colour has no reliable hue, and scaling a tiny saturation blows up
            # small differences into noise (e.g. grey Steelix -> gold): take the shiny's hue and
            # saturation directly
            h, sat = hs, ss
        else:
            h = (h + (hs - hn)) % 1.0
            sat = min(1.0, sat * (ss / sn))
        val = min(1.0, val * (vs / vn)) if vn > 0.05 else vs
        r, g, b = colorsys.hsv_to_rgb(h, sat, val)
        out.append(to_ds((round(r * 255), round(g * 255), round(b * 255))))
    return out


def base_key(species_dir, face):
    for gender in ('male', 'female'):
        key = species_dir / f'{gender}_{face}.png.key'
        if key.exists():
            return key
    sys.exit(f'error: no {face} .key in {species_dir}')


def import_form(name, number, suffix, types, stats, ability, kind='mega'):
    species = name.lower()
    species_dir = POKEMON / species
    src = find_pack_folder(name, suffix)
    folder = f'{kind}_{number}'  # mega_1 / mega_2 / legendary_1 / legendary_2
    dst = species_dir / 'forms' / folder
    dst.mkdir(parents=True, exist_ok=True)

    front = Image.open(src / 'front_160x80_TWO_IDENTICAL_FRAMES.png')
    back = Image.open(src / 'back_160x80_TWO_IDENTICAL_FRAMES.png')
    for face, img in (('front', front), ('back', back)):
        assert img.mode == 'P' and img.size == (160, 80), f'{src}: {face} is not a 160x80 indexed PNG'
        scaled = scale_sprite(face, img)
        scaled.save(dst / f'{face}.png', bits=4, **({'transparency': img.info['transparency']} if 'transparency' in img.info else {}))
        shutil.copyfile(base_key(species_dir, face), dst / f'{face}.png.key')

    palette = front.getpalette()[:48]
    assert palette == back.getpalette()[:48], f'{src}: front and back palettes differ'
    normal = [tuple(palette[i:i + 3]) for i in range(0, 48, 3)]
    write_jasc(dst / 'normal.pal', normal)
    write_jasc(dst / 'shiny.pal', make_shiny(normal, read_jasc(species_dir / 'normal.pal'), read_jasc(species_dir / 'shiny.pal')))

    # Packs with a high-resolution source render: rebuild the sprites from it (the pack's own 80x80
    # sprites are nearest-neighbour samples that read as a blurry mesh of colours)
    from rebuild_mega_sprites import rebuild_form, source_images
    sources = source_images(src)
    if sources is not None:
        rebuild_form(species, folder, *sources)

    data = json.loads((species_dir / 'data.json').read_text())
    hp, atk, dfn, spa, spd, spe = stats
    data['base_stats'] = {'hp': hp, 'attack': atk, 'defense': dfn, 'speed': spe,
                          'special_attack': spa, 'special_defense': spd}
    data['types'] = [f'TYPE_{types[0]}', f'TYPE_{types[-1]}']
    data['abilities'] = [f'ABILITY_{ability}', 'ABILITY_NONE']
    data['evolutions'] = []
    keep = ['base_stats', 'types', 'catch_rate', 'base_exp_reward', 'ev_yields', 'held_items', 'gender_ratio',
            'hatch_cycles', 'base_friendship', 'exp_rate', 'egg_groups', 'abilities', 'safari_flee_rate',
            'body_color', 'flip_sprite', 'icon_palette', 'learnset', 'evolutions']
    data = {k: data[k] for k in keep if k in data}
    (dst / 'data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')
    return f'{species}/forms/{folder}'


def main():
    argp = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argp.add_argument('names', nargs='+', help='species names as in MEGA_DATA (e.g. Lucario Charizard)')
    argp.add_argument('--legendary', action='store_true',
                      help='import the Legendary Megas (LEGENDARY_DATA) instead of the Megas')
    argp.add_argument('--skip-existing', action='store_true',
                      help="don't re-import forms that already have a folder (e.g. adding a Mega 2)")
    args = argp.parse_args()

    table = json.loads(MEGA_TABLE.read_text())
    data, kind, key = (LEGENDARY_DATA, 'legendary', 'legendary_mega') if args.legendary else (MEGA_DATA, 'mega', 'mega')
    for name in args.names:
        if name not in data:
            sys.exit(f'error: {name} is not in {"LEGENDARY_DATA" if args.legendary else "MEGA_DATA"}')

        species_const = f'SPECIES_{name.upper()}'
        row = next((r for r in table if r['species'] == species_const), None)
        if row is None:
            row = {'species': species_const}
            table.append(row)

        for number, suffix, types, stats, ability in data[name]:
            if args.skip_existing and (POKEMON / name.lower() / 'forms' / f'{kind}_{number}').exists():
                print(f'{name}: {kind} {number} already imported, skipped')
                continue
            row[f'{key}_{number}'] = import_form(name, number, suffix, types, stats, ability, kind)
            print(f'{name}: {kind} {number} <- {suffix}')

    MEGA_TABLE.write_text(json.dumps(table, indent=4) + '\n')


if __name__ == '__main__':
    main()
