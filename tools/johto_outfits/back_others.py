from PIL import Image
def load(p):
    im = Image.open(p); W, H = im.size
    return im, W, H, [[im.getpixel((x, y)) for x in range(W)] for y in range(H)]
def frames(px, H):
    seps = [y for y in range(H) if all(v == 255 for v in px[y])]
    b = [0] + [y + 1 for y in seps]; e = seps + [H]
    return list(zip(b, e))
def save(im, out, path, prev, newpal=None):
    p = im.getpalette()
    for i, c in (newpal or {}).items(): p[3*i:3*i+3] = list(c)
    img = Image.new('P', im.size); img.putpalette(p); img.putdata([v for r in out for v in r]); img.save(path)
    img.convert('RGB').resize((im.size[0] * 3, im.size[1] * 3), Image.NEAREST).save(prev)

def juniper():
    im, W, H, px = load('/home/claude/pokeplatinum/res/trainers/classes/player_female/back.png')
    HAIR = {3, 4, 5, 6}; CLIP = {7, 1}
    out = [r[:] for r in px]
    for s, e in frames(px, H):
        hp = [(x, y) for y in range(s, e) for x in range(W) if px[y][x] in HAIR | CLIP]
        if not hp: continue
        top = min(y for _, y in hp); bot = max(y for x, y in hp if px[y][x] in HAIR)
        width = {y: [x for x, yy in hp if yy == y] for y in range(top, bot + 1)}
        maxw = max(max(v) - min(v) for v in width.values() if v)
        # bun = top rows clearly narrower than the head
        cut = top
        while cut < bot and (not width[cut] or max(width[cut]) - min(width[cut]) < 0.8 * maxw): cut += 1
        hxs = [x for x, y in hp]
        for y in range(s, cut):
            for x in range(max(0, min(hxs) - 3), min(W, max(hxs) + 4)):
                if px[y][x] not in (11, 12):
                    out[y][x] = 0
        # clip -> hair
        for x, y in hp:
            if px[y][x] in CLIP and y >= cut: out[y][x] = 5
        # round the crown: trim the corners of the first rows, then outline the new edge
        xs = width[cut]; L, R = min(xs), max(xs)
        for i, t in enumerate((6, 4, 2, 1, 1)):
            y = cut + i
            for x in list(range(L, L + t)) + list(range(R - t + 1, R + 1)):
                if out[y][x] in HAIR | {13}: out[y][x] = 0
        for y in range(cut - 2, cut + 6):
            for x in range(L - 2, R + 3):
                if out[y][x] == 13 and not any(out[y + b][x + a] in HAIR for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[y][x] = 0
        for y in range(cut - 1, cut + 6):
            for x in range(L - 1, R + 2):
                if out[y][x] == 0 and any(out[y + b][x + a] in HAIR for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[y][x] = 13
        for x in range(L + 4, R - 3):
            if out[cut][x] in HAIR: out[cut][x] = 6
        # long hair down the back: from the back half of the head down ~20 rows
        head_rows = [y for y in range(cut, bot + 1) if width[y]]
        hx0 = min(min(width[y]) for y in head_rows); hx1 = max(max(width[y]) for y in head_rows)
        back_w = int((hx1 - hx0) * 0.6)
        length = 22
        tips = [0, 2, 1, 3, 0, 2, 1]
        for i in range(length + 1):
            y = bot - 3 + i
            if y >= e: break
            x0 = hx0 + 1 + i // 5
            x1 = hx0 + back_w - i // 3
            for x in range(x0, x1 + 1):
                k = x - x0
                end = length - tips[k % len(tips)]
                if i > end: continue
                if px[y][x] not in (2, 8, 9, 15, 14, 0, 13, 3, 4, 5, 6): continue
                edge = x in (x0, x1) or i == end
                out[y][x] = 13 if edge else (4 if (k + i // 3) % 5 == 0 else (6 if k == 1 else 5))
    save(im, out, '/home/claude/pokeplatinum/res/johto_outfits/player_female/back.png', '/home/claude/ow/back_jun_new.png')

def barry():
    im, W, H, px = load('/home/claude/pokeplatinum/res/trainers/classes/rival/back.png')
    out = [r[:] for r in px]
    for s, e in frames(px, H):
        hair = [(x, y) for y in range(s, e) for x in range(W) if px[y][x] in (6, 9)]
        hb = max(y for _, y in hair) if hair else s + 30
        for y in range(s, e):
            for x in range(W):
                v = px[y][x]
                if y > hb - 6:
                    if v == 15: out[y][x] = 3          # white stripe -> orange
                    elif v == 8: out[y][x] = 2         # grey stripe shade -> dark orange
                    elif v == 7: out[y][x] = 15        # scarf -> white shirt
                    elif v == 1: out[y][x] = 8
                    elif v in (4, 5) and y > hb + 30: out[y][x] = 13 if v == 4 else 4
    save(im, out, '/home/claude/pokeplatinum/res/johto_outfits/rival/back.png', '/home/claude/ow/back_barry_new.png')

juniper(); barry()
