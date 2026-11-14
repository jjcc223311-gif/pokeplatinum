#ifndef POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_FOREIGN_H
#define POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_FOREIGN_H

#include "applications/legendary_dex/infomain.h"
#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "heap.h"

void LegDex_InfoMainForeign_InitScreen(PokedexScreenManager *screenManager, PokedexApp *pokedexApp, enum HeapID heapID);
void LegDex_InfoMainForeign_FreeScreen(PokedexScreenManager *screenManager);
void LegDex_InfoMainForeign_SetDisplayPosition(PokedexScreenManager *screenManager, int posX, int posY);
void LegDex_InfoMainForeign_SetAnimationMode(PokedexScreenManager *screenManager, enum AnimationMode animationMode);
int LegDex_InfoMainForeign_GetScreenStateCount(PokedexScreenManager *screenManager);
BOOL LegDex_InfoMainForeign_SetEntryOffset(PokedexScreenManager *screenManager, int entryOffset);
void LegDex_InfoMainForeign_SetLanguage(PokedexScreenManager *screenManager, int languageID);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_INFOMAIN_FOREIGN_H
