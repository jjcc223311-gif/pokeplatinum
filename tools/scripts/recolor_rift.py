#!/usr/bin/env python3
"""Distorted Rift: build the purple copies of the Distortion World room's colours.

usage: recolor_rift.py
  - res/field/mapmodels/texture_sets/map_texture_set_073.nsbtx -> map_texture_set_074.nsbtx
  - res/field/lighting/lighting_set_001.json                   -> lighting_set_004.json

Blue / cyan colours (hue 150-265 degrees) are moved into the purple band (265-285 degrees);
greys, the magenta transparency key and the rose / mauve tones are left alone. The same
mapping is applied at runtime to the sky background and cloud palettes (RiftShiftColor in
src/overlay009/ov9_02249960.c).
"""
import colorsys
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUE_FROM = (150 / 360, 265 / 360)
HUE_TO = (265 / 360, 285 / 360)


def shift_rgb(r, g, b):
    """r, g, b in 0..31; returns the purple-shifted colour (0..31)."""
    h, s, v = colorsys.rgb_to_hsv(r / 31, g / 31, b / 31)

    if s < 0.15 or not (HUE_FROM[0] <= h <= HUE_FROM[1]):
        return r, g, b

    t = (h - HUE_FROM[0]) / (HUE_FROM[1] - HUE_FROM[0])
    h = HUE_TO[0] + t * (HUE_TO[1] - HUE_TO[0])
    nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
    return round(nr * 31), round(ng * 31), round(nb * 31)


def shift_bgr555(c):
    r, g, b = c & 31, (c >> 5) & 31, (c >> 10) & 31
    r, g, b = shift_rgb(r, g, b)
    return (c & 0x8000) | r | (g << 5) | (b << 10)


def recolor_nsbtx(src, dst):
    data = bytearray(src.read_bytes())
    base = data.find(b'TEX0')
    assert base >= 0, src

    size = struct.unpack_from('<H', data, base + 0x30)[0] << 3
    start = base + struct.unpack_from('<I', data, base + 0x38)[0]

    for off in range(start, start + size, 2):
        struct.pack_into('<H', data, off, shift_bgr555(struct.unpack_from('<H', data, off)[0]))

    dst.write_bytes(bytes(data))


def recolor_lighting(src, dst):
    sets = json.loads(src.read_text())

    for entry in sets:
        for light in entry['lights']:
            col = light['color']
            col['red'], col['green'], col['blue'] = shift_rgb(col['red'], col['green'], col['blue'])

    dst.write_text(json.dumps(sets, indent=4) + '\n')


def main():
    tex = ROOT / 'res/field/mapmodels/texture_sets'
    recolor_nsbtx(tex / 'map_texture_set_073.nsbtx', tex / 'map_texture_set_074.nsbtx')
    light = ROOT / 'res/field/lighting'
    recolor_lighting(light / 'lighting_set_001.json', light / 'lighting_set_004.json')


if __name__ == '__main__':
    main()
