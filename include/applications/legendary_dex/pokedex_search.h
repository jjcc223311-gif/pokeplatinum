#ifndef POKEPLATINUM_LEGDEX_POKEDEX_SEARCH_H
#define POKEPLATINUM_LEGDEX_POKEDEX_SEARCH_H

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/pokedex_sort.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "heap.h"

enum FilterMethod {
    FM_ORDER,
    FM_NAME,
    FM_TYPE,
    FM_FORM,
    MAX_FILTER_METHOD
};

void LegDex_PokedexSearch_TransitionFunctions(PokedexScreenManager *param0, PokedexApp *param1, enum HeapID heapID);
void LegDex_PokedexSearch_FreeData(PokedexScreenManager *param0);
void LegDex_PokedexSearch_SetFilterMethod(PokedexScreenManager *param0, enum FilterMethod filterMethod);
enum FilterMethod LegDex_PokedexSearch_GetFilterMethod(const PokedexScreenManager *param0);
void LegDex_PokedexSearch_SetSortOrder(PokedexScreenManager *param0, enum SortOrder sortOrder);
enum SortOrder LegDex_PokedexSearch_GetSortOrder(const PokedexScreenManager *param0);
void LegDex_PokedexSearch_SetFilterName(PokedexScreenManager *param0, enum FilterName filterName);
enum FilterName LegDex_PokedexSearch_GetFilterName(const PokedexScreenManager *param0);
void LegDex_PokedexSearch_SetFilterType(PokedexScreenManager *param0, enum FilterType filterType, int typeSlot);
enum FilterType LegDex_PokedexSearch_GetFilterType(const PokedexScreenManager *param0, int typeSlot);
void LegDex_PokedexSearch_SetFilterForm(PokedexScreenManager *param0, enum FilterForm filterForm);
enum FilterForm LegDex_PokedexSearch_GetFilterForm(const PokedexScreenManager *param0);
void LegDex_PokedexSearch_SetFilteredState(PokedexScreenManager *param0, BOOL applyFilter);
BOOL LegDex_PokedexSearch_GetFilteredState(const PokedexScreenManager *param0);
int LegDex_PokedexSearch_GetScreenState(const PokedexScreenManager *param0);
int LegDex_PokedexSearch_GetScreenTimer(const PokedexScreenManager *param0);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_SEARCH_H
