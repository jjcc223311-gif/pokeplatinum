#ifndef POKEPLATINUM_CONSTANTS_SPECIES_H
#define POKEPLATINUM_CONSTANTS_SPECIES_H

#include "generated/species.h"

#define MAX_SPECIES        SPECIES_BAD_EGG
#define NATIONAL_DEX_COUNT (MAX_SPECIES - 2) // every real species, including Gen 5

// The ORIGINAL Pokedex (and the save data sized by it) only covers #1-493. Gen 5 species are not
// recorded there (they will get the Legendary Pokedex), so its save layout, completion goal and
// listings stay exactly as in vanilla and old saves keep loading.
#define POKEDEX_SPECIES_COUNT 493
#define POKEDEX_MAX_SPECIES   (POKEDEX_SPECIES_COUNT + 2) // vanilla MAX_SPECIES (save arrays)

#endif // POKEPLATINUM_CONSTANTS_SPECIES_H
