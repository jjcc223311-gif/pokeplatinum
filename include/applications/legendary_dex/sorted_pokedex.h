#ifndef POKEPLATINUM_LEGDEX_SORTEDPOKEDEX_H
#define POKEPLATINUM_LEGDEX_SORTEDPOKEDEX_H

#include "constants/species.h"

#include "applications/legendary_dex/species_caught_status.h"

// The Legendary Pokédex is a reference: it lists every species, #1-649
#define LEGDEX_SPECIES_COUNT NATIONAL_DEX_COUNT

typedef struct {
    SpeciesCaughtStatus caughtStatusArray[LEGDEX_SPECIES_COUNT];
    int currentStatusIndex;
    int caughtStatusLength;
    int displayPokedex[LEGDEX_SPECIES_COUNT]; // contains index for caughtStatusArray, not species
    int currentDisplayIndex;
    int numDisplayed;
} SortedPokedex;

#endif // POKEPLATINUM_LEGDEX_SORTEDPOKEDEX_H
