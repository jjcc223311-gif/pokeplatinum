#!/usr/bin/env python3
"""Juniper's extra field poses (bike, surf, fishing, Poketch, save, Poke Ball, healing, Sprayduck,
Vs. Seeker), recoloured from Dawn's sheets read from git HEAD.

Dawn's beanie becomes Juniper's light-brown hair, her navy hair dark brown, her skirt green and the
beanie pin red (Juniper's clip). White/grey pixels are only recoloured in the head rows of each 32x32
frame so Poke Balls, the bike and the Poketch keep their colours (they go into the two spare slots;
the fishing sheet has none, so its whites change everywhere, including the fishing line).
usage: juniper_field_poses.py   (run with a Python that has Pillow)
"""
import io
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DIR = 'res/graphics/field_sprites/player'
SHEETS = ['player_f_bike', 'player_f_fishing', 'player_f_holding_pokeball', 'player_f_pokecenter_heal',
          'player_f_poketch', 'player_f_save', 'player_f_sprayduck', 'player_f_surf', 'player_f_vs_seeker']

# Dawn colour -> Juniper colour, applied to the palette (everywhere)
PALETTE_SWAP = {
    (173, 165, 206): (131, 90, 57),    # beanie shade -> hair dark
    (57, 99, 140): (98, 57, 41),       # beanie outline -> hair deepest
    (57, 66, 82): (74, 41, 33),        # navy hair -> darkest brown
    (239, 148, 198): (230, 98, 90),    # pink pin -> red clip
    (198, 107, 156): (164, 57, 65),
    (198, 57, 57): (57, 99, 74),       # red skirt -> green
    (247, 107, 74): (82, 148, 98),
}
# Dawn colour -> Juniper colour, only in the head rows (needs a spare palette slot each)
HEAD_SWAP = {
    (239, 239, 255): (189, 139, 82),   # white beanie -> hair
    (206, 206, 222): (164, 115, 66),   # beanie shade -> hair shade
}
HEAD_ROWS = range(0, 21)


def near(a, b, tol=24):
    return sum((p - q) ** 2 for p, q in zip(a, b)) <= tol * tol


def git_image(path):
    data = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT, capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data))


def convert(name):
    img = git_image(f'{DIR}/{name}.png')
    pal = [tuple(img.getpalette()[3 * i:3 * i + 3]) for i in range(16)]
    used = set(img.get_flattened_data())
    new = list(pal)
    for i, c in enumerate(pal):
        for k, v in PALETTE_SWAP.items():
            if i and near(c, k):
                new[i] = v
    spare = [i for i in range(1, 16) if i not in used]
    head = {}
    for i, c in enumerate(pal):
        for k, v in HEAD_SWAP.items():
            if i and i in used and near(c, k):
                if spare:
                    head[i] = spare.pop(0)
                    new[head[i]] = v
                else:  # no spare slot (fishing): recolour that white everywhere
                    new[i] = v
    out = img.copy()
    out.putpalette([v for c in new for v in c])  # exactly 16 colours (field textures need it)
    px = out.load()
    for y in range(out.height):
        if y % 32 in HEAD_ROWS:
            for x in range(out.width):
                if px[x, y] in head:
                    px[x, y] = head[px[x, y]]
    out.save(ROOT / DIR / f'{name}.png')
    return len(head)


def main():
    for name in SHEETS:
        print(name, 'head colours moved:', convert(name))


if __name__ == '__main__':
    main()
