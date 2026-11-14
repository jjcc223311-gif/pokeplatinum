#!/usr/bin/env python3
"""Give every species after Arceus (#494 up to SPECIES_EGG - 1) a cry bank + wave archive in
res/sound/pl_sound_data.json.

Cries are played with bank = wave archive = species number, so species N must sit at index N of
both lists. Shaymin-Sky's cry used index 494 (Victini's number); it is moved to the free index 699
(its code references it by name, shaymin_forms_sky_cry_swar). Names use WAVE_ARC_PV_GEN5_<dex>
because the vanilla names (WAVE_ARC_PV494...) follow the DP internal numbering.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cjson_format  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SOUND = ROOT / 'res' / 'sound' / 'pl_sound_data.json'
SKY_SLOT = 699

species = (ROOT / 'generated' / 'species.txt').read_text().split()
d = json.loads(SOUND.read_text())
w, b = d['wavarcInfo'], d['bankInfo']

if w[494].get('name') == 'WAVE_ARC_PV516_SKY':
    assert not w[SKY_SLOT].get('name') and not b[SKY_SLOT].get('name')
    w[SKY_SLOT], w[494] = w[494], {'name': ''}
    b[SKY_SLOT], b[494] = b[494], {'name': ''}

end = species.index('SPECIES_EGG')
assert end <= SKY_SLOT
for i in range(494, end):
    stem = species[i][len('SPECIES_'):].lower()
    wname = f'WAVE_ARC_PV_GEN5_{i:03}'
    assert w[i].get('name') in ('', wname), (i, w[i])
    w[i] = {'name': wname, 'fileName': f'{stem}/cry.swar'}
    b[i] = {'name': f'BANK_PV_GEN5_{i:03}', 'fileName': f'{stem}/cry.sbnk', 'waves': [wname, '', '', '']}

SOUND.write_text(cjson_format.dumps(d))
print(f'cries registered for #494-{end - 1}')
