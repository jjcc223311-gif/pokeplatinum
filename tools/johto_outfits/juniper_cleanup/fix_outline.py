import numpy as np
from PIL import Image
def fix(path, out=None, sep=255, OUT=None):
    im = Image.open(path); a = np.array(im).astype(int); p = im.getpalette()
    col = lambda i: tuple(p[3*i:3*i+3])
    H, W = a.shape
    if OUT is None:
        OUT = min(range(1, 16), key=lambda i: sum(col(i)))
    gray = [i for i in range(2, 16) if (lambda c: max(c) - min(c) < 40 and 80 < sum(c) < 600)(col(i))]
    light = [i for i in range(2, 16) if sum(col(i)) >= 600]
    hair = [i for i in range(2, 16) if (lambda c: c[0] > c[2] + 40 and c[0] < 200)(col(i))]
    def nb(y, x, d8=True):
        r = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if (dy or dx) and (d8 or not (dy and dx)):
                    yy, xx = y + dy, x + dx
                    r.append(a[yy, xx] if 0 <= yy < H and 0 <= xx < W else 0)
        return r
    b = a.copy(); n = 0
    for y in range(H):
        for x in range(W):
            v = a[y, x]
            if v in (0, sep): continue
            n8 = nb(y, x)
            edge = 0 in n8 or sep in n8
            # antialiased greys/whites sitting on the silhouette edge belong to the outline
            if edge and (v in gray or v in light):
                b[y, x] = OUT; n += 1
            # greys wedged between the outline and hair are outline too
            elif v in gray and OUT in nb(y, x, False) and any(c in hair for c in n8) and not any(c in light for c in n8):
                b[y, x] = OUT; n += 1
    o = Image.fromarray(b.astype(np.uint8), 'P'); o.putpalette(p); o.save(out or path)
    return n
