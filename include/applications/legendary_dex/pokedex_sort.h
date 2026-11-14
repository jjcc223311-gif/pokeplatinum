#ifndef POKEPLATINUM_LEGDEX_POKEDEXSORT_H
#define POKEPLATINUM_LEGDEX_POKEDEXSORT_H

#include "constants/heap.h"

#include "applications/legendary_dex/pokedex_sort_data.h"
#include "applications/legendary_dex/species_caught_status.h"

#include "pokedex.h"
#include "string_gf.h"
#include "trainer_info.h"

enum SortOrder {
    SO_NUMERICAL,
    SO_ALPHABETICAL,
    SO_HEAVIEST,
    SO_LIGHTEST,
    SO_TALLEST,
    SO_SMALLEST,
    MAX_SORT_ORDER
};

enum FilterName {
    FN_NONE,
    FN_ABC,
    FN_DEF,
    FN_GHI,
    FN_JKL,
    FN_MNO,
    FN_PQR,
    FN_STU,
    FN_VWX,
    FN_YZ,
    MAX_FILTER_NAME
};

enum FilterType {
    FT_NONE,
    FT_NORMAL,
    FT_FIGHTING,
    FT_FLYING,
    FT_POISON,
    FT_GROUND,
    FT_ROCK,
    FT_BUG,
    FT_GHOST,
    FT_STEEL,
    FT_FIRE,
    FT_WATER,
    FT_GRASS,
    FT_ELECTRIC,
    FT_PSYCHIC,
    FT_ICE,
    FT_DRAGON,
    FT_DARK,
    MAX_FILTER_TYPE
};

enum FilterForm { // called form in game, but refers to body shape
    FF_NONE,
    FF_QUADRUPED,
    FF_BIPEDALTAILLESS,
    FF_BIPEDALTAILED,
    FF_SERPENTINE,
    FF_MULTIWINGED,
    FF_WINGED,
    FF_INSECTOID,
    FF_HEADBASE,
    FF_HEADARMS,
    FF_HEADLEGS,
    FF_TENTACLES,
    FF_FINS,
    FF_HEAD,
    FF_MULTIBODY,
    MAX_FILTER_FORM
};

typedef struct PokedexDefaultSortParams {
    const Pokedex *pokedex;
    const TrainerInfo *trainerInfo;
    int timeOfDay;
    BOOL fullmoonIslandVisible;
    BOOL newmoonIslandVisible;
    BOOL springPathVisible;
    BOOL seabreakPathVisible;
    u32 currentSpecies;
    u32 bootMode;
} PokedexDefaultSortParams;

void LegDex_PokedexSort_DefaultPokedexSort(PokedexSortData *param0, PokedexDefaultSortParams *param1, enum HeapID heapID);
void LegDex_PokedexSort_PokedexStatusFreeHWData(PokedexSortData *param0);
u32 LegDex_PokedexSort_Gender(const PokedexSortData *param0, int species, int formIndex);
u32 LegDex_PokedexSort_UnownForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_ShellosForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_GastrodonForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_BurmyForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_WormadamForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_DefaultForm(const PokedexSortData *param0, u32 species);
u32 LegDex_PokedexSort_NumGendersVisible(const PokedexSortData *param0, int species);
u32 LegDex_PokedexSort_SpindaForm(const PokedexSortData *param0);
u32 LegDex_PokedexSort_DeoxysForm(const PokedexSortData *param0, int formIndex);
u32 LegDex_PokedexSort_Form(const PokedexSortData *param0, u32 species, int formIndex);
u32 LegDex_PokedexSort_NumFormsSeen(const PokedexSortData *param0, u32 species);
BOOL LegDex_PokedexSort_IsNationalUnlocked(const PokedexSortData *param0);
void LegDex_PokedexSort_SetCurrentSpecies(PokedexSortData *param0, u32 param1);
u32 LegDex_PokedexSort_GetCurrentSpecies(const PokedexSortData *param0);
void LegDex_PokedexSort_SetBootMode(PokedexSortData *param0, u32 param1);
u32 LegDex_PokedexSort_GetBootMode(const PokedexSortData *param0);
BOOL LegDex_PokedexSort_Sort(PokedexSortData *param0, enum SortOrder sortOrder, enum FilterName filterName, enum FilterType typeFilter1, enum FilterType typeFilter2, enum FilterForm filterForm, int isNationalDex, enum HeapID heapID, BOOL isFiltered);
BOOL LegDex_PokedexSort_SortUnfiltered(PokedexSortData *param0, enum SortOrder sortOrder, enum FilterName filterName, enum FilterType filterType1, enum FilterType filterType2, enum FilterForm filterForm, int isNationalDex, enum HeapID heapID);
BOOL LegDex_ov21_021D36A4(const PokedexSortData *param0, int param1);
BOOL LegDex_ov21_021D36C0(PokedexSortData *param0, int param1);
int LegDex_PokedexSort_IsNationalDex(const PokedexSortData *param0);
BOOL LegDex_PokedexSort_IsValidStatusIndex(const PokedexSortData *param0, int dexIndex);
BOOL LegDex_PokedexSort_SetCurrentStatusIndex(PokedexSortData *param0, int param1);
BOOL LegDex_PokedexSort_TakeStep_Loop(PokedexSortData *param0, int param1);
int LegDex_PokedexSort_CurrentStatusIndex(const PokedexSortData *param0);
int LegDex_PokedexSort_CaughtStatusLength(const PokedexSortData *param0);
int LegDex_PokedexSort_SpeciesToStatusIndex(const PokedexSortData *param0, u32 param1);
BOOL LegDex_PokedexSort_SetCurrentStatusIndexWithSpecies(PokedexSortData *param0, int param1);
enum Species LegDex_PokedexSort_CurrentSpecies(const PokedexSortData *param0);
int LegDex_PokedexSort_CurrentCaughtStatus(const PokedexSortData *param0);
const SpeciesCaughtStatus *LegDex_PokedexSort_StatusIndexToCaughtStatus(const PokedexSortData *param0, int dexIndex);
BOOL LegDex_PokedexSort_IsValidDisplayIndex(const PokedexSortData *param0, int param1);
BOOL LegDex_PokedexSort_SetCurrentValues(PokedexSortData *param0, int param1);
BOOL LegDex_PokedexSort_TakeStep(PokedexSortData *param0, int param1);
BOOL LegDex_PokedexSort_IsValidStep(PokedexSortData *param0, int param1);
int LegDex_PokedexSort_CurrentDisplayIndex(const PokedexSortData *param0);
int PokedexSort_NumSpeciesDisplayed(const PokedexSortData *param0);
int LegDex_PokedexSort_DisplayIndexToStatusIndex(const PokedexSortData *param0, int param1);
void LegDex_PokedexSort_UpdateCurrentValues(PokedexSortData *param0);
int LegDex_PokedexSort_NumEncountered(const PokedexSortData *param0);
int LegDex_PokedexSort_NumCaught(const PokedexSortData *param0);
String *LegDex_PokedexSort_TrainerName(const PokedexSortData *param0);
u32 LegDex_PokedexSort_TrainerGender(const PokedexSortData *param0);
BOOL LegDex_ov21_021D392C(const PokedexSortData *param0, int param1);
BOOL LegDex_PokedexSort_CanDetectForms(const PokedexSortData *param0);
void LegDex_ov21_021D3960(PokedexSortData *param0);
u32 LegDex_ov21_021D3998(const PokedexSortData *param0);

// Forms page: species whose forms are listed by include/data/legdex_tables.h (Origin Formes, Arceus,
// Kyurem, Gen 5 forms, ...). Count is 0 for other species.
int LegDex_ExtraFormCount(u32 species);
int LegDex_ExtraForm(u32 species, int formIndex);
int LegDex_ExtraFormLabel(u32 species, int formIndex); // legdex_sections text entry

#endif // POKEPLATINUM_LEGDEX_POKEDEXSORT_H
