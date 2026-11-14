#!/usr/bin/env python3
"""Write the Gen 5 Pokédex entries from tools/gen5_pack/gen5_dex_entries.txt into each species'
data.json (pokedex_data.<lang>.entry_text, 3 lines; every language gets the English text).
Species names inside the text are written in capitals, like the rest of the Platinum Pokédex.
usage: set_gen5_dex_entries.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIDTH = 35


def wrap(text):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > WIDTH:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}' if cur else w
    lines.append(cur)
    return lines


def main():
    entries = {}
    for line in (ROOT / 'tools' / 'gen5_pack' / 'gen5_dex_entries.txt').read_text().splitlines():
        if line and not line.startswith('#'):
            name, text = line.split('|', 1)
            entries[name] = text
    names = sorted(entries, key=len, reverse=True)
    bad = []
    for name, text in entries.items():
        for other in names:
            text = re.sub(rf'\b{other.capitalize()}\b', other, text)
        lines = wrap(text)
        if len(lines) > 3:
            bad.append((name, lines))
            continue
        entry = [l + '\n' for l in lines[:-1]] + [lines[-1]]
        p = ROOT / 'res' / 'pokemon' / name.lower() / 'data.json'
        data = json.loads(p.read_text())
        for lang, d in data['pokedex_data'].items():
            if isinstance(d, dict) and 'entry_text' in d:
                d['entry_text'] = entry
        p.write_text(json.dumps(data, indent=4, ensure_ascii=False) + '\n')
    for name, lines in bad:
        print('TOO LONG', name, lines)
    print(f'{len(entries) - len(bad)} entries written')


if __name__ == '__main__':
    main()
