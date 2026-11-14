#include "applications/legendary_dex/pokedex_sort.h"

#include <string.h>

#include "constants/heap.h"
#include "constants/species.h"
#include "generated/gender_ratios.h"
#include "generated/genders.h"
#include "generated/species_data_params.h"

#include "applications/legendary_dex/pokedex_sort_data.h"
#include "applications/legendary_dex/sorted_pokedex.h"
#include "applications/legendary_dex/species_caught_status.h"

#include "graphics.h"
#include "heap.h"
#include "pokedex.h"
#include "pokedex_data_index.h"
#include "pokedex_heightweight.h"
#include "pokedex_memory.h"
#include "pokemon.h"
#include "constants/forms.h"
#include "string_gf.h"
#include "system.h"
#include "trainer_info.h"

#include "data/legdex_tables.h"

#define NUMSTATFILES 11

// zukan_data holds the original Pokédex's 47 listings (#1-493) first, then the same 47 listings
// for the Legendary Pokédex (#1-649); see PackDexLists in tools/dataproc/src/speciesproc.c
#define LEGDEX_LISTS_OFFSET PDSI_NUMSORTS
#define BLANKSPACE   (LEGDEX_SPECIES_COUNT + 1)

enum PokedexDataSortIndex {
    PDSI_NATIONAL,
    PDSI_SINNOH,
    PDSI_ALPHABETICAL,
    PDSI_HEAVIEST,
    PDSI_LIGHTEST,
    PDSI_TALLEST,
    PDSI_SMALLEST,
    PDSI_ABC,
    PDSI_DEF,
    PDSI_GHI,
    PDSI_JKL,
    PDSI_MNO,
    PDSI_PQR,
    PDSI_STU,
    PDSI_VWX,
    PDSI_YZ,
    PDSI_NORMAL,
    PDSI_FIGHTING,
    PDSI_FLYING,
    PDSI_POISON,
    PDSI_GROUND,
    PDSI_ROCK,
    PDSI_BUG,
    PDSI_GHOST,
    PDSI_STEEL,
    PDSI_FIRE,
    PDSI_WATER,
    PDSI_GRASS,
    PDSI_ELECTRIC,
    PDSI_PSYCHIC,
    PDSI_ICE,
    PDSI_DRAGON,
    PDSI_DARK,
    PDSI_QUADRUPED,
    PDSI_BIPEDALTAILLESS,
    PDSI_BIPEDALTAILED,
    PDSI_SERPENTINE,
    PDSI_MULTIWINGED,
    PDSI_WINGED,
    PDSI_INSECTOID,
    PDSI_HEADBASE,
    PDSI_HEADARMS,
    PDSI_HEADLEGS,
    PDSI_TENTACLES,
    PDSI_FINS,
    PDSI_HEAD,
    PDSI_MULTIBODY,
    PDSI_NUMSORTS
};

// Reference Pokédex: every species counts as seen and caught
static BOOL LegDex_IsListed(int species)
{
    return species >= 1 && species <= NATIONAL_DEX_COUNT;
}

static void FilterUnencountered(u16 *encounteredDex, int *caughtStatusLength, const Pokedex *pokedex, const u16 *fullDex, int pokedexLength);
static void IntersectPokedexes(u16 *resultingPokedex, int *numResulting, const u16 *pokedex1, int dexLen1, const u16 *pokedex2, int dexLen2, BOOL keepUncaught, const Pokedex *pokedex);
static void UpdateCaughtStatus(SortedPokedex *sortedPokedex, const Pokedex *pokedex, const u16 *encounteredPokedex, int caughtStatusLength);
static void PopulateDisplayPokedex_Blanks(SortedPokedex *sortedPokedex, const u16 *fullDex, int pokedexLength);
static void PopulateDisplayPokedex(SortedPokedex *sortedPokedex);
static void NumEncounteredAndCaught(SortedPokedex *sortedPokedex, int *caughtStatusLength, int *numCaught);
static u16 *PokedexFromNARC(enum HeapID heapID, int pokedexSort, int *pokedexLength);
static void DexSortOrder(int sortOrder, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex);
static void FilterByName(int filterName, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex);
static void FilterByType(int typeFilter, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex);
static void FilterByForm(int filterForm, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex);

void LegDex_PokedexSort_DefaultPokedexSort(PokedexSortData *param0, PokedexDefaultSortParams *param1, enum HeapID heapID)
{
    int sortOrder;
    int filterName;
    int filterType1;
    int filterType2;
    int filterForm;
    BOOL dexExists;
    u32 isNationalDex;

    memset(param0, 0, sizeof(PokedexSortData));

    param0->pokedex = param1->pokedex;
    param0->timeOfDay = param1->timeOfDay;

    if (TRUE) {
        param0->isNationalDexUnlocked = TRUE;
    } else {
        param0->isNationalDexUnlocked = FALSE;
    }

    if (param1->bootMode == POKEDEX_BOOT_DEFAULT) {
        if (param0->isNationalDexUnlocked) {
            isNationalDex = TRUE;
        } else {
            isNationalDex = FALSE;
        }
    } else {
        isNationalDex = param1->bootMode;
    }

    if (isNationalDex == TRUE) {
        param0->isNationalDex = TRUE;
        sortOrder = SO_NUMERICAL;
        filterName = FN_NONE;
        filterType1 = FT_NONE;
        filterType2 = FT_NONE;
        filterForm = FF_NONE;
    } else {
        param0->isNationalDex = FALSE;
        sortOrder = SO_NUMERICAL;
        filterName = FN_NONE;
        filterType1 = FT_NONE;
        filterType2 = FT_NONE;
        filterForm = FF_NONE;
    }

    dexExists = LegDex_PokedexSort_SortUnfiltered(param0, sortOrder, filterName, filterType1, filterType2, filterForm, param0->isNationalDex, heapID);

    GF_ASSERT(dexExists);

    LegDex_PokedexSort_SetCurrentStatusIndexWithSpecies(param0, param1->currentSpecies);
    LegDex_PokedexSort_SetCurrentSpecies(param0, param1->currentSpecies);
    LegDex_PokedexSort_SetBootMode(param0, param1->bootMode);

    param0->trainerGameCode = TrainerInfo_GameCode(param1->trainerInfo);
    param0->trainerGender = TrainerInfo_Gender(param1->trainerInfo);
    param0->trainerName = TrainerInfo_NameNewString(param1->trainerInfo, heapID);
    param0->HWData = Pokedex_HeightWeightData(heapID);

    if (param0->trainerGender == 0) {
        Pokedex_HeightWeightData_Load(param0->HWData, 0, heapID);
    } else {
        Pokedex_HeightWeightData_Load(param0->HWData, 1, heapID);
    }

    param0->fullmoonIslandVisible = param1->fullmoonIslandVisible;
    param0->newmoonIslandVisible = param1->newmoonIslandVisible;
    param0->springPathVisible = param1->springPathVisible;
    param0->seabreakPathVisible = param1->seabreakPathVisible;
}

void LegDex_PokedexSort_PokedexStatusFreeHWData(PokedexSortData *param0)
{
    String_Free(param0->trainerName);
    Pokedex_HeightWeightData_Release(param0->HWData);
    Pokedex_HeightWeightData_Free(param0->HWData);

    param0->HWData = NULL;
}

// Reference Pokédex: genders and forms don't depend on what the player has seen. Every form of a
// species is listed, in form-number order.
u32 LegDex_PokedexSort_Gender(const PokedexSortData *param0, int species, int formIndex)
{
    switch (SpeciesData_GetSpeciesValue(species, SPECIES_DATA_GENDER_RATIO)) {
    case GENDER_RATIO_NO_GENDER:
        return formIndex == 0 ? GENDER_NONE : (u32)-1;
    case GENDER_RATIO_FEMALE_ONLY:
        return formIndex == 0 ? GENDER_FEMALE : (u32)-1;
    case GENDER_RATIO_MALE_ONLY:
        return formIndex == 0 ? GENDER_MALE : (u32)-1;
    default:
        return formIndex == 0 ? GENDER_MALE : formIndex == 1 ? GENDER_FEMALE : (u32)-1;
    }
}

u32 LegDex_PokedexSort_UnownForm(const PokedexSortData *param0, int formIndex)
{
    GF_ASSERT(formIndex < UNOWN_FORM_COUNT);
    return formIndex;
}

u32 LegDex_PokedexSort_ShellosForm(const PokedexSortData *param0, int formIndex)
{
    GF_ASSERT(formIndex < SHELLOS_FORM_COUNT);
    return formIndex;
}

u32 LegDex_PokedexSort_GastrodonForm(const PokedexSortData *param0, int formIndex)
{
    GF_ASSERT(formIndex < GASTRODON_FORM_COUNT);
    return formIndex;
}

u32 LegDex_PokedexSort_BurmyForm(const PokedexSortData *param0, int formIndex)
{
    GF_ASSERT(formIndex < BURMY_FORM_COUNT);
    return formIndex;
}

u32 LegDex_PokedexSort_WormadamForm(const PokedexSortData *param0, int formIndex)
{
    GF_ASSERT(formIndex < WORMADAM_FORM_COUNT);
    return formIndex;
}

u32 LegDex_PokedexSort_DefaultForm(const PokedexSortData *param0, u32 species)
{
    return 0;
}

u32 LegDex_PokedexSort_NumGendersVisible(const PokedexSortData *param0, int species)
{
    return LegDex_PokedexSort_Gender(param0, species, 1) == (u32)-1 ? 1 : 2;
}

u32 LegDex_PokedexSort_SpindaForm(const PokedexSortData *param0)
{
    return 0;
}

u32 LegDex_PokedexSort_DeoxysForm(const PokedexSortData *param0, int formIndex)
{
    return formIndex;
}

u32 LegDex_PokedexSort_Form(const PokedexSortData *param0, u32 species, int formIndex)
{
    return formIndex;
}

u32 LegDex_PokedexSort_NumFormsSeen(const PokedexSortData *param0, u32 species)
{
    switch (species) {
    case SPECIES_UNOWN:
        return UNOWN_FORM_COUNT;
    case SPECIES_SHELLOS:
        return SHELLOS_FORM_COUNT;
    case SPECIES_GASTRODON:
        return GASTRODON_FORM_COUNT;
    case SPECIES_BURMY:
        return BURMY_FORM_COUNT;
    case SPECIES_WORMADAM:
        return WORMADAM_FORM_COUNT;
    case SPECIES_DEOXYS:
        return DEOXYS_FORM_COUNT;
    case SPECIES_SHAYMIN:
        return SHAYMIN_FORM_COUNT;
    case SPECIES_GIRATINA:
        return GIRATINA_FORM_COUNT;
    case SPECIES_ROTOM:
        return ROTOM_FORM_COUNT;
    }

    return LegDex_ExtraFormCount(species);
}

BOOL LegDex_PokedexSort_IsNationalUnlocked(const PokedexSortData *param0)
{
    return TRUE;
}

void LegDex_PokedexSort_SetCurrentSpecies(PokedexSortData *param0, u32 species)
{
    param0->currentSpecies = species;
}

u32 LegDex_PokedexSort_GetCurrentSpecies(const PokedexSortData *param0)
{
    return param0->currentSpecies;
}

void LegDex_PokedexSort_SetBootMode(PokedexSortData *param0, u32 bootMode)
{
    param0->bootMode = bootMode;
}

u32 LegDex_PokedexSort_GetBootMode(const PokedexSortData *param0)
{
    return param0->bootMode;
}

BOOL LegDex_PokedexSort_Sort(PokedexSortData *param0, enum SortOrder sortOrder, enum FilterName filterName, enum FilterType filterType1, enum FilterType filterType2, enum FilterForm filterForm, int isNationalDex, enum HeapID heapID, BOOL isFiltered)
{
    u16 *encounteredPokedex;
    int caughtStatusLength;
    u16 *resultingPokedex;
    int numResulting;
    u16 *fullDex;
    int fullDexLength;
    BOOL dexExists;

    encounteredPokedex = Heap_AllocAtEnd(heapID, sizeof(u16) * LEGDEX_SPECIES_COUNT);

    GF_ASSERT(encounteredPokedex);
    memset(encounteredPokedex, 0, sizeof(u16) * LEGDEX_SPECIES_COUNT);

    caughtStatusLength = 0;
    resultingPokedex = Heap_AllocAtEnd(heapID, sizeof(u16) * LEGDEX_SPECIES_COUNT);

    GF_ASSERT(resultingPokedex);
    memset(resultingPokedex, 0, sizeof(u16) * LEGDEX_SPECIES_COUNT);

    numResulting = 0;

    if (isNationalDex == FALSE) {
        fullDex = PokedexFromNARC(heapID, PDSI_SINNOH, &fullDexLength);
        FilterUnencountered(encounteredPokedex, &caughtStatusLength, param0->pokedex, fullDex, fullDexLength);
    } else {
        fullDex = PokedexFromNARC(heapID, PDSI_NATIONAL, &fullDexLength);
        FilterUnencountered(encounteredPokedex, &caughtStatusLength, param0->pokedex, fullDex, fullDexLength);
    }

    DexSortOrder(sortOrder, resultingPokedex, &numResulting, encounteredPokedex, caughtStatusLength, heapID, param0->pokedex);

    memcpy(encounteredPokedex, resultingPokedex, sizeof(u16) * numResulting);
    caughtStatusLength = numResulting;

    memset(resultingPokedex, 0, sizeof(u16) * numResulting);
    numResulting = 0;

    do {
        FilterByName(filterName, resultingPokedex, &numResulting, encounteredPokedex, caughtStatusLength, heapID, param0->pokedex);

        if (numResulting == 0) {
            dexExists = FALSE;
            break;
        }

        memcpy(encounteredPokedex, resultingPokedex, sizeof(u16) * numResulting);
        caughtStatusLength = numResulting;

        memset(resultingPokedex, 0, sizeof(u16) * numResulting);
        numResulting = 0;

        FilterByType(filterType1, resultingPokedex, &numResulting, encounteredPokedex, caughtStatusLength, heapID, param0->pokedex);

        if (numResulting == 0) {
            dexExists = FALSE;
            break;
        }

        memcpy(encounteredPokedex, resultingPokedex, sizeof(u16) * numResulting);
        caughtStatusLength = numResulting;

        memset(resultingPokedex, 0, sizeof(u16) * numResulting);
        numResulting = 0;

        FilterByType(filterType2, resultingPokedex, &numResulting, encounteredPokedex, caughtStatusLength, heapID, param0->pokedex);

        if (numResulting == 0) {
            dexExists = FALSE;
            break;
        }

        memcpy(encounteredPokedex, resultingPokedex, sizeof(u16) * numResulting);
        caughtStatusLength = numResulting;

        memset(resultingPokedex, 0, sizeof(u16) * numResulting);
        numResulting = 0;

        FilterByForm(filterForm, resultingPokedex, &numResulting, encounteredPokedex, caughtStatusLength, heapID, param0->pokedex);

        if (numResulting == 0) {
            dexExists = FALSE;
            break;
        }

        memcpy(encounteredPokedex, resultingPokedex, sizeof(u16) * numResulting);
        caughtStatusLength = numResulting;

        memset(resultingPokedex, 0, sizeof(u16) * numResulting);
        numResulting = 0;

        UpdateCaughtStatus(&param0->sortedPokedex, param0->pokedex, encounteredPokedex, caughtStatusLength);

        if ((sortOrder != SO_NUMERICAL) || (filterName != FN_NONE) || (filterType1 != FT_NONE) || (filterType2 != FT_NONE) || (filterForm != FF_NONE)) {
            isFiltered = TRUE;
        }

        if (isFiltered == FALSE) {
            PopulateDisplayPokedex_Blanks(&param0->sortedPokedex, fullDex, fullDexLength);
        } else {
            PopulateDisplayPokedex(&param0->sortedPokedex);
        }

        dexExists = TRUE;
    } while (FALSE);

    NumEncounteredAndCaught(&param0->sortedPokedex, &param0->numEncountered, &param0->numCaught);

    Heap_Free(encounteredPokedex);
    Heap_Free(resultingPokedex);
    Heap_Free(fullDex);

    return dexExists;
}

BOOL LegDex_PokedexSort_SortUnfiltered(PokedexSortData *param0, enum SortOrder sortOrder, enum FilterName filterName, enum FilterType filterType1, enum FilterType filterType2, enum FilterForm filterForm, int isNationalDex, enum HeapID heapID)
{
    return LegDex_PokedexSort_Sort(param0, sortOrder, filterName, filterType1, filterType2, filterForm, isNationalDex, heapID, FALSE);
}

BOOL LegDex_ov21_021D36A4(const PokedexSortData *param0, int param1)
{
    if (param1 == 0) {
        return TRUE;
    }

    if (param0->isNationalDexUnlocked) {
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_ov21_021D36C0(PokedexSortData *param0, int param1)
{
    BOOL v0 = LegDex_ov21_021D36A4(param0, param1);

    if (v0) {
        param0->isNationalDex = param1;
    }

    return v0;
}

int LegDex_PokedexSort_IsNationalDex(const PokedexSortData *param0)
{
    return param0->isNationalDex;
}

BOOL LegDex_PokedexSort_IsValidStatusIndex(const PokedexSortData *param0, int dexIndex)
{
    if (((dexIndex) >= 0) && ((dexIndex) < param0->sortedPokedex.caughtStatusLength)) {
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_PokedexSort_SetCurrentStatusIndex(PokedexSortData *param0, int statusIndex)
{
    if (LegDex_PokedexSort_IsValidStatusIndex(param0, statusIndex)) {
        param0->sortedPokedex.currentStatusIndex = statusIndex;
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_PokedexSort_TakeStep_Loop(PokedexSortData *param0, int step)
{
    if (LegDex_PokedexSort_IsValidStatusIndex(param0, param0->sortedPokedex.currentStatusIndex + step)) {
        param0->sortedPokedex.currentStatusIndex += step;
        return TRUE;
    }

    if (step >= 0) {
        param0->sortedPokedex.currentStatusIndex = param0->sortedPokedex.caughtStatusLength - 1;
    } else {
        param0->sortedPokedex.currentStatusIndex = 0;
    }

    return FALSE;
}

int LegDex_PokedexSort_CurrentStatusIndex(const PokedexSortData *param0)
{
    return param0->sortedPokedex.currentStatusIndex;
}

int LegDex_PokedexSort_CaughtStatusLength(const PokedexSortData *param0)
{
    return param0->sortedPokedex.caughtStatusLength;
}

int LegDex_PokedexSort_SpeciesToStatusIndex(const PokedexSortData *param0, u32 species)
{
    int statusIndex;
    int caughtStatusLength = LegDex_PokedexSort_CaughtStatusLength(param0);
    int compareSpecies;

    for (statusIndex = 0; statusIndex < caughtStatusLength; statusIndex++) {
        compareSpecies = param0->sortedPokedex.caughtStatusArray[statusIndex].species;

        if (compareSpecies == species) {
            break;
        }
    }

    return statusIndex;
}

BOOL LegDex_PokedexSort_SetCurrentStatusIndexWithSpecies(PokedexSortData *param0, int species)
{
    u32 caughtStatusLength = LegDex_PokedexSort_CaughtStatusLength(param0);
    u32 statusIndex = LegDex_PokedexSort_SpeciesToStatusIndex(param0, species);

    if (caughtStatusLength > statusIndex) {
        return LegDex_PokedexSort_SetCurrentStatusIndex(param0, statusIndex);
    }

    return FALSE;
}

enum Species LegDex_PokedexSort_CurrentSpecies(const PokedexSortData *param0)
{
    return param0->sortedPokedex.caughtStatusArray[param0->sortedPokedex.currentStatusIndex].species;
}

int LegDex_PokedexSort_CurrentCaughtStatus(const PokedexSortData *param0)
{
    return param0->sortedPokedex.caughtStatusArray[param0->sortedPokedex.currentStatusIndex].caughtStatus;
}

const SpeciesCaughtStatus *LegDex_PokedexSort_StatusIndexToCaughtStatus(const PokedexSortData *param0, int statusIndex)
{
    if (LegDex_PokedexSort_IsValidStatusIndex(param0, statusIndex)) {
        return &param0->sortedPokedex.caughtStatusArray[statusIndex];
    }

    return NULL;
}

BOOL LegDex_PokedexSort_IsValidDisplayIndex(const PokedexSortData *param0, int displayIndex)
{
    if ((param0->sortedPokedex.numDisplayed > displayIndex) && (displayIndex >= 0)) {
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_PokedexSort_SetCurrentValues(PokedexSortData *param0, int displayIndex)
{
    if (LegDex_PokedexSort_IsValidDisplayIndex(param0, displayIndex)) {
        param0->sortedPokedex.currentDisplayIndex = displayIndex;

        LegDex_PokedexSort_SetCurrentStatusIndex(param0, param0->sortedPokedex.displayPokedex[param0->sortedPokedex.currentDisplayIndex]);
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_PokedexSort_TakeStep(PokedexSortData *param0, int step)
{
    if (LegDex_PokedexSort_IsValidStep(param0, step)) {
        param0->sortedPokedex.currentDisplayIndex += step;

        LegDex_PokedexSort_SetCurrentStatusIndex(param0, param0->sortedPokedex.displayPokedex[param0->sortedPokedex.currentDisplayIndex]);
        return TRUE;
    }

    return FALSE;
}

BOOL LegDex_PokedexSort_IsValidStep(PokedexSortData *param0, int step)
{
    if (LegDex_PokedexSort_IsValidDisplayIndex(param0, param0->sortedPokedex.currentDisplayIndex + step)) {
        return TRUE;
    }

    return FALSE;
}

int LegDex_PokedexSort_CurrentDisplayIndex(const PokedexSortData *param0)
{
    return param0->sortedPokedex.currentDisplayIndex;
}

int LegDex_PokedexSort_NumDisplayed(const PokedexSortData *param0)
{
    return param0->sortedPokedex.numDisplayed;
}

int LegDex_PokedexSort_DisplayIndexToStatusIndex(const PokedexSortData *param0, int displayIndex)
{
    return param0->sortedPokedex.displayPokedex[displayIndex];
}

void LegDex_PokedexSort_UpdateCurrentValues(PokedexSortData *param0)
{
    for (int displayIndex = 0; displayIndex < param0->sortedPokedex.numDisplayed; displayIndex++) {
        if (LegDex_PokedexSort_DisplayIndexToStatusIndex(param0, displayIndex) == LegDex_PokedexSort_CurrentStatusIndex(param0)) {
            LegDex_PokedexSort_SetCurrentValues(param0, displayIndex);
            break;
        }
    }
}

int LegDex_PokedexSort_NumEncountered(const PokedexSortData *param0)
{
    return param0->numEncountered;
}

int LegDex_PokedexSort_NumCaught(const PokedexSortData *param0)
{
    return param0->numCaught;
}

String *LegDex_PokedexSort_TrainerName(const PokedexSortData *param0)
{
    return param0->trainerName;
}

u32 LegDex_PokedexSort_TrainerGender(const PokedexSortData *param0)
{
    return param0->trainerGender;
}

BOOL LegDex_ov21_021D392C(const PokedexSortData *param0, int param1)
{
    int species = LegDex_PokedexSort_CurrentSpecies(param0);

    if (Pokedex_CanDetectLanguages(param0->pokedex) == 0) {
        return FALSE;
    }

    return Pokedex_IsLanguageObtained(param0->pokedex, species, param1);
}

BOOL LegDex_PokedexSort_CanDetectForms(const PokedexSortData *param0)
{
    return TRUE; // reference Pokédex: the forms page is always there
}

void LegDex_ov21_021D3960(PokedexSortData *param0)
{
    if (gSystem.touchHeld) {
        param0->unk_1758 = 0;
        return;
    }

    if (gSystem.pressedKeys) {
        if (param0->unk_1758 == 0) {
            param0->unk_1758 = 1;
        } else {
            param0->unk_1758 = 2;
        }
    }
}

u32 LegDex_ov21_021D3998(const PokedexSortData *param0)
{
    return param0->unk_1758;
}

static void FilterUnencountered(u16 *encounteredDex, int *caughtStatusLength, const Pokedex *pokedex, const u16 *fullDex, int pokedexLength)
{
    *caughtStatusLength = 0;

    for (int species = 0; species < pokedexLength; species++) {
        if (LegDex_IsListed(fullDex[species])) {
            encounteredDex[*caughtStatusLength] = fullDex[species];
            (*caughtStatusLength)++;
        }
    }
}

static void IntersectPokedexes(u16 *resultingPokedex, int *numResulting, const u16 *pokedex1, int dexLen1, const u16 *pokedex2, int dexLen2, BOOL keepUncaught, const Pokedex *pokedex)
{
    int dexIndex2;

    *numResulting = 0;

    for (int dexIndex1 = 0; dexIndex1 < dexLen1; dexIndex1++) {
        for (dexIndex2 = 0; dexIndex2 < dexLen2; dexIndex2++) {
            if (pokedex1[dexIndex1] == pokedex2[dexIndex2]) {
                if (keepUncaught == TRUE) {
                    break;
                } else {
                    if (LegDex_IsListed(pokedex1[dexIndex1])) {
                        break;
                    }
                }
            }
        }

        if (dexIndex2 < dexLen2) {
            resultingPokedex[*numResulting] = pokedex1[dexIndex1];
            (*numResulting)++;
        }
    }
}

static void UpdateCaughtStatus(SortedPokedex *sortedPokedex, const Pokedex *pokedex, const u16 *encounteredPokedex, int caughtStatusLength)
{
    sortedPokedex->caughtStatusLength = 0;

    for (int dexIndex = 0; dexIndex < caughtStatusLength; dexIndex++) {
        if (LegDex_IsListed(encounteredPokedex[dexIndex])) {
            sortedPokedex->caughtStatusArray[sortedPokedex->caughtStatusLength].caughtStatus = CS_CAUGHT;
        } else {
            sortedPokedex->caughtStatusArray[sortedPokedex->caughtStatusLength].caughtStatus = CS_ENCOUNTERED;
        }

        sortedPokedex->caughtStatusArray[sortedPokedex->caughtStatusLength].species = encounteredPokedex[dexIndex];
        sortedPokedex->caughtStatusLength++;
    }
}

static void PopulateDisplayPokedex_Blanks(SortedPokedex *sortedPokedex, const u16 *fullDex, int pokedexLength)
{
    int encounteredIndex = 0;
    sortedPokedex->numDisplayed = 0;

    for (int dexIndex = 0; dexIndex < pokedexLength; dexIndex++) {
        if (encounteredIndex < sortedPokedex->caughtStatusLength) {
            if (sortedPokedex->caughtStatusArray[encounteredIndex].species == fullDex[dexIndex]) {
                sortedPokedex->displayPokedex[sortedPokedex->numDisplayed] = encounteredIndex;
                encounteredIndex++;
                sortedPokedex->numDisplayed++;
            } else {
                sortedPokedex->displayPokedex[sortedPokedex->numDisplayed] = BLANKSPACE;
                sortedPokedex->numDisplayed++;
            }
        }
    }
}

static void PopulateDisplayPokedex(SortedPokedex *sortedPokedex)
{
    sortedPokedex->numDisplayed = 0;

    for (int encounteredIndex = 0; encounteredIndex < sortedPokedex->caughtStatusLength; encounteredIndex++) {
        sortedPokedex->displayPokedex[sortedPokedex->numDisplayed] = encounteredIndex;
        sortedPokedex->numDisplayed++;
    }
}

static u16 *PokedexFromNARC(enum HeapID heapID, int pokedexSort, int *pokedexLength)
{
    u32 pokedexSize;

    GF_ASSERT(PDSI_NUMSORTS > pokedexSort);

    enum NarcID pokedexDataNarcIndex = Pokedex_Data_NARC_Index();
    u16 *pokedexFromFile = LoadMemberFromNARC_OutFileSize(pokedexDataNarcIndex, NUMSTATFILES + LEGDEX_LISTS_OFFSET + pokedexSort, 0, heapID, 0, &pokedexSize);
    *pokedexLength = pokedexSize / (sizeof(u16));

    return pokedexFromFile;
}

static void DexSortOrder(int sortOrder, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex)
{
    u16 *pokedexFromFile;
    int pokedexLength;
    BOOL keepUncaught = FALSE;

    switch (sortOrder) {
    case SO_NUMERICAL:
        pokedexFromFile = NULL;
        break;
    case SO_ALPHABETICAL:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_ALPHABETICAL, &pokedexLength);
        keepUncaught = TRUE;
        break;
    case SO_HEAVIEST:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_HEAVIEST, &pokedexLength);
        break;
    case SO_LIGHTEST:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_LIGHTEST, &pokedexLength);
        break;
    case SO_TALLEST:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_TALLEST, &pokedexLength);
        break;
    case SO_SMALLEST:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_SMALLEST, &pokedexLength);
        break;
    default:
        GF_ASSERT(FALSE);
        break;
    }

    if (pokedexFromFile != NULL) {
        IntersectPokedexes(resultingPokedex, numResulting, pokedexFromFile, pokedexLength, encounteredPokedex, caughtStatusLength, keepUncaught, pokedex);
        Heap_Free(pokedexFromFile);
    } else {
        memcpy(resultingPokedex, encounteredPokedex, (sizeof(u16)) * caughtStatusLength);
        *numResulting = caughtStatusLength;
    }
}

static void FilterByName(int filterName, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex)
{
    u16 *pokedexFromFile;
    int pokedexLength;

    switch (filterName) {
    case FN_NONE:
        pokedexFromFile = NULL;
        break;
    case FN_ABC:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_ABC, &pokedexLength);
        break;
    case FN_DEF:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_DEF, &pokedexLength);
        break;
    case FN_GHI:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_GHI, &pokedexLength);
        break;
    case FN_JKL:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_JKL, &pokedexLength);
        break;
    case FN_MNO:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_MNO, &pokedexLength);
        break;
    case FN_PQR:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_PQR, &pokedexLength);
        break;
    case FN_STU:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_STU, &pokedexLength);
        break;
    case FN_VWX:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_VWX, &pokedexLength);
        break;
    case FN_YZ:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_YZ, &pokedexLength);
        break;
    default:
        GF_ASSERT(FALSE);
        break;
    }

    if (pokedexFromFile != NULL) {
        IntersectPokedexes(resultingPokedex, numResulting, encounteredPokedex, caughtStatusLength, pokedexFromFile, pokedexLength, TRUE, pokedex);
        Heap_Free(pokedexFromFile);
    } else {
        memcpy(resultingPokedex, encounteredPokedex, (sizeof(u16)) * caughtStatusLength);
        *numResulting = caughtStatusLength;
    }
}

static void FilterByType(int typeFilter, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex)
{
    u16 *pokedexFromFile;
    int pokedexLength;

    switch (typeFilter) {
    case FT_NONE:
        pokedexFromFile = NULL;
        break;
    case FT_NORMAL:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_NORMAL, &pokedexLength);
        break;
    case FT_FIGHTING:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_FIGHTING, &pokedexLength);
        break;
    case FT_FLYING:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_FLYING, &pokedexLength);
        break;
    case FT_POISON:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_POISON, &pokedexLength);
        break;
    case FT_GROUND:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_GROUND, &pokedexLength);
        break;
    case FT_ROCK:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_ROCK, &pokedexLength);
        break;
    case FT_BUG:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_BUG, &pokedexLength);
        break;
    case FT_GHOST:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_GHOST, &pokedexLength);
        break;
    case FT_STEEL:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_STEEL, &pokedexLength);
        break;
    case FT_FIRE:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_FIRE, &pokedexLength);
        break;
    case FT_WATER:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_WATER, &pokedexLength);
        break;
    case FT_GRASS:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_GRASS, &pokedexLength);
        break;
    case FT_ELECTRIC:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_ELECTRIC, &pokedexLength);
        break;
    case FT_PSYCHIC:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_PSYCHIC, &pokedexLength);
        break;
    case FT_ICE:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_ICE, &pokedexLength);
        break;
    case FT_DRAGON:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_DRAGON, &pokedexLength);
        break;
    case FT_DARK:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_DARK, &pokedexLength);
        break;
    default:
        GF_ASSERT(FALSE);
        break;
    }

    if (pokedexFromFile != NULL) {
        IntersectPokedexes(resultingPokedex, numResulting, encounteredPokedex, caughtStatusLength, pokedexFromFile, pokedexLength, FALSE, pokedex);
        Heap_Free(pokedexFromFile);
    } else {
        memcpy(resultingPokedex, encounteredPokedex, (sizeof(u16)) * caughtStatusLength);
        *numResulting = caughtStatusLength;
    }
}

static void FilterByForm(int filterForm, u16 *resultingPokedex, int *numResulting, const u16 *encounteredPokedex, int caughtStatusLength, enum HeapID heapID, const Pokedex *pokedex)
{
    u16 *pokedexFromFile;
    int pokedexLength;

    switch (filterForm) {
    case FF_NONE:
        pokedexFromFile = NULL;
        break;
    case FF_QUADRUPED:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_QUADRUPED, &pokedexLength);
        break;
    case FF_BIPEDALTAILLESS:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_BIPEDALTAILLESS, &pokedexLength);
        break;
    case FF_BIPEDALTAILED:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_BIPEDALTAILED, &pokedexLength);
        break;
    case FF_SERPENTINE:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_SERPENTINE, &pokedexLength);
        break;
    case FF_MULTIWINGED:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_MULTIWINGED, &pokedexLength);
        break;
    case FF_WINGED:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_WINGED, &pokedexLength);
        break;
    case FF_INSECTOID:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_INSECTOID, &pokedexLength);
        break;
    case FF_HEADBASE:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_HEADBASE, &pokedexLength);
        break;
    case FF_HEADARMS:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_HEADARMS, &pokedexLength);
        break;
    case FF_HEADLEGS:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_HEADLEGS, &pokedexLength);
        break;
    case FF_TENTACLES:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_TENTACLES, &pokedexLength);
        break;
    case FF_FINS:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_FINS, &pokedexLength);
        break;
    case FF_HEAD:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_HEAD, &pokedexLength);
        break;
    case FF_MULTIBODY:
        pokedexFromFile = PokedexFromNARC(heapID, PDSI_MULTIBODY, &pokedexLength);
        break;
    default:
        GF_ASSERT(FALSE);
        break;
    }

    if (pokedexFromFile != NULL) {
        IntersectPokedexes(resultingPokedex, numResulting, encounteredPokedex, caughtStatusLength, pokedexFromFile, pokedexLength, TRUE, pokedex);
        Heap_Free(pokedexFromFile);
    } else {
        memcpy(resultingPokedex, encounteredPokedex, (sizeof(u16)) * caughtStatusLength);
        *numResulting = caughtStatusLength;
    }
}

static void NumEncounteredAndCaught(SortedPokedex *sortedPokedex, int *caughtStatusLength, int *numCaught)
{
    *caughtStatusLength = 0;
    *numCaught = 0;

    for (int statusIndex = 0; statusIndex < sortedPokedex->caughtStatusLength; statusIndex++) {
        if (sortedPokedex->caughtStatusArray[statusIndex].caughtStatus == CS_CAUGHT) {
            (*numCaught)++;
        }

        (*caughtStatusLength)++;
    }
}

static const LegDexForm *LegDex_FindExtraForm(u32 species, int formIndex)
{
    for (int i = 0; i < (int)NELEMS(sLegDexExtraForms); i++) {
        if (sLegDexExtraForms[i].species == species) {
            if (formIndex == 0) {
                return &sLegDexExtraForms[i];
            }

            formIndex--;
        }
    }

    return NULL;
}

int LegDex_ExtraFormCount(u32 species)
{
    int count = 0;

    for (int i = 0; i < (int)NELEMS(sLegDexExtraForms); i++) {
        if (sLegDexExtraForms[i].species == species) {
            count++;
        }
    }

    return count;
}

int LegDex_ExtraForm(u32 species, int formIndex)
{
    const LegDexForm *entry = LegDex_FindExtraForm(species, formIndex);
    return entry != NULL ? entry->form : 0;
}

int LegDex_ExtraFormLabel(u32 species, int formIndex)
{
    const LegDexForm *entry = LegDex_FindExtraForm(species, formIndex);
    return entry != NULL ? entry->label : LegDexSections_Text_Unknown;
}
