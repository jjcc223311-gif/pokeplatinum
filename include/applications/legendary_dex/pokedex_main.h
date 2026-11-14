#ifndef POKEPLATINUM_LEGDEX_POKEDEX_MAIN_H
#define POKEPLATINUM_LEGDEX_POKEDEX_MAIN_H

#include <nnsys.h>

#include "applications/legendary_dex/pokedex_app.h"
#include "applications/legendary_dex/pokedex_graphics.h"
#include "applications/legendary_dex/pokedex_sort_data.h"
#include "applications/legendary_dex/pokedex_text_manager.h"
#include "applications/legendary_dex/pokedex_updater.h"
#include "applications/legendary_dex/struct_ov21_021D423C_decl.h"
#include "applications/legendary_dex/struct_ov21_021E68F4.h"

#include "bg_window.h"
#include "heap.h"
#include "overlay_manager.h"
#include "pokedex.h"
#include "pokedex_memory.h"
#include "sprite.h"
#include "string_gf.h"
#include "touch_screen.h"
#include "trainer_info.h"

typedef struct PokedexLoadingScreen {
    BgConfig *bgConfig;
    NNSG2dScreenData *screenData;
    int layer;
    int topStart;
    int bottomStart;
    int topDist;
    int bottomDist;
    int counter;
    int duration;
} PokedexLoadingScreen;

typedef struct {
    const Pokedex *pokedex;
    const TrainerInfo *trainerInfo;
    int timeOfDay;
    BOOL fullmoonIslandVisible;
    BOOL newmoonIslandVisible;
    BOOL springPathVisible;
    BOOL seabreakPathVisible;
    PokedexMemory *pokedexMemory;
} PokedexOverlayArgs;

int LegDex_PokedexMain_Init(ApplicationManager *appMan, int *state);
int LegDex_PokedexMain_Main(ApplicationManager *appMan, int *state);
int LegDex_PokedexMain_Exit(ApplicationManager *appMan, int *state);
PokedexApp *LegDex_PokedexMain_NewPokedexApp(enum HeapID heapID, const PokedexOverlayArgs *pokedexOverlayArgs);
BOOL LegDex_ov21_021D10B8(PokedexApp *pokedexApp);
void LegDex_PokedexMain_InitGX(enum HeapID heapID);
void LegDex_PokedexMain_FreeGraphics(void);
void LegDex_ov21_021D12D8(PokedexApp *pokedexApp);
PokedexUpdater *LegDex_ov21_021D12EC(PokedexApp *pokedexApp);
PokedexUpdater *LegDex_ov21_021D1300(PokedexApp *pokedexApp);
PokedexUpdater *LegDex_ov21_021D1314(PokedexApp *pokedexApp);
PokedexUpdater *LegDex_ov21_021D1328(PokedexApp *pokedexApp);
UnkStruct_ov21_021D423C *LegDex_ov21_021D133C(PokedexApp *pokedexApp);
UnkStruct_ov21_021D423C *LegDex_ov21_021D1350(PokedexApp *pokedexApp);
UnkStruct_ov21_021D423C *LegDex_ov21_021D1364(PokedexApp *pokedexApp);
UnkStruct_ov21_021D423C *LegDex_ov21_021D1378(PokedexApp *pokedexApp);
int *LegDex_ov21_021D138C(PokedexApp *pokedexApp);
int *LegDex_ov21_021D13A0(PokedexApp *pokedexApp);
int *LegDex_ov21_021D13B4(PokedexApp *pokedexApp);
int *LegDex_ov21_021D13C8(PokedexApp *pokedexApp);
BOOL *LegDex_ov21_021D13DC(PokedexApp *pokedexApp);
PokedexSortData *LegDex_PokedexMain_GetSortData(PokedexApp *pokedexApp);
PokedexGraphicData *LegDex_PokedexMain_GetGraphicData(PokedexApp *pokedexApp);
PokedexScreenManager *LegDex_ov21_021D1410(PokedexApp *pokedexApp, int param1);
PokedexScreenManager *LegDex_ov21_021D1430(PokedexApp *pokedexApp, int param1);
void LegDex_ov21_021D144C(Sprite *param0, int param1);
void LegDex_PokedexMain_SetButtonY(Sprite *param0, PokedexTextData *textData, int setY);
void LegDex_ov21_021D1524(Sprite *param0, PokedexTextData *textData, int param2, int param3, int param4);
void LegDex_PokedexMain_SetHitTableRect(TouchScreenHitTable *hitTable, int top, int bottom, int left, int right);
void LegDex_PokedexMain_SetLoadingScreenParams(PokedexLoadingScreen *pokedexLoadingScreen, BgConfig *bgConfig, int layer, NNSG2dScreenData *screenData, int topStart, int topEnd, int bottomStart, int bottomEnd, int duration);
BOOL LegDex_PokedexMain_LoadingScreenMove(PokedexLoadingScreen *pokedexLoadingScreen);
void LegDex_PokedexMain_DisplayNameNumberText(Window *window, int dexNumber, int species, enum HeapID heapID);
Window *LegDex_PokedexMain_DisplayNameNumber(PokedexGraphicData *pokedexgraphicData, const PokedexSortData *pokedexSortData, enum HeapID heapID, int species);
Window *LegDex_PokedexMain_DisplayNameNumberNational(PokedexTextManager *textMan, enum HeapID heapID, int species);
Window *LegDex_PokedexMain_DisplayNameNumberLocal(PokedexTextManager *textMan, enum HeapID heapID, int species);
void LegDex_PokedexMain_EntryNameNumber(PokedexGraphicData *param0, const PokedexSortData *pokedexSortData, enum HeapID heapID, int statusIndex, fx32 x, fx32 y);
void LegDex_ov21_021D1848(PokedexGraphicData *pokedexGraphicData, int param1, int param2);
void LegDex_ov21_021D1858(PokedexSpeciesLabel *param0, int param1, int param2);
void LegDex_PokedexMain_DisplayPokemonSprite(PokedexGraphicData *pokedexGraphicData, PokedexSortData *pokedexSortData, int species, int face, int x, int y);
u32 LegDex_PokedexMain_DisplaySpeciesSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int species, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayUnownSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayShellosSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayGastrodonSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayBurmySprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayWormadamSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayDeoxysSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayShayminSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayGiratinaSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
u32 LegDex_PokedexMain_DisplayRotomSprite(PokedexGraphicData *pokedexGraphicData, const PokedexSortData *pokedexSortData, int face, int x, int y, int formIndex, int spriteIndex);
String *LegDex_PokedexMain_GetMessage(int entryID, enum HeapID heapID);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_MAIN_H
