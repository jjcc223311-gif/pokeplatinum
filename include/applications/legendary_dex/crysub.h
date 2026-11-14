#ifndef POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_CRYSUB_H
#define POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_CRYSUB_H

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "heap.h"

void LegDex_CrySub_Init(PokedexScreenManager *screenMan, PokedexApp *pokedexApp, enum HeapID heapID);
void LegDex_CrySub_Free(PokedexScreenManager *screenMan);
int LegDex_CrySub_GetPitch(const PokedexScreenManager *screenMan);

#endif // POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_CRYSUB_H
