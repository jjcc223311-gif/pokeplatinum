#!/usr/bin/env python3
"""Juniper's Trainer Card portrait (female player, Platinum card), drawn from her battle front sprite.

The Platinum card shows the player as a one-colour (blue-grey) picture using card palette 0, so the
sprite is converted by brightness. It is written over Dawn's tiles (plus unused tiles) in
res/graphics/trainer_case/player_tiles.png and laid out in dawn.NSCR, 5 x 10 tiles like Lucas.
Lucas's tiles are not touched. usage: juniper_trainer_card.py   (Python with Pillow)
"""
import struct
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / 'res' / 'graphics' / 'trainer_case'
FRONT = ROOT / 'res' / 'trainers' / 'classes' / 'player_female' / 'front.png'

# card palette 0, light -> dark: (index, brightness)
RAMP = [(13, 255), (2, 228), (3, 205), (7, 180), (4, 164), (8, 157), (5, 131), (9, 128), (1, 115), (6, 98), (14, 22)]
X0, Y0, W, H = 23, 6, 5, 10


def load_nscr(path):
    d = bytearray(path.read_bytes())
    size = struct.unpack_from('<I', d, 0x20)[0]
    return d, list(struct.unpack_from(f'<{size // 2}H', d, 0x24))


def main():
    tiles_img = Image.open(CASE / 'player_tiles.png')
    tiles = tiles_img.load()
    tw = tiles_img.width // 8
    n_tiles = tw * (tiles_img.height // 8)

    def tile_px(t):
        ty, tx = divmod(t, tw)
        return tuple(tiles[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))

    lucas_data, lucas = load_nscr(CASE / 'lucas.NSCR')
    dawn_data, dawn = load_nscr(CASE / 'dawn.NSCR')
    lucas_tiles = {e & 0x3FF for e in lucas}
    dawn_tiles = {e & 0x3FF for e in dawn} - {0}
    used = lucas_tiles | {0}
    free = [t for t in range(1, n_tiles) if t not in used]

    # Juniper, fitted into 40 x 80
    src = Image.open(FRONT)
    pal = src.getpalette()
    frame = src.crop((0, 0, 80, 80))
    frame.putpalette(pal)
    px = frame.load()
    xs = [x for x in range(80) for y in range(80) if px[x, y]]
    ys = [y for x in range(80) for y in range(80) if px[x, y]]
    box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = min(W * 8 / bw, H * 8 / bh)
    nw, nh = max(1, round(bw * scale)), max(1, round(bh * scale))
    fig = frame.crop(box).resize((nw, nh), Image.NEAREST)
    fp = fig.load()
    canvas = [[0] * (W * 8) for _ in range(H * 8)]
    ox, oy = (W * 8 - nw) // 2, H * 8 - nh
    lums = []
    for y in range(nh):
        for x in range(nw):
            i = fp[x, y]
            if i:
                r, g, b = pal[3 * i:3 * i + 3]
                lums.append(0.3 * r + 0.59 * g + 0.11 * b)
    lo, hi = min(lums), max(lums)
    for y in range(nh):
        for x in range(nw):
            i = fp[x, y]
            if not i:
                continue
            r, g, b = pal[3 * i:3 * i + 3]
            l = 0.3 * r + 0.59 * g + 0.11 * b
            if l < 40:
                idx = 14
            else:
                l = 70 + (l - lo) / max(1, hi - lo) * 185
                idx = min(RAMP[:-1], key=lambda e: abs(e[1] - l))[0]
            canvas[oy + y][ox + x] = idx

    # white outline around the figure, like Lucas
    for y in range(H * 8):
        for x in range(W * 8):
            if canvas[y][x] == 0 and any(0 <= y + dy < H * 8 and 0 <= x + dx < W * 8 and canvas[y + dy][x + dx] not in (0, 13)
                                         for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))):
                canvas[y][x] = -1
    canvas = [[13 if v == -1 else v for v in row] for row in canvas]

    # cut into tiles, reuse identical ones
    slots = iter(free)
    made = {}
    new_map = list(dawn)
    for i in range(len(new_map)):
        new_map[i] = 0
    for ty in range(H):
        for tx in range(W):
            t = tuple(canvas[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8))
            if not any(t):
                continue
            if t not in made:
                slot = next(slots)
                made[t] = slot
                sy, sx = divmod(slot, tw)
                for k, v in enumerate(t):
                    tiles[sx * 8 + k % 8, sy * 8 + k // 8] = v
            new_map[(Y0 + ty) * 32 + X0 + tx] = made[t]
    # blank Dawn's old tiles that are no longer used
    for t in {e & 0x3FF for e in dawn} - set(made.values()) - lucas_tiles - {0}:
        sy, sx = divmod(t, tw)
        for k in range(64):
            tiles[sx * 8 + k % 8, sy * 8 + k // 8] = 0
    tiles_img.save(CASE / 'player_tiles.png')
    struct.pack_into(f'<{len(new_map)}H', dawn_data, 0x24, *new_map)
    (CASE / 'dawn.NSCR').write_bytes(bytes(dawn_data))
    print(f'{len(made)} tiles used')


if __name__ == '__main__':
    main()
