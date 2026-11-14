#ifndef POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_H
#define POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_H

/**
 * Animation modes for Pokedex info screen transitions.
 * Used by both the default language and multi-language info screens.
 */
enum AnimationMode {
    ANIM_POSITION_BLEND = 0, // Animate position and blend transparency
    ANIM_BLEND, // Animate blend transparency only
    ANIM_POSITION, // Animate position only
};

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/pokedex_sort_data.h"
#include "applications/legendary_dex/pokedex_text_manager.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "bg_window.h"
#include "heap.h"

/**
 * State information for the Pokedex info main screen.
 */
typedef struct InfoMainState {
    int *displayWorkData; // Work data pointer set from LegDex_ov21_021D138C
    PokedexSortData *sortData; // Pokemon sort/listing data
    int displayPositionX; // X coordinate for display position animation
    int displayPositionY; // Y coordinate for display position animation
    const PokedexScreenManager *screenManager; // Screen manager reference
    enum AnimationMode animationMode;
    int entryOffset; // Dex entry offset (0 = current entry)
    BOOL playCry; // Flag to play Pokemon cry
} InfoMainState;

void LegDex_InfoMain_InitScreen(PokedexScreenManager *screenManager, PokedexApp *pokedexApp, enum HeapID heapID);
void LegDex_InfoMain_FreeScreen(PokedexScreenManager *screenManager);
BOOL LegDex_InfoMain_SetDisplayPosition(InfoMainState *displayState, int unused);
BOOL LegDex_InfoMain_SetEntryOffset(InfoMainState *displayState, int entryOffset);
void LegDex_InfoMain_RenderHeightWeightEntry(Window *window, int species, enum HeapID heapID, int entryOffset, u32 textColor);
int LegDex_PokedexGraphics_GetAnimIDfromType(int monType);
Window *LegDex_InfoMain_CreateCategoryWindow(PokedexTextManager *textMan, enum Species species, enum HeapID heapID);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_H
