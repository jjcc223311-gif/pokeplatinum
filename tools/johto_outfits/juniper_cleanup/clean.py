import numpy as np
from PIL import Image
from collections import Counter
def despeckle(idx, passes=2, protect=()):
    """Replace pixels whose colour has <=1 matching 8-neighbours with the neighbourhood majority
    (only when that majority is strong), leaving transparent edges and protected colours alone."""
    a = idx.copy(); H, W = a.shape
    for _ in range(passes):
        b = a.copy()
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                v = a[y, x]
                if v == 0 or v in protect: continue
                nb = [a[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]
                if 0 in nb: continue
                same = sum(1 for n in nb if n == v)
                if same <= 1:
                    c, n = Counter(nb).most_common(1)[0]
                    if n >= 5: b[y, x] = c
        a = b
    return a
