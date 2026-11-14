import sys
sys.path.insert(0, '/home/claude/ow')
from PIL import Image
import jun_tmpl as T
from lucas_rgb import save, preview
SRC = '/home/claude/pokeplatinum/res/graphics/field_sprites/player/'
CH = '.123456789ABCDEF'
walk = Image.open(SRC + 'player_f.png')
WP = [tuple(walk.getpalette()[3*i:3*i+3]) for i in range(16)]
OUT, DG, G, GB, DR, HM, R, COATG, HL, RA, SKS, COATW, HH, SK, EW = WP[1:]
HAIR = (HM, HL, HH, (98, 57, 41), (74, 41, 33), (164, 115, 66))
YEL, YELS, JEANS, JEANSD = (236, 196, 72), (189, 139, 82), (80, 114, 192), (52, 76, 148)

def sheet(path):
    im = Image.open(path); p = im.getpalette(); pal = [tuple(p[3*i:3*i+3]) for i in range(16)]
    return [[[None if im.getpixel((x, k*32+y)) == 0 else pal[im.getpixel((x, k*32+y))] for x in range(32)]
             for y in range(32)] for k in range(im.size[1] // 32)], pal[0]

BASE = None
def base():
    global BASE
    if BASE is None:
        fr, _ = sheet(SRC + 'player_f.png')
        BASE = {'up': fr[0], 'down': fr[4], 'left': fr[8], 'right': fr[12]}
    return BASE

def match(fr):
    """Best (facing, dx, dy, score): where the old Juniper head (rows 5-18 of a base frame) sits."""
    best = None
    for name, bf in base().items():
        pts = [(x, y, bf[y][x]) for y in range(5, 19) for x in range(32) if bf[y][x] is not None]
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                sc = 0
                for x, y, c in pts:
                    X, Y = x + dx, y + dy
                    sc += not (0 <= X < 32 and 0 <= Y < 32 and fr[Y][X] == c)
                if best is None or sc < best[3]: best = (name, dx, dy, sc)
    return best

def template(face):
    if face == 'right':
        return {y: [(31 - x - len(s) + 1, s[::-1]) for x, s in p] for y, p in T.LEFT.items()}, True
    return getattr(T, face.upper()), False

COATS = (COATG, COATW, (239, 239, 255), (206, 206, 222), EW)
def head_span(bf):
    span = {}
    for y in range(5, 19):
        xs = [x for x in range(32) if bf[y][x] is not None]
        if xs: span[y] = (min(xs), max(xs))
    return span

def put_head(fr, face, dx, dy):
    tm, _ = template(face)
    bf = base()[face]
    span = head_span(bf)
    out = [r[:] for r in fr]
    cx = 15.5 + dx
    def outside(x, y):
        sp = span.get(min(max(y - dy, 5), 18))
        return sp is None or x - dx < sp[0] - 1 or x - dx > sp[1] + 1
    greens = [(x, y) for y in range(0, min(32, 20 + dy)) for x in range(32)
              if (fr[y][x] in (DG, G) or (fr[y][x] == RA and abs(x - cx) >= 8)) and outside(x, y)]
    keep = {(x + a, y + b) for x, y in greens for a in range(-2, 3) for b in range(-2, 3)}
    for y, pieces in tm.items():
        for x, s in pieces:
            for i, c in enumerate(s):
                X, Y = x + i + dx, y + dy
                if c == ' ' or not (0 <= X < 32 and 0 <= Y < 32): continue
                v = fr[Y][X]
                if (X, Y) in keep and v is not None: continue
                if v is not None:
                    sp = span.get(y)
                    outside = sp is None or not (sp[0] - 1 <= x + i <= sp[1] + 1)
                    if y <= 18 and outside and v not in HAIR + (OUT,): continue  # held item / hand
                    if y >= 19:
                        back = face == 'up' and 8 <= x + i <= 23
                        if back and v not in HAIR + COATS + (OUT, (0, 0, 0), (123, 66, 66), (74, 41, 33)): continue
                        if not back and v not in HAIR: continue  # hair hangs behind the body
                out[Y][X] = None if c == '.' else WP[CH.index(c)]
    DARK = ((123, 66, 66), (74, 41, 33), (98, 57, 41), (0, 0, 0))
    for y in range(10, 26):
        sp = span.get(min(max(y, 5), 18))
        if not sp: continue
        for x in range(32):
            X, Y = x + dx, y + dy
            if not (0 <= X < 32 and 0 <= Y < 32) or (X, Y) in keep: continue
            mid = (span[14][0] + span[14][1]) / 2
            behind = (face == 'left' and (x > sp[1] or (x >= mid + 1 and y >= 12))) or \
                     (face == 'right' and (x < sp[0] or (x <= mid - 1 and y >= 12)))
            inner = 0 < X < 31 and out[Y][X - 1] is not None and out[Y][X + 1] is not None \
                and 0 < Y < 31 and out[Y - 1][X] is not None and out[Y + 1][X] is not None
            if behind and inner and out[Y][X] in DARK + (OUT,):
                out[Y][X] = HM
    if face == 'up':
        # back of the head: everything between the hair edges at rows 12-17 is hair
        for y in range(12, 22):
            Y = y + dy
            if not 0 <= Y < 32: continue
            xs = [X for X in range(32) if out[Y][X] in HAIR]
            if len(xs) < 2: continue
            for X in range(min(xs) + 1, max(xs)):
                v = out[Y][X]
                if v is None or v in HAIR or v == RA or (X, Y) in keep: continue
                if y < 18 or v in COATS + (DG, G, GB, OUT, (0, 0, 0)):
                    out[Y][X] = HM
        for Y in range(max(0, 10 + dy), min(32, 22 + dy)):
            for X in range(1, 31):
                if out[Y][X] in ((74, 41, 33), (98, 57, 41)) and out[Y][X - 1] in HAIR and out[Y][X + 1] in HAIR:
                    out[Y][X] = HM
        hairish = HAIR
        for _ in range(2):
            for Y in range(max(0, 10 + dy), min(32, 22 + dy)):
                for X in range(1, 31):
                    if out[Y][X] in (OUT, GB) and out[Y][X - 1] in hairish and out[Y][X + 1] in hairish:
                        out[Y][X] = HM
    return out

def body(fr, dy, face, cx, legs=True):
    out = [r[:] for r in fr]
    DARK = ((123, 66, 66), (74, 41, 33), (98, 57, 41), (131, 90, 57))
    for y in range(32):
        r = y - dy
        for x in range(32):
            v = fr[y][x]
            if v is None: continue
            near = abs(x - cx) <= 5
            if r >= 19 and v == GB and face != 'up': out[y][x] = YEL
            elif r >= 19 and v == DR and face != 'up': out[y][x] = YELS
            elif r >= 24 and v == G and legs: out[y][x] = JEANS
            elif r >= 24 and v == DG and legs: out[y][x] = JEANSD
            elif legs and r >= 26 and abs(x - cx) <= 7 and v in (SK, SKS, (255, 214, 189), (222, 165, 123)):
                out[y][x] = JEANS if v in (SK, (255, 214, 189)) else JEANSD
            elif legs and r >= 27 and abs(x - cx) <= 7 and v in (RA, R): out[y][x] = YEL
            elif face in ('up', 'left', 'right') and 17 <= r < 26 and v in DARK: out[y][x] = HM
            elif face == 'down' and 20 <= r < (23 if not legs else 26) and near and v in DARK:
                out[y][x] = YEL if v == (131, 90, 57) else YELS
            elif legs and r >= 26 and abs(x - cx) <= 4 and v in DARK: out[y][x] = JEANSD
    return out

def convert(path):
    frames, bg = sheet(path)
    res, info = [], []
    for k, fr in enumerate(frames):
        face, dx, dy, sc = match(fr)
        sp = head_span(base()[face]); mid = (sp[16][0] + sp[16][1]) / 2 if 16 in sp else 15.5
        n = body(fr, dy, face, mid + dx, legs='bike' not in path)
        n = put_head(n, face, dx, dy)
        res.append(n); info.append((k, face, dx, dy, sc))
    return res, bg, info
