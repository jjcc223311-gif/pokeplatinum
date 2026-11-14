from PIL import Image, ImageDraw
CH = '.123456789ABCDEF'
def load(path):
    im = Image.open(path); return im, [tuple(im.getpalette()[3*i:3*i+3]) for i in range(16)]
def frame(im, k): return [[im.getpixel((x, k*32+y)) for x in range(32)] for y in range(32)]
def apply(fr, tmpl, x0, y0, clear_rows=None):
    """tmpl: list of strings; '.' = transparent (clears), ' ' = keep original."""
    out = [r[:] for r in fr]
    if clear_rows:
        for y in range(*clear_rows):
            out[y] = [0]*32
    for dy, row in enumerate(tmpl):
        for dx, c in enumerate(row):
            if c == ' ': continue
            x, y = x0+dx, y0+dy
            if 0 <= x < 32 and 0 <= y < 32:
                out[y][x] = CH.index(c)
    return out
def render(frames, pal, path, S=10, grid=True):
    W = len(frames)*(32*S+8)
    img = Image.new('RGB', (W, 32*S), (120, 160, 120)); d = ImageDraw.Draw(img)
    for i, fr in enumerate(frames):
        ox = i*(32*S+8)
        for y in range(32):
            for x in range(32):
                v = fr[y][x]
                if v: d.rectangle((ox+x*S, y*S, ox+x*S+S-1, y*S+S-1), fill=pal[v])
        if grid:
            for g in range(0, 33, 4):
                d.line((ox+g*S, 0, ox+g*S, 32*S), fill=(100, 140, 100)); d.line((ox, g*S, ox+32*S, g*S), fill=(100, 140, 100))
    img.save(path)
