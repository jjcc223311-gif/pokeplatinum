# Johto outfits (staging)

Johto-outfit versions of the player and Barry sprites, made from `tools/johto_outfits/reference.png`.
Not wired into the build yet: the outfit switch (Suitcase / Personal Bag) will load these.

- `player_male` = Lucas, `player_female` = Juniper, `rival` = Barry
- `front.png` 80x80 battle front, `mugshot.png` 96x64 VS-screen close-up, 16 colours, index 0 transparent

Rebuild with:
    python3 tools/johto_outfits/ref_to_front.py tools/johto_outfits/reference.png X0 X1 Y0 Y1 72 out.png
    python3 tools/johto_outfits/ref_to_mugshot.py tools/johto_outfits/reference.png CX TOP 420 out.png
(Lucas 205 518 59 662 / 352 55, Barry 756 1138 69 662 / 930 60, Juniper 1387 1714 79 664 / 1575 75)
