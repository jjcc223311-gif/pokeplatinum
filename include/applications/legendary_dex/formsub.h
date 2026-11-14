#ifndef POKEPLATINUM_LEGDEX_POKEDEX_FORMSUB_H
#define POKEPLATINUM_LEGDEX_POKEDEX_FORMSUB_H

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "heap.h"

void LegDex_FormSub_Init(PokedexScreenManager *screenMan, PokedexApp *pokedexApp, enum HeapID heapID);
void LegDex_FormSub_Free(PokedexScreenManager *screenMan);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_FORMSUB_H
