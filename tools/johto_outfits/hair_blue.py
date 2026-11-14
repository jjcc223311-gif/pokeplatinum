"""Brighten Lucas's hair from navy to the reference's blue, only on hair pixels."""
from PIL import Image
from collections import Counter
DARKEST, DARK, MID = (30, 38, 100), (46, 72, 166), (82, 124, 218)
MAP = {(32, 32, 41): DARKEST, (57, 65, 82): DARK, (57, 66, 82): DARK, (57, 98, 139): MID, (57, 99, 140): MID}
BLACK = (0, 0, 0)

def recolor(path, frame_h, depth, halves=1, MAP=MAP):
    im = Image.open(path); W, H = im.size; p = im.getpalette(); n = len(p) // 3
    pal = [tuple(p[3*i:3*i+3]) for i in range(n)]
    px = [[im.getpixel((x, y)) for x in range(W)] for y in range(H)]
    rgb = [[pal[v] if v < n else None for v in row] for row in px]
    hair = set()
    fw = W // halves
    for f0 in range(0, H, frame_h):
        for h0 in range(0, W, fw):
            cells = [(x, y) for y in range(f0, min(H, f0 + frame_h)) for x in range(h0, h0 + fw)
                     if px[y][x] not in (0, 255) and px[y][x] < 16]
            if not cells: continue
            top = min(y for _, y in cells)
            lim = top + depth
            seeds = [(x, y) for x, y in cells if y <= top + 2 and rgb[y][x] in MAP]
            seen = set(seeds); st = list(seeds)
            while st:
                x, y = st.pop()
                for a in (-1, 0, 1):
                    for b in (-1, 0, 1):
                        q = (x + a, y + b)
                        if q in seen or not (h0 <= q[0] < h0 + fw and f0 <= q[1] <= lim and q[1] < H): continue
                        c = rgb[q[1]][q[0]]
                        if c in MAP or c == BLACK:
                            seen.add(q); st.append(q)
            hair |= {q for q in seen if rgb[q[1]][q[0]] in MAP}
    for x, y in hair: rgb[y][x] = MAP[rgb[y][x]]
    # rebuild indices 1..15
    cnt = Counter(c for row in rgb for c in row if c is not None)
    bg = pal[0]
    cnt.pop(bg, None)
    cols = list(cnt)
    protected = {DARKEST, DARK, MID, BLACK, (222, 164, 123), (255, 213, 189), (222, 172, 139), (255, 222, 197), (238, 238, 255)}
    while len(cols) > 15:
        cand = [(a, b) for i, a in enumerate(cols) for b in cols[i+1:] if not ({a, b} & protected)]
        a, b = min(cand, key=lambda ab: sum((u - v) ** 2 for u, v in zip(*ab)))
        keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
        print('   merge', drop, '->', keep)
        for row in rgb:
            for i, c in enumerate(row):
                if c == drop: row[i] = keep
        cnt[keep] += cnt.pop(drop); cols.remove(drop)
    newpal = [bg] + cols
    out = Image.new('P', (W, H))
    flat = [v for c in newpal for v in c]
    flat += list(p[len(flat):]) if len(p) > len(flat) else []
    flat += [0] * (768 - len(flat))
    out.putpalette(flat[:768])
    out.putdata([255 if px[y][x] == 255 else (0 if rgb[y][x] is None or (px[y][x] == 0) else newpal.index(rgb[y][x]))
                 for y in range(H) for x in range(W)])
    # keep the original palette length
    if n == 16:
        out.putpalette(flat[:48])
    out.save(path)
    print(path, 'hair px', len(hair), 'colors', len(newpal))

import sys
B = '/home/claude/pokeplatinum/res/johto_outfits/'
FRONT = {(32, 32, 41): DARK, (57, 65, 82): MID, (57, 66, 82): MID}
MUG = {(65, 65, 90): DARK, (90, 98, 123): MID}
for f in sys.argv[1:]:
    if f == 'front': recolor(B + 'player_male/front.png', 80, 18, MAP=FRONT)
    if f == 'front_scan': recolor(B + 'player_male/front_scan.png', 80, 18, halves=2, MAP=FRONT)
    if f == 'mugshot': recolor(B + 'player_male/mugshot.png', 64, 30, MAP=MUG)
