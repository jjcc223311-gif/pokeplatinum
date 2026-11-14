#ifndef POKEPLATINUM_LEGDEX_POKEDEX_FORMMAIN_H
#define POKEPLATINUM_LEGDEX_POKEDEX_FORMMAIN_H

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "heap.h"

void LegDex_FormMain_Init(PokedexScreenManager *screenMan, PokedexApp *pokedexApp, enum HeapID heapID);
void LegDex_FormMain_Free(PokedexScreenManager *screenMan);
BOOL LegDex_FormMain_NextForm(PokedexScreenManager *screenMan, int formDelta);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_FORMMAIN_H
