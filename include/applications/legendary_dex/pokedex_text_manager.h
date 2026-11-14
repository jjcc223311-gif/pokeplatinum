#ifndef POKEPLATINUM_LEGDEX_POKEDEX_TEXT_MANAGER_H
#define POKEPLATINUM_LEGDEX_POKEDEX_TEXT_MANAGER_H

#include <nnsys.h>

#include "generated/text_banks.h"

#include "struct_decls/font_oam.h"
#include "struct_decls/struct_02012744_decl.h"

#include "bg_window.h"
#include "char_transfer.h"
#include "heap.h"
#include "sprite.h"
#include "string_gf.h"

typedef struct PokedexTextData {
    FontOAM *fontOAM;
    CharTransferAllocation allocation;
} PokedexTextData;

typedef struct PokedexTextManager {
    UnkStruct_02012744 *unk_00;
    SpriteList *spriteList;
    BgConfig *bgConfig;
    PokedexTextData *textData;
    int numTextData;
    enum HeapID heapID;
} PokedexTextManager;

typedef struct PokedexTextManagerTemplate {
    SpriteList *spriteList;
    BgConfig *bgConfig;
    int numTextData;
    enum HeapID heapID;
} PokedexTextManagerTemplate;

typedef struct PokedexDisplayBox {
    PokedexTextManager *textMan;
    const Window *window;
    const NNSG2dImagePaletteProxy *paletteProxy;
    const Sprite *sprite;
    int x;
    int y;
    int spriteResourcePriority;
    int spriteListPriority;
    enum NNS_G2D_VRAM_TYPE vramType;
    enum HeapID heapID;
} PokedexDisplayBox;

PokedexTextManager *LegDex_PokedexTextManager_New(const PokedexTextManagerTemplate *textManTemplate);
void LegDex_PokedexTextManager_Free(PokedexTextManager *textMan);
PokedexTextData *LegDex_PokedexTextManager_NextTextData(const PokedexDisplayBox *displayBox);
PokedexTextData *LegDex_PokedexTextManager_NextTextDataNew(const PokedexDisplayBox *displayBox, int size);
void LegDex_PokedexTextManager_FreeTextData(PokedexTextData *textData);
void LegDex_PokedexTextManager_FreeAllTextData(PokedexTextManager *textMan);
Window *LegDex_PokedexTextManager_NewWindow(PokedexTextManager *textMan, int width, int height);
void LegDex_PokedexTextManager_FreeWindow(Window *window);
u32 LegDex_PokedexTextManager_DisplayMessage(PokedexTextManager *textMan, Window *window, u32 bankID, u32 entryID, int xOffset, int yOffset);
void LegDex_PokedexTextManager_DisplayMessageTopRight(PokedexTextManager *textMan, Window *window, u32 bankID, u32 entryID);
void LegDex_PokedexTextManager_DisplayString(PokedexTextManager *textMan, Window *window, String *string, int xOffset, int yOffset);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_TEXT_MANAGER_H
