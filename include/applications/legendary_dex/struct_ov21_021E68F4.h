#ifndef POKEPLATINUM_LEGDEX_STRUCT_OV21_021E68F4_H
#define POKEPLATINUM_LEGDEX_STRUCT_OV21_021E68F4_H

#include "applications/legendary_dex/pokedex_updater.h"
#include "applications/legendary_dex/struct_ov21_021D4660.h"

typedef struct PokedexScreenManager {
    void *pageData;
    void *pageGraphics;
    PokedexDataFunction dataFunc[3];
    PokedexGraphicsFunction graphicsFunc[3];
    UnkStruct_ov21_021D4660 *screenStates;
    int numStates;
} PokedexScreenManager;

#endif // POKEPLATINUM_LEGDEX_STRUCT_OV21_021E68F4_H
