#ifndef POKEPLATINUM_LEGDEX_POKEDEX_TEXT_H
#define POKEPLATINUM_LEGDEX_POKEDEX_TEXT_H

#include "constants/heap.h"

#include "string_gf.h"

void LegDex_PokedexText_Free(String *string);
int LegDex_PokedexText_ForeignLanguage(int languageIndex);
String *LegDex_PokedexText_NameNumber(int species, int language, enum HeapID heapID);
String *LegDex_PokedexText_Category(int species, int language, enum HeapID heapID);
String *LegDex_PokedexText_DexEntry(int species, int language, int entryOffset, enum HeapID heapID);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_TEXT_H
