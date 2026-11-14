#include "applications/legendary_dex/pokedex_graphics.h"

#include <string.h>

#include "bg_window.h"
#include "font.h"
#include "gx_layers.h"
#include "pokemon.h"
#include "software_sprite.h"
#include "sprite_transfer.h"
#include "sys_task.h"
#include "unk_02012744.h"

#include "res/graphics/pokedex/zukan.naix"

static void InitBackgrounds(BgConfig *bgConfig, enum HeapID heapID);
static void FreeBackgrounds(BgConfig *bgConfig);
static void InitWindow(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreeWindow(PokedexGraphicData *pokedexGraphicData);
static void NewPokemonSprite(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreePokemonSprite(PokedexGraphicData *pokedexGraphicData);
static void InitSpeciesLabelGraphics(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreeSpeciesLabelGraphics(PokedexGraphicData *pokedexGraphicData);
static void InitSpeciesLabel(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreeSpeciesLabel(PokedexGraphicData *pokedexGraphicData);
static void InitCursorGraphics(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreeCursorGraphics(PokedexGraphicData *pokedexGraphicData);
static void InitCursor(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID);
static void FreeCursor(PokedexGraphicData *pokedexGraphicData);
static void StartCursorPulse(PokedexGraphicData *pokedexGraphicData);
static void EndCursorPulse(PokedexGraphicData *pokedexGraphicData);
static void PulseCursor(SysTask *sysTask, void *data);
static void SetCursorSpritePos(PokedexCursorGraphics *pokedexCursorGraphics, int x, int y, int width, int height);
static void StartCursorTransform(PokedexGraphicData *pokedexGraphicData);
static void EndCursorTransform(PokedexGraphicData *pokedexGraphicData);
static void InsitigateCursorTransformation(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height);
static void TransformCursor(SysTask *sysTask, void *data);

void LegDex_PokedexGraphics_Init(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    GraphicsModes graphicsModes;
    PokedexTextManagerTemplate textManTemplate;

    pokedexGraphicData->pokedexGraphics = NARC_ctor(NARC_INDEX_RESOURCE__ENG__ZUKAN__ZUKAN, heapID);
    pokedexGraphicData->bgConfig = BgConfig_New(heapID);

    graphicsModes.displayMode = GX_DISPMODE_GRAPHICS;
    graphicsModes.mainBgMode = GX_BGMODE_0;
    graphicsModes.subBgMode = GX_BGMODE_1;
    graphicsModes.bg0As2DOr3D = GX_BG0_AS_3D;

    SetAllGraphicsModes(&graphicsModes);

    InitBackgrounds(pokedexGraphicData->bgConfig, heapID);
    InitWindow(pokedexGraphicData, heapID);

    pokedexGraphicData->spriteList = SpriteList_InitRendering(128, &pokedexGraphicData->g2Renderer, heapID);
    pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR] = SpriteResourceCollection_New(32, SPRITE_RESOURCE_CHAR, heapID);
    pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT] = SpriteResourceCollection_New(32, SPRITE_RESOURCE_PLTT, heapID);
    pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL] = SpriteResourceCollection_New(32, SPRITE_RESOURCE_CELL, heapID);
    pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM] = SpriteResourceCollection_New(32, SPRITE_RESOURCE_ANIM, heapID);

    GXLayers_EngineAToggleLayers(GX_PLANEMASK_OBJ, 1);
    GXLayers_EngineBToggleLayers(GX_PLANEMASK_OBJ, 1);

    textManTemplate.spriteList = pokedexGraphicData->spriteList;
    textManTemplate.bgConfig = pokedexGraphicData->bgConfig;
    textManTemplate.numTextData = 16;
    textManTemplate.heapID = heapID;

    pokedexGraphicData->textMan = LegDex_PokedexTextManager_New(&textManTemplate);

    Font_InitManager(FONT_SUBSCREEN, heapID);

    NewPokemonSprite(pokedexGraphicData, heapID);
    InitSpeciesLabelGraphics(pokedexGraphicData, heapID);
    InitSpeciesLabel(pokedexGraphicData, heapID);
    InitCursorGraphics(pokedexGraphicData, heapID);
    InitCursor(pokedexGraphicData, heapID);
}

void LegDex_PokedexGraphics_Free(PokedexGraphicData *pokedexGraphicData)
{
    FreeSpeciesLabel(pokedexGraphicData);
    FreeSpeciesLabelGraphics(pokedexGraphicData);
    FreeCursor(pokedexGraphicData);
    FreeCursorGraphics(pokedexGraphicData);
    FreeWindow(pokedexGraphicData);
    FreeBackgrounds(pokedexGraphicData->bgConfig);

    Heap_Free(pokedexGraphicData->bgConfig);
    SpriteList_Delete(pokedexGraphicData->spriteList);
    SpriteResourceCollection_Delete(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR]);
    SpriteResourceCollection_Delete(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT]);
    SpriteResourceCollection_Delete(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL]);
    SpriteResourceCollection_Delete(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM]);

    LegDex_PokedexTextManager_Free(pokedexGraphicData->textMan);
    Font_Free(FONT_SUBSCREEN);
    FreePokemonSprite(pokedexGraphicData);
    NARC_dtor(pokedexGraphicData->pokedexGraphics);

    memset(pokedexGraphicData, 0, sizeof(PokedexGraphicData));
}

void LegDex_PokemonGraphics_UpdateSprites(PokedexGraphicData *pokedexGraphicData)
{
    SpriteList_Update(pokedexGraphicData->spriteList);

    NNS_G2dSetupSoftwareSpriteCamera();

    PokemonSpriteManager_DrawSprites(pokedexGraphicData->spriteMan);
    SoftwareSpriteManager_DrawVisible(pokedexGraphicData->unk_164);
}

void LegDex_PokemonGraphics_UpdateCharAndPltt(PokedexGraphicData *pokedexGraphicData)
{
    Bg_RunScheduledUpdates(pokedexGraphicData->bgConfig);
    PokemonSpriteManager_UpdateCharAndPltt(pokedexGraphicData->spriteMan);
}

void LegDex_PokemonGraphics_SetCharCenterXY(PokedexGraphicData *pokedexGraphicData, int x, int y)
{
    LegDex_PokemonGraphics_SetSpriteCenterXY(pokedexGraphicData, x, y, SPRITE_RESOURCE_CHAR);
}

PokemonSprite *LegDex_PokemonGraphics_GetPokemonChar(const PokedexGraphicData *pokedexGraphicData)
{
    return LegDex_PokedexGraphics_GetPokemonSprite(pokedexGraphicData, SPRITE_RESOURCE_CHAR);
}

void LegDex_PokedexGraphics_SetPokemonCharHide(const PokedexGraphicData *pokedexGraphicData, BOOL unhidden)
{
    LegDex_PokedexGraphics_SetPokemonSpriteHide(pokedexGraphicData, unhidden, SPRITE_RESOURCE_CHAR);
}

void LegDex_PokedexGraphics_LoadPokemonSprite(PokedexGraphicData *pokedexGraphicData, enum Species species, int gender, int face, int shiny, u8 form, u32 personality, int x, int y, int spriteIndex)
{
    PokemonSpriteTemplate spriteTemplate;
    s16 yOffset;

    if (pokedexGraphicData->pokemonSprite[spriteIndex]) {
        PokemonSprite_Delete(pokedexGraphicData->pokemonSprite[spriteIndex]);
    }

    if (gender == -1) {
        gender = Pokemon_GetGenderOf(species, 0);
    }

    BuildPokemonSpriteTemplate(&spriteTemplate, species, gender, face, shiny, form, personality);

    if (face == 0) {
        yOffset = LoadPokemonSpriteYOffset(species, gender, face, form, personality);
        yOffset += 0;
    } else {
        yOffset = 0;
    }

    pokedexGraphicData->pokemonSprite[spriteIndex] = PokemonSpriteManager_CreateSprite(pokedexGraphicData->spriteMan, &spriteTemplate, x, y + yOffset, 0, 0, NULL, NULL);
}

void LegDex_PokemonGraphics_SetSpriteCenterXY(PokedexGraphicData *pokedexGraphicData, int x, int y, int spriteIndex)
{
    PokemonSprite_SetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_X_CENTER, x);
    PokemonSprite_SetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_Y_CENTER, y);
}

void LegDex_PokemonGraphics_GetSpriteCenterXY(PokedexGraphicData *pokedexGraphicData, int *x, int *y, int spriteIndex)
{
    *x = PokemonSprite_GetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_X_CENTER);
    *y = PokemonSprite_GetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_Y_CENTER);
}

PokemonSprite *LegDex_PokedexGraphics_GetPokemonSprite(const PokedexGraphicData *pokedexGraphicData, int spriteIndex)
{
    return pokedexGraphicData->pokemonSprite[spriteIndex];
}

void LegDex_PokedexGraphics_SetPokemonSpriteHide(const PokedexGraphicData *pokedexGraphicData, BOOL unhidden, int spriteIndex)
{
    if (pokedexGraphicData->pokemonSprite[spriteIndex] == NULL) {
        return;
    }

    if (unhidden == TRUE) {
        PokemonSprite_SetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_HIDE, FALSE);
    } else {
        PokemonSprite_SetAttribute(pokedexGraphicData->pokemonSprite[spriteIndex], MON_SPRITE_HIDE, TRUE);
    }
}

Sprite *LegDex_PokedexGraphics_GetNameTag(const PokedexGraphicData *pokedexGraphicData)
{
    GF_ASSERT(pokedexGraphicData->pokedexSpeciesLabel.nameTag);
    return pokedexGraphicData->pokedexSpeciesLabel.nameTag;
}

Sprite *LegDex_PokedexGraphics_GetCaughtIcon(const PokedexGraphicData *pokedexGraphicData)
{
    GF_ASSERT(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon);
    return pokedexGraphicData->pokedexSpeciesLabel.caughtIcon;
}

void LegDex_PokedexGraphics_UpdatePokedexSpeciesLabel(PokedexGraphicData *pokedexGraphicData, PokedexDisplayBox *displayBox, int size, enum Species species, BOOL isNationalDex)
{
    LegDex_PokedexGraphics_UpdateSpeciesLabel(&pokedexGraphicData->pokedexSpeciesLabel, displayBox, size, species, isNationalDex);
}

void LegDex_PokedexGraphics_UpdateSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel, PokedexDisplayBox *displayBox, int size, enum Species species, BOOL isNationalDex)
{
    if (species == pokedexSpeciesLabel->species && isNationalDex == pokedexSpeciesLabel->isNationalDex) {
        sub_020129D0(pokedexSpeciesLabel->textData->fontOAM, TRUE);
        return;
    } else {
        pokedexSpeciesLabel->species = species;
        pokedexSpeciesLabel->isNationalDex = isNationalDex;
    }

    if (pokedexSpeciesLabel->textData) {
        LegDex_PokedexTextManager_FreeTextData(pokedexSpeciesLabel->textData);
    }

    if (size != 0) {
        pokedexSpeciesLabel->textData = LegDex_PokedexTextManager_NextTextDataNew(displayBox, size);
    } else {
        pokedexSpeciesLabel->textData = LegDex_PokedexTextManager_NextTextData(displayBox);
    }
}

SpriteResource *LegDex_PokedexGraphics_GetSpeciesLabelSpriteResource(const PokedexGraphicData *pokedexGraphicData, enum SpriteResourceType spriteResourceType)
{
    GF_ASSERT(spriteResourceType <= 3);
    return pokedexGraphicData->pokedexSpeciesLabel.spriteResource[spriteResourceType];
}

void LegDex_PokedexGraphics_SetSpeciesLabelGXOamMode(const PokedexGraphicData *pokedexGraphicData, GXOamMode mode)
{
    Sprite_SetExplicitOAMMode(pokedexGraphicData->pokedexSpeciesLabel.nameTag, mode);
    Sprite_SetExplicitOAMMode(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon, mode);
    sub_02012AF0(pokedexGraphicData->pokedexSpeciesLabel.textData->fontOAM, mode);
}

void LegDex_PokedexGraphics_SetSpeciesLabelPriority(const PokedexGraphicData *pokedexGraphicData, int priority)
{
    Sprite_SetExplicitPriority(pokedexGraphicData->pokedexSpeciesLabel.nameTag, priority);
    Sprite_SetExplicitPriority(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon, priority);
    sub_02012A00(pokedexGraphicData->pokedexSpeciesLabel.textData->fontOAM, priority);
}

void LegDex_PokedexGraphics_SetPokedexSpeciesLabelDraw(const PokedexGraphicData *pokedexGraphicData, BOOL draw)
{
    if (pokedexGraphicData->pokedexSpeciesLabel.nameTag) {
        Sprite_SetDrawFlag(pokedexGraphicData->pokedexSpeciesLabel.nameTag, draw);
    }

    if (pokedexGraphicData->pokedexSpeciesLabel.caughtIcon) {
        Sprite_SetDrawFlag(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon, draw);
    }

    if (pokedexGraphicData->pokedexSpeciesLabel.textData->fontOAM) {
        sub_020129D0(pokedexGraphicData->pokedexSpeciesLabel.textData->fontOAM, draw);
    }
}

void LegDex_PokedexGraphics_InitBlendTransition(PokedexBlendTransition *blendTransition, u8 numSteps, int startBackgroundBrightness, int endBackgroundBrightness, int startSpriteBrightness, int endSpriteBrightness, GXBlendPlaneMask plane1, GXBlendPlaneMask plane2, BOOL isSubscreen)
{
    blendTransition->isSubscreen = isSubscreen;
    blendTransition->plane1 = plane1;
    blendTransition->plane2 = plane2 | GX_BLEND_PLANEMASK_BD;
    blendTransition->startBackgroundBrightness = startBackgroundBrightness;
    blendTransition->deltaBackgroundBrightness = endBackgroundBrightness - startBackgroundBrightness;
    blendTransition->startSpriteBrightness = startSpriteBrightness;
    blendTransition->deltaSpriteBrightness = endSpriteBrightness - startSpriteBrightness;
    blendTransition->numSteps = numSteps;
    blendTransition->step = 0;
}

BOOL LegDex_PokedexGraphics_TakeBlendTransitionStep(PokedexBlendTransition *blendTransition)
{
    if (LegDex_PokedexGraphics_BlendTransitionComplete(blendTransition) == FALSE) {
        int ev1 = LegDex_PokedexGraphics_BlendSprites(blendTransition);
        int brightness = LegDex_PokedexGraphics_BlendScreen(blendTransition);

        if (blendTransition->isSubscreen == FALSE) {
            G2_SetBlendBrightnessExt(blendTransition->plane1, blendTransition->plane2, ev1, 0, brightness);
        } else {
            G2S_SetBlendBrightnessExt(blendTransition->plane1, blendTransition->plane2, ev1, 0, brightness);
        }

        blendTransition->step++;
    }

    return LegDex_PokedexGraphics_BlendTransitionComplete(blendTransition);
}

int LegDex_PokedexGraphics_BlendSprites(PokedexBlendTransition *blendTransition)
{
    fx32 spriteBrightness = FX_Mul(blendTransition->deltaSpriteBrightness << FX32_SHIFT, blendTransition->step << FX32_SHIFT);
    spriteBrightness = FX_Div(spriteBrightness, blendTransition->numSteps << FX32_SHIFT);

    return (spriteBrightness >> FX32_SHIFT) + blendTransition->startSpriteBrightness;
}

int LegDex_PokedexGraphics_BlendScreen(PokedexBlendTransition *blendTransition)
{
    fx32 backgroundBrightness = FX_Mul(blendTransition->deltaBackgroundBrightness << FX32_SHIFT, blendTransition->step << FX32_SHIFT);
    backgroundBrightness = FX_Div(backgroundBrightness, blendTransition->numSteps << FX32_SHIFT);

    return (backgroundBrightness >> FX32_SHIFT) + blendTransition->startBackgroundBrightness;
}

BOOL LegDex_PokedexGraphics_BlendTransitionComplete(PokedexBlendTransition *blendTransition)
{
    return blendTransition->step > blendTransition->numSteps;
}

void LegDex_PokedexGraphics_BlendPokemonChar(const PokedexGraphicData *pokedexGraphicData, PokedexBlendTransition *blendTransition)
{
    int oppBackgroundBrightness = -LegDex_PokedexGraphics_BlendScreen(blendTransition);
    PokemonSprite *pokemonSprite = LegDex_PokemonGraphics_GetPokemonChar(pokedexGraphicData);

    PokemonSprite_StartFade(pokemonSprite, oppBackgroundBrightness, oppBackgroundBrightness, 0, 0);
}

void LegDex_PokedexGraphics_BlendPokemonSprite(const PokedexGraphicData *pokedexGraphicData, PokedexBlendTransition *blendTransition, int spriteIndex)
{
    int oppBackgroundBrightness = -LegDex_PokedexGraphics_BlendScreen(blendTransition);
    PokemonSprite *pokemonSprite = LegDex_PokedexGraphics_GetPokemonSprite(pokedexGraphicData, spriteIndex);

    PokemonSprite_StartFade(pokemonSprite, oppBackgroundBrightness, oppBackgroundBrightness, 0, 0);
}

void LegDex_PokedexGraphics_CurrentButtonTransformation(const PokedexPanelData *pokedexPanelData, PokedexGraphicData *pokedexGraphicData)
{
    int x, y, width, height;

    LegDex_PokedexPanel_GetCurrentButtonXY(pokedexPanelData, &x, &y);
    LegDex_PokedexPanel_GetCurrentButtonWidthHeight(pokedexPanelData, &width, &height);
    LegDex_PokedexGraphics_TransformCursor(pokedexGraphicData, x, y, width, height);
}

void LegDex_PokedexGraphics_TransformCursor(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height)
{
    InsitigateCursorTransformation(pokedexGraphicData, x, y, width, height);
}

void LegDex_PokedexGraphics_SetDrawCursor(PokedexCursorGraphics *pokedexCursorGraphics, BOOL draw)
{
    for (int cornerType = 0; cornerType < MAX_CORNER_TYPE; cornerType++) {
        Sprite_SetDrawFlag(pokedexCursorGraphics->sprite[cornerType], draw);
    }
}

BOOL LegDex_PokedexGraphics_GetDrawCursor(PokedexCursorGraphics *pokedexCursorGraphics)
{
    return Sprite_GetDrawFlag(pokedexCursorGraphics->sprite[CORNER_TYPE_TOP_LEFT]);
}

void LegDex_PokedexGraphics_SetStaticCursorSize(PokedexCursorGraphics *pokedexCursorGraphics, BOOL isStaticSize)
{
    pokedexCursorGraphics->isStaticSize = isStaticSize;

    if (isStaticSize == FALSE) {
        pokedexCursorGraphics->scale = 0;
    }
}

void LegDex_PokedexGraphics_GoToCurrentButton(const PokedexPanelData *pokedexPanelData, PokedexGraphicData *pokedexGraphicData)
{
    int x, y, width, height;

    LegDex_PokedexPanel_GetCurrentButtonXY(pokedexPanelData, &x, &y);
    LegDex_PokedexPanel_GetCurrentButtonWidthHeight(pokedexPanelData, &width, &height);
    LegDex_PokedexGraphics_SetCursorPosAndSize(pokedexGraphicData, x, y, width, height);
}

void LegDex_PokedexGraphics_SetCursorPosAndSize(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height)
{
    pokedexGraphicData->cursorGraphics.x = x;
    pokedexGraphicData->cursorGraphics.y = y;
    pokedexGraphicData->cursorGraphics.width = width;
    pokedexGraphicData->cursorGraphics.height = height;

    SetCursorSpritePos(&pokedexGraphicData->cursorGraphics, pokedexGraphicData->cursorGraphics.x, pokedexGraphicData->cursorGraphics.y, pokedexGraphicData->cursorGraphics.width, pokedexGraphicData->cursorGraphics.height);

    pokedexGraphicData->cursorMan.x = x;
    pokedexGraphicData->cursorMan.y = y;
    pokedexGraphicData->cursorMan.width = width;
    pokedexGraphicData->cursorMan.height = height;
    pokedexGraphicData->cursorMan.isMoving = FALSE;
}

void LegDex_PokedexGraphics_InitTransformation(SpriteTransformation *spriteTransformation, int startX, int endX, int startY, int endY, int numSteps)
{
    spriteTransformation->currentX = startX;
    spriteTransformation->currentY = startY;
    spriteTransformation->startX = startX;
    spriteTransformation->startY = startY;
    spriteTransformation->deltaX = endX - startX;
    spriteTransformation->deltaY = endY - startY;
    spriteTransformation->numSteps = numSteps;
    spriteTransformation->step = 0;
}

BOOL LegDex_PokedexGraphics_TakeTransformStep(SpriteTransformation *spriteTransformation)
{
    fx32 x = FX_Mul(spriteTransformation->deltaX << FX32_SHIFT, spriteTransformation->step << FX32_SHIFT);
    x = FX_Div(x, spriteTransformation->numSteps << FX32_SHIFT);
    fx32 y = FX_Mul(spriteTransformation->deltaY << FX32_SHIFT, spriteTransformation->step << FX32_SHIFT);
    y = FX_Div(y, spriteTransformation->numSteps << FX32_SHIFT);

    spriteTransformation->currentX = (x >> FX32_SHIFT) + spriteTransformation->startX;
    spriteTransformation->currentY = (y >> FX32_SHIFT) + spriteTransformation->startY;

    if (spriteTransformation->step + 1 <= spriteTransformation->numSteps) {
        spriteTransformation->step++;
        return FALSE;
    }

    spriteTransformation->step = spriteTransformation->numSteps;
    return TRUE;
}

NARC *LegDex_PokedexGraphics_GetNARC(PokedexGraphicData *pokedexGraphicData)
{
    return pokedexGraphicData->pokedexGraphics;
}

static void *LoadGraphicsFile(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BOOL isCompressed, enum HeapID heapID)
{
    void *graphicFile = NARC_AllocAndReadWholeMember(pokedexGraphicData->pokedexGraphics, memberIndex, heapID);

    if (graphicFile != NULL) {
        if (isCompressed) {
            void *uncompressedGraphicFile = Heap_Alloc(heapID, MI_GetUncompressedSize(graphicFile));

            if (uncompressedGraphicFile) {
                MI_UncompressLZ8(graphicFile, uncompressedGraphicFile);
                Heap_Free(graphicFile);
            }

            graphicFile = uncompressedGraphicFile;
        }
    }

    return graphicFile;
}

u32 LegDex_PokedexGraphics_LoadGraphicNarcCharacterData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BgConfig *bgConfig, u32 bgLayer, u32 tileStart, u32 size, BOOL isCompressed, enum HeapID heapID)
{
    void *graphicFile = LoadGraphicsFile(pokedexGraphicData, memberIndex, isCompressed, heapID);

    if (graphicFile != NULL) {
        NNSG2dCharacterData *charData;

        if (NNS_G2dGetUnpackedBGCharacterData(graphicFile, &charData)) {
            if (size == 0) {
                size = charData->szByte;
            }

            Bg_LoadTiles(bgConfig, bgLayer, charData->pRawData, size, tileStart);
        }

        Heap_Free(graphicFile);
    }

    return size;
}

// Legendary Pokédex: recolour the app's screens gold. Grey / black / white stay as they are (so text
// stays readable); every coloured entry becomes a gold shade of the same brightness.
static void LegDex_TintPaletteGold(u16 *colors, u32 szByte)
{
    for (u32 i = 0; i < szByte / 2; i++) {
        int r = colors[i] & 0x1F;
        int g = (colors[i] >> 5) & 0x1F;
        int b = (colors[i] >> 10) & 0x1F;
        int max = r > g ? (r > b ? r : b) : (g > b ? g : b);
        int min = r < g ? (r < b ? r : b) : (g < b ? g : b);

        if (max - min < 4) {
            continue;
        }

        int lum = (r * 77 + g * 150 + b * 29) >> 8;
        int nr = lum * 5 / 4 + 6;
        int ng = lum + 2;
        int nb = lum * 2 / 5;

        nr = nr > 31 ? 31 : nr;
        ng = ng > 29 ? 29 : ng;
        colors[i] = (colors[i] & 0x8000) | nr | (ng << 5) | (nb << 10);
    }
}

void LegDex_PokedexGraphics_LoadGraphicNarcPaletteData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, enum PaletteLoadLocation loadLocation, u32 offset, u32 szByte, enum HeapID heapID)
{
    static void (*const sPaletteLoadFuncs[])(const void *, u32, u32) = {
        GX_LoadBGPltt,
        GX_LoadOBJPltt,
        GX_LoadBGExtPltt,
        GX_LoadOBJExtPltt,
        GXS_LoadBGPltt,
        GXS_LoadOBJPltt,
        GXS_LoadBGExtPltt,
        GXS_LoadOBJExtPltt
    };

    void *graphicFile = LoadGraphicsFile(pokedexGraphicData, memberIndex, FALSE, heapID);

    if (graphicFile != NULL) {
        NNSG2dPaletteData *paletteData;

        if (NNS_G2dGetUnpackedPaletteData(graphicFile, &paletteData)) {
            if (szByte == 0) {
                szByte = paletteData->szByte;
            }

            LegDex_TintPaletteGold(paletteData->pRawData, szByte);
            DC_FlushRange(paletteData->pRawData, szByte);
            sPaletteLoadFuncs[loadLocation](paletteData->pRawData, offset, szByte);
        }

        Heap_Free(graphicFile);
    }
}

void *LegDex_PokedexGraphics_GetGraphicNarcTilemapData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BOOL isCompressed, NNSG2dScreenData **screenData, enum HeapID heapID)
{
    void *graphicFile = LoadGraphicsFile(pokedexGraphicData, memberIndex, isCompressed, heapID);

    if (graphicFile != NULL) {
        if (NNS_G2dGetUnpackedScreenData(graphicFile, screenData) == FALSE) {
            Heap_Free(graphicFile);
            return NULL;
        }
    }

    return graphicFile;
}

void *LegDex_PokedexGraphics_GetGraphicNarcPaletteData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, NNSG2dPaletteData **paletteData, enum HeapID heapID)
{
    void *graphicFile = LoadGraphicsFile(pokedexGraphicData, memberIndex, FALSE, heapID);

    if (graphicFile != NULL) {
        if (NNS_G2dGetUnpackedPaletteData(graphicFile, paletteData) == FALSE) {
            Heap_Free(graphicFile);
            return NULL;
        }

        LegDex_TintPaletteGold((*paletteData)->pRawData, (*paletteData)->szByte);
    }

    return graphicFile;
}

void *LegDex_PokedexGraphics_GetGraphicNarcCharacterData(PokedexGraphicData *pokedexGraphicData, u32 memberIndex, BOOL isCompressed, NNSG2dCharacterData **characterData, enum HeapID heapID)
{
    void *graphicFile = LoadGraphicsFile(pokedexGraphicData, memberIndex, isCompressed, heapID);

    if (graphicFile != NULL) {
        if (NNS_G2dGetUnpackedBGCharacterData(graphicFile, characterData) == FALSE) {
            Heap_Free(graphicFile);
            return NULL;
        }
    }

    return graphicFile;
}

static void InitBackgrounds(BgConfig *bgConfig, enum HeapID heapID)
{
    BgTemplate bgT0 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x800,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_16,
        .screenBase = GX_BG_SCRBASE_0x0000,
        .charBase = GX_BG_CHARBASE_0x04000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 0,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_MAIN_1, &bgT0, BG_TYPE_STATIC);
    Bg_ClearTilesRange(BG_LAYER_MAIN_1, 32, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_MAIN_1);

    BgTemplate bgT1 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x800,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_16,
        .screenBase = GX_BG_SCRBASE_0x0800,
        .charBase = GX_BG_CHARBASE_0x0c000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 1,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_MAIN_2, &bgT1, BG_TYPE_STATIC);
    Bg_ClearTilesRange(BG_LAYER_MAIN_2, 32, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_MAIN_2);

    Bg_SetPriority(BG_LAYER_MAIN_0, 2);
    GXLayers_EngineAToggleLayers(GX_PLANEMASK_BG0, 1);

    BgTemplate bgT2 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x800,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_16,
        .screenBase = GX_BG_SCRBASE_0x1000,
        .charBase = GX_BG_CHARBASE_0x14000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 3,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_MAIN_3, &bgT2, BG_TYPE_STATIC);
    Bg_ClearTilesRange(BG_LAYER_MAIN_3, 32, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_MAIN_3);

    BgTemplate bgT3 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x800,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_16,
        .screenBase = GX_BG_SCRBASE_0x0000,
        .charBase = GX_BG_CHARBASE_0x04000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 0,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_SUB_1, &bgT3, BG_TYPE_STATIC);
    Bg_ClearTilesRange(BG_LAYER_SUB_1, 32, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_SUB_1);

    BgTemplate bgT4 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x800,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_16,
        .screenBase = GX_BG_SCRBASE_0x1000,
        .charBase = GX_BG_CHARBASE_0x08000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 2,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_SUB_2, &bgT4, BG_TYPE_STATIC);
    Bg_ClearTilesRange(BG_LAYER_SUB_2, 32, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_SUB_2);

    BgTemplate bgT5 = {
        .x = 0,
        .y = 0,
        .bufferSize = 0x400,
        .baseTile = 0,
        .screenSize = BG_SCREEN_SIZE_256x256,
        .colorMode = GX_BG_COLORMODE_256,
        .screenBase = GX_BG_SCRBASE_0x0800,
        .charBase = GX_BG_CHARBASE_0x10000,
        .bgExtPltt = GX_BG_EXTPLTT_01,
        .priority = 1,
        .areaOver = 0,
        .mosaic = 0
    };

    Bg_InitFromTemplate(bgConfig, BG_LAYER_SUB_3, &bgT5, BG_TYPE_AFFINE);
    Bg_ClearTilesRange(BG_LAYER_SUB_3, 64, 0, heapID);
    Bg_ClearTilemap(bgConfig, BG_LAYER_SUB_3);
}

static void FreeBackgrounds(BgConfig *bgConfig)
{
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_MAIN_1);
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_MAIN_2);
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_MAIN_3);
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_SUB_1);
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_SUB_3);
    Bg_FreeTilemapBuffer(bgConfig, BG_LAYER_SUB_2);
}

static void InitWindow(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    Window_Add(pokedexGraphicData->bgConfig, &pokedexGraphicData->window, 1, 0, 0, 32, 32, 0, 0);
    Window_FillTilemap(&pokedexGraphicData->window, 0);
    Window_CopyToVRAM(&pokedexGraphicData->window);
}

static void FreeWindow(PokedexGraphicData *pokedexGraphicData)
{
    Window_Remove(&pokedexGraphicData->window);
}

static void NewPokemonSprite(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    pokedexGraphicData->spriteMan = PokemonSpriteManager_New(heapID);

    NNSGfdTexKey texKey = NNS_GfdAllocTexVram(0x8000, 0, 0);
    NNSGfdPlttKey plttKey = NNS_GfdAllocPlttVram(0x80, 0, NNS_GFD_ALLOC_FROM_LOW);

    PokemonSpriteManager_SetCharBaseAddrAndSize(pokedexGraphicData->spriteMan, NNS_GfdGetTexKeyAddr(texKey), NNS_GfdGetTexKeySize(texKey));
    PokemonSpriteManager_SetPlttBaseAddrAndSize(pokedexGraphicData->spriteMan, NNS_GfdGetPlttKeyAddr(plttKey), NNS_GfdGetPlttKeySize(plttKey));

    for (int spriteIndex = 0; spriteIndex < NUM_VISIBLE_SPRITES; spriteIndex++) {
        pokedexGraphicData->pokemonSprite[spriteIndex] = NULL;
    }

    {
        SoftwareSpriteManagerTemplate v3 = {
            .numSprites = 8,
            .numChars = 8,
            .numPalettes = 8,
            .heapID = HEAP_ID_SYSTEM
        };

        v3.heapID = heapID;
        pokedexGraphicData->unk_164 = SoftwareSpriteManager_New(&v3);
    }
}

static void FreePokemonSprite(PokedexGraphicData *pokedexGraphicData)
{
    for (int spriteIndex = 0; spriteIndex < NUM_VISIBLE_SPRITES; spriteIndex++) {
        if (pokedexGraphicData->pokemonSprite[spriteIndex]) {
            PokemonSprite_Delete(pokedexGraphicData->pokemonSprite[spriteIndex]);
        }
    }

    PokemonSpriteManager_Free(pokedexGraphicData->spriteMan);
    SoftwareSpriteManager_Free(pokedexGraphicData->unk_164);
}

static void InitSpeciesLabelGraphics(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    PokedexSpeciesLabel *pokedexSpeciesLabel = &pokedexGraphicData->pokedexSpeciesLabel;
    NARC *pokedexGraphicsNARC = LegDex_PokedexGraphics_GetNARC(pokedexGraphicData);

    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR] = SpriteResourceCollection_AddTilesFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexGraphicsNARC, name_tag_NCGR_lz, TRUE, 3000, NNS_G2D_VRAM_TYPE_2DMAIN, heapID);

    SpriteTransfer_RequestCharAtEnd(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResource_ReleaseData(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);

    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT] = SpriteResourceCollection_AddPaletteFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexGraphicsNARC, buttons_NCLR, FALSE, 3000, NNS_G2D_VRAM_TYPE_2DMAIN, 1, heapID);

    SpriteTransfer_RequestPlttFreeSpace(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResource_ReleaseData(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);

    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CELL] = SpriteResourceCollection_AddFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexGraphicsNARC, name_tag_cell_NCER_lz, TRUE, 3000, SPRITE_RESOURCE_CELL, heapID);
    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_ANIM] = SpriteResourceCollection_AddFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], pokedexGraphicsNARC, name_tag_anim_NANR_lz, TRUE, 3000, SPRITE_RESOURCE_ANIM, heapID);
}

void LegDex_PokedexGraphics_InitSpeciesLabelGraphics(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteResourceCollection **spriteResourceCollection, enum HeapID heapID, NARC *narc)
{
    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR] = SpriteResourceCollection_AddTilesFrom(spriteResourceCollection[SPRITE_RESOURCE_CHAR], narc, name_tag_NCGR_lz, TRUE, 3000, NNS_G2D_VRAM_TYPE_2DMAIN, heapID);

    SpriteTransfer_RequestCharAtEnd(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResource_ReleaseData(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);

    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT] = SpriteResourceCollection_AddPaletteFrom(spriteResourceCollection[SPRITE_RESOURCE_PLTT], narc, buttons_NCLR, FALSE, 3000, NNS_G2D_VRAM_TYPE_2DMAIN, 1, heapID);

    SpriteTransfer_RequestPlttFreeSpace(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResource_ReleaseData(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);

    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CELL] = SpriteResourceCollection_AddFrom(spriteResourceCollection[SPRITE_RESOURCE_CELL], narc, name_tag_cell_NCER_lz, TRUE, 3000, SPRITE_RESOURCE_CELL, heapID);
    pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_ANIM] = SpriteResourceCollection_AddFrom(spriteResourceCollection[SPRITE_RESOURCE_ANIM], narc, name_tag_anim_NANR_lz, TRUE, 3000, SPRITE_RESOURCE_ANIM, heapID);
}

static void FreeSpeciesLabelGraphics(PokedexGraphicData *pokedexGraphicData)
{
    PokedexSpeciesLabel *pokedexSpeciesLabel = &pokedexGraphicData->pokedexSpeciesLabel;

    SpriteTransfer_ResetCharTransfer(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteTransfer_ResetPlttTransfer(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);

    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CELL]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_ANIM]);
}

void LegDex_PokedexGraphics_FreeSpeciesLabelGraphics(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteResourceCollection **spriteResourceCollection)
{
    SpriteTransfer_ResetCharTransfer(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteTransfer_ResetPlttTransfer(pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);

    SpriteResourceCollection_Remove(spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResourceCollection_Remove(spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResourceCollection_Remove(spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_CELL]);
    SpriteResourceCollection_Remove(spriteResourceCollection[SPRITE_RESOURCE_ANIM], pokedexSpeciesLabel->spriteResource[SPRITE_RESOURCE_ANIM]);
}

static void InitSpeciesLabel(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    SpriteResourcesHeader spriteResourcesHeader;
    SpriteListTemplate spriteListTemplate;

    SpriteResourcesHeader_Init(&spriteResourcesHeader, 3000, 3000, 3000, 3000, 0xffffffff, 0xffffffff, FALSE, 0, pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], NULL, NULL);

    spriteListTemplate.list = pokedexGraphicData->spriteList;
    spriteListTemplate.resourceData = &spriteResourcesHeader;
    spriteListTemplate.priority = 0;
    spriteListTemplate.vramType = NNS_G2D_VRAM_TYPE_2DMAIN;
    spriteListTemplate.heapID = heapID;
    spriteListTemplate.position.x = 0;
    spriteListTemplate.position.y = 0;

    pokedexGraphicData->pokedexSpeciesLabel.nameTag = SpriteList_Add(&spriteListTemplate);

    Sprite_SetDrawFlag(pokedexGraphicData->pokedexSpeciesLabel.nameTag, FALSE);
    Sprite_SetPriority(pokedexGraphicData->pokedexSpeciesLabel.nameTag, 1);

    spriteListTemplate.position.x = 0;
    spriteListTemplate.position.y = 0;

    pokedexGraphicData->pokedexSpeciesLabel.caughtIcon = SpriteList_Add(&spriteListTemplate);

    Sprite_SetDrawFlag(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon, FALSE);
    Sprite_SetAnim(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon, 1);

    pokedexGraphicData->pokedexSpeciesLabel.textData = NULL;
    pokedexGraphicData->pokedexSpeciesLabel.species = SPECIES_NONE;
    pokedexGraphicData->pokedexSpeciesLabel.isNationalDex = FALSE;
}

static void FreeSpeciesLabel(PokedexGraphicData *pokedexGraphicData)
{
    Sprite_Delete(pokedexGraphicData->pokedexSpeciesLabel.nameTag);
    pokedexGraphicData->pokedexSpeciesLabel.nameTag = NULL;

    Sprite_Delete(pokedexGraphicData->pokedexSpeciesLabel.caughtIcon);
    pokedexGraphicData->pokedexSpeciesLabel.caughtIcon = NULL;

    if (pokedexGraphicData->pokedexSpeciesLabel.textData) {
        LegDex_PokedexTextManager_FreeTextData(pokedexGraphicData->pokedexSpeciesLabel.textData);
        pokedexGraphicData->pokedexSpeciesLabel.textData = NULL;
    }
}

void LegDex_PokedexGraphics_NewSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel, SpriteList *spriteList, SpriteResourceCollection **spriteResourceCollection, enum HeapID heapID, int headerPriority)
{
    SpriteResourcesHeader spriteResourcesHeader;
    SpriteListTemplate spriteListTemplate;

    SpriteResourcesHeader_Init(&spriteResourcesHeader, 3000, 3000, 3000, 3000, 0xffffffff, 0xffffffff, FALSE, headerPriority, spriteResourceCollection[SPRITE_RESOURCE_CHAR], spriteResourceCollection[SPRITE_RESOURCE_PLTT], spriteResourceCollection[SPRITE_RESOURCE_CELL], spriteResourceCollection[SPRITE_RESOURCE_ANIM], NULL, NULL);

    spriteListTemplate.list = spriteList;
    spriteListTemplate.resourceData = &spriteResourcesHeader;
    spriteListTemplate.priority = 0;
    spriteListTemplate.vramType = NNS_G2D_VRAM_TYPE_2DMAIN;
    spriteListTemplate.heapID = heapID;
    spriteListTemplate.position.x = 0;
    spriteListTemplate.position.y = 0;

    pokedexSpeciesLabel->nameTag = SpriteList_Add(&spriteListTemplate);

    Sprite_SetDrawFlag(pokedexSpeciesLabel->nameTag, FALSE);
    Sprite_SetPriority(pokedexSpeciesLabel->nameTag, 1);

    spriteListTemplate.position.x = 0;
    spriteListTemplate.position.y = 0;

    pokedexSpeciesLabel->caughtIcon = SpriteList_Add(&spriteListTemplate);

    Sprite_SetDrawFlag(pokedexSpeciesLabel->caughtIcon, FALSE);
    Sprite_SetAnim(pokedexSpeciesLabel->caughtIcon, 1);

    pokedexSpeciesLabel->textData = NULL;
    pokedexSpeciesLabel->species = SPECIES_NONE;
    pokedexSpeciesLabel->isNationalDex = FALSE;
}

void LegDex_PokedexGraphics_FreeSpeciesLabel(PokedexSpeciesLabel *pokedexSpeciesLabel)
{
    Sprite_Delete(pokedexSpeciesLabel->nameTag);
    pokedexSpeciesLabel->nameTag = NULL;

    Sprite_Delete(pokedexSpeciesLabel->caughtIcon);
    pokedexSpeciesLabel->caughtIcon = NULL;

    if (pokedexSpeciesLabel->textData) {
        LegDex_PokedexTextManager_FreeTextData(pokedexSpeciesLabel->textData);
        pokedexSpeciesLabel->textData = NULL;
    }
}

void LegDex_PokedexGraphics_SetSpeciesLabelDraw(PokedexSpeciesLabel *pokedexSpeciesLabel, BOOL draw)
{
    if (pokedexSpeciesLabel->nameTag) {
        Sprite_SetDrawFlag(pokedexSpeciesLabel->nameTag, draw);
    }

    if (pokedexSpeciesLabel->caughtIcon) {
        Sprite_SetDrawFlag(pokedexSpeciesLabel->caughtIcon, draw);
    }

    if (pokedexSpeciesLabel->textData->fontOAM) {
        sub_020129D0(pokedexSpeciesLabel->textData->fontOAM, draw);
    }
}

static void InitCursorGraphics(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    PokedexCursorGraphics *pokedexCursorGraphics = &pokedexGraphicData->cursorGraphics;
    NARC *pokedexGraphicsNARC = LegDex_PokedexGraphics_GetNARC(pokedexGraphicData);

    pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CHAR] = SpriteResourceCollection_AddTilesFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexGraphicsNARC, cursor_NCGR_lz, TRUE, 12000, NNS_G2D_VRAM_TYPE_2DSUB, heapID);

    SpriteTransfer_RequestCharAtEnd(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResource_ReleaseData(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CHAR]);

    pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_PLTT] = SpriteResourceCollection_AddPaletteFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexGraphicsNARC, cursor_NCLR, FALSE, 12000, NNS_G2D_VRAM_TYPE_2DSUB, 1, heapID);

    SpriteTransfer_RequestPlttFreeSpace(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResource_ReleaseData(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_PLTT]);

    pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CELL] = SpriteResourceCollection_AddFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexGraphicsNARC, cursor_cell_NCER_lz, TRUE, 12000, SPRITE_RESOURCE_CELL, heapID);
    pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_ANIM] = SpriteResourceCollection_AddFrom(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], pokedexGraphicsNARC, cursor_anim_NANR_lz, TRUE, 12000, SPRITE_RESOURCE_ANIM, heapID);
}

static void FreeCursorGraphics(PokedexGraphicData *pokedexGraphicData)
{
    PokedexCursorGraphics *pokedexCursorGraphics = &pokedexGraphicData->cursorGraphics;

    SpriteTransfer_ResetCharTransfer(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteTransfer_ResetPlttTransfer(pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_PLTT]);

    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CHAR]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_PLTT]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_CELL]);
    SpriteResourceCollection_Remove(pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], pokedexCursorGraphics->spriteResource[SPRITE_RESOURCE_ANIM]);
}

static void InitCursor(PokedexGraphicData *pokedexGraphicData, enum HeapID heapID)
{
    SpriteResourcesHeader resourceData;
    SpriteListTemplate spriteListTemplate;
    PokedexCursorGraphics *pokedexCursorGraphics = &pokedexGraphicData->cursorGraphics;

    SpriteResourcesHeader_Init(&resourceData, 12000, 12000, 12000, 12000, 0xffffffff, 0xffffffff, FALSE, 0, pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CHAR], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_PLTT], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_CELL], pokedexGraphicData->spriteResourceCollection[SPRITE_RESOURCE_ANIM], NULL, NULL);

    spriteListTemplate.list = pokedexGraphicData->spriteList;
    spriteListTemplate.resourceData = &resourceData;
    spriteListTemplate.priority = 0;
    spriteListTemplate.vramType = NNS_G2D_VRAM_TYPE_2DSUB;
    spriteListTemplate.heapID = heapID;
    spriteListTemplate.position.y = (192 << FX32_SHIFT) + (100 * FX32_ONE);
    spriteListTemplate.position.x = (100 * FX32_ONE);

    for (int cornerType = 0; cornerType < MAX_CORNER_TYPE; cornerType++) {
        pokedexCursorGraphics->sprite[cornerType] = SpriteList_Add(&spriteListTemplate);
        Sprite_SetAnim(pokedexCursorGraphics->sprite[cornerType], cornerType);
    }

    LegDex_PokedexGraphics_SetDrawCursor(pokedexCursorGraphics, 0);
    StartCursorPulse(pokedexGraphicData);
    StartCursorTransform(pokedexGraphicData);
}

static void FreeCursor(PokedexGraphicData *pokedexGraphicData)
{
    PokedexCursorGraphics *pokedexCursorGraphics = &pokedexGraphicData->cursorGraphics;

    EndCursorTransform(pokedexGraphicData);
    EndCursorPulse(pokedexGraphicData);

    for (int cornerType = 0; cornerType < MAX_CORNER_TYPE; cornerType++) {
        Sprite_Delete(pokedexCursorGraphics->sprite[cornerType]);
    }
}

static void StartCursorPulse(PokedexGraphicData *pokedexGraphicData)
{
    pokedexGraphicData->cursorPulse = SysTask_Start(PulseCursor, &pokedexGraphicData->cursorGraphics, 1);
}

static void EndCursorPulse(PokedexGraphicData *pokedexGraphicData)
{
    SysTask_Done(pokedexGraphicData->cursorPulse);
}

static void PulseCursor(SysTask *sysTask, void *data)
{
    PokedexCursorGraphics *pokedexCursorGraphics = data;
    int scale;

    if (pokedexCursorGraphics->isStaticSize) {
        SetCursorSpritePos(pokedexCursorGraphics, pokedexCursorGraphics->x, pokedexCursorGraphics->y, pokedexCursorGraphics->width, pokedexCursorGraphics->height);
        return;
    }

    pokedexCursorGraphics->scale = (pokedexCursorGraphics->scale + 1) % (32 * 2);

    if (pokedexCursorGraphics->scale < 32) {
        scale = pokedexCursorGraphics->scale;
    } else {
        scale = (32 * 2) - (pokedexCursorGraphics->scale + 1);
    }

    fx32 size = FX_Mul(4 << FX32_SHIFT, scale << FX32_SHIFT);
    size = FX_Div(size, 32 << FX32_SHIFT);
    size >>= FX32_SHIFT;
    int width = pokedexCursorGraphics->width + size;
    int height = pokedexCursorGraphics->height + size;

    SetCursorSpritePos(pokedexCursorGraphics, pokedexCursorGraphics->x, pokedexCursorGraphics->y, width, height);
}

static void SetCursorSpritePos(PokedexCursorGraphics *pokedexCursorGraphics, int x, int y, int width, int height)
{
    VecFx32 position;
    int cornerX, cornerY;

    for (int cornerType = 0; cornerType < MAX_CORNER_TYPE; cornerType++) {
        LegDex_PokedexPanel_GetCursorCornerPos(cornerType, &cornerX, &cornerY, x, y, width, height);
        position.x = cornerX << FX32_SHIFT;
        position.y = (cornerY << FX32_SHIFT) + (192 << FX32_SHIFT);

        Sprite_SetPosition(pokedexCursorGraphics->sprite[cornerType], &position);
    }
}

static void InsitigateCursorTransformation(PokedexGraphicData *pokedexGraphicData, int x, int y, int width, int height)
{
    PokedexCursorManager *cursorMan = &pokedexGraphicData->cursorMan;

    if ((cursorMan->x == x) && (cursorMan->y == y) && (cursorMan->width == width) && (cursorMan->height == height)) {
        return;
    }

    cursorMan->cursorGraphics = &pokedexGraphicData->cursorGraphics;

    LegDex_PokedexGraphics_InitTransformation(&cursorMan->centerPoint, cursorMan->cursorGraphics->x, x, cursorMan->cursorGraphics->y, y, 3);
    LegDex_PokedexGraphics_InitTransformation(&cursorMan->size, cursorMan->cursorGraphics->width, width, cursorMan->cursorGraphics->height, height, 3);

    cursorMan->x = x;
    cursorMan->y = y;
    cursorMan->width = width;
    cursorMan->height = height;
    cursorMan->isMoving = TRUE;
}

static void TransformCursor(SysTask *sysTask, void *data)
{
    PokedexCursorManager *cursorMan = data;

    if (cursorMan->isMoving == FALSE) {
        return;
    }

    BOOL transformFinished = LegDex_PokedexGraphics_TakeTransformStep(&cursorMan->centerPoint);
    LegDex_PokedexGraphics_TakeTransformStep(&cursorMan->size);

    cursorMan->cursorGraphics->x = cursorMan->centerPoint.currentX;
    cursorMan->cursorGraphics->y = cursorMan->centerPoint.currentY;
    cursorMan->cursorGraphics->width = cursorMan->size.currentX;
    cursorMan->cursorGraphics->height = cursorMan->size.currentY;

    if (transformFinished == TRUE) {
        cursorMan->isMoving = FALSE;
    }
}

static void StartCursorTransform(PokedexGraphicData *pokedexGraphicData)
{
    pokedexGraphicData->cursorTransorm = SysTask_Start(TransformCursor, &pokedexGraphicData->cursorMan, 0);
}

static void EndCursorTransform(PokedexGraphicData *pokedexGraphicData)
{
    SysTask_Done(pokedexGraphicData->cursorTransorm);
    pokedexGraphicData->cursorTransorm = NULL;
}
