#ifndef POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_MANAGER_H
#define POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_MANAGER_H

#include "heap.h"

typedef struct PokedexGraphicsManager {
    int state;
    enum HeapID heapID;
    void *pageGraphics;
} PokedexGraphicsManager;

#endif // POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_MANAGER_H
