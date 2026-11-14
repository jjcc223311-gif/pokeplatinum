#ifndef POKEPLATINUM_CONSTANTS_FORMS_H
#define POKEPLATINUM_CONSTANTS_FORMS_H

#include "constants/species.h"

#define MOVESET_FORM_DEOXYS_ATTACK   NATIONAL_DEX_COUNT + 1
#define MOVESET_FORM_DEOXYS_DEFENSE  NATIONAL_DEX_COUNT + 2
#define MOVESET_FORM_DEOXYS_SPEED    NATIONAL_DEX_COUNT + 3
#define MOVESET_FORM_WORMADAM_SANDY  NATIONAL_DEX_COUNT + 4
#define MOVESET_FORM_WORMADAM_TRASH  NATIONAL_DEX_COUNT + 5
#define MOVESET_FORM_GIRATINA_ORIGIN NATIONAL_DEX_COUNT + 6
#define MOVESET_FORM_SHAYMIN_SKY     NATIONAL_DEX_COUNT + 7
#define MOVESET_FORM_ROTOM_HEAT      NATIONAL_DEX_COUNT + 8
#define MOVESET_FORM_ROTOM_WASH      NATIONAL_DEX_COUNT + 9
#define MOVESET_FORM_ROTOM_FROST     NATIONAL_DEX_COUNT + 10
#define MOVESET_FORM_ROTOM_FAN       NATIONAL_DEX_COUNT + 11
#define MOVESET_FORM_ROTOM_MOW       NATIONAL_DEX_COUNT + 12

#define MOVESET_MAX MOVESET_FORM_ROTOM_MOW

#define UNOWN_FORM_A     0
#define UNOWN_FORM_B     1
#define UNOWN_FORM_C     2
#define UNOWN_FORM_D     3
#define UNOWN_FORM_E     4
#define UNOWN_FORM_F     5
#define UNOWN_FORM_G     6
#define UNOWN_FORM_H     7
#define UNOWN_FORM_I     8
#define UNOWN_FORM_J     9
#define UNOWN_FORM_K     10
#define UNOWN_FORM_L     11
#define UNOWN_FORM_M     12
#define UNOWN_FORM_N     13
#define UNOWN_FORM_O     14
#define UNOWN_FORM_P     15
#define UNOWN_FORM_Q     16
#define UNOWN_FORM_R     17
#define UNOWN_FORM_S     18
#define UNOWN_FORM_T     19
#define UNOWN_FORM_U     20
#define UNOWN_FORM_V     21
#define UNOWN_FORM_W     22
#define UNOWN_FORM_X     23
#define UNOWN_FORM_Y     24
#define UNOWN_FORM_Z     25
#define UNOWN_FORM_EXC   26
#define UNOWN_FORM_QUE   27
#define UNOWN_FORM_COUNT 28

#define CASTFORM_FORM_NORMAL 0
#define CASTFORM_FORM_SUNNY  1
#define CASTFORM_FORM_RAINY  2
#define CASTFORM_FORM_SNOWY  3
#define CASTFORM_FORM_COUNT  4

#define DEOXYS_FORM_NORMAL  0
#define DEOXYS_FORM_ATTACK  1
#define DEOXYS_FORM_DEFENSE 2
#define DEOXYS_FORM_SPEED   3
#define DEOXYS_FORM_COUNT   4

#define BURMY_FORM_PLANT 0
#define BURMY_FORM_SAND  1
#define BURMY_FORM_TRASH 2
#define BURMY_FORM_COUNT 3

#define WORMADAM_FORM_PLANT 0
#define WORMADAM_FORM_SAND  1
#define WORMADAM_FORM_TRASH 2
#define WORMADAM_FORM_COUNT 3

#define CHERRIM_FORM_OVERCAST 0
#define CHERRIM_FORM_SUNSHINE 1
#define CHERRIM_FORM_COUNT    2

#define SHELLOS_FORM_WEST  0
#define SHELLOS_FORM_EAST  1
#define SHELLOS_FORM_COUNT 2

#define GASTRODON_FORM_WEST  0
#define GASTRODON_FORM_EAST  1
#define GASTRODON_FORM_COUNT 2

#define ROTOM_FORM_BASE  0
#define ROTOM_FORM_HEAT  1
#define ROTOM_FORM_WASH  2
#define ROTOM_FORM_FROST 3
#define ROTOM_FORM_FAN   4
#define ROTOM_FORM_MOW   5
#define ROTOM_FORM_COUNT 6

#define GIRATINA_FORM_ALTERED 0
#define GIRATINA_FORM_ORIGIN  1
#define GIRATINA_FORM_COUNT   2

// Origin Formes (held Adamant / Lustrous Orb), like Giratina's; data and sprites from
// res/pokemon/extra_forms.json
#define DIALGA_FORM_BASE   0
#define DIALGA_FORM_ORIGIN 1
#define DIALGA_FORM_COUNT  2

#define PALKIA_FORM_BASE   0
#define PALKIA_FORM_ORIGIN 1
#define PALKIA_FORM_COUNT  2

// Form numbers used by every Mega / Legendary Mega (forms are 5 bits: 0-31; Unown uses up to 27).
// Which species have which of them, and where each species' own data lives, is
// res/pokemon/mega_forms.json. A species with a _2 form always has the matching _1 form.
#define FORM_MEGA_2           28 // second Mega (e.g. Charizard, Mewtwo)
#define FORM_MEGA_1           29 // every species' first Mega
#define FORM_LEGENDARY_MEGA_1 30
#define FORM_LEGENDARY_MEGA_2 31

#define FORM_IS_MEGA(form) ((form) >= FORM_MEGA_2 && (form) <= FORM_LEGENDARY_MEGA_2)

#define SHAYMIN_FORM_LAND  0
#define SHAYMIN_FORM_SKY   1
#define SHAYMIN_FORM_COUNT 2

#define ARCEUS_FORM_LIGHT 19 // = TYPE_LIGHT (Light Plate); sprite from res/pokemon/extra_forms.json
#define ARCEUS_FORM_COUNT 20 // forms are type numbers; 18 (Fairy) is unused

// Gen 5 alternate forms; data and sprites from res/pokemon/extra_forms.json
#define BASCULIN_FORM_RED_STRIPED  0
#define BASCULIN_FORM_BLUE_STRIPED 1

#define DARMANITAN_FORM_STANDARD 0
#define DARMANITAN_FORM_ZEN      1

// Deerling / Sawsbuck: the season when they were met (spring, summer, autumn, winter)
#define SEASON_FORM_SPRING 0
#define SEASON_FORM_SUMMER 1
#define SEASON_FORM_AUTUMN 2
#define SEASON_FORM_WINTER 3
#define SEASON_FORM_COUNT  4

// Tornadus / Thundurus / Landorus (Reveal Glass)
#define FORCES_OF_NATURE_FORM_INCARNATE 0
#define FORCES_OF_NATURE_FORM_THERIAN   1

#define KELDEO_FORM_ORDINARY 0
#define KELDEO_FORM_RESOLUTE 1 // knows Secret Sword

#define MELOETTA_FORM_ARIA      0
#define MELOETTA_FORM_PIROUETTE 1 // in battle, after Relic Song

// Genesect: held Drive (also sets Techno Blast's type)
#define GENESECT_FORM_NONE  0
#define GENESECT_FORM_DOUSE 1
#define GENESECT_FORM_SHOCK 2
#define GENESECT_FORM_BURN  3
#define GENESECT_FORM_CHILL 4

#define EGG_FORM_BASE    0
#define EGG_FORM_MANAPHY 1
#define EGG_FORM_COUNT   2

#endif
