import sys
sys.path.insert(0, '/home/claude/ow')
from PIL import Image
import lucas_tmpl as T
SRC = '/home/claude/pokeplatinum/res/graphics/field_sprites/player/'
CH = '.123456789ABCDEF'
RED, PINK, DRED = (189, 57, 74), (222, 107, 123), (123, 66, 66)
BLACK, WHITE, LGRAY, NAVY, LAV = (0, 0, 0), (239, 239, 255), (206, 206, 222), (57, 66, 82), (173, 165, 206)
SKIN, SKINS, BLUE = (255, 214, 189), (222, 165, 123), (57, 99, 140)
TAN, DGRAY, BROWN = (206, 170, 116), (64, 64, 78), (140, 96, 64)
BERET = (RED, PINK)

walk = Image.open(SRC + 'player_m.png')
WP = [tuple(walk.getpalette()[3*i:3*i+3]) for i in range(16)]

def sheet(path):
    im = Image.open(path); p = im.getpalette(); pal = [tuple(p[3*i:3*i+3]) for i in range(16)]
    n = im.size[1] // 32
    frames = [[[None if im.getpixel((x, k*32+y)) == 0 else pal[im.getpixel((x, k*32+y))] for x in range(32)] for y in range(32)] for k in range(n)]
    return frames, pal[0]

def beret_box(fr):
    """(anchor_row, xmin, xmax) of the beret: the connected red/pink blob starting at the topmost
    red pixel. anchor = its last row holding red."""
    pts = [(x, y) for y in range(0, 26) for x in range(32) if fr[y][x] == RED]
    if len(pts) < 8: return None
    start = min(pts, key=lambda p: (p[1], p[0]))
    seen = {start}; stack = [start]
    while stack:
        x, y = stack.pop()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                q = (x + a, y + b)
                if q not in seen and 0 <= q[0] < 32 and 0 <= q[1] < 32 and fr[q[1]][q[0]] in BERET:
                    seen.add(q); stack.append(q)
    reds = [(x, y) for x, y in seen if fr[y][x] == RED]
    bot = max(y for _, y in reds)
    xs = [x for x, y in seen if y >= bot - 6]
    global LAST_COMP
    LAST_COMP = (seen, min(x for x, _ in seen), max(x for x, _ in seen))
    return bot, min(xs), max(xs)

BASE = None
def base():
    global BASE
    if BASE is None:
        fr, _ = sheet(SRC + 'player_m.png')
        BASE = {'up': fr[0], 'down': fr[4], 'left': fr[8], 'right': fr[12]}
    return BASE

def facing(fr):
    b = beret_box(fr)
    best = None
    for name, bf in base().items():
        bb = beret_box(bf)
        dy = b[0] - bb[0]; dx = round(((b[1] + b[2]) - (bb[1] + bb[2])) / 2)
        score = 0
        for y in range(bb[0] - 10, bb[0] + 3):
            for x in range(bb[1] - 1, bb[2] + 2):
                ty, tx = y + dy, x + dx
                a = bf[y][x] if 0 <= y < 32 and 0 <= x < 32 else None
                c = fr[ty][tx] if 0 <= ty < 32 and 0 <= tx < 32 else None
                score += a != c
        if best is None or score < best[0]: best = (score, name)
    return best[1], best[0]

def put_head(fr, face):
    key = {'up': 'UP', 'down': 'DOWN', 'left': 'LEFT', 'right': 'LEFT'}[face]
    x0, y0, t = getattr(T, key)
    t = [r.replace(' ', '.') for r in t]
    bb = beret_box(base()['left' if face == 'right' else face])
    if face == 'right':
        t = [r[::-1] for r in t]; x0 = 32 - x0 - len(t[0])
        bb = (bb[0], 31 - bb[2], 31 - bb[1])
    b = beret_box(fr)
    comp, cxmin, cxmax = LAST_COMP
    dy = b[0] - bb[0]; dx = round(((b[1] + b[2]) - (bb[1] + bb[2])) / 2)
    # things held next to the head (Poke Ball, hand, VS Seeker) stay in front of the new hair
    keep = {(x, y) for y in range(32) for x in range(32) if fr[y][x] is not None and y <= b[0] + 1 and (
        x < cxmin - 1 or x > cxmax + 1 or (fr[y][x] in BERET and (x, y) not in comp))}
    out = [r[:] for r in fr]
    for (x, y) in comp:
        out[y][x] = None
    for ry, row in enumerate(t):
        for rx, c in enumerate(row):
            X, Y = x0 + rx + dx, y0 + ry + dy
            if 0 <= X < 32 and 0 <= Y < 32 and (X, Y) not in keep:
                out[Y][X] = None if c == '.' else WP[CH.index(c)]
    return out, b[0] - bb[0], dx

def body(fr, face, top, dx):
    """top: offset so that base-frame torso starts at row 22+top."""
    out = [r[:] for r in fr]
    t0 = 22 + top
    cx = 15 + dx
    for y in range(max(0, t0), 32):
        for x in range(32):
            v = fr[y][x]
            if v == LAV: out[y][x] = DGRAY
            elif v == RED and not any(0 <= x + a < 32 and 0 <= y + b < 32 and fr[y + b][x + a] == WHITE
                                       for a in (-1, 0, 1) for b in (-1, 0, 1)):
                near_skin = any(0 <= x + a < 32 and fr[y][x + a] in (SKIN, SKINS) for a in (-1, 1))
                out[y][x] = NAVY if near_skin else TAN
            if face == 'down' and y < t0 + 4 and abs(x - cx) <= 3 and v in (WHITE, LGRAY, LAV, PINK):
                out[y][x] = DGRAY
    for y in range(max(0, t0 + 5), 32):
        for x in range(32):
            v = out[y][x]
            if v not in (NAVY, BLUE): continue
            side = [out[y][x + a] if 0 <= x + a < 32 else None for a in (-1, 1)]
            if not any(c in (NAVY, BLUE, TAN, BROWN) for c in side): continue  # 1px line (fishing rod)
            if v == NAVY: out[y][x] = TAN
            else: out[y][x] = BROWN if y == t0 + 5 else NAVY
    for y in range(32):
        for x in range(32):
            v = out[y][x]
            if v == DRED: out[y][x] = BROWN
            elif v in (RED, PINK) and y >= t0:
                ball = any(0 <= x + a < 32 and 0 <= y + b < 32 and fr[y + b][x + a] == WHITE
                           for a in (-1, 0, 1) for b in (-1, 0, 1))
                if not ball: out[y][x] = TAN if v == RED else DGRAY
    return out

def convert(path, legs=True):
    frames, bg = sheet(path)
    res = []; info = []
    for k, fr in enumerate(frames):
        if beret_box(fr) is None:
            res.append(fr); info.append((k, None)); continue
        face, score = facing(fr)
        n, top, dx = put_head(fr, face)
        n = body(n, face, top, dx) if legs else n
        res.append(n); info.append((k, face, score))
    return res, bg, info

def save(frames, bg, path):
    cols = []
    for fr in frames:
        for row in fr:
            for c in row:
                if c is not None and c not in cols: cols.append(c)
    if len(cols) > 15:
        from collections import Counter
        cnt = Counter(c for fr in frames for row in fr for c in row if c is not None)
        while len(cols) > 15:
            a, b = min(((a, b) for i, a in enumerate(cols) for b in cols[i + 1:]),
                       key=lambda ab: sum((p - q) ** 2 for p, q in zip(*ab)))
            keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
            print('  merge', drop, '->', keep, 'in', path.split('/')[-1])
            for fr in frames:
                for row in fr:
                    for i, c in enumerate(row):
                        if c == drop: row[i] = keep
            cnt[keep] += cnt.pop(drop); cols.remove(drop)
    pal = [bg] + cols
    im = Image.new('P', (32, 32 * len(frames)))
    flat = []
    for c in pal: flat += list(c)
    flat += [0] * (48 - len(flat))
    im.putpalette(flat + [0] * (768 - len(flat)))
    for k, fr in enumerate(frames):
        for y in range(32):
            for x in range(32):
                c = fr[y][x]
                im.putpixel((x, k * 32 + y), 0 if c is None else pal.index(c))
    im.save(path)

def preview(frames, path, S=3, per=16, labels=None):
    from PIL import ImageDraw
    rows = (len(frames) + per - 1) // per
    o = Image.new('RGB', (per * (32 * S + 4), rows * (32 * S + 14)), (120, 160, 120)); d = ImageDraw.Draw(o)
    for i, fr in enumerate(frames):
        X, Y = (i % per) * (32 * S + 4), (i // per) * (32 * S + 14)
        for y in range(32):
            for x in range(32):
                c = fr[y][x]
                if c is not None: d.rectangle((X + x * S, Y + 12 + y * S, X + x * S + S - 1, Y + 12 + y * S + S - 1), fill=c)
        if labels: d.text((X, Y), labels[i], fill=(0, 0, 0))
    o.save(path)
