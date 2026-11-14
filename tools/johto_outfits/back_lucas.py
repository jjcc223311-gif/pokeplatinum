import sys
from PIL import Image
SRC = '/home/claude/pokeplatinum/res/trainers/classes/player_male/back.png'
OUT = '/home/claude/pokeplatinum/res/johto_outfits/player_male/back.png'
im = Image.open(SRC); W, H = im.size
px = [[im.getpixel((x, y)) for x in range(W)] for y in range(H)]
BERET = {2, 3}
# frames are 80 tall with a 1-px separator row (index 255) between them
starts = [0] + [y + 1 for y in range(H) if all(v == 255 for v in px[y])]
def frame_rows(s):
    e = s
    while e < H and not all(v == 255 for v in px[e]): e += 1
    return s, e
out = [r[:] for r in px]
for s in starts:
    s, e = frame_rows(s)
    # beret = connected blob of red/pink starting from the topmost red pixel, plus its band/logo
    reds = [(x, y) for y in range(s, e) for x in range(W) if px[y][x] in BERET]
    if not reds: continue
    top = min(y for _, y in reds)
    seed = min((p for p in reds if p[1] == top), key=lambda p: p[0])
    comp = {seed}; st = [seed]
    while st:
        x, y = st.pop()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                q = (x + a, y + b)
                if q not in comp and s <= q[1] < e and 0 <= q[0] < W and px[q[1]][q[0]] in BERET:
                    comp.add(q); st.append(q)
    bot = max(y for _, y in comp); xmin = min(x for x, _ in comp); xmax = max(x for x, _ in comp)
    # band and logo: anything non-outline inside the beret's rows/cols that is not skin or dark hair
    mask = set(comp)
    for y in range(top, bot + 2):
        row = [x for x, yy in comp if yy == y]
        if not row: continue
        for x in range(min(row), max(row) + 1):
            if px[y][x] not in (0, 13, 12, 4, 255): mask.add((x, y))
    # band row(s) right under the red: gray/lavender strip
    for y in range(bot - 1, bot + 3):
        for x in range(xmin, xmax + 1):
            if px[y][x] in (8, 9, 14, 6, 15): mask.add((x, y))
    H_ = bot - top + 1
    for (x, y) in mask:
        t = (y - top) / max(1, H_)
        out[y][x] = 7 if t < 0.25 else (1 if t < 0.6 else 5)
        if px[y][x] == 10: out[y][x] = 4          # old beret edge shade -> darkest hair
    # strands in the lower half
    for (x, y) in mask:
        t = (y - top) / max(1, H_)
        if t > 0.35 and (x + (y - top)) % 6 == 0: out[y][x] = 5 if out[y][x] != 5 else 4
    # spikes along the top edge, sweeping back (left)
    cols = sorted({x for x, _ in mask})
    topy = {x: min(y for xx, y in mask if xx == x) for x in cols}
    for y in range(top, min(e, bot + 4)):
        for x in range(xmin - 1, xmax + 2):
            if out[y][x] == 10: out[y][x] = 4
    # shirt: the white front of the top (front side, below the head) becomes the black shirt
    for y in range(bot + 3, e):
        for x in range((xmin + xmax) // 2 - 3, W):
            if px[y][x] in (6, 15, 14): out[y][x] = 4
            elif px[y][x] in (8, 9): out[y][x] = 5
    spikes = set()
    for i, c in enumerate(cols[2:-2:6]):
        y0 = topy[c]; h = 5 + (i % 2)
        for k in range(1, h + 1):
            w = max(1, 5 - k)
            xs = c - k
            for x in range(xs, xs + w):
                if 0 <= x < W and out[y0 - k][x] == 0:
                    out[y0 - k][x] = 7 if k < h - 1 else 1
                    spikes.add((x, y0 - k))
    for y in range(s, e):
        for x in range(W):
            if out[y][x] == 0 and any(0 <= x + a < W and s <= y + b < e and out[y + b][x + a] in (1, 7, 5)
                                      and (x + a, y + b) in spikes
                                      for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = 13
    # body: red/pink below the head -> tan (palette 2/3 become tan colours)
# palette: 2 red -> tan, 3 pink -> light tan, 10 dark red -> brown
p = im.getpalette()
for i, c in ((2, (206, 170, 116)), (3, (232, 204, 160)), (10, (140, 96, 64))):
    p[3*i:3*i+3] = list(c)
img = Image.new('P', (W, H)); img.putpalette(p)
img.putdata([v for r in out for v in r])
import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT)
img.convert('RGB').resize((W * 3, H * 3), Image.NEAREST).save('/home/claude/ow/back_lucas_new.png')
