"""Juniper battle back sprite, repainted from Dawn's (player_female/back.png, read from git HEAD).

usage: juniper_back.py <out_dir>   writes back.png + preview.png into out_dir (does not touch res/)
"""
import io
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path('/workspaces/pokeplatinum')
SRC = 'res/trainers/classes/player_female/back.png'

T, REDD, COAT, HAIR3, HAIR4, HAIR5, HAIR6, RED, SHADE, FOLD, A, SKIN, SKINL, D, COATD, WHITE = range(16)
PALETTE = [
    (197, 189, 156),  # 0 transparent
    (156, 41, 49),    # 1 red dark (clip / earring)
    (222, 234, 230),  # 2 coat
    (98, 57, 41),     # 3 hair deepest
    (148, 98, 57),    # 4 hair dark
    (197, 139, 82),   # 5 hair mid
    (230, 189, 123),  # 6 hair light
    (238, 82, 74),    # 7 red
    (180, 189, 205),  # 8 coat shade
    (131, 139, 156),  # 9 coat fold
    (123, 65, 65),    # 10 brown outline (skin)
    (222, 164, 123),  # 11 skin
    (255, 213, 189),  # 12 skin light
    (0, 0, 0),        # 13 outline
    (98, 115, 123),   # 14 coat dark
    (250, 250, 255),  # 15 coat white
]

# Every frame's head is Dawn's frame-0 head moved; ANCHOR0 is the beanie top in frame 0.
ANCHOR0 = (23, 9)

# ---- Juniper's head, in frame-0 coordinates --------------------------------------------------
# hair silhouette: row -> (left x, right x) inclusive, outline included
SKULL = {
    11: (21, 38), 12: (19, 41), 13: (18, 43), 14: (17, 45), 15: (17, 46), 16: (17, 46), 17: (17, 46),
    18: (17, 46), 19: (17, 46), 20: (17, 47), 21: (17, 47), 22: (17, 47), 23: (17, 47), 24: (17, 47),
    25: (17, 47), 26: (17, 47), 27: (17, 46), 28: (18, 39), 29: (19, 38), 30: (20, 37), 31: (22, 36),
    32: (24, 35), 33: (27, 33),
}
BUN = {5: (27, 32), 6: (25, 34), 7: (24, 35), 8: (23, 36), 9: (23, 36), 10: (23, 36), 11: (23, 36), 12: (24, 35)}
BUN_C = (29.5, 9.0)       # bun centre
SWEEP = (30.0, 13.0)      # point the hair is swept up to (bun base)
# neck (skin) rows under the hair, left/right x
NECK = {32: (34, 36), 33: (34, 36), 34: (29, 38), 35: (29, 38), 36: (29, 39), 37: (29, 39), 38: (29, 39)}
COLLAR_Y = 39             # first row of the lab-coat collar behind the neck
# rows 28..40 at x >= FACE_X are Dawn's cheek / jaw (kept, her dark hair lock recoloured brown)
FACE_X = 39
CLIP = [(21, 11, 'dd.'), (20, 12, 'd77d'), (20, 13, 'd71d'), (20, 14, 'd71d'), (21, 15, 'dd')]
EAR = [(37, 29, 'aba'), (36, 30, 'abcb'), (36, 31, 'abbb'), (37, 32, 'aba'), (37, 33, 'd7d'), (37, 34, 'd1d'), (38, 35, 'd')]

# ---- back outline per pose (absolute coordinates in that frame) -------------------------------
# Dawn's long hair left of / below this line is removed; hair right of it becomes lab coat.
BACK = {
    0: [(29, 39), (23, 41), (20, 44), (19, 49), (22, 54), (28, 57), (32, 59)],
    1: [(23, 42), (17, 44), (13, 48), (12, 54), (15, 60), (22, 63), (30, 64)],
    2: [(40, 40), (33, 42), (26, 44), (23, 46), (24, 50), (28, 54), (34, 56), (37, 58)],
    3: [(33, 41), (28, 43), (26, 45), (27, 46), (30, 47), (28, 51), (24, 55)],
    5: [(40, 46), (35, 48), (32, 50), (32, 52), (29, 55), (24, 58)],
}
POSE = {0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 5, 6: 5, 7: 5}

SYM = {'d': D, '7': RED, '1': REDD, 'a': A, 'b': SKIN, 'c': SKINL, '3': HAIR3, '4': HAIR4, '5': HAIR5, '6': HAIR6}


def git_image(path):
    data = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT, capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data))


def edge_x(poly, y):
    """x of the back line at row y (None above / below it)."""
    if y < poly[0][1]:
        return None
    for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / max(1, y1 - y0)
    return None


def hair_shade(x, y):
    """Hair swept up into the bun: strands radiate from SWEEP, lit from the top left."""
    dx, dy = x - SWEEP[0], y - SWEEP[1]
    r = math.hypot(dx, dy)
    th = math.atan2(dy, dx)
    strand = (th / 0.42) % 1.0
    lit = -(dx * 0.55 + dy * 0.85)           # higher = toward the light (top left)
    if r > 6 and strand < 0.16:
        return HAIR4 if lit > -14 else HAIR3
    if lit > 2 and 0.45 < strand < 0.75 and r > 4:
        return HAIR6
    if lit < -12:
        return HAIR4
    return HAIR5


def bun_shade(x, y):
    dx, dy = x - BUN_C[0], y - BUN_C[1]
    th = math.atan2(dy, dx)
    swirl = ((th + math.hypot(dx, dy) * 0.45) / 0.9) % 1.0   # coiled strands
    if swirl < 0.22:
        return HAIR4
    if dx + dy < -3 and swirl > 0.55:
        return HAIR6
    if dx + dy > 4:
        return HAIR4
    return HAIR5


def convert(frame, fi):
    w, h = frame.size
    src = frame.load()
    g = lambda x, y: src[x, y] if 0 <= x < w and 0 <= y < h else 0
    ax, ay = next((x, y) for y in range(h) for x in range(w) if src[x, y] == 14)
    ox, oy = ax - ANCHOR0[0], ay - ANCHOR0[1]          # frame-0 -> this frame
    poly = BACK[POSE[fi]]
    hat_top, brim = ay, ay + 19

    out = Image.new('P', frame.size, 0)
    o = out.load()

    # 1. body: Dawn's colours -> Juniper's
    for y in range(h):
        for x in range(w):
            c = src[x, y]
            if c == 0 or y < brim:          # beanie is redrawn below
                continue
            ex = edge_x(poly, y)
            hair = c in (4, 5)
            if hair or (c == 13 and ex is not None and x < ex and any(g(*p) in (4, 5) for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)))):
                if ex is not None and x < ex:
                    continue                 # Dawn's long hair hanging off the back
                if ex is None:
                    continue
                n = COAT
            elif c == 13:
                n = D
            elif c in (2,):
                n = COAT
            elif c in (3, 15):
                n = WHITE
            elif c in (8, 1, 7):
                n = SHADE
            elif c == 14:
                n = COATD
            elif c == 10:
                n = A if any(g(*p) in (11, 12) for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))) else FOLD
            else:
                n = c
            o[x, y] = n

    # strand lines that were inside Dawn's hair: drop them (now the back of the coat)
    for y in range(brim, h):
        for x in range(w):
            if src[x, y] == 13 and o[x, y] == D:
                nb = [g(x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j]
                if all(v in (4, 5, 13) for v in nb):
                    o[x, y] = COAT

    # 2. head
    def put(x, y, v):
        x, y = x + ox, y + oy
        if 0 <= x < w and 0 <= y < h:
            o[x, y] = v

    # clear Dawn's hair in the head / nape area that is outside Juniper's head
    for y in range(brim, brim + 21):
        y0 = y - oy
        for x in range(w):
            x0 = x - ox
            if src[x, y] in (4, 5) or (src[x, y] == 13 and any(g(*p) in (4, 5) for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)))):
                if x0 >= FACE_X and y0 <= 34:
                    o[x, y] = {4: HAIR4, 5: HAIR5}.get(src[x, y], D)   # lock in front of the ear
                elif y0 < COLLAR_Y:
                    o[x, y] = 0
    # Dawn's pink hair clip / white lock by the face
    for y in range(brim, brim + 12):
        for x in range(w):
            x0 = x - ox
            if src[x, y] in (1, 7) or (src[x, y] in (8, 15, 14) and x0 >= 34 and x0 <= 42 and y - oy < 36):
                o[x, y] = HAIR6 if src[x, y] == 15 else HAIR5 if src[x, y] == 8 else HAIR4

    for y, (l, r) in SKULL.items():
        for x in range(l, r + 1):
            edge = x in (l, r) or (y - 1 not in SKULL or not SKULL[y - 1][0] <= x <= SKULL[y - 1][1]) \
                or (y + 1 not in SKULL or not SKULL[y + 1][0] <= x <= SKULL[y + 1][1])
            if y >= 28 and x >= FACE_X:
                continue
            put(x, y, D if edge and not (y >= 27 and x >= FACE_X - 1 and not x == l) else hair_shade(x, y))
    for y, (l, r) in BUN.items():
        for x in range(l, r + 1):
            edge = x in (l, r) or y - 1 not in BUN or not BUN[y - 1][0] <= x <= BUN[y - 1][1]
            if y >= 11 and not edge and y in SKULL:
                put(x, y, bun_shade(x, y))
            else:
                put(x, y, D if edge else bun_shade(x, y))
    # bun / skull seam: a dark crease under the bun
    for x in range(BUN[12][0], BUN[12][1] + 1):
        put(x, 13, HAIR4)
    # the hairline at the nape: little wisps
    for x, y in ((28, 33), (31, 33), (30, 34)):
        put(x, y, HAIR4)
    # neck
    for y, (l, r) in NECK.items():
        for x in range(l, r + 1):
            if (x + ox, y + oy) and 0 <= y + oy < h and 0 <= x + ox < w and o[x + ox, y + oy] in (D, HAIR4, HAIR5) and y <= 34 and x in (24, 27, 30, 26, 29):
                continue
            v = A if x == l else SKIN if (y <= 34 or x < l + 4) else SKINL if x > r - 4 else SKIN
            put(x, y, v)
    for x, y, s in CLIP + EAR:
        for i, ch in enumerate(s):
            if ch != '.':
                put(x + i, y, SYM[ch])

    # 4. fill gaps between the back line and the body, then outline the back
    for y in range(poly[0][1], poly[-1][1] + 1):
        ex = edge_x(poly, y)
        if ex is None:
            continue
        xl = int(round(ex))
        body = [x for x in range(max(0, xl), w) if src[x, y] not in (0, 4, 5, 13)]
        if not body:
            continue
        for x in range(max(0, xl), body[0]):
            if o[x, y] in (0, D):
                o[x, y] = COAT
    # leftovers of Dawn's hair outline left of the back line, and her flying scarf -> coat tail
    for y in range(h):
        ex = edge_x(poly, y)
        for x in range(w):
            body_nb = any(g(*p) in (2, 3, 10, 11, 12, 8, 14, 15, 1, 7) for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)))
            left = ex is not None and x < ex or ex is None and y >= poly[0][1] - 0 and y <= poly[-1][1]
            if src[x, y] == 13 and o[x, y] == D and (ex is not None and x < ex - 1) and not body_nb:
                o[x, y] = 0
            if ex is not None and x < ex and src[x, y] in (8, 14) and y > poly[0][1] + 6:
                o[x, y] = COAT if src[x, y] == 8 else SHADE
    for y in range(h):
        for x in range(w):
            if o[x, y] in (COAT, WHITE, SHADE) and src[x, y] in (4, 5, 13, 0):
                nb = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                if any(not (0 <= p[0] < w and 0 <= p[1] < h) or o[p] == 0 for p in nb):
                    o[x, y] = D
    # rim light just inside the back outline, soft shadow further in
    for y in range(h):
        for x in range(1, w):
            if o[x, y] == COAT and o[x - 1, y] == D and src[x, y] in (4, 5, 13, 0):
                o[x, y] = WHITE
            elif o[x, y] == COAT and src[x, y] in (4, 5, 13, 0) and x + 3 < w and o[x + 3, y] in (D, COATD, A, FOLD):
                o[x, y] = SHADE
    # isolated pixels
    for y in range(h):
        for x in range(w):
            if o[x, y] and not any(0 <= x + i < w and 0 <= y + j < h and o[x + i, y + j]
                                   for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j):
                o[x, y] = 0
    return out


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    src = git_image(SRC)
    n = (src.height + 1) // 81
    sheet = Image.new('P', src.size, 0)
    sheet.putpalette([v for c in PALETTE for v in c] + [0] * (768 - 48))
    for i in range(n):
        f = src.crop((0, 81 * i, 80, 81 * i + 80))
        sheet.paste(convert(f, i), (0, 81 * i))
    sp, op = src.load(), sheet.load()
    for i in range(1, n):
        for x in range(80):
            op[x, 81 * i - 1] = sp[x, 81 * i - 1]
    sheet.save(out_dir / 'back.png')

    bg = (96, 144, 96, 255)
    prev = Image.new('RGBA', (n * 82, 2 * 84), bg)
    for i in range(n):
        for row, im in enumerate((src, sheet)):
            crop = im.crop((0, 81 * i, 80, 81 * i + 80))
            mask = Image.new('L', (80, 80))
            mask.putdata([0 if v == 0 else 255 for v in crop.get_flattened_data()])
            prev.paste(crop.convert('RGBA'), (i * 82, row * 84), mask)
    prev.resize((prev.width * 3, prev.height * 3), Image.NEAREST).save(out_dir / 'preview.png')
    big = sheet.crop((0, 0, 80, 80)).convert('RGBA')
    m = Image.new('L', (80, 80)); m.putdata([0 if v == 0 else 255 for v in sheet.crop((0, 0, 80, 80)).get_flattened_data()])
    zb = Image.new('RGBA', (80, 80), bg); zb.paste(big, (0, 0), m)
    zb.resize((640, 640), Image.NEAREST).save(out_dir / 'frame0_big.png')


if __name__ == '__main__':
    main()
