#include "applications/legendary_dex/footprint.h"

#include "res/pokemon/pokefoot.naix"

enum NarcID LegDex_GetPokedexFootprintsNarcID(void)
{
    return NARC_INDEX_POKETOOL__POKEFOOT__POKEFOOT;
}

int LegDex_GetSpeciesFootprintTiles(enum Species species)
{
    return none_footprint_NCGR_lz + species;
}

int LegDex_GetSharedFootprintPalette(void)
{
    return footprint_NCLR;
}

int LegDex_GetSharedFootprintCells(void)
{
    return footprint_cell_NCER_lz;
}

int LegDex_GetSharedFootprintAnims(void)
{
    return footprint_anim_NANR_lz;
}
