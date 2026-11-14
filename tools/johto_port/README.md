# Johto port tools

`import_hg_maps.py` copies HeartGold overworld maps into the Platinum build.
It reads the prebuilt archives from a `pret/pokeheartgold` checkout (no ROM needed).

```
python3 tools/johto_port/import_hg_maps.py /path/to/pokeheartgold --register
```

`--register` also appends the new files to the `meson.build` lists and `.order`
files. Run it with `--register` only once per batch, otherwise the lists get
duplicate entries. `maps.json` says which HeartGold maps to import and which
Platinum slot numbers they take.

## What it converts

| HeartGold | Platinum | Notes |
| --- | --- | --- |
| `a/0/6/5` map files | `res/field/mapmodels/data/map_data_NNN.bin` | 0x14-byte header + BG-sound section dropped; Platinum uses a 0x10-byte header. Terrain, props, model and BDHC sections are the same format. Prop model IDs are renumbered. |
| `a/0/4/4` map textures | `res/field/mapmodels/texture_sets/` | |
| `a/0/4/0` building models | `res/field/props/models/johto_build_NNN.nsbmd` | Appended after Platinum's 590 prop models. |
| `a/0/7/0` building textures | `res/field/props/texture_sets/` | |
| `a/0/4/3` building lists | `res/field/props/model_sets/*.json` | |
| `a/0/4/2` area data | `res/field/area_data/*.json` | Lighting uses Platinum's outdoor set. |

It also extends `res/prebuilt/fielddata/build_model/build_model_matshp.dat`,
which has one entry per prop model ID; new IDs get "draw whole model" entries.

## First batch (test area)

| Matrix `Johto` (6x1) | Map data | Header |
| --- | --- | --- |
| x 0-1 | 670, 671 | `MAP_HEADER_CHERRYGROVE_CITY` |
| x 2-4 | 672, 673, 674 | `MAP_HEADER_ROUTE_29` |
| x 5 | 675 | `MAP_HEADER_NEW_BARK_TOWN` |

Temporary test warp: `JOHTO_TEMP_TEST` in `include/constants/johto.h` makes
Mom in Twinleaf Town offer a warp to New Bark Town (183, 13).

## Not ported yet

- NPCs, signs, warps and scripts (the maps have empty events)
- Johto music (placeholder Sinnoh tracks are used)
- Wild encounters, trainers
- Door animations for HeartGold building models
- HeartGold-only tile behaviors (headbutt trees are plain solid tiles for now)
- Town Map / Pokétch map position while in Johto
