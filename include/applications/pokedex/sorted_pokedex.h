#ifndef POKEPLATINUM_SORTEDPOKEDEX_H
#define POKEPLATINUM_SORTEDPOKEDEX_H

#include "constants/species.h"

#include "applications/pokedex/species_caught_status.h"

typedef struct {
    SpeciesCaughtStatus caughtStatusArray[POKEDEX_SPECIES_COUNT];
    int currentStatusIndex;
    int caughtStatusLength;
    int displayPokedex[POKEDEX_SPECIES_COUNT]; // contains index for caughtStatusArray, not species
    int currentDisplayIndex;
    int numDisplayed;
} SortedPokedex;

#endif // POKEPLATINUM_SORTEDPOKEDEX_H
