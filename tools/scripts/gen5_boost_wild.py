#!/usr/bin/env python3
"""Slightly boost the encounter rate of the Gen 5 Pokemon already in each wild table.

usage: gen5_boost_wild.py            -> writes tools/gen5_pack/GEN5_WILD_BOOST.md (plan only)
       gen5_boost_wild.py --apply    -> also writes res/field/maps/*/encounters.json

For every table that already has a Gen 5 Pokemon, that Gen 5 family takes over ONE more slot:
  - land: a 5% slot (slots 7-8), else a 1% slot (11-12): typically 10% -> 15%
  - surf / good rod / super rod: the 4% slot, else the 1% slot: typically 5% -> 9%
The slot taken over must hold a non-Gen 5 species that also appears in another slot of the same
table, so every Pokemon that could be found there before still can. The slot keeps its level; the
evolution stage is picked from that level like the Phase 5 plan. Tables without Gen 5 Pokemon,
time-of-day / swarm / radar / dual-slot overrides and the old rod are untouched.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen5_wild_plan as wp  # noqa: E402

ROOT = wp.ROOT
LAND_ORDER = [6, 7, 10, 11]  # 0-based: 5%, 5%, 1%, 1%
WATER_ORDER = [3, 4]  # 4%, 1%


def is_gen5(species):
    return species in wp.SPECIES and wp.SPECIES.index(species) in wp.GEN5


def base(species):
    return wp.species_data(species[len('SPECIES_'):])['offspring']


def boost(entries, order, rates):
    """Returns (slot, old species, new species, old share, new share) or None."""
    names = [e['species'] for e in entries]
    gen5 = [s for s in names if is_gen5(s)]
    if not gen5:
        return None
    # the most common Gen 5 family in the table (ties: the first one)
    fam = max(dict.fromkeys(base(s) for s in gen5), key=lambda b: sum(base(s) == b for s in gen5))
    old_share = sum(r for r, s in zip(rates, names) if is_gen5(s))
    for slot in order:
        cur = names[slot]
        if cur == 'SPECIES_NONE' or is_gen5(cur) or names.count(cur) < 2:
            continue
        e = entries[slot]
        level = e['level'] if 'level' in e else e['level_min']
        new = 'SPECIES_' + wp.stage_for(fam[len('SPECIES_'):], level)
        e['species'] = new
        return slot, cur, new, old_share, old_share + rates[slot]
    return None


def main():
    write = '--apply' in sys.argv
    rows = []
    for f in sorted(wp.MAPS.glob('*/encounters.json')):
        d = json.loads(f.read_text())
        changed = False
        tables = [('land', 'land_rate', 'land_encounters', LAND_ORDER, wp.LAND_RATES)]
        tables += [(k, f'{k}_rate', f'{k}_encounters', WATER_ORDER, wp.WATER_RATES) for k in ('surf', 'good_rod', 'super_rod')]
        for kind, rate_key, key, order, rates in tables:
            if not d.get(rate_key):
                continue
            res = boost(d[key], order, rates)
            if res:
                slot, old, new, a, b = res
                rows.append((f.parent.name, kind, slot + 1, old[8:].title(), new[8:].title(), a, b))
                changed = True
        if changed and write:
            f.write_text(json.dumps(d, indent=4) + '\n')
    out = ['# Gen 5 wild encounter boost', '',
           'Each table that already had a Gen 5 Pokémon gives that family one more slot (a 5%/4% slot, else 1%).',
           'The replaced Pokémon still appears in another slot of the same table.', '',
           '| Map | Table | Slot | Replaced | Now | Gen 5 share |', '|---|---|---|---|---|---|']
    out += [f'| {m} | {k} | {s} | {o} | {n} | {a}% → {b}% |' for m, k, s, o, n, a, b in rows]
    (ROOT / 'tools' / 'gen5_pack' / 'GEN5_WILD_BOOST.md').write_text('\n'.join(out) + '\n')
    print(len(rows), 'tables boosted', '(applied)' if write else '(plan only)')


if __name__ == '__main__':
    main()
