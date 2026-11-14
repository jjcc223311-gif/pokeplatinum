#!/usr/bin/env python3
"""Rebuild a form's 80x80 battle sprites from a pack's high-resolution source render.

The sprite packs shipped 80x80 sprites made by nearest-neighbour sampling of large renders
(~1250 px), which keeps random single pixels and loses the outlines: the result reads as a
blurry mesh of colours. This rebuilds them properly:

  1. crop the render to the Pokemon and scale it to fill the 80x80 frame like a vanilla
     sprite (feet on the base species' baseline; backs bottom-aligned like vanilla backs),
  2. downscale with area averaging (every output pixel is the average of its source area),
  3. reduce front + back together to one shared 15-colour palette (+ transparency),
  4. remove stray single pixels, then draw a 1-pixel outline in the darkest colour.

usage: rebuild_sprite_from_source.py <front.png> <back.png | -> <base species dir> <out dir> [--preview out.png]
  A source sheet with front and back side by side (e.g. front_back.png) is passed as <front.png>
  with <back.png> = '-'. Writes <out dir>/front.png, back.png (160x80, two identical frames,
  4-bit indexed) and normal.pal. shiny.pal / .key / data.json are left to the caller.
"""
import argparse
from collections import Counter
from pathlib import Path

from PIL import Image

FRAME = 80
ALPHA_CUT = 128
FRONT_MAX = 80
BACK_MAX = 80


def split_sheet(sheet):
    w, h = sheet.size
    return sheet.crop((0, 0, w // 2, h)), sheet.crop((w // 2, 0, w, h))


def opaque_bbox(img):
    return img.getchannel('A').point(lambda a: 255 if a >= ALPHA_CUT else 0).getbbox()


def base_bottom(base_dir, face):
    """Lowest opaque row (exclusive) of the base species' vanilla sprite, so the form stands where
    the normal Pokemon stands."""
    for gender in ('male', 'female'):
        path = Path(base_dir) / f'{gender}_{face}.png'
        if path.exists():
            box = Image.open(path).crop((0, 0, FRAME, FRAME)).getbbox()
            if box:
                return box[3]
    return FRAME


def fit(img, face, bottom):
    """Crop to the Pokemon and area-downscale it into the 80x80 frame."""
    img = img.convert('RGBA')
    img = img.crop(opaque_bbox(img))
    w, h = img.size
    limit = FRONT_MAX if face == 'front' else BACK_MAX
    s = min(limit / w, bottom / h)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))

    # Two steps: a box filter to ~2x the target keeps every source pixel's weight, then LANCZOS
    # (on a picture that is already almost the right size) keeps the edges sharp.
    mid = img.resize((nw * 2, nh * 2), Image.BOX)
    small = mid.resize((nw, nh), Image.LANCZOS)

    frame = Image.new('RGBA', (FRAME, FRAME), (0, 0, 0, 0))
    frame.paste(small, ((FRAME - nw) // 2, bottom - nh))
    return frame


def to_ds(c):
    return tuple((v >> 3) << 3 | (v >> 5) for v in c)


def build_palette(frames):
    """One 15-colour palette for all opaque pixels of every frame."""
    pixels = []
    for f in frames:
        pixels += [p[:3] for p in f.get_flattened_data() if p[3] >= ALPHA_CUT]

    strip = Image.new('RGB', (len(pixels), 1))
    strip.putdata(pixels)
    q = strip.quantize(colors=15, method=Image.Quantize.MEDIANCUT, kmeans=4)
    pal = q.getpalette()
    used = sorted(set(q.get_flattened_data()))
    colours = sorted({to_ds(tuple(pal[i * 3:i * 3 + 3])) for i in used}, key=lambda c: sum(c))
    return colours


def nearest(colours, c):
    return min(range(len(colours)), key=lambda i: sum((a - b) ** 2 for a, b in zip(colours[i], c)))


def index_frame(frame, colours):
    """Returns a grid of indexes (0 = transparent, 1.. = colours[i - 1]) the size of the frame."""
    px = frame.load()
    cache = {}
    w, h = frame.size
    grid = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < ALPHA_CUT:
                continue
            key = (r, g, b)
            if key not in cache:
                cache[key] = nearest(colours, key) + 1
            grid[y][x] = cache[key]
    return grid


def neighbours(grid, x, y, diag=True):
    h, w = len(grid), len(grid[0])
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (dx or dy) and (diag or not (dx and dy)):
                nx, ny = x + dx, y + dy
                yield grid[ny][nx] if 0 <= nx < w and 0 <= ny < h else 0


def clean(grid):
    """Removes speckle: an opaque pixel whose colour none of its 8 neighbours share takes the most
    common neighbouring colour (ignoring transparency)."""
    out = [row[:] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = grid[y][x]
            if c == 0:
                continue
            ns = list(neighbours(grid, x, y))
            if c in ns:
                continue
            opaque = [n for n in ns if n]
            if len(opaque) >= 5:
                out[y][x] = Counter(opaque).most_common(1)[0][0]
    return out


def outline(grid, outline_index):
    """Every opaque pixel touching transparency (4-neighbours) becomes the outline colour; lone
    opaque pixels with fewer than 2 opaque neighbours are dropped first."""
    g = [row[:] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if g[y][x] and sum(1 for n in neighbours(grid, x, y) if n) < 2:
                g[y][x] = 0
    out = [row[:] for row in g]
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] and 0 in neighbours(g, x, y, diag=False):
                out[y][x] = outline_index
    return out


def to_image(grid, colours):
    img = Image.new('P', (FRAME * 2, FRAME), 0)
    pal = [(0, 0, 0)] + colours + [(0, 0, 0)] * (15 - len(colours))
    # the transparent colour: an unused bright green, like the vanilla sprites' index 0
    pal[0] = (144, 200, 152) if (144, 200, 152) not in colours else (255, 0, 255)
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    data = [grid[y][x] for y in range(FRAME) for x in range(FRAME)]
    frame = Image.new('P', (FRAME, FRAME), 0)
    frame.putdata(data)
    img.paste(frame, (0, 0))
    img.paste(frame, (FRAME, 0))
    return img, pal


def rebuild(front_src, back_src, base_dir):
    if back_src is None:
        front_src, back_src = split_sheet(front_src)

    frames = {
        'front': fit(front_src, 'front', base_bottom(base_dir, 'front')),
        'back': fit(back_src, 'back', FRAME),
    }
    colours = build_palette(frames.values())
    outline_index = 1  # colours are sorted darkest first

    out = {}
    pal = None
    for face, frame in frames.items():
        grid = outline(clean(index_frame(frame, colours)), outline_index)
        out[face], pal = to_image(grid, colours)
    return out, pal


def write_jasc(path, colours):
    with open(path, 'w', newline='\r\n') as f:
        f.write(f'JASC-PAL\n0100\n{len(colours)}\n')
        for c in colours:
            f.write(f'{c[0]} {c[1]} {c[2]}\n')


def main():
    argp = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argp.add_argument('front')
    argp.add_argument('back')
    argp.add_argument('base_dir')
    argp.add_argument('out_dir')
    args = argp.parse_args()

    front = Image.open(args.front)
    back = None if args.back == '-' else Image.open(args.back)
    images, pal = rebuild(front, back, args.base_dir)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for face, img in images.items():
        img.save(out / f'{face}.png', bits=4, transparency=0)
    write_jasc(out / 'normal.pal', pal)


if __name__ == '__main__':
    main()


# ----- Mode-based reduction (default): keeps flat colour regions and line art -----

LINE_SHARE = 0.28  # a dark line colour wins an output pixel when it covers this much of its area


def fit_box(img, face, bottom):
    """Crop to the Pokemon; returns (cropped RGBA, output size, paste position)."""
    img = img.convert('RGBA')
    img = img.crop(opaque_bbox(img))
    w, h = img.size
    limit = FRONT_MAX if face == 'front' else BACK_MAX
    s = min(limit / w, bottom / h)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    return img, (nw, nh), ((FRAME - nw) // 2, bottom - nh)


def mode_reduce(src_rgba, colours, size):
    """Each output pixel takes the most common palette colour of its source area (transparent when
    most of the area is); a dark colour covering LINE_SHARE of the area wins, so outlines and
    interior line art survive the reduction."""
    nw, nh = size
    # Work on a ~4x intermediate so the per-cell histograms are cheap
    work = src_rgba.resize((nw * 4, nh * 4), Image.BOX)
    px = work.load()
    lum = [sum(c) for c in colours]
    dark_cut = sorted(lum)[max(0, len(lum) // 5)]  # darkest fifth of the palette = line colours
    cache = {}

    def idx(c):
        if c not in cache:
            cache[c] = nearest(colours, c) + 1
        return cache[c]

    grid = [[0] * nw for _ in range(nh)]
    for oy in range(nh):
        for ox in range(nw):
            counts = Counter()
            alpha = 0
            for y in range(oy * 4, oy * 4 + 4):
                for x in range(ox * 4, ox * 4 + 4):
                    r, g, b, a = px[x, y]
                    if a >= ALPHA_CUT:
                        counts[idx((r, g, b))] += 1
                    else:
                        alpha += 1
            if alpha > 8 or not counts:
                continue
            total = sum(counts.values())
            dark = [(n, i) for i, n in counts.items() if lum[i - 1] <= dark_cut]
            if dark and max(dark)[0] >= total * LINE_SHARE:
                grid[oy][ox] = max(dark)[1]
            else:
                grid[oy][ox] = counts.most_common(1)[0][0]
    return grid


def rebuild_mode(front_src, back_src, base_dir):
    if back_src is None:
        front_src, back_src = split_sheet(front_src)

    boxes = {
        'front': fit_box(front_src, 'front', base_bottom(base_dir, 'front')),
        'back': fit_box(back_src, 'back', FRAME),
    }
    # Palette from the sources at a moderate size (keeps the artist's colours, not blends)
    samples = []
    for img, size, _ in boxes.values():
        samples.append(img.resize((size[0] * 2, size[1] * 2), Image.NEAREST))
    colours = build_palette(samples)

    out = {}
    pal = None
    for face, (img, size, pos) in boxes.items():
        small = mode_reduce(img, colours, size)
        grid = [[0] * FRAME for _ in range(FRAME)]
        for y in range(size[1]):
            for x in range(size[0]):
                grid[pos[1] + y][pos[0] + x] = small[y][x]
        grid = outline(clean(grid), 1)
        out[face], pal = to_image(grid, colours)
    return out, pal


def scale2x(img):
    """EPX / Scale2x on an RGBA image: doubles the size and keeps edges and diagonals sharp."""
    w, h = img.size
    src = img.load()
    out = Image.new('RGBA', (w * 2, h * 2))
    dst = out.load()
    get = lambda x, y: src[min(max(x, 0), w - 1), min(max(y, 0), h - 1)]
    for y in range(h):
        for x in range(w):
            p = get(x, y)
            a, b, c, d = get(x, y - 1), get(x + 1, y), get(x - 1, y), get(x, y + 1)
            e0 = a if (c == a and c != d and a != b) else p
            e1 = b if (a == b and a != c and b != d) else p
            e2 = c if (d == c and d != b and c != a) else p
            e3 = d if (b == d and b != a and d != c) else p
            dst[x * 2, y * 2] = e0
            dst[x * 2 + 1, y * 2] = e1
            dst[x * 2, y * 2 + 1] = e2
            dst[x * 2 + 1, y * 2 + 1] = e3
    return out


def indexed_frame_rgba(path):
    """First 80x80 frame of a 4-bit sprite PNG as RGBA (index 0 transparent)."""
    im = Image.open(path)
    idx = im.crop((0, 0, FRAME, FRAME))
    rgba = idx.convert('RGBA')
    rgba.putdata([(0, 0, 0, 0) if i == 0 else c for i, c in zip(idx.get_flattened_data(), rgba.get_flattened_data())])
    return rgba


def enlarge_pixel_art(front_rgba, back_rgba, base_dir):
    """Native small pixel art (the 64 px packs): Scale2x twice, then the mode reduction to fill the
    frame. Keeps the original palette colours and line art."""
    big = lambda im: scale2x(scale2x(im.crop(opaque_bbox(im))))
    return rebuild_mode(big(front_rgba), big(back_rgba), base_dir)
