#!/usr/bin/env python3
"""Phase 7 character sprites.

  Flint   -> Nate     (elite_four_flint, npc/flint.png)
  Volkner -> Hugh     (leader_volkner,   npc/volkner.png)
  Aaron   -> Beatrice (elite_four_aaron, npc/aaron.png)
  Candice -> Dawn     (leader_candice,   npc/candice.png) using Dawn's ORIGINAL sprites (read from git HEAD)
  Dawn    -> Juniper  (player_female / dp_player_female fronts, player/player_f.png + dp_player_f.png walk/run)

Battle fronts: front.png (every animation frame = the standing pose), front_scan.png (both halves),
mugshot.png (VS screen) = a 2x close-up of the head, cut from the front sprite (placeholder art).
Kept as before (no art in the packs, listed in the report): Juniper's battle back sprite and her
bike / surf / fishing / other field poses; Juniper's running frames reuse her walking frames.
usage: phase7_sprites.py   (run with a Python that has Pillow)
"""
import io
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'tools' / 'gen5_pack'
CLASSES = ROOT / 'res' / 'trainers' / 'classes'
FIELD = ROOT / 'res' / 'graphics' / 'field_sprites'


def git_image(path):
    data = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT, capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data))


def as16(im):
    """An indexed image limited to 16 colours (index 0 = transparent) and its 16-colour palette."""
    assert im.mode == 'P', im.mode
    pal = (im.getpalette() + [0] * 48)[:48]
    px = list(im.get_flattened_data())
    assert max(px) < 16, 'more than 16 colours'
    return px, pal


def make(size, px_rows, pal, palette_len):
    out = Image.new('P', size, 0)
    out.putpalette(pal + [0] * (3 * palette_len - len(pal)))
    for (x, y), img in px_rows:
        out.paste(img, (x, y))
    return out


def front_set(cls, sprite):
    """Write front.png / front_scan.png / mugshot.png for a trainer class from an 80x80 sprite."""
    px, pal = as16(sprite)
    frame = Image.new('P', (80, 80))
    frame.putdata(px)
    old = Image.open(CLASSES / cls / 'front.png')
    n = (old.height + 1) // 81
    front = Image.new('P', (80, old.height), 0)
    front.putpalette(pal + [0] * (768 - len(pal)))
    for i in range(n):
        front.paste(frame, (0, 81 * i))
    front.save(CLASSES / cls / 'front.png')
    scan = Image.new('P', (160, 80), 0)
    scan.putpalette(pal)
    scan.paste(frame, (0, 0))
    scan.paste(frame, (80, 0))
    scan.save(CLASSES / cls / 'front_scan.png')
    if (CLASSES / cls / 'mugshot.png').exists():
        box = frame.getbbox() if hasattr(frame, 'getbbox') else (0, 0, 80, 80)
        mask = Image.new('L', (80, 80))
        mask.putdata([255 if p else 0 for p in px])
        x0, y0, x1, y1 = mask.getbbox()
        cx = (x0 + x1) // 2
        crop = frame.crop((max(0, cx - 24), y0, max(0, cx - 24) + 48, y0 + 32))
        mug = Image.new('P', (96, 64), 0)
        mug.putpalette(pal + [0] * (768 - len(pal)))
        mug.paste(crop.resize((96, 64), Image.NEAREST), (0, 0))
        mug.save(CLASSES / cls / 'mugshot.png')


def column(frames, pal, total):
    """Stack 32x32 frames into the 32 x (32*total) overworld texture."""
    out = Image.new('P', (32, 32 * total), 0)
    out.putpalette(pal)
    for i, f in enumerate(frames):
        out.paste(f, (0, 32 * i))
    return out


def cells(sheet, cols):
    return [sheet.crop((32 * (i % cols), 32 * (i // cols), 32 * (i % cols) + 32, 32 * (i // cols) + 32))
            for i in range((sheet.width // 32) * (sheet.height // 32))]


def walk16(frames12):
    """Pack frames (per direction: idle, step A, step B; up, down, left, right) -> Platinum 16-frame order."""
    out = []
    for d in range(4):
        idle, a, b = frames12[3 * d:3 * d + 3]
        out += [idle, a, idle, b]
    return out


def main():
    report = []
    # --- Candice -> Dawn (Dawn's original art, from git HEAD) ---
    dawn_front = git_image('res/trainers/classes/dp_player_female/front.png').crop((0, 0, 80, 80))
    front_set('leader_candice', dawn_front)
    dawn_ow = git_image('res/graphics/field_sprites/player/dp_player_f.png')
    pal = (dawn_ow.getpalette() + [0] * 48)[:48]
    column([dawn_ow.crop((0, 32 * i, 32, 32 * i + 32)) for i in range(16)], pal, 16).save(FIELD / 'npc' / 'candice.png')
    report.append('Candice -> Dawn: battle front + overworld = Dawn\'s original sprites; VS mugshot cut from her front')

    # --- Flint -> Nate, Volkner -> Hugh, Aaron -> Beatrice ---
    nate = PACK / 'nate' / 'Nate_Platinum_Sprites'
    for cls, npc, front, ow in [
        ('elite_four_flint', 'flint', nate / 'battle' / 'opponent-front' / 'standing.png', ('nate', nate / 'sprite-sheets' / '209-on-foot.png')),
        ('leader_volkner', 'volkner', PACK / 'hugh_bianca' / 'hugh' / 'battle' / 'opponent-front' / 'standing.png',
         ('native', PACK / 'hugh_bianca' / 'platinum-native' / 'hugh' / 'overworld' / 'texture-order.png')),
        ('elite_four_aaron', 'aaron', PACK / 'hugh_bianca' / 'bianca' / 'battle' / 'opponent-front' / 'standing.png',
         ('native', PACK / 'hugh_bianca' / 'platinum-native' / 'bianca' / 'overworld' / 'texture-order.png')),
    ]:
        img = Image.open(front)
        img.seek(0)
        front_set(cls, img.convert('P') if img.mode != 'P' else img)
        kind, sheet_path = ow
        sheet = Image.open(sheet_path)
        pal = (sheet.getpalette() + [0] * 48)[:48]
        if kind == 'native':
            frames = cells(sheet, 4)[:16]
        else:
            frames = walk16(cells(sheet, sheet.width // 32)[:12])
        column(frames, pal, 16).save(FIELD / 'npc' / f'{npc}.png')
        report.append(f'{cls}: battle front + overworld replaced; VS mugshot cut from the front sprite')

    # --- Dawn -> Juniper ---
    jfront = Image.open(PACK / 'juniper' / 'custom-battle' / 'trainer-front-80x80.png')
    for cls in ('player_female', 'dp_player_female', 'dp_player_female_2'):
        if (CLASSES / cls / 'front.png').exists():
            front_set(cls, jfront)
    jsheet = Image.open(PACK / 'juniper' / 'overworld' / 'sprite-sheet.png')
    jpal = (jsheet.getpalette() + [0] * 48)[:48]
    walk = walk16(cells(jsheet, 4)[:12])
    for f in ('player_f.png', 'dp_player_f.png'):
        column(walk + walk, jpal, 32).save(FIELD / 'player' / f)
    report.append('Dawn -> Juniper: player / companion battle fronts and walking overworld (running reuses walking)')
    report.append('KEPT (no Juniper art in the pack): battle back sprite (throw), bike, surf, fishing, Pokétch, '
                  'save, Poké Ball, Sprayduck, healing, Vs. Seeker and contest field poses')
    import make_vs_mugshots  # VS-screen close-ups (replace front_set's simple crop)
    make_vs_mugshots.main()
    (PACK / 'phase7_sprite_report.txt').write_text('\n'.join(report) + '\n')
    print('\n'.join(report))


if __name__ == '__main__':
    main()
