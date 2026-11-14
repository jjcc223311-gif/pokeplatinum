#ifndef POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_H
#define POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_H

#include <nitro.h>

#include "constants/species.h"

#include "applications/legendary_dex/pokedex_panel.h"
#include "applications/legendary_dex/pokedex_text_manager.h"

#include "graphics.h"
#include "heap.h"
#include "narc.h"
#include "pokemon_sprite.h"
#include "software_sprite.h"
#include "sprite_resource.h"
#include "sprite_util.h"
#include "sys_task_manager.h"

typedef struct PokedexSpeciesLabel {
    Sprite *nameTag; // displays caughtIcon, dex number, and name
    Sprite *caughtIcon;
    PokedexTextData *textData;
    SpriteResource *spriteResource[MAX_SPRITE_RESOURCE_GEN4];
    VecFx32 dummy;
    enum Species species;
    BOOL isNationalDex;
} PokedexSpeciesLabel;

typedef struct PokedexBlendTransition {
    BOOL isSubscreen;
    GXBlendPlaneMask plane1;
    GXBlendPlaneMask plane2;
    int startBackgroundBrightness;
    int deltaBackgroundBrightness;
    int startSpriteBrightness;
    int deltaSpriteBrightness;
    int numSteps;
    int step;
} PokedexBlendTransition;

typedef struct PokedexCursorGraphics {
    Sprite *sprite[MAX_SPRITE_RESOURCE_GEN4];
    SpriteResource *spriteResource[MAX_SPRITE_RESOURCE_GEN4];
    int x;
    int y;
    int width;
    int height;
    BOOL isStaticSize;
    int scale;
} PokedexCursorGraphics;

typedef struct SpriteTransformation {
    int currentX;
    int currentY;
    int startX;
    int startY;
    int deltaX;
    int deltaY;
    int step;
    int numSteps;
} SpriteTransformation;

typedef struct PokedexCursorManager {
    PokedexCursorGraphics *cursorGraphics;
    SpriteTransformation centerPoint;
    SpriteTransformation size;
    int x;
    int y;
    int width;
    int height;
    BOOL isMoving;
} PokedexCursorManager;

enum FormPageSpriteIndex {
    SPRITEINDEX_CURRENT_FRONT,
    SPRITEINDEX_CURRENT_BACK,
    SPRITEINDEX_PREVIOUS_FRONT,
    SPRITEINDEX_PREVIOUS_BACK,
    NUM_VISIBLE_SPRITES,
};

typedef struct PokedexGraphicData {
    BgConfig *bgConfig;
    Window window;
    G2dRenderer g2Renderer;
    SpriteList *spriteList;
    SpriteResourceCollection *spriteResourceCollection[MAX_SPRITE_RESOURCE_GEN4];
    PokedexTextManager *textMan;
    PokemonSpriteManager *spriteMan;
    PokemonSprite *pokemonSprite[NUM_VISIBLE_SPRITES];
    SoftwareSpriteManager *unk_164;
    PokedexBlendTransition blendMain;
    PokedexBlendTransition blendSub;
    PokedexSpeciesLabel pokedexSpeciesLabel;
    PokedexCursorGraphics cursorGraphics;
    PokedexCursorManager cursorMan;
    SysTask *cursorPulse;
    SysTask *cursorTransorm;
    NARC *pokedexGraphics;
} PokedexGraphicData;

void LegDex_PokedexGraphics_Init(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
void LegDex_PokedexGraphics_Free(PokedexGraphicData *pokedexGraphicData);
void LegDex_PokemonGraphics_UpdateSprites(PokedexGraphicData *pokedexGraphicData);
void LegDex_PokemonGraphics_UpdateCharAndPltt(PokedexGraphicData *pokedexGraphicData);
void LegDex_PokemonGraphics_SetCharCenterXY(PokedexGraphicData *pokedexGraphicData, int x, int y);
PokemonSprite *LegDex_PokemonGraphics_GetPokemonChar(const PokedexGraphicData *pokedexGraphicData);
void LegDex_PokedexGraphics_SetPokemonCharHide(const PokedexGraphicData *pokedexGraphicData, BOOL unhidden);
void LegDex_PokedexGraphics_LoadPokemonSprite(PokedexGraphicData *pokedexGraphicData, enum Species species, int gender, int face, int shiny, u8 form, u32 personality, int x, int y, int spriteIndex);
void LegDex_PokemonGraphics_SetSpriteCenterXY(PokedexGraphicData *pokedexGraphicData, int x, int y, int spriteIndex);
void LegDex_PokemonGraphics_GetSpriteCenterXY(PokedexGraphicData *pokedexGraphicData, int *x, int *y, int spriteIndex);
PokemonSprite *LegDex_PokedexGraphics_GetPokemonSprite(const PokedexGraphicData *pokedexGraphicData, int spriteIndex);
void LegDex_PokedexGraphics_SetPokemonSpriteHide(const PokedexGraphicData *pokedexGraphicData, BOOL unhidden, int spriteIndex);
Sprite *LegDex_PokedexGraphics_GetNameTag(const PokedexGraphicData *pokedexGraphicData);
Sprite *LegDex_PokedexGraphics_GetCaughtIcon(const PokedexGraphicData *pokedexGraphicData);
void LegDex_PokedexGraphics_UpdatePokedexSpeciesLabel(PokedexGraphicData *pokedexGraphicData, PokedexDisplayBox *displayBox, int size, enum Species species, BOOL isNationalDex);
void LegDex_PokedexGraphics_UpdateSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel, PokedexDisplayBox *displayBox, int size, enum Species species, BOOL isNationalDex);
SpriteResource *LegDex_PokedexGraphics_GetSpeciesLabelSpriteResource(const PokedexGraphicData *pokedexGraphicData, enum SpriteResourceType spriteResourceType);
void LegDex_PokedexGraphics_SetSpeciesLabelGXOamMode(const PokedexGraphicData *pokedexGraphicData, GXOamMode mode);
void LegDex_PokedexGraphics_SetSpeciesLabelPriority(const PokedexGraphicData *pokedexGraphicData, int priority);
void LegDex_PokedexGraphics_SetPokedexSpeciesLabelDraw(const PokedexGraphicData *pokedexGraphicData, BOOL draw);
void LegDex_PokedexGraphics_InitBlendTransition(PokedexBlendTransition *blendTransition, u8 numSteps, int startBackgroundBrightness, int endBackgroundBrightness, int startSpriteBrightness, int endSpriteBrightness, GXBlendPlaneMask plane1, GXBlendPlaneMask plane2, BOOL isSubscreen);
BOOL LegDex_PokedexGraphics_TakeBlendTransitionStep(PokedexBlendTransition *blendTransition);
int LegDex_PokedexGraphics_BlendSprites(PokedexBlendTransition *blendTransition);
int LegDex_PokedexGraphics_BlendScreen(PokedexBlendTransition *blendTransition);
BOOL LegDex_PokedexGraphics_BlendTransitionComplete(PokedexBlendTransition *blendTransition);
void LegDex_PokedexGraphics_BlendPokemonChar(const PokedexGraphicData *pokedexGraphicData, PokedexBlendTransition *blendTransition);
void LegDex_PokedexGraphics_BlendPokemonSprite(const PokedexGraphicData *pokedexGraphicData, PokedexBlendTransition *blendTransition, int spriteIndex);
void LegDex_PokedexGraphics_CurrentButtonTransformation(const PokedexPanelData *pokedexPanelData, PokedexGraphicData *pokedexGraphicData);
void LegDex_PokedexGraphics_TransformCursor(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height);
void LegDex_PokedexGraphics_SetDrawCursor(PokedexCursorGraphics *pokedexCursorGraphics, BOOL draw);
BOOL LegDex_PokedexGraphics_GetDrawCursor(PokedexCursorGraphics *pokedexCursorGraphics);
void LegDex_PokedexGraphics_SetStaticCursorSize(PokedexCursorGraphics *pokedexCursorGraphics, BOOL isStaticSize);
void LegDex_PokedexGraphics_GoToCurrentButton(const PokedexPanelData *pokedexPanelData, PokedexGraphicData *pokedexGraphicData);
void LegDex_PokedexGraphics_SetCursorPosAndSize(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height);
void LegDex_PokedexGraphics_InitTransformation(SpriteTransformation *spriteTransformation, int startX, int endX, int startY, int endY, int numSteps);
BOOL LegDex_PokedexGraphics_TakeTransformStep(SpriteTransformation *spriteTransformation);
NARC *LegDex_PokedexGraphics_GetNARC(PokedexGraphicData *pokedexGraphicData);
u32 LegDex_PokedexGraphics_LoadGraphicNarcCharacterData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BgConfig *bgConfig, u32 bgLayer, u32 tileStart, u32 size, BOOL isCompressed, enum HeapID heapID);
void LegDex_PokedexGraphics_LoadGraphicNarcPaletteData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, enum PaletteLoadLocation loadLocation, u32 offset, u32 szByte, enum HeapID heapID);
void *LegDex_PokedexGraphics_GetGraphicNarcTilemapData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BOOL isCompressed, NNSG2dScreenData **screenData, enum HeapID heapID);
void *LegDex_PokedexGraphics_GetGraphicNarcPaletteData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, NNSG2dPaletteData **paletteData, enum HeapID heapID);
void *LegDex_PokedexGraphics_GetGraphicNarcCharacterData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BOOL isCompressed, NNSG2dCharacterData **characterData, enum HeapID heapID);
void LegDex_PokedexGraphics_InitSpeciesLabelGraphics(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteResourceCollection **spriteResourceCollection, enum HeapID heapID, NARC *narc);
void LegDex_PokedexGraphics_FreeSpeciesLabelGraphics(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteResourceCollection **spriteResourceCollection);
void LegDex_PokedexGraphics_NewSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteList *spriteList, SpriteResourceCollection **spriteResourceCollection, enum HeapID heapID, int headerPriority);
void LegDex_PokedexGraphics_FreeSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel);
void LegDex_PokedexGraphics_SetSpeciesLabelDraw(PokedexSpeciesLabel *pokedexSpeciesLabel, BOOL draw);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_GRAPHICS_H
