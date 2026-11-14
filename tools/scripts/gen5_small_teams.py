#!/usr/bin/env python3
"""Give every small trainer team (1-3 Pokemon) one more Gen 5 Pokemon.

usage: gen5_small_teams.py            -> writes tools/gen5_pack/GEN5_SMALL_TEAMS.md (plan only)
       gen5_small_teams.py --apply    -> also writes res/trainers/data/*.json

Rules (built on the Phase 6 helpers in gen5_trainer_plan.py):
  - teams of 1-3 Pokemon (except the unused dummy_* trainers) get one extra Gen 5 Pokemon; it leads the team (the ace stays last)
  - level: the team's lowest level (solo teams: one below their only Pokemon, at least 2)
  - species fits the trainer class's types, is not a family already in the team, no legendaries;
    starters / pseudo-legendaries only for strong classes; evolution stage from the level
  - the same trainer (rematches, every Barry battle) prefers a Gen 5 family he already uses in his
    other battles, else the same new family every time
  - custom-move teams get the species' latest level-up moves; held items follow the team's format
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen5_trainer_plan as tp  # noqa: E402

MAX_TEAM = 3
# Barry's first battle stays starter-only (user request); his Gen 5 Pokemon first appears on Route 203
SMALL_TEAM_SKIP = {'rival_route_201_chimchar', 'rival_route_201_piplup', 'rival_route_201_turtwig'}


def trainer_key(d, stem):
    cls = d['class'][len('TRAINER_CLASS_'):]
    if cls in ('RIVAL', 'DP_PLAYER_MALE', 'DP_PLAYER_FEMALE'):
        return d['name']
    return tp.re.sub(r'_rematch.*$|_\d+$', '', stem)


def main():
    write = '--apply' in sys.argv
    locs = tp.trainer_locations()
    files = sorted(tp.TRAINERS.glob('*.json'))
    teams = {f: json.loads(f.read_text()) for f in files}

    # Gen 5 families each trainer already uses somewhere
    used = {}
    for f, d in teams.items():
        for p in d['party']:
            s = p['species'][8:]
            if tp.gen(s) == 5:
                used.setdefault(trainer_key(d, f.stem), []).append((p['level'], tp.base_of(s)))
    # earliest (lowest-level) family first, so e.g. Barry's first teams get the family he uses next
    used = {k: [b for _, b in sorted(v)] for k, v in used.items()}

    chosen_family = {}  # trainer key -> family picked for its teams that need a new one
    rows = []
    for f, d in teams.items():
        party = d['party']
        cls = d['class'][len('TRAINER_CLASS_'):]
        if f.stem in tp.SKIP or f.stem in SMALL_TEAM_SKIP or f.stem.startswith('dummy') or cls == 'PLAYER_MALE' or not 1 <= len(party) <= MAX_TEAM:
            continue
        key = trainer_key(d, f.stem)
        strong = cls in tp.STRONG
        team_bases = {tp.base_of(p['species'][8:]) for p in party}
        level = min(p['level'] for p in party)
        if len(party) == 1:
            level = max(2, level - 1)

        base = next((b for b in dict.fromkeys(used.get(key, [])) if b not in team_bases), None)
        if base is None and key in chosen_family and chosen_family[key] not in team_bases:
            base = chosen_family[key]
        if base is None:
            pool = [c for c in tp.candidates(cls, level, strong) if tp.gen(c[1]) == 5 and c[0] not in team_bases]
            pool = pool or [c for c in tp.candidates(None, level, strong) if tp.gen(c[1]) == 5 and c[0] not in team_bases]
            if not pool:
                continue
            base = pool[tp.rng(key, 'small-team') % len(pool)][0]
            chosen_family[key] = base
        species = tp.stage_for(base, level)

        has_moves = any(p.get('moves') for p in party)
        has_items = any(p.get('item') for p in party)
        new = {'species': 'SPECIES_' + species, 'form': 0, 'level': level,
               'item': 'ITEM_NONE' if has_items else None,
               'moves': (tp.level_moves(species, level) or None) if has_moves else None,
               'iv_scale': party[0].get('iv_scale', 0), 'ball_seal': 0}
        party.insert(0, new)
        rows.append((locs.get('TRAINER_' + f.stem.upper(), '-'), f"{d['name']} ({cls.replace('_', ' ').title()})",
                     f.stem, f"{species.title()} Lv {level}", len(party)))
        if write:
            f.write_text(json.dumps(d, indent=4, ensure_ascii=False) + '\n')

    out = ['# Small teams: one more Gen 5 Pokémon', '',
           'Every team of 1-3 Pokémon gets one extra Gen 5 Pokémon as its lead (the ace stays last).', '',
           '| Location | Trainer | File | Added | Team size |', '|---|---|---|---|---|']
    out += [f'| {a} | {b} | {c} | {e} | {n} |' for a, b, c, e, n in sorted(rows)]
    (tp.ROOT / 'tools' / 'gen5_pack' / 'GEN5_SMALL_TEAMS.md').write_text('\n'.join(out) + '\n')
    print(len(rows), 'teams get a Gen 5 Pokemon', '(applied)' if write else '(plan only)')


if __name__ == '__main__':
    main()
