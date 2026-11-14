#!/usr/bin/env python3
"""Create res/moves/<move>/ for the Gen 5 moves (468-559) from the move pack.

usage: import_gen5_moves.py [--force]

Source of truth: tools/gen5_pack/items_and_moves/moves/gen5_moves.csv (type, power, accuracy, PP,
category, priority, effect chance, flags, name, description). Each move's Platinum battle effect
comes from EFFECTS below: 'exact' (an existing Platinum effect does the same thing), 'approx'
(closest existing effect until its own effect is written) or 'new' (its own effect).
anim.s is a PLACEHOLDER copied from a similar existing move until the converted animation
replaces it; that move's HIDES_HP_GAUGES / HIDES_SHADOWS flags are copied with it.
Writes tools/gen5_pack/gen5_moves_status.md.
"""
import csv
import json
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOVES = ROOT / 'res' / 'moves'
CSV = ROOT / 'tools' / 'gen5_pack' / 'items_and_moves' / 'moves' / 'gen5_moves.csv'

# id: (Platinum effect, status, note, placeholder animation)
EFFECTS = {
    468: ('HONE_CLAWS', 'new', 'Attack and accuracy +1', 'sharpen'),
    469: ('WIDE_GUARD', 'new', "protects the user's side from spread moves this turn", 'protect'),
    470: ('GUARD_SPLIT', 'new', 'averages Defense and Sp. Def', 'pain_split'),
    471: ('POWER_SPLIT', 'new', 'averages Attack and Sp. Atk', 'pain_split'),
    472: ('WONDER_ROOM', 'new', '5 turns: Defense and Sp. Def swapped (use again to end)', 'trick_room'),
    473: ('PSYSHOCK', 'new', "special, hits the target's Defense", 'psybeam'),
    474: ('VENOSHOCK', 'new', 'double power vs a poisoned target', 'sludge_bomb'),
    475: ('SPEED_UP_2', 'approx', 'no weight loss', 'agility'),
    476: ('MAKE_GLOBAL_TARGET', 'exact', 'Follow Me effect', 'poison_powder'),
    477: ('TELEKINESIS', 'new', 'target floats 3 turns; moves always hit it', 'kinesis'),
    478: ('MAGIC_ROOM', 'new', '5 turns: held items have no effect (use again to end)', 'trick_room'),
    479: ('SMACK_DOWN', 'new', 'grounds the target', 'rock_throw'),
    480: ('ALWAYS_CRIT', 'new', 'always a critical hit', 'vital_throw'),
    481: ('HIT', 'exact', 'exact in single battles (no splash damage)', 'flame_wheel'),
    482: ('POISON_HIT', 'exact', '', 'surf'),
    483: ('QUIVER_DANCE', 'new', 'Sp. Atk, Sp. Def and Speed +1', 'dragon_dance'),
    484: ('HEAVY_SLAM', 'new', 'power from weight ratio', 'body_slam'),
    485: ('SYNCHRONOISE', 'new', 'no effect unless the target shares a type', 'hyper_voice'),
    486: ('ELECTRO_BALL', 'new', 'power from Speed ratio', 'shock_wave'),
    487: ('SOAK', 'new', 'target becomes pure Water type', 'water_sport'),
    488: ('RAISE_SPEED_HIT', 'new', "hit, then the user's Speed +1", 'flame_wheel'),
    489: ('COIL', 'new', 'Attack, Defense and accuracy +1', 'bulk_up'),
    490: ('LOWER_SPEED_HIT', 'exact', '', 'low_kick'),
    491: ('LOWER_SP_DEF_2_HIT', 'exact', '', 'acid'),
    492: ('FOUL_PLAY', 'new', "uses the target's Attack and Attack stages", 'faint_attack'),
    493: ('SIMPLE_BEAM', 'new', "target's ability becomes Simple", 'signal_beam'),
    494: ('ENTRAINMENT', 'new', "target's ability becomes the user's", 'teeter_dance'),
    495: ('AFTER_YOU', 'new', 'exact in singles (doubles turn order unchanged)', 'helping_hand'),
    496: ('HIT', 'exact', 'exact in single battles', 'hyper_voice'),
    497: ('ECHOED_VOICE', 'new', '+40 power per consecutive turn (max 200)', 'hyper_voice'),
    498: ('CHIP_AWAY', 'new', "ignores the target's Defense stages (not evasion)", 'slam'),
    499: ('CLEAR_SMOG', 'new', "resets the target's stat changes", 'smog'),
    500: ('STORED_POWER', 'new', '20 + 20 per raised stat stage', 'psywave'),
    501: ('QUICK_GUARD', 'new', "protects the user's side from priority moves this turn", 'detect'),
    502: ('ALLY_SWITCH', 'new', 'fails (exact in singles; no swap in doubles)', 'teleport'),
    503: ('THAW_AND_BURN_HIT', 'exact', '', 'water_pulse'),
    504: ('SHELL_SMASH', 'new', 'Def/Sp. Def -1, Atk/Sp. Atk/Speed +2', 'withdraw'),
    505: ('HEAL_PULSE', 'new', "heals half the target's max HP", 'heal_bell'),
    506: ('HEX', 'new', 'double power vs a statused target', 'shadow_ball'),
    507: ('FLY', 'approx', 'works like Fly', 'fly'),
    508: ('SHIFT_GEAR', 'new', 'Attack +1, Speed +2', 'iron_defense'),
    509: ('DRAGON_TAIL', 'new', 'forces a switch (ends wild battles)', 'seismic_toss'),
    510: ('INCINERATE', 'new', "burns up the target's Berry", 'ember'),
    511: ('QUASH', 'new', 'exact in singles (doubles turn order unchanged)', 'taunt'),
    512: ('ACROBATICS', 'new', 'double power without a held item', 'aerial_ace'),
    513: ('REFLECT_TYPE', 'new', "user becomes the target's type(s)", 'conversion'),
    514: ('RETALIATE', 'new', 'double power if an ally fainted last turn', 'facade'),
    515: ('FINAL_GAMBIT', 'new', "damage = user's HP, user faints", 'focus_punch'),
    516: ('BESTOW', 'new', 'gives the held item to a target with none', 'covet'),
    517: ('BURN_HIT', 'exact', '', 'fire_spin'),
    518: ('HIT', 'exact', 'exact in single battles (no combos)', 'water_pulse'),
    519: ('HIT', 'exact', 'exact in single battles (no combos)', 'flamethrower'),
    520: ('HIT', 'exact', 'exact in single battles (no combos)', 'energy_ball'),
    521: ('SWITCH_HIT', 'exact', 'U-turn effect', 'shock_wave'),
    522: ('LOWER_SP_ATK_HIT', 'exact', '', 'bug_buzz'),
    523: ('LOWER_SPEED_HIT', 'exact', '', 'earthquake'),
    524: ('ALWAYS_CRIT', 'new', 'always a critical hit', 'icy_wind'),
    525: ('DRAGON_TAIL', 'new', 'forces a switch (ends wild battles)', 'iron_tail'),
    526: ('WORK_UP', 'new', 'Attack and Sp. Atk +1', 'bulk_up'),
    527: ('LOWER_SPEED_HIT', 'exact', '', 'thunder_shock'),
    528: ('RECOIL_QUARTER', 'exact', '', 'spark'),
    529: ('HIGH_CRITICAL', 'exact', '', 'drill_peck'),
    530: ('HIT_TWICE', 'exact', '', 'dragon_claw'),
    531: ('FLINCH_HIT', 'exact', '', 'zen_headbutt'),
    532: ('RECOVER_HALF_DAMAGE_DEALT', 'exact', '', 'giga_drain'),
    533: ('CHIP_AWAY', 'new', "ignores the target's Defense stages (not evasion)", 'slash'),
    534: ('LOWER_DEFENSE_HIT', 'exact', '', 'x_scissor'),
    535: ('HEAVY_SLAM', 'new', 'power from weight ratio', 'flare_blitz'),
    536: ('LOWER_ACCURACY_HIT', 'exact', '', 'razor_leaf'),
    537: ('FLINCH_MINIMIZE_DOUBLE_HIT', 'exact', 'Stomp effect', 'stomp'),
    538: ('COTTON_GUARD', 'new', 'Defense +3 (message says "sharply")', 'cotton_spore'),
    539: ('LOWER_ACCURACY_HIT', 'exact', '', 'dark_pulse'),
    540: ('PSYSHOCK', 'new', "special, hits the target's Defense", 'psychic'),
    541: ('MULTI_HIT', 'exact', '', 'double_slap'),
    542: ('HURRICANE', 'new', '30% confusion; rain: never misses, sun: 50% accuracy; hits Fly/Bounce', 'twister'),
    543: ('RECOIL_QUARTER', 'exact', '', 'take_down'),
    544: ('HIT_TWICE', 'exact', '', 'metal_claw'),
    545: ('BURN_HIT', 'exact', '', 'lava_plume'),
    546: ('HIT', 'exact', 'Normal type without a Drive (Drive items not in the game)', 'tri_attack'),
    547: ('SLEEP_HIT', 'new', '10% sleep (no Meloetta form change yet)', 'sing'),
    548: ('PSYSHOCK', 'new', "special, hits the target's Defense", 'night_slash'),
    549: ('LOWER_SPEED_HIT', 'exact', '', 'icy_wind'),
    550: ('PARALYZE_HIT', 'exact', '', 'volt_tackle'),
    551: ('BURN_HIT', 'exact', '', 'flamethrower'),
    552: ('RAISE_SP_ATK_HIT', 'exact', '', 'lava_plume'),
    553: ('FREEZE_SHOCK', 'new', 'charge turn, 30% paralysis', 'ice_beam'),
    554: ('ICE_BURN', 'new', 'charge turn, 30% burn', 'ice_beam'),
    555: ('LOWER_SP_ATK_HIT', 'exact', '', 'hyper_voice'),
    556: ('FLINCH_HIT', 'exact', '', 'avalanche'),
    557: ('V_CREATE', 'new', "user's Defense, Sp. Def and Speed -1 after hitting", 'flare_blitz'),
    558: ('FUSION_FLARE', 'new', 'double power after Fusion Bolt the same turn', 'flamethrower'),
    559: ('FUSION_BOLT', 'new', 'double power after Fusion Flare the same turn', 'thunderbolt'),
}

POWER_OVERRIDES = {}

# Charge-turn messages (put in script.s, like Razor Wind)
CHARGE_MESSAGES = {553: 'PokemonCloakedInFreezingLight', 554: 'PokemonCloakedInFreezingAir'}  # variable-power moves with an approximated effect

RANGES = {'SELECTED': 'RANGE_SINGLE_TARGET', 'USER': 'RANGE_USER', 'ALL_ADJACENT': 'RANGE_ALL_ADJACENT',
          'ADJACENT_FOES': 'RANGE_ADJACENT_OPPONENTS', 'USER_SIDE': 'RANGE_USER_SIDE', 'FIELD': 'RANGE_FIELD'}
CONTEST_TYPES = {'FIRE': 'COOL', 'ELECTRIC': 'COOL', 'FIGHTING': 'COOL', 'FLYING': 'COOL', 'DRAGON': 'COOL',
                 'STEEL': 'COOL', 'WATER': 'BEAUTY', 'ICE': 'BEAUTY', 'PSYCHIC': 'SMART', 'GHOST': 'SMART',
                 'DARK': 'SMART', 'NORMAL': 'CUTE', 'GRASS': 'CUTE', 'BUG': 'TOUGH', 'POISON': 'TOUGH',
                 'ROCK': 'TOUGH', 'GROUND': 'TOUGH'}


def wrap(text):
    words = ' '.join(text.replace("'", '’').split())  # the game's charmap uses ’
    for width in (19, 20, 21):
        lines = textwrap.wrap(words, width)
        if len(lines) <= 5:
            return [l + '\n' for l in lines[:-1]] + [lines[-1]]
    lines = textwrap.wrap(words, 21)[:5]
    return [l + '\n' for l in lines[:-1]] + [lines[-1]]


def main():
    force = '--force' in sys.argv
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
    status = ['# Gen 5 moves (468-559): effect status', '',
              '| # | Move | Effect | Status | Note | Animation |', '|---|---|---|---|---|---|']
    for r in rows:
        mid = int(r['id'])
        stem = r['constant'][len('MOVE_'):].lower()
        d = MOVES / stem
        effect, kind, note, anim = EFFECTS[mid]
        st = json.loads(r['stat_changes'])
        inf = json.loads(r['inflicts'])
        chance = 0
        if inf.get('chance'):
            chance = inf['chance']
        elif int(r['flinch_chance']):
            chance = int(r['flinch_chance'])
        elif st and st[0]['chance']:
            chance = st[0]['chance']
        if effect in ('LOWER_SPEED_HIT', 'LOWER_SP_ATK_HIT', 'LOWER_SP_DEF_2_HIT', 'RAISE_SPEED_HIT') and chance == 0:
            chance = 100
        if effect == 'HIT':
            chance = 0
        power = POWER_OVERRIDES.get(mid, int(r['power']))
        acc = int(r['accuracy'])
        flags_in = json.loads(r['flags'])
        flags = []
        if 'MOVE_FLAG_CONTACT' in flags_in:
            flags.append('MOVE_FLAG_MAKES_CONTACT')
        if 'MOVE_FLAG_PROTECT' in flags_in:
            flags.append('MOVE_FLAG_CAN_PROTECT')
        if 'MOVE_FLAG_REFLECTABLE' in flags_in:
            flags.append('MOVE_FLAG_CAN_MAGIC_COAT')
        if 'MOVE_FLAG_SNATCH' in flags_in:
            flags.append('MOVE_FLAG_CAN_SNATCH')
        if 'MOVE_FLAG_MIRROR_MOVE' in flags_in:
            flags.append('MOVE_FLAG_CAN_MIRROR_MOVE')
        if power > 0 and chance == 0 and effect not in ('FLINCH_HIT', 'FLINCH_MINIMIZE_DOUBLE_HIT'):
            flags.append('MOVE_FLAG_TRIGGERS_KINGS_ROCK')
        src = json.loads((MOVES / anim / 'data.json').read_text())
        flags += [f for f in src['flags'] if f in ('MOVE_FLAG_HIDES_HP_GAUGES', 'MOVE_FLAG_HIDES_SHADOWS')]
        data = {
            'name': r['name'].replace("'", '’'),
            'description': wrap(r['description']),
            'class': 'CLASS_' + r['category'][len('MOVE_CATEGORY_'):],
            'type': r['type'],
            'power': power,
            'accuracy': 0 if acc > 100 else acc,
            'pp': int(r['pp']),
            'effect': {'type': f'BATTLE_EFFECT_{effect}', 'chance': chance},
            'range': RANGES[r['target'][len('MOVE_TARGET_'):]],
            'priority': int(r['priority']),
            'flags': flags,
            'contest': {'effect': 'CONTEST_EFFECT_BASIC', 'type': 'CONTEST_TYPE_' + CONTEST_TYPES[r['type'][5:]]},
        }
        status.append(f"| {mid} | {r['name']} | {effect} | {kind} | {note} | placeholder ({anim}) |")
        if d.exists() and not force:
            continue
        d.mkdir(exist_ok=True)
        (d / 'data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')
        msg = CHARGE_MESSAGES.get(mid)
        buffer = f'    BufferMessage BattleStrings_Text_{msg}_Ally, TAG_NICKNAME, BTLSCR_ATTACKER\n' if msg else ''
        (d / 'script.s').write_text('#include "macros/btlcmd.inc"\n\n\n_000:\n' + buffer + '    GoToEffectScript \n')
        if (d / 'anim.s').exists() and 'PLACEHOLDER' not in (d / 'anim.s').read_text():
            continue  # keep a converted animation
        anim_src = (MOVES / anim / 'anim.s').read_text()
        (d / 'anim.s').write_text(f'// PLACEHOLDER animation: copy of {anim} until the Black 2 animation is converted\n' + anim_src)
    (ROOT / 'tools' / 'gen5_pack' / 'gen5_moves_status.md').write_text('\n'.join(status) + '\n')
    print(f'{len(rows)} moves')


if __name__ == '__main__':
    main()
