#ifndef POKEPLATINUM_LEGDEX_POKEDEX_PANEL_H
#define POKEPLATINUM_LEGDEX_POKEDEX_PANEL_H

#include "constants/heap.h"

enum PanelMovementType {
    PANEL_MOVEMENT_MULTICOL = 0,
    PANEL_MOVEMENT_MULTIROW,
    PANEL_MOVEMENT_COL,
    PANEL_MOVEMENT_ROW,
    PANEL_MOVEMENT_JUMP
};

enum CursorMovementType {
    CURSOR_MOVEMENT_SELECT = 0,
    CURSOR_MOVEMENT_IMPASSE,
    CURSOR_MOVEMENT_SKIP
};

enum CornerType {
    CORNER_TYPE_TOP_LEFT = 0,
    CORNER_TYPE_TOP_RIGHT,
    CORNER_TYPE_BOTTOM_LEFT,
    CORNER_TYPE_BOTTOM_RIGHT,
    MAX_CORNER_TYPE
};

typedef struct PokedexCursorData {
    int x;
    int y;
    int width;
    int height;
    enum CursorMovementType cursorColMovementType;
    enum CursorMovementType cursorRowMovementType;
    int button;
} PokedexCursorData;

typedef struct PokedexPanelData {
    const PokedexCursorData *pokedexCursorData;
    int numCols;
    int numRows;
    int col;
    int row;
} PokedexPanelData;

PokedexPanelData *LegDex_PokedexPanel_Alloc(enum HeapID heapID);
void LegDex_PokedexPanel_Free(PokedexPanelData *pokedexPanelData);
void LegDex_PokedexPanel_New(PokedexPanelData *pokedexPanelData, const PokedexCursorData *pokedexCursorData, int numCols, int numRows);
void LegDex_PokedexPanel_Move(PokedexPanelData *pokedexPanelData, enum PanelMovementType movementType, int val);
int LegDex_PokedexPanel_GetCurrentButton(const PokedexPanelData *pokedexPanelData);
void LegDex_PokedexPanel_GetCurrentButtonXY(const PokedexPanelData *pokedexPanelData, int *x, int *y);
void LegDex_PokedexPanel_GetCurrentButtonWidthHeight(const PokedexPanelData *pokedexPanelData, int *width, int *height);
void LegDex_PokedexPanel_InitCursorData(PokedexCursorData *pokedexCursorData, int x, int y, int width, int height, enum CursorMovementType cursorColMovementType, enum CursorMovementType cursorRowMovementType, int button);
void LegDex_PokedexPanel_GetCursorCornerPos(enum CornerType cornerType, int *cornerX, int *cornerY, int x, int y, int width, int height);

#endif // POKEPLATINUM_LEGDEX_POKEDEX_PANEL_H
