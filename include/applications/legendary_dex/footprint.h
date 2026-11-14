#ifndef POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_FOOTPRINT_H
#define POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_FOOTPRINT_H

#include "constants/narc.h"
#include "constants/species.h"

enum NarcID LegDex_GetPokedexFootprintsNarcID(void);
int LegDex_GetSpeciesFootprintTiles(enum Species species);
int LegDex_GetSharedFootprintPalette(void);
int LegDex_GetSharedFootprintCells(void);
int LegDex_GetSharedFootprintAnims(void);

#endif // POKEPLATINUM_LEGDEX_APPLICATIONS_POKEDEX_FOOTPRINT_H
