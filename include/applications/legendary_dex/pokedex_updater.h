#ifndef POKEPLATINUM_LEGDEX_POKEDEX_UPDATER_H
#define POKEPLATINUM_LEGDEX_POKEDEX_UPDATER_H

#include "applications/legendary_dex/pokedex_data_manager.h"
#include "applications/legendary_dex/pokedex_graphics_manager.h"

#include "heap.h"

typedef BOOL (*PokedexDataFunction)(PokedexDataManager *dataMan, void *data);

typedef BOOL (*PokedexGraphicsFunction)(void *graphics, PokedexGraphicsManager *graphicsMan, const void *data, const PokedexDataManager *dataMan);

typedef struct PokedexUpdater {
    void *pageData;
    void *pageGraphics;
    int state;
    PokedexDataManager dataMan;
    PokedexDataFunction dataFunc[3];
    PokedexGraphicsManager graphicsMan;
    PokedexGraphicsFunction graphicsFunc[3];
    enum HeapID heapID;
} PokedexUpdater;

typedef struct PokedexUpdaterTemplate {
    void *pageData;
    void *pageGraphics;
    const PokedexDataFunction *dataFunc;
    const PokedexGraphicsFunction *graphicsFunc;
} PokedexUpdaterTemplate;

PokedexUpdater *LegDex_PokedexUpdater_New(enum HeapID heapID);
void LegDex_PokedexUpdater_PopulateUpdater(PokedexUpdater *pokedexUpdater, const PokedexUpdaterTemplate *pokedexUpdaterTemplate);
BOOL LegDex_PokedexUpdater_UpdateData(PokedexUpdater *pokedexUpdater);
BOOL LegDex_PokedexUpdater_UpdateGraphics(PokedexUpdater *pokedexUpdater);
void LegDex_PokedexUpdater_SetDataUnchanged(PokedexUpdater *pokedexUpdater, BOOL unchanged);
void LegDex_PokedexUpdater_DataExit(PokedexUpdater *pokedexUpdater);
BOOL LegDex_PokedexUpdater_IsPageExited(PokedexUpdater *pokedexUpdater);
BOOL LegDex_PokedexUpdater_IsPageDataActive(PokedexUpdater *pokedexUpdater);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_UPDATER_H
