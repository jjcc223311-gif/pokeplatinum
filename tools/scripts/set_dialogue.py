#!/usr/bin/env python3
"""Rewrite in-game messages with automatic line wrapping.

Each message is a list of paragraphs; every paragraph becomes one or more text-box pages.
First line ends "\\n", later lines scroll with "\\f", paragraphs end with "\\r".
end=True keeps a trailing "\\r" on the last paragraph.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIDTH = 36


def wrap(words_text, width=WIDTH):
    lines, cur = [], ''
    for w in words_text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}' if cur else w
    if cur:
        lines.append(cur)
    return lines


def build(paragraphs, end):
    out = []
    for pi, para in enumerate(paragraphs):
        lines = wrap(para)
        for li, line in enumerate(lines):
            last_line = li == len(lines) - 1
            if not last_line:
                out.append(line + ('\n' if li == 0 else '\f'))
            elif pi < len(paragraphs) - 1 or end:
                out.append(line + '\r')
            else:
                out.append(line)
    return out


def set_messages(file, changes):
    path = ROOT / 'res' / 'text' / f'{file}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    by_id = {m['id']: m for m in data['messages']}
    for mid, (paragraphs, end) in changes.items():
        by_id[mid]['en_US'] = build(paragraphs, end)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    for file, changes in spec.items():
        set_messages(file, {k: (v['text'], v.get('end', False)) for k, v in changes.items()})
