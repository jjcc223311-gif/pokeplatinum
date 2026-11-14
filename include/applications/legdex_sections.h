#ifndef POKEPLATINUM_LEGDEX_SECTIONS_H
#define POKEPLATINUM_LEGDEX_SECTIONS_H

#include "overlay_manager.h"
#include "savedata.h"

// The Legendary Pokédex's home screen: tabs for the Pokémon list (the Pokédex app itself), the Mega
// Evolution section, the Types section and the Abilities section.

enum LegDexSectionsTab {
    LEGDEX_TAB_POKEMON = 0,
    LEGDEX_TAB_MEGA,
    LEGDEX_TAB_TYPES,
    LEGDEX_TAB_ABILITIES,
    LEGDEX_TAB_COUNT,
};

enum LegDexSectionsChoice {
    LEGDEX_CHOICE_EXIT = 0,
    LEGDEX_CHOICE_OPEN_LIST, // open the Pokémon list, then come back here
};

typedef struct LegDexSectionsArgs {
    SaveData *saveData;
    enum LegDexSectionsChoice choice; // out
    // Kept between visits while the start menu is open
    u8 tab;
    u16 cursor[LEGDEX_TAB_COUNT];
    u16 scroll[LEGDEX_TAB_COUNT];
} LegDexSectionsArgs;

BOOL LegDexSections_Init(ApplicationManager *appMan, int *state);
BOOL LegDexSections_Main(ApplicationManager *appMan, int *state);
BOOL LegDexSections_Exit(ApplicationManager *appMan, int *state);

#endif // POKEPLATINUM_LEGDEX_SECTIONS_H
