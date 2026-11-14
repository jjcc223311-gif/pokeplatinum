#!/usr/bin/env python3
"""Convert the Black 2 move animations in tools/gen5_pack/move_animations/ into Platinum anim.s.

usage: convert_gen5_anims.py <first move id> <last move id>

What converts:
  - particles: Black 2's SPA files use the same SPA "12_1" format as Platinum, so they are copied
    into res/graphics/battle/particles/gen5_particle_<member>.spa and loaded with
    LoadParticleResource
  - EmitterAdd / EmitterAddAt / EmitterAddOrtho -> CreateEmitter at the attacker / defender
  - EmitterMove -> CreateEmitter + Func_MoveEmitterA2BLinear (attacker <-> defender)
  - WaitFrames / Wait -> Delay / WaitForAnimTasks
  - PlaySE -> the matching Platinum move sound (SEQ_SE_W014_01 -> SEQ_SE_DP_W014); sounds that
    only exist in Gen 5 fall back to the sound of the placeholder animation's move
  - McssMoveXY -> Func_MoveBattler there and back; CameraShake / shaking BgMove / McssCircle ->
    Func_Shake; McssPalFade (fading in) -> Func_FadeBattlerSprite
Dropped (no Platinum equivalent in the 2D battle scene): 3D camera moves, backgrounds, sprite
scaling / rotation / vanish, moving sounds. "Battle Scene: OFF" skips move animations entirely,
and every particle system is unloaded at the end.
Writes tools/gen5_pack/gen5_anim_report.md (appends one line per move).
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'tools' / 'gen5_pack' / 'move_animations'
PARTICLES = ROOT / 'res' / 'graphics' / 'battle' / 'particles'
MOVES = ROOT / 'res' / 'moves'
NAIX = ROOT / 'build' / 'res' / 'sound' / 'pl_sound_data.naix'

CB = {'EFFVM_EMIT_ATTACKER': 'EMITTER_CB_SET_POS_TO_ATTACKER', 'EFFVM_EMIT_DEFENDER': 'EMITTER_CB_SET_POS_TO_DEFENDER',
      'EFFVM_ATTACKER': 'EMITTER_CB_SET_POS_TO_ATTACKER', 'EFFVM_DEFENDER': 'EMITTER_CB_SET_POS_TO_DEFENDER'}
SPRITE = {'EFFVM_ATTACKER': 'BATTLE_ANIM_BATTLER_SPRITE_ATTACKER', 'EFFVM_DEFENDER': 'BATTLE_ANIM_BATTLER_SPRITE_DEFENDER'}
BATTLER = {'EFFVM_ATTACKER': 'BATTLE_ANIM_ATTACKER', 'EFFVM_DEFENDER': 'BATTLE_ANIM_DEFENDER'}
PAN = {'EFFVM_ATTACKER': 'BATTLE_SOUND_PAN_LEFT', 'EFFVM_DEFENDER': 'BATTLE_SOUND_PAN_RIGHT'}


def platinum_sounds():
    names = set(re.findall(r'#define (SEQ_SE_DP_\w+_sseq)', NAIX.read_text()))
    return names


def map_sound(name, sounds):
    m = re.match(r'SEQ_SE_W(\d+)', name)
    if m:
        for cand in (f'SEQ_SE_DP_W{m.group(1)}_sseq', f'SEQ_SE_DP_W{m.group(1)}B_sseq', f'SEQ_SE_DP_W{m.group(1)}C_sseq'):
            if cand in sounds:
                return cand
    return None


def args_of(line):
    parts = line.split(None, 1)
    return parts[0], [a.strip() for a in parts[1].split(',')] if len(parts) > 1 else []


def num(s):
    try:
        return int(s, 0)
    except ValueError:
        return 0


def fallback_sound(move_dir):
    anim = (move_dir / 'anim.s').read_text() if (move_dir / 'anim.s').exists() else ''
    m = re.search(r'(SEQ_SE_DP_\w+_sseq)', anim)
    return m.group(1) if m else 'SEQ_SE_DP_050_sseq'


def register_particle(member):
    name = f'gen5_particle_{member}.spa'
    src = PACK / 'shared' / 'particles' / f'{member}.spa'
    if not src.exists():
        return None
    dst = PARTICLES / name
    if not dst.exists():
        shutil.copy(src, dst)
    mb = (PARTICLES / 'meson.build').read_text()
    if f"'{name}'" not in mb:
        mb = mb.replace("    'shadow_force.spa',\n)", f"    'shadow_force.spa',\n    '{name}',\n)") if "    'shadow_force.spa',\n)" in mb else \
            re.sub(r"(    'gen5_particle_\d+\.spa',\n)\)", rf"\1    '{name}',\n)", mb, count=1)
        assert f"'{name}'" in mb, name
        (PARTICLES / 'meson.build').write_text(mb)
        order = (PARTICLES / 'battle_particles.order').read_text().rstrip('\n')
        (PARTICLES / 'battle_particles.order').write_text(order + f'\n{name}\n')
    return f'gen5_particle_{member}_spa'


def convert(move_dir_name, sounds):
    mid = int(move_dir_name.split('_')[0])
    src = (PACK / 'moves' / move_dir_name / 'animation.s').read_text().splitlines()
    data = json.loads((PACK / 'moves' / move_dir_name / 'move_data.json').read_text())
    stem = data['constant'][len('MOVE_'):].lower()
    move_dir = MOVES / stem
    fallback = fallback_sound(move_dir)

    out, slots, notes = [], {}, set()
    emitters = 0
    started = False
    used_sound = 0
    for raw in src:
        line = raw.strip()
        if not line or line.startswith('.') or line.startswith('Script'):
            continue
        if line.endswith(':'):
            if started:
                break  # only the first variant
            started = True
            continue
        cmd, a = args_of(line)
        if cmd == 'End':
            break
        if cmd == 'ParticleLoad':
            sym = register_particle(num(a[0]))
            if sym and num(a[0]) not in slots and len(slots) < 4:
                slots[num(a[0])] = len(slots)
                out.append(f'    LoadParticleResource {slots[num(a[0])]}, {sym}')
        elif cmd in ('EmitterAdd', 'EmitterAddAt', 'EmitterAddOrtho', 'EmitterMoveFrom', 'OrbitEmitters'):
            spa = num(a[0])
            if spa in slots and emitters < 20:
                target = next((x for x in a if x.startswith('EFFVM_EMIT') or x in CB), 'EFFVM_EMIT_DEFENDER')
                out.append(f'    CreateEmitter {slots[spa]}, {num(a[1])}, {CB.get(target, "EMITTER_CB_SET_POS_TO_DEFENDER")}')
                emitters += 1
                if cmd != 'EmitterAdd':
                    notes.add(f'{cmd} -> emitter at the battler')
        elif cmd == 'EmitterMove':
            spa = num(a[0])
            if spa in slots and emitters < 20:
                src_b, dst_b = a[3], a[4]
                mode = 'EMITTER_ANIMATION_MODE_DEF_TO_ATK' if 'DEFENDER' in src_b else 'EMITTER_ANIMATION_MODE_ATK_TO_DEF'
                out.append(f'    CreateEmitter {slots[spa]}, {num(a[1])}, {CB.get(src_b, "EMITTER_CB_SET_POS_TO_ATTACKER")}')
                out.append(f'    Func_MoveEmitterA2BLinear {emitters}, 0, 0, 0, 12, 64, {mode}')
                emitters += 1
        elif cmd == 'WaitFrames':
            out.append(f'    Delay {max(1, num(a[0]))}')
        elif cmd == 'Wait':
            out.append('    WaitForAnimTasks')
        elif cmd == 'PlaySE':
            if a[0] == 'SEQ_SE_DUMMY5':
                continue
            seq = map_sound(a[0], sounds)
            if seq is None:
                seq = fallback
                notes.add('Gen 5-only sounds -> placeholder move sound')
            if used_sound >= 6:
                continue
            used_sound += 1
            pan = PAN.get(a[2] if len(a) > 2 else '', 'BATTLE_SOUND_PAN_CENTER')
            delay = num(a[3]) if len(a) > 3 else 0
            if delay > 0:
                out.append(f'    PlayDelayedSoundEffect {seq}, {pan}, {delay}')
            else:
                out.append(f'    PlayPannedSoundEffect {seq}, {pan}')
        elif cmd == 'McssMoveXY' and a[0] in SPRITE:
            dx = num(a[2])
            if dx:
                px = 12 if dx > 0 else -12
                if a[0] == 'EFFVM_ATTACKER':
                    out.append(f'    Func_MoveBattler {SPRITE[a[0]]}, {px}, 0, 3')
                    out.append(f'    Func_MoveBattler {SPRITE[a[0]]}, {-px}, 0, 3')
                else:
                    out.append(f'    Func_Shake 2, 0, 1, 2, {SPRITE[a[0]]}')
        elif cmd == 'CameraShake' or (cmd == 'BgMove' and num(a[0]) == 2) or cmd == 'McssCircle':
            out.append('    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER')
            notes.add('camera / background shake -> defender shake')
        elif cmd == 'McssPalFade' and a[0] in BATTLER:
            if num(a[1]) < num(a[2]):
                color = num(a[4]) if len(a) > 4 else 0x7FFF
                out.append(f'    Func_FadeBattlerSprite {BATTLER[a[0]]}, 1, 0, {hex(color & 0x7FFF)}, {min(16, max(4, num(a[2])))}, 0')
        else:
            notes.add(cmd)

    if not slots and not any(l.strip().startswith('Func_') for l in out):
        return None, 'nothing convertible (background / camera only)'
    body = ['#include "macros/btlanimcmd.inc"', '',
            f'// Converted from the Black 2 animation ({move_dir_name}) by tools/scripts/convert_gen5_anims.py', '',
            'L_0:'] + out + ['    WaitForAnimTasks', '    WaitForAllEmitters'] + \
           [f'    UnloadParticleSystem {s}' for s in sorted(slots.values())] + ['    End', '']
    dropped = sorted(n for n in notes if not n.startswith(('Gen 5', 'camera', 'Emitter', 'Orbit')))
    note = '; '.join(sorted(n for n in notes if n.startswith(('Gen 5', 'camera', 'Emitter', 'Orbit'))))
    if dropped:
        note += ('; ' if note else '') + 'dropped: ' + ', '.join(dropped)
    return '\n'.join(body), note


def main():
    first, last = int(sys.argv[1]), int(sys.argv[2])
    sounds = platinum_sounds()
    report = ROOT / 'tools' / 'gen5_pack' / 'gen5_anim_report.md'
    lines = report.read_text().splitlines() if report.exists() else ['# Gen 5 move animations', '',
                                                                      '| # | Move | Result | Notes |', '|---|---|---|---|']
    for d in sorted((PACK / 'moves').iterdir()):
        mid = int(d.name.split('_')[0])
        if not first <= mid <= last:
            continue
        body, note = convert(d.name, sounds)
        name = json.loads((d / 'move_data.json').read_text())['name']
        stem = json.loads((d / 'move_data.json').read_text())['constant'][5:].lower()
        lines = [l for l in lines if not l.startswith(f'| {mid} |')]
        if body is None:
            lines.append(f'| {mid} | {name} | PLACEHOLDER kept | {note} |')
        else:
            (MOVES / stem / 'anim.s').write_text(body)
            lines.append(f'| {mid} | {name} | converted | {note} |')
        print(mid, name, 'converted' if body else 'placeholder', note)
    head, rows = lines[:4], sorted(lines[4:], key=lambda l: int(l.split('|')[1]))
    report.write_text('\n'.join(head + rows) + '\n')


if __name__ == '__main__':
    main()
