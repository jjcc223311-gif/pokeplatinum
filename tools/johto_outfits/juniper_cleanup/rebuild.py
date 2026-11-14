import sys, numpy as np
from PIL import Image
from collections import deque
sys.path.insert(0, '/home/claude/jclean')
from clean import despeckle
REF = '/home/claude/outfit_work/ref.png'
PACKPAL = Image.open('/home/claude/jun_pack/res/trainers/classes/player_female/front.png').getpalette()[:48]
PAL = [tuple(PACKPAL[3*i:3*i+3]) for i in range(16)]

def cutout(box):
    a = np.array(Image.open(REF).convert('RGB')).astype(int)
    x0, y0, x1, y1 = box
    crop = a[y0:y1, x0:x1]
    bg = np.array([244, 240, 238]); near = np.abs(crop - bg).sum(2) <= 24
    h, w = near.shape; seen = np.zeros_like(near); dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x]: seen[y, x] = 1; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not seen[y, x]: seen[y, x] = 1; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not seen[ny, nx]: seen[ny, nx] = 1; dq.append((ny, nx))
    return crop, 1 - seen

def shrink(crop, alpha, W, H):
    rgba = np.dstack([crop * alpha[..., None], alpha * 255]).astype(np.uint8)
    small = np.array(Image.fromarray(rgba, 'RGBA').resize((W, H), Image.BOX)).astype(float)
    al = small[..., 3]
    rgb = np.where(al[..., None] > 0, small[..., :3] * 255 / np.maximum(al[..., None], 1), 0)
    return rgb, al

def to_pal(rgb, op):
    P = np.array(PAL[1:], float)
    d = ((rgb[..., None, :] - P[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1) + 1
    return np.where(op, idx, 0).astype(np.uint8)

def outline(idx):
    sil = idx > 0; edge = np.zeros_like(sil)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sh = np.zeros_like(sil)
        ys = slice(max(dy, 0), sil.shape[0] + min(dy, 0)); yd = slice(max(-dy, 0), sil.shape[0] + min(-dy, 0))
        xs = slice(max(dx, 0), sil.shape[1] + min(dx, 0)); xd = slice(max(-dx, 0), sil.shape[1] + min(-dx, 0))
        sh[ys, xs] = sil[yd, xd]; edge |= sh
    edge &= ~sil
    out = idx.copy(); out[edge] = 1
    return out

def save(idx, path):
    im = Image.fromarray(idx, 'P'); p = list(PACKPAL) + [0] * (768 - 48); p[0:3] = [0, 0, 0]
    im.putpalette(p); im.save(path)

def front(H=74):
    crop, al = cutout((1387, 79, 1715, 665))
    W = round(crop.shape[1] * H / crop.shape[0])
    rgb, a = shrink(crop, al, W, H)
    idx = to_pal(rgb, a > 200)
    canvas = np.zeros((80, 80), np.uint8); ox = (80 - W) // 2; oy = 80 - H - 2
    canvas[oy:oy + H, ox:ox + W] = idx
    canvas = despeckle(canvas, 2, protect=(1, 14, 15, 10))
    canvas = outline(canvas)
    save(canvas, '/home/claude/jclean/front_new.png')

def mug():
    cx, top, cw = 1575, 75, 420; ch = cw * 64 // 96
    crop, al = cutout((cx - cw // 2, top, cx - cw // 2 + cw, top + ch))
    rgb, a = shrink(crop, al, 96, 64)
    idx = to_pal(rgb, a > 200)
    idx = despeckle(idx, 2, protect=(1, 14, 15, 10))
    idx = outline(idx); idx[-1, :] = np.where(idx[-2, :] > 0, idx[-1, :], idx[-1, :])
    save(idx, '/home/claude/jclean/mug_new.png')
front(); mug()
