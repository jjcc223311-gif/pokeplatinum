#ifndef POKEPLATINUM_PLTT_TRANSFER_H
#define POKEPLATINUM_PLTT_TRANSFER_H

#include <nnsys.h>

#include "constants/heap.h"

typedef struct PlttTransferTaskTemplate {
    NNSG2dPaletteData *data;
    NNS_G2D_VRAM_TYPE vramType;
    u32 plttIndex;
    u32 resourceID;
} PlttTransferTaskTemplate;

void PlttTransfer_Init(int capacity, enum HeapID heapID);
void PlttTransfer_MarkReservedSlots(u16 reservedMask, NNS_G2D_VRAM_TYPE vramType);
void PlttTransfer_Free(void);
void PlttTransfer_Clear(void);
BOOL PlttTransfer_RequestWholeRange(const PlttTransferTaskTemplate *template);
BOOL PlttTransfer_RequestFreeSpace(const PlttTransferTaskTemplate *template);

/**
 * @brief Check whether PlttTransfer_RequestFreeSpace would succeed for a palette of the given
 * size, so callers with optional palettes can skip them instead of hitting an assert.
 */
BOOL PlttTransfer_CanRequestFreeSpace(int numPalettes, NNS_G2D_VRAM_TYPE vramType);
void PlttTransfer_ReplacePlttData(int resourceID, NNSG2dPaletteData *data);
BOOL PlttTransfer_HasTask(int resourceID);
void PlttTransfer_ResetTask(int resourceID);
void PlttTransfer_ResetAllTasks(void);
NNSG2dImagePaletteProxy *PlttTransfer_GetPaletteProxy(int resourceID);
NNSG2dImagePaletteProxy *PlttTransfer_ToggleExtPalette(int resourceID, NNSG2dImageProxy *imageProxy);
u32 PlttTransfer_GetPlttOffset(const NNSG2dImagePaletteProxy *paletteProxy, NNS_G2D_VRAM_TYPE vramType);

#endif // POKEPLATINUM_PLTT_TRANSFER_H
