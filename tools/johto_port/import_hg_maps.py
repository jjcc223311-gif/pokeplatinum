#!/usr/bin/env python3
"""Import HeartGold overworld maps into the Platinum build.

Reads a pret/pokeheartgold checkout (prebuilt NARCs under files/a/) and writes
Platinum-format resources into res/field/:

  * map data   (a/0/6/5)  -> res/field/mapmodels/data/map_data_NNN.bin
      HG header is 0x14 bytes (4 section sizes + magic 0x1234 + BG-sound size)
      followed by a BG-sound section. Platinum's header is 0x10 bytes and has
      no BG-sound section; the remaining sections (terrain attributes, props,
      model, BDHC) are identical in layout. Prop model IDs are remapped to the
      indices the HG building models get in Platinum's prop_models.narc.
  * map textures (a/0/4/4) -> res/field/mapmodels/texture_sets/
  * building models (a/0/4/0) -> res/field/props/models/johto_build_NNN.nsbmd
  * building texture pack (a/0/7/0) -> res/field/props/texture_sets/
  * building model list (a/0/4/3) -> res/field/props/model_sets/*.json

It only writes the binary/JSON resources; build lists (meson.build / .order)
are updated by register_lists() so every list stays in step.

Usage: import_hg_maps.py <pokeheartgold dir>
"""
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIELD = ROOT / 'res' / 'field'


def read_narc(path):
    d = path.read_bytes()
    assert d[:4] == b'NARC', path
    off = struct.unpack_from('<H', d, 12)[0]
    assert d[off:off + 4] == b'BTAF'
    size, count = struct.unpack_from('<IH', d, off + 4)
    entries = [struct.unpack_from('<II', d, off + 12 + 8 * i) for i in range(count)]
    off += size
    assert d[off:off + 4] == b'BTNF'
    off += struct.unpack_from('<I', d, off + 4)[0]
    assert d[off:off + 4] == b'GMIF'
    base = off + 8
    return [d[base + s:base + e] for s, e in entries]


PROP_SIZE = 0x30


def convert_map(hg, prop_remap):
    attr, props, model, bdhc, magic, bgs = struct.unpack_from('<4I2H', hg, 0)
    assert magic == 0x1234, 'not a HeartGold map file'
    body = bytearray(hg[0x14 + bgs:])
    assert len(body) == attr + props + model + bdhc
    assert props % PROP_SIZE == 0
    for k in range(props // PROP_SIZE):
        o = attr + k * PROP_SIZE
        hg_id = struct.unpack_from('<I', body, o)[0]
        struct.pack_into('<I', body, o, prop_remap[hg_id])
    assert body[attr + props:attr + props + 4] == b'BMD0'
    assert body[attr + props + model:attr + props + model + 4] == b'BDHC'
    return struct.pack('<4I', attr, props, model, bdhc) + bytes(body)


def append_list(meson, order, names, keep_ext=False):
    """Append file names after the last quoted entry of the meson files() list
    that lists the same kind of file, and to the matching .order file."""
    text = meson.read_text()
    ext = names[0].rsplit('.', 1)[1]
    last = None
    for m in re.finditer(r"'[^']+\." + ext + "'(,?)", text):
        last = m
    insert_at = last.end()
    if last.group(1):  # entries end with commas
        add = ''.join(f"\n    '{n}'," for n in names)
    else:
        add = ''.join(f",\n    '{n}'" for n in names)
    meson.write_text(text[:insert_at] + add + text[insert_at:])
    with order.open('a') as f:
        for n in names:
            f.write((n if keep_ext else n.rsplit('.', 1)[0]) + '\n')


def extend_matshp(total_models):
    """build_model_matshp.dat holds one (idsCount, idsIndex) locator per prop
    model ID and is indexed by model ID when props are drawn. Add locators with
    idsCount 0 (= draw the whole model normally) for the new model IDs."""
    path = ROOT / 'res' / 'prebuilt' / 'fielddata' / 'build_model' / 'build_model_matshp.dat'
    d = path.read_bytes()
    n_loc, n_ids = struct.unpack_from('<HH', d, 0)
    if n_loc >= total_models:
        return
    locs = d[4:4 + 4 * n_loc]
    ids = d[4 + 4 * n_loc:]
    assert len(ids) == 4 * n_ids
    extra = struct.pack('<HH', 0, 0xFFFF) * (total_models - n_loc)
    path.write_bytes(struct.pack('<HH', total_models, n_ids) + locs + extra + ids)


def main():
    hg = pathlib.Path(sys.argv[1]) / 'files' / 'a'
    cfg = json.loads((pathlib.Path(__file__).parent / 'maps.json').read_text())

    land = read_narc(hg / '0' / '6' / '5')
    map_tex = read_narc(hg / '0' / '4' / '4')
    build_models = read_narc(hg / '0' / '4' / '0')
    build_packs = read_narc(hg / '0' / '4' / '3')
    build_tex = read_narc(hg / '0' / '7' / '0')
    area = read_narc(hg / '0' / '4' / '2')

    # --- area data: building pack + map texture
    pack_id, tex_id = struct.unpack_from('<HH', area[cfg['hg_area_data']], 0)
    n = struct.unpack_from('<H', build_packs[pack_id], 0)[0]
    pack = list(struct.unpack_from(f'<{n}H', build_packs[pack_id], 2))

    # --- building models -> prop models appended after the existing ones
    prop_order = FIELD / 'props' / 'models' / 'map_prop_models.order'
    order = prop_order.read_text().split()
    remap, new_models = {}, []
    for hg_id in pack:
        name = f'johto_build_{hg_id:03d}.nsbmd'
        (FIELD / 'props' / 'models' / name).write_bytes(build_models[hg_id])
        if name not in order:
            new_models.append(name)
        # narc index = line number in the order file (existing + newly appended)
        remap[hg_id] = (order + new_models).index(name)

    # --- map data
    first = cfg['first_map_data']
    for i, hg_land in enumerate(cfg['hg_land_ids']):
        out = FIELD / 'mapmodels' / 'data' / f'map_data_{first + i:03d}.bin'
        out.write_bytes(convert_map(land[hg_land], remap))

    # --- textures
    mts = cfg['map_texture_set']
    pts = cfg['prop_texture_set']
    pms = cfg['prop_model_set']
    (FIELD / 'mapmodels' / 'texture_sets' / f'map_texture_set_{mts:03d}.nsbtx').write_bytes(map_tex[tex_id])
    (FIELD / 'props' / 'texture_sets' / f'prop_texture_set_{pts:03d}.nsbtx').write_bytes(build_tex[pack_id])

    # --- prop model set (same list as HG's building pack)
    (FIELD / 'props' / 'model_sets' / f'prop_model_set_{pms:03d}.json').write_text(json.dumps(
        {'mapPropModels': [f'johto_build_{h:03d}_nsbmd' for h in pack]}, indent=4) + '\n')

    # --- area data
    ad = cfg['area_data']
    (FIELD / 'area_data' / f'area_data_{ad:03d}.json').write_text(json.dumps({
        'mapPropSet': f'prop_model_set_{pms:03d}',
        'mapTextureSet': f'map_texture_set_{mts:03d}',
        'lightingSet': cfg['lighting_set'],
        'dummy': 0,
    }, indent=4) + '\n')

    if '--register' in sys.argv:
        append_list(FIELD / 'props' / 'models' / 'meson.build', prop_order, new_models, True)
        append_list(FIELD / 'mapmodels' / 'data' / 'meson.build',
                    FIELD / 'mapmodels' / 'data' / 'map_data.order',
                    [f'map_data_{first + i:03d}.bin' for i in range(len(cfg['hg_land_ids']))], True)
        append_list(FIELD / 'mapmodels' / 'texture_sets' / 'meson.build',
                    FIELD / 'mapmodels' / 'texture_sets' / 'map_texture_sets.order',
                    [f'map_texture_set_{mts:03d}.nsbtx'])
        append_list(FIELD / 'props' / 'texture_sets' / 'meson.build',
                    FIELD / 'props' / 'texture_sets' / 'prop_texture_sets.order',
                    [f'prop_texture_set_{pts:03d}.nsbtx'], True)
        append_list(FIELD / 'props' / 'model_sets' / 'meson.build',
                    FIELD / 'props' / 'model_sets' / 'prop_model_sets.order',
                    [f'prop_model_set_{pms:03d}.json'])
        append_list(FIELD / 'area_data' / 'meson.build',
                    FIELD / 'area_data' / 'area_data.order',
                    [f'area_data_{ad:03d}.json'])

    extend_matshp(len(order) + len(new_models))

    print('building pack', pack_id, '-> prop ids', remap)
    print('map texture', tex_id)


if __name__ == '__main__':
    main()
