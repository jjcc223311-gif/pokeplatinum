#include "applications/legdex_sections.h"

#include <nitro.h>
#include <string.h>

#include "constants/charcode.h"
#include "constants/forms.h"
#include "constants/heap.h"
#include "constants/species.h"
#include "constants/string.h"
#include "generated/abilities.h"
#include "generated/genders.h"
#include "generated/pokemon_types.h"
#include "generated/species_data_params.h"

#include "data/legdex_tables.h"

#include "bg_window.h"
#include "character_sprite.h"
#include "font.h"
#include "gx_layers.h"
#include "heap.h"
#include "message.h"
#include "overlay_manager.h"
#include "pokedex.h"
#include "pokemon.h"
#include "save_player.h"
#include "savedata.h"
#include "screen_fade.h"
#include "sound_playback.h"
#include "string_gf.h"
#include "system.h"
#include "text.h"

#include "res/text/bank/legdex_sections.h"

// The Legendary Pokédex's home screen and its Mega Evolution, Types and Abilities sections.
// Bottom screen: tabs, the list of the current section and the controls. Top screen: the selected
// entry. Everything is drawn into two full-screen windows with a gold palette, plus one background
// layer on the top screen for a Pokémon sprite (Mega section).

#define HEAP_ID_LEGDEX_SECTIONS HEAP_ID_POKEDEX

#define SCREEN_W 256
#define SCREEN_H 192

#define TAB_H      24
#define ROW_H      16
#define LIST_Y     (TAB_H + 2)
#define LIST_ROWS  9
#define FOOTER_Y   (SCREEN_H - 16)
#define HEADER_H   24
#define LINE_H     16
#define TEXT_LEFT  8
#define TEXT_RIGHT 248

#define HOLDER_LINES 5

// Gold palette (BG palette 0 on both screens)
enum {
    COL_BACKDROP = 0,
    COL_TEXT,
    COL_TEXT_SHADOW,
    COL_CREAM,
    COL_LIGHT_GOLD,
    COL_GOLD,
    COL_DARK_GOLD,
    COL_WHITE,
    COL_WHITE_SHADOW,
    COL_HIGHLIGHT,
    COL_GREEN,
    COL_RED,
    COL_GRAY,
};

#define TEXTCOLOR_BODY      TEXT_COLOR(COL_TEXT, COL_TEXT_SHADOW, COL_CREAM)
#define TEXTCOLOR_HIGHLIGHT TEXT_COLOR(COL_TEXT, COL_TEXT_SHADOW, COL_HIGHLIGHT)
#define TEXTCOLOR_TAB       TEXT_COLOR(COL_TEXT, COL_TEXT_SHADOW, COL_LIGHT_GOLD)
#define TEXTCOLOR_HEADER    TEXT_COLOR(COL_WHITE, COL_WHITE_SHADOW, COL_DARK_GOLD)
#define TEXTCOLOR_STRIP     TEXT_COLOR(COL_WHITE, COL_WHITE_SHADOW, COL_GOLD)

static const u16 sGoldPalette[16] = {
    GX_RGB(22, 16, 3), // backdrop
    GX_RGB(9, 6, 1), // text
    GX_RGB(27, 23, 14), // text shadow
    GX_RGB(31, 30, 26), // cream
    GX_RGB(31, 27, 13), // light gold
    GX_RGB(29, 22, 5), // gold
    GX_RGB(21, 14, 1), // dark gold
    GX_RGB(31, 31, 31), // white
    GX_RGB(15, 10, 1), // shadow on gold
    GX_RGB(31, 29, 18), // highlighted row
    GX_RGB(8, 20, 8), // green
    GX_RGB(25, 8, 6), // red
    GX_RGB(15, 15, 15), // gray
    GX_RGB(0, 0, 0),
    GX_RGB(0, 0, 0),
    GX_RGB(0, 0, 0),
};

#define SPRITE_PALETTE   1
#define SPRITE_TILE      1
#define SPRITE_X_TILES   22
#define SPRITE_Y_TILES   3
#define SPRITE_W_TILES   10
#define SPRITE_SIZE      (SPRITE_W_TILES * SPRITE_W_TILES * TILE_SIZE_4BPP)
#define NUM_LISTED_TYPES (NUM_POKEMON_TYPES - 1) // without the Mystery type

typedef struct LegDexSections {
    enum HeapID heapID;
    LegDexSectionsArgs *args;
    Pokedex *pokedex;
    BgConfig *bgConfig;
    Window top;
    Window bottom;
    MessageLoader *text;
    MessageLoader *speciesNames;
    MessageLoader *abilityNames;
    MessageLoader *abilityDescriptions;
    MessageLoader *typeNames;
    String *str;
    String *str2;
    String *line;
    u8 types[NUM_LISTED_TYPES];
    u16 abilityOrder[LEGDEX_NUM_ABILITIES - 1]; // alphabetical, without ABILITY_NONE
    int holderPage;
    BOOL exiting;
} LegDexSections;

static void LegDexSections_VBlank(void *data);
static void InitBgs(LegDexSections *app);
static void FreeBgs(LegDexSections *app);
static void SortAbilities(LegDexSections *app);
static int ListCount(LegDexSections *app, int tab);
static BOOL HandleInput(LegDexSections *app);
static void Redraw(LegDexSections *app);
static void DrawTop(LegDexSections *app);
static void RedrawCursor(LegDexSections *app, int oldCursor, int oldScroll);
static void DrawList(LegDexSections *app);
static void DrawListRowAt(LegDexSections *app, int row);

// ---------------------------------------------------------------------------------------------
// Helpers

static void AppendText(LegDexSections *app, String *dst, u32 entryID)
{
    MessageLoader_GetString(app->text, entryID, app->line);
    String_Concat(dst, app->line);
}

static void AppendNumber(LegDexSections *app, String *dst, int num, int digits, enum PaddingMode padding)
{
    String_FormatInt(app->line, num, digits, padding, CHARSET_MODE_EN);
    String_Concat(dst, app->line);
}

static void AppendSpeciesName(LegDexSections *app, String *dst, int species)
{
    MessageLoader_GetString(app->speciesNames, species, app->line);
    String_Concat(dst, app->line);
}

static void Print(Window *window, const String *string, int x, int y, TextColor color)
{
    Text_AddPrinterWithParamsAndColor(window, FONT_SYSTEM, string, x, y, TEXT_SPEED_INSTANT, color, NULL);
}

static void PrintEntry(LegDexSections *app, Window *window, u32 entryID, int x, int y, TextColor color)
{
    MessageLoader_GetString(app->text, entryID, app->str2);
    Print(window, app->str2, x, y, color);
}

// Appends `item` to a comma-separated list, starting a new line when it wouldn't fit
static void AppendListItem(String *dst, const String *item, int *lineWidth, int maxWidth, BOOL first)
{
    int itemWidth = Font_CalcStringWidth(FONT_SYSTEM, item, 0);
    int spaceWidth = 4;

    if (!first) {
        String_AppendChar(dst, CHAR_COMMA);
        *lineWidth += 4;

        if (*lineWidth + spaceWidth + itemWidth > maxWidth) {
            String_AppendChar(dst, CHAR_CR);
            *lineWidth = 0;
        } else {
            String_AppendChar(dst, CHAR_SPACE);
            *lineWidth += spaceWidth;
        }
    }

    String_Concat(dst, item);
    *lineWidth += itemWidth;
}

// Prints a string line by line from `y`; returns the y below it. Lines past the screen are dropped.
static int PrintLines(LegDexSections *app, Window *window, const String *string, int x, int y, TextColor color)
{
    int numLines = String_NumLines(string);

    for (int i = 0; i < numLines && y + LINE_H <= SCREEN_H; i++) {
        String_CopyLineNum(app->line, string, i);
        Print(window, app->line, x, y, color);
        y += LINE_H;
    }

    return y;
}

static const LegDexForm *FindFormLabel(int species, int form)
{
    for (int i = 0; i < (int)NELEMS(sLegDexExtraForms); i++) {
        if (sLegDexExtraForms[i].species == species && sLegDexExtraForms[i].form == form) {
            return &sLegDexExtraForms[i];
        }
    }

    return NULL;
}

// "CHARIZARD (MEGA 2)", "TORNADUS (THERIAN FORME)", "PIKACHU"
static void AppendHolderName(LegDexSections *app, String *dst, int species, int form)
{
    AppendSpeciesName(app, dst, species);

    switch (form) {
    case 0:
        return;
    case FORM_MEGA_1:
        AppendText(app, dst, LegDexSections_Text_SuffixMega1);
        return;
    case FORM_MEGA_2:
        AppendText(app, dst, LegDexSections_Text_SuffixMega2);
        return;
    case FORM_LEGENDARY_MEGA_1:
        AppendText(app, dst, LegDexSections_Text_SuffixLegendary1);
        return;
    case FORM_LEGENDARY_MEGA_2:
        AppendText(app, dst, LegDexSections_Text_SuffixLegendary2);
        return;
    }

    const LegDexForm *label = FindFormLabel(species, form);

    if (label != NULL) {
        AppendText(app, dst, LegDexSections_Text_OpenParen);
        AppendText(app, dst, label->label);
        AppendText(app, dst, LegDexSections_Text_CloseParen);
    }
}

// "MEGA CHARIZARD 2" (list) / "LEGENDARY MEGA LUCARIO" (title)
static void AppendMegaName(LegDexSections *app, String *dst, int species, int form, BOOL title)
{
    BOOL legendary = form == FORM_LEGENDARY_MEGA_1 || form == FORM_LEGENDARY_MEGA_2;

    if (legendary) {
        AppendText(app, dst, title ? LegDexSections_Text_LegendaryTitlePrefix : LegDexSections_Text_LegendaryPrefix);
    } else {
        AppendText(app, dst, LegDexSections_Text_MegaPrefix);
    }

    AppendSpeciesName(app, dst, species);

    if (form == FORM_MEGA_2 || form == FORM_LEGENDARY_MEGA_2) {
        AppendText(app, dst, LegDexSections_Text_SecondSuffix);
    }
}

static BOOL MegaUnlocked(LegDexSections *app, int species)
{
    // Gen 5 species aren't recorded in the Pokédex save data, so their Megas are always shown
    if (species > POKEDEX_SPECIES_COUNT) {
        return TRUE;
    }

    return Pokedex_HasCaughtSpecies(app->pokedex, species);
}

static int TypeMultiplier(int attackType, int defendType)
{
    for (int i = 0; i < (int)NELEMS(sLegDexTypeChart); i++) {
        if (sLegDexTypeChart[i][0] == attackType && sLegDexTypeChart[i][1] == defendType) {
            return sLegDexTypeChart[i][2];
        }
    }

    return 10;
}

// ---------------------------------------------------------------------------------------------
// Application

BOOL LegDexSections_Init(ApplicationManager *appMan, int *state)
{
    Heap_Create(HEAP_ID_APPLICATION, HEAP_ID_LEGDEX_SECTIONS, 0x30000);

    LegDexSections *app = ApplicationManager_NewData(appMan, sizeof(LegDexSections), HEAP_ID_LEGDEX_SECTIONS);
    memset(app, 0, sizeof(LegDexSections));

    app->heapID = HEAP_ID_LEGDEX_SECTIONS;
    app->args = ApplicationManager_Args(appMan);
    app->args->choice = LEGDEX_CHOICE_EXIT;
    app->pokedex = SaveData_GetPokedex(app->args->saveData);

    SetScreenColorBrightness(DS_SCREEN_MAIN, COLOR_BLACK);
    SetScreenColorBrightness(DS_SCREEN_SUB, COLOR_BLACK);
    SetVBlankCallback(NULL, NULL);
    SetHBlankCallback(NULL, NULL);
    GXLayers_DisableEngineALayers();
    GXLayers_DisableEngineBLayers();
    GX_SetVisiblePlane(0);
    GXS_SetVisiblePlane(0);
    SetAutorepeat(4, 8);

    InitBgs(app);

    Text_ResetAllPrinters();
    app->text = MessageLoader_Init(MSG_LOADER_PRELOAD_ENTIRE_BANK, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_LEGDEX_SECTIONS, app->heapID);
    app->speciesNames = MessageLoader_Init(MSG_LOADER_PRELOAD_ENTIRE_BANK, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_SPECIES_NAME, app->heapID);
    app->abilityNames = MessageLoader_Init(MSG_LOADER_PRELOAD_ENTIRE_BANK, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_ABILITY_NAMES, app->heapID);
    app->abilityDescriptions = MessageLoader_Init(MSG_LOADER_PRELOAD_ENTIRE_BANK, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_ABILITY_DESCRIPTIONS, app->heapID);
    app->typeNames = MessageLoader_Init(MSG_LOADER_PRELOAD_ENTIRE_BANK, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_POKEMON_TYPE_NAMES, app->heapID);
    app->str = String_Init(1024, app->heapID);
    app->str2 = String_Init(256, app->heapID);
    app->line = String_Init(256, app->heapID);

    int n = 0;
    for (int type = 0; type < NUM_POKEMON_TYPES; type++) {
        if (type != TYPE_MYSTERY) {
            app->types[n++] = type;
        }
    }

    SortAbilities(app);

    if (app->args->tab >= LEGDEX_TAB_COUNT) {
        app->args->tab = LEGDEX_TAB_POKEMON;
    }

    for (int tab = 0; tab < LEGDEX_TAB_COUNT; tab++) {
        if (app->args->cursor[tab] >= ListCount(app, tab)) {
            app->args->cursor[tab] = 0;
            app->args->scroll[tab] = 0;
        }
    }

    SetVBlankCallback(LegDexSections_VBlank, app);
    GXLayers_TurnBothDispOn();

    return TRUE;
}

BOOL LegDexSections_Main(ApplicationManager *appMan, int *state)
{
    LegDexSections *app = ApplicationManager_Data(appMan);

    switch (*state) {
    case 0:
        Redraw(app);
        Bg_ToggleLayer(BG_LAYER_MAIN_0, TRUE);
        Bg_ToggleLayer(BG_LAYER_MAIN_1, TRUE);
        Bg_ToggleLayer(BG_LAYER_SUB_0, TRUE);
        StartScreenFade(FADE_BOTH_SCREENS, FADE_TYPE_BRIGHTNESS_IN, FADE_TYPE_BRIGHTNESS_IN, COLOR_BLACK, 6, 1, app->heapID);
        *state = 1;
        break;
    case 1:
        if (IsScreenFadeDone()) {
            *state = 2;
        }
        break;
    case 2:
        if (HandleInput(app)) {
            StartScreenFade(FADE_BOTH_SCREENS, FADE_TYPE_BRIGHTNESS_OUT, FADE_TYPE_BRIGHTNESS_OUT, COLOR_BLACK, 6, 1, app->heapID);
            *state = 3;
        }
        break;
    case 3:
        if (IsScreenFadeDone()) {
            return TRUE;
        }
        break;
    }

    return FALSE;
}

BOOL LegDexSections_Exit(ApplicationManager *appMan, int *state)
{
    LegDexSections *app = ApplicationManager_Data(appMan);
    enum HeapID heapID = app->heapID;

    String_Free(app->line);
    String_Free(app->str2);
    String_Free(app->str);
    MessageLoader_Free(app->typeNames);
    MessageLoader_Free(app->abilityDescriptions);
    MessageLoader_Free(app->abilityNames);
    MessageLoader_Free(app->speciesNames);
    MessageLoader_Free(app->text);

    FreeBgs(app);
    SetVBlankCallback(NULL, NULL);


    ApplicationManager_FreeData(appMan);
    Heap_Destroy(heapID);

    return TRUE;
}

static void LegDexSections_VBlank(void *data)
{
    LegDexSections *app = data;
    Bg_RunScheduledUpdates(app->bgConfig);
}

static void InitBgs(LegDexSections *app)
{
    GXBanks banks = {
        GX_VRAM_BG_128_B,
        GX_VRAM_BGEXTPLTT_NONE,
        GX_VRAM_SUB_BG_128_C,
        GX_VRAM_SUB_BGEXTPLTT_NONE,
        GX_VRAM_OBJ_NONE,
        GX_VRAM_OBJEXTPLTT_NONE,
        GX_VRAM_SUB_OBJ_NONE,
        GX_VRAM_SUB_OBJEXTPLTT_NONE,
        GX_VRAM_TEX_NONE,
        GX_VRAM_TEXPLTT_NONE,
    };

    GXLayers_SetBanks(&banks);
    app->bgConfig = BgConfig_New(app->heapID);

    GraphicsModes graphicsModes = {
        .displayMode = GX_DISPMODE_GRAPHICS,
        .mainBgMode = GX_BGMODE_0,
        .subBgMode = GX_BGMODE_0,
        .bg0As2DOr3D = GX_BG0_AS_2D,
    };

    SetAllGraphicsModes(&graphicsModes);

    BgTemplate template = {
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
        .mosaic = FALSE,
    };

    // Top screen: Pokémon sprite (layer 0) in front of the text window (layer 1)
    Bg_InitFromTemplate(app->bgConfig, BG_LAYER_MAIN_0, &template, BG_TYPE_STATIC);
    Bg_ClearTilemap(app->bgConfig, BG_LAYER_MAIN_0);

    template.screenBase = GX_BG_SCRBASE_0x0800;
    template.charBase = GX_BG_CHARBASE_0x08000;
    template.priority = 1;
    Bg_InitFromTemplate(app->bgConfig, BG_LAYER_MAIN_1, &template, BG_TYPE_STATIC);
    Bg_ClearTilemap(app->bgConfig, BG_LAYER_MAIN_1);

    // Bottom screen: tabs + list
    template.screenBase = GX_BG_SCRBASE_0x0000;
    template.charBase = GX_BG_CHARBASE_0x04000;
    template.priority = 0;
    Bg_InitFromTemplate(app->bgConfig, BG_LAYER_SUB_0, &template, BG_TYPE_STATIC);
    Bg_ClearTilemap(app->bgConfig, BG_LAYER_SUB_0);

    Bg_ToggleLayer(BG_LAYER_MAIN_0, FALSE);
    Bg_ToggleLayer(BG_LAYER_MAIN_1, FALSE);
    Bg_ToggleLayer(BG_LAYER_MAIN_2, FALSE);
    Bg_ToggleLayer(BG_LAYER_MAIN_3, FALSE);
    Bg_ToggleLayer(BG_LAYER_SUB_0, FALSE);
    Bg_ToggleLayer(BG_LAYER_SUB_1, FALSE);
    Bg_ToggleLayer(BG_LAYER_SUB_2, FALSE);
    Bg_ToggleLayer(BG_LAYER_SUB_3, FALSE);

    Bg_LoadPalette(BG_LAYER_MAIN_1, (void *)sGoldPalette, sizeof(sGoldPalette), 0);
    Bg_LoadPalette(BG_LAYER_SUB_0, (void *)sGoldPalette, sizeof(sGoldPalette), 0);
    Bg_ClearTilesRange(BG_LAYER_MAIN_0, TILE_SIZE_4BPP, 0, app->heapID);
    Bg_ClearTilesRange(BG_LAYER_MAIN_1, TILE_SIZE_4BPP, 0, app->heapID);
    Bg_ClearTilesRange(BG_LAYER_SUB_0, TILE_SIZE_4BPP, 0, app->heapID);

    Window_Add(app->bgConfig, &app->top, BG_LAYER_MAIN_1, 0, 0, 32, 24, 0, 1);
    Window_Add(app->bgConfig, &app->bottom, BG_LAYER_SUB_0, 0, 0, 32, 24, 0, 1);
}

static void FreeBgs(LegDexSections *app)
{
    Window_Remove(&app->top);
    Window_Remove(&app->bottom);

    for (int layer = BG_LAYER_MAIN_0; layer <= BG_LAYER_SUB_3; layer++) {
        Bg_ToggleLayer(layer, FALSE);
    }

    Bg_FreeTilemapBuffer(app->bgConfig, BG_LAYER_MAIN_0);
    Bg_FreeTilemapBuffer(app->bgConfig, BG_LAYER_MAIN_1);
    Bg_FreeTilemapBuffer(app->bgConfig, BG_LAYER_SUB_0);
    Heap_Free(app->bgConfig);
}

// Case-insensitive alphabetical order of two strings (< 0: a first)
static int CompareNames(const String *a, const String *b)
{
    const charcode_t *ca = String_GetData(a);
    const charcode_t *cb = String_GetData(b);

    for (int i = 0;; i++) {
        charcode_t x = ca[i], y = cb[i];

        if (x >= CHAR_a && x <= CHAR_z) {
            x = x - CHAR_a + CHAR_A;
        }

        if (y >= CHAR_a && y <= CHAR_z) {
            y = y - CHAR_a + CHAR_A;
        }

        if (x != y || x == CHAR_EOS) {
            return (int)x - (int)y;
        }
    }
}

static void SortAbilities(LegDexSections *app)
{
    int count = LEGDEX_NUM_ABILITIES - 1;
    String **names = Heap_Alloc(app->heapID, sizeof(String *) * LEGDEX_NUM_ABILITIES);

    for (int ability = 1; ability < LEGDEX_NUM_ABILITIES; ability++) {
        names[ability] = String_Init(32, app->heapID);
        MessageLoader_GetString(app->abilityNames, ability, names[ability]);
    }

    // Insertion sort by name
    for (int i = 0; i < count; i++) {
        int ability = i + 1;
        int j = i;

        while (j > 0 && CompareNames(names[app->abilityOrder[j - 1]], names[ability]) > 0) {
            app->abilityOrder[j] = app->abilityOrder[j - 1];
            j--;
        }

        app->abilityOrder[j] = ability;
    }

    for (int ability = 1; ability < LEGDEX_NUM_ABILITIES; ability++) {
        String_Free(names[ability]);
    }

    Heap_Free(names);
}

static int ListCount(LegDexSections *app, int tab)
{
    switch (tab) {
    case LEGDEX_TAB_MEGA:
        return NELEMS(sLegDexMegas);
    case LEGDEX_TAB_TYPES:
        return NUM_LISTED_TYPES;
    case LEGDEX_TAB_ABILITIES:
        return LEGDEX_NUM_ABILITIES - 1;
    default:
        return 1;
    }
}

// ---------------------------------------------------------------------------------------------
// Input

static void MoveCursor(LegDexSections *app, int delta)
{
    int tab = app->args->tab;
    int count = ListCount(app, tab);
    int cursor = app->args->cursor[tab] + delta;

    if (cursor < 0) {
        cursor = delta == -1 ? count - 1 : 0;
    } else if (cursor >= count) {
        cursor = delta == 1 ? 0 : count - 1;
    }

    if (cursor == app->args->cursor[tab]) {
        return;
    }

    int oldCursor = app->args->cursor[tab];
    int oldScroll = app->args->scroll[tab];

    app->args->cursor[tab] = cursor;

    if (cursor < app->args->scroll[tab]) {
        app->args->scroll[tab] = cursor;
    } else if (cursor >= app->args->scroll[tab] + LIST_ROWS) {
        app->args->scroll[tab] = cursor - LIST_ROWS + 1;
    }

    app->holderPage = 0;
    Sound_PlayEffect(SEQ_SE_DP_SELECT5_sseq);
    RedrawCursor(app, oldCursor, oldScroll);
}

static void ChangeTab(LegDexSections *app, int tab)
{
    app->args->tab = (tab + LEGDEX_TAB_COUNT) % LEGDEX_TAB_COUNT;
    app->holderPage = 0;
    Sound_PlayEffect(SEQ_SE_DP_SELECT5_sseq);
    Redraw(app);
}

static void Confirm(LegDexSections *app)
{
    if (app->args->tab == LEGDEX_TAB_POKEMON) {
        app->args->choice = LEGDEX_CHOICE_OPEN_LIST;
        app->exiting = TRUE;
        Sound_PlayEffect(SEQ_SE_DP_DECIDE_sseq);
    } else if (app->args->tab == LEGDEX_TAB_ABILITIES) {
        app->holderPage++; // wraps to the first page in DrawAbility
        Sound_PlayEffect(SEQ_SE_DP_DECIDE_sseq);
        DrawTop(app);
        Window_CopyToVRAM(&app->top);
    }
}

static BOOL HandleInput(LegDexSections *app)
{
    if (JOY_NEW(PAD_BUTTON_B)) {
        app->args->choice = LEGDEX_CHOICE_EXIT;
        Sound_PlayEffect(SEQ_SE_DP_DECIDE_sseq);
        return TRUE;
    }

    if (JOY_NEW(PAD_BUTTON_A)) {
        Confirm(app);
    } else if (JOY_NEW(PAD_BUTTON_R)) {
        ChangeTab(app, app->args->tab + 1);
    } else if (JOY_NEW(PAD_BUTTON_L)) {
        ChangeTab(app, app->args->tab - 1);
    } else if (JOY_REPEAT(PAD_KEY_UP)) {
        MoveCursor(app, -1);
    } else if (JOY_REPEAT(PAD_KEY_DOWN)) {
        MoveCursor(app, 1);
    } else if (JOY_REPEAT(PAD_KEY_LEFT)) {
        MoveCursor(app, -LIST_ROWS);
    } else if (JOY_REPEAT(PAD_KEY_RIGHT)) {
        MoveCursor(app, LIST_ROWS);
    } else if (gSystem.touchPressed) {
        int x = gSystem.touchX, y = gSystem.touchY;

        if (y < TAB_H) {
            int tab = x / (SCREEN_W / LEGDEX_TAB_COUNT);

            if (tab != app->args->tab) {
                ChangeTab(app, tab);
            }
        } else if (y >= LIST_Y && y < LIST_Y + LIST_ROWS * ROW_H) {
            int row = app->args->scroll[app->args->tab] + (y - LIST_Y) / ROW_H;

            if (row < ListCount(app, app->args->tab)) {
                if (row == app->args->cursor[app->args->tab]) {
                    Confirm(app);
                } else {
                    MoveCursor(app, row - app->args->cursor[app->args->tab]);
                }
            }
        }
    }

    return app->exiting;
}

// ---------------------------------------------------------------------------------------------
// Drawing

static void HideSprite(LegDexSections *app)
{
    Bg_ClearTilemap(app->bgConfig, BG_LAYER_MAIN_0);
    Bg_CopyTilemapBufferToVRAM(app->bgConfig, BG_LAYER_MAIN_0);
}

static void ShowSprite(LegDexSections *app, int species, int form)
{
    PokemonSpriteTemplate sprite;
    u16 tilemap[SPRITE_W_TILES * SPRITE_W_TILES];
    u8 *tiles = Heap_Alloc(app->heapID, SPRITE_SIZE);

    BuildPokemonSpriteTemplate(&sprite, species, GENDER_MALE, FACE_FRONT, FALSE, form, 0);
    CharacterSprite_LoadTiledData(sprite.narcID, sprite.character, app->heapID, 0, 0, SPRITE_W_TILES, SPRITE_W_TILES, tiles);
    Bg_LoadTiles(app->bgConfig, BG_LAYER_MAIN_0, tiles, SPRITE_SIZE, SPRITE_TILE);
    Heap_Free(tiles);

    void *palette = CharacterSprite_LoadPalette(sprite.narcID, sprite.palette, app->heapID);
    Bg_LoadPalette(BG_LAYER_MAIN_0, palette, PALETTE_SIZE_BYTES, PLTT_OFFSET(SPRITE_PALETTE));
    Heap_Free(palette);

    for (int i = 0; i < SPRITE_W_TILES * SPRITE_W_TILES; i++) {
        tilemap[i] = (SPRITE_TILE + i) | (SPRITE_PALETTE << 12);
    }

    Bg_LoadToTilemapRect(app->bgConfig, BG_LAYER_MAIN_0, tilemap, SPRITE_X_TILES, SPRITE_Y_TILES, SPRITE_W_TILES, SPRITE_W_TILES);
    Bg_CopyTilemapBufferToVRAM(app->bgConfig, BG_LAYER_MAIN_0);
}

static void DrawTopHeader(LegDexSections *app, const String *title)
{
    Window_FillTilemap(&app->top, COL_CREAM);
    Window_FillRectWithColor(&app->top, COL_DARK_GOLD, 0, 0, SCREEN_W, HEADER_H);
    Window_FillRectWithColor(&app->top, COL_GOLD, 0, HEADER_H - 2, SCREEN_W, 2);
    Print(&app->top, title, TEXT_LEFT, 4, TEXTCOLOR_HEADER);
}

static void DrawStrip(LegDexSections *app, u32 entryID, int y)
{
    Window_FillRectWithColor(&app->top, COL_GOLD, 0, y, SCREEN_W, LINE_H);
    PrintEntry(app, &app->top, entryID, TEXT_LEFT, y, TEXTCOLOR_STRIP);
}

static void DrawHome(LegDexSections *app)
{
    MessageLoader_GetString(app->text, LegDexSections_Text_Title, app->str);
    DrawTopHeader(app, app->str);

    MessageLoader_GetString(app->text, LegDexSections_Text_HomeInfo, app->str);
    int y = PrintLines(app, &app->top, app->str, TEXT_LEFT, 32, TEXTCOLOR_BODY);

    y += 4;
    u32 labels[] = { LegDexSections_Text_HomeCountSpecies, LegDexSections_Text_HomeCountMegas, LegDexSections_Text_HomeCountTypes, LegDexSections_Text_HomeCountAbilities };
    int counts[] = { NATIONAL_DEX_COUNT, NELEMS(sLegDexMegas), NUM_LISTED_TYPES, LEGDEX_NUM_ABILITIES - 1 };

    for (int i = 0; i < (int)NELEMS(labels); i++) {
        String_Clear(app->str);
        AppendText(app, app->str, labels[i]);
        AppendNumber(app, app->str, counts[i], 3, PADDING_MODE_NONE);
        Print(&app->top, app->str, TEXT_LEFT + 8 + (i % 2) * 112, y, TEXTCOLOR_BODY);
        y += (i % 2) * LINE_H;
    }

    y += 8;
    PrintEntry(app, &app->top, LegDexSections_Text_HomeOpen, TEXT_LEFT, y, TEXTCOLOR_BODY);
    MessageLoader_GetString(app->text, LegDexSections_Text_HomeSections, app->str);
    PrintLines(app, &app->top, app->str, TEXT_LEFT, y + LINE_H, TEXTCOLOR_BODY);
}

static void DrawMega(LegDexSections *app)
{
    const LegDexSpeciesForm *mega = &sLegDexMegas[app->args->cursor[LEGDEX_TAB_MEGA]];
    int species = mega->species;
    int form = mega->form;

    if (!MegaUnlocked(app, species)) {
        MessageLoader_GetString(app->text, LegDexSections_Text_Unknown, app->str);
        DrawTopHeader(app, app->str);
        MessageLoader_GetString(app->text, LegDexSections_Text_NotCaught, app->str);
        PrintLines(app, &app->top, app->str, TEXT_LEFT, 32, TEXTCOLOR_BODY);
        return;
    }

    String_Clear(app->str);
    AppendMegaName(app, app->str, species, form, TRUE);
    DrawTopHeader(app, app->str);
    ShowSprite(app, species, form);

    // Type
    int y = 28;
    int type1 = SpeciesData_GetFormValue(species, form, SPECIES_DATA_TYPE_1);
    int type2 = SpeciesData_GetFormValue(species, form, SPECIES_DATA_TYPE_2);

    PrintEntry(app, &app->top, LegDexSections_Text_Type, TEXT_LEFT, y, TEXTCOLOR_BODY);
    MessageLoader_GetString(app->typeNames, type1, app->str);

    if (type2 != type1) {
        String_AppendChar(app->str, CHAR_SPACE);
        String_AppendChar(app->str, CHAR_SLASH);
        String_AppendChar(app->str, CHAR_SPACE);
        MessageLoader_GetString(app->typeNames, type2, app->line);
        String_Concat(app->str, app->line);
    }

    Print(&app->top, app->str, 48, y, TEXTCOLOR_BODY);

    // Base stats, 3 per line; the total goes on the "Base stats" line
    y += LINE_H + 2;
    PrintEntry(app, &app->top, LegDexSections_Text_BaseStats, TEXT_LEFT, y, TEXTCOLOR_BODY);
    int totalY = y;
    y += LINE_H;

    static const u8 statParams[] = { SPECIES_DATA_BASE_HP, SPECIES_DATA_BASE_ATK, SPECIES_DATA_BASE_DEF, SPECIES_DATA_BASE_SP_ATK, SPECIES_DATA_BASE_SP_DEF, SPECIES_DATA_BASE_SPEED };
    static const u16 statLabels[] = { LegDexSections_Text_StatHP, LegDexSections_Text_StatAtk, LegDexSections_Text_StatDef, LegDexSections_Text_StatSpA, LegDexSections_Text_StatSpD, LegDexSections_Text_StatSpe };
    int total = 0;

    for (int i = 0; i < 6; i++) {
        int value = SpeciesData_GetFormValue(species, form, statParams[i]);
        int x = TEXT_LEFT + 8 + (i % 3) * 56;

        total += value;
        PrintEntry(app, &app->top, statLabels[i], x, y + (i / 3) * LINE_H, TEXTCOLOR_BODY);
        String_Clear(app->str);
        AppendNumber(app, app->str, value, 3, PADDING_MODE_SPACES);
        Print(&app->top, app->str, x + 24, y + (i / 3) * LINE_H, TEXTCOLOR_BODY);
    }

    PrintEntry(app, &app->top, LegDexSections_Text_StatTotal, TEXT_LEFT + 8 + 112, totalY, TEXTCOLOR_BODY);
    String_Clear(app->str);
    AppendNumber(app, app->str, total, 3, PADDING_MODE_NONE);
    Print(&app->top, app->str, TEXT_LEFT + 8 + 112 + 32, totalY, TEXTCOLOR_BODY);

    // Ability (with the description of the first one)
    y += 2 * LINE_H + 2;
    int ability1 = SpeciesData_GetFormValue(species, form, SPECIES_DATA_ABILITY_1);
    int ability2 = SpeciesData_GetFormValue(species, form, SPECIES_DATA_ABILITY_2);

    PrintEntry(app, &app->top, LegDexSections_Text_Ability, TEXT_LEFT, y, TEXTCOLOR_BODY);
    MessageLoader_GetString(app->abilityNames, ability1, app->str);

    if (ability2 != ABILITY_NONE && ability2 != ability1) {
        String_AppendChar(app->str, CHAR_SPACE);
        String_AppendChar(app->str, CHAR_SLASH);
        String_AppendChar(app->str, CHAR_SPACE);
        MessageLoader_GetString(app->abilityNames, ability2, app->line);
        String_Concat(app->str, app->line);
    }

    Print(&app->top, app->str, 64, y, TEXTCOLOR_BODY);
    y += LINE_H;
    MessageLoader_GetString(app->abilityDescriptions, ability1, app->str);
    y = PrintLines(app, &app->top, app->str, TEXT_LEFT + 8, y, TEXTCOLOR_BODY);

    // How to get it
    u32 how;

    switch (form) {
    case FORM_MEGA_2:
        how = LegDexSections_Text_HowMega2;
        break;
    case FORM_LEGENDARY_MEGA_1:
        how = LegDexSections_Text_HowLegendary1;
        break;
    case FORM_LEGENDARY_MEGA_2:
        how = LegDexSections_Text_HowLegendary2;
        break;
    default:
        how = LegDexSections_Text_HowMega1;
        break;
    }

    y += 2;
    if (y + 2 * LINE_H <= SCREEN_H) {
        PrintEntry(app, &app->top, LegDexSections_Text_HowToGet, TEXT_LEFT, y, TEXTCOLOR_BODY);
        PrintEntry(app, &app->top, how, TEXT_LEFT + 8, y + LINE_H, TEXTCOLOR_BODY);
    }
}

// "x2  FIRE, ICE" etc. for one multiplier; returns the y below it
static int DrawMatchupLine(LegDexSections *app, int y, int type, BOOL attacking, int multiplier, u32 labelEntry)
{
    int lineWidth = 0;
    BOOL first = TRUE;

    String_Clear(app->str);

    for (int i = 0; i < NUM_LISTED_TYPES; i++) {
        int other = app->types[i];
        int value = attacking ? TypeMultiplier(type, other) : TypeMultiplier(other, type);

        if (value == multiplier) {
            MessageLoader_GetString(app->typeNames, other, app->str2);
            AppendListItem(app->str, app->str2, &lineWidth, TEXT_RIGHT - 48, first);
            first = FALSE;
        }
    }

    if (first) {
        AppendText(app, app->str, LegDexSections_Text_None);
    }

    PrintEntry(app, &app->top, labelEntry, TEXT_LEFT, y, TEXTCOLOR_BODY);
    return PrintLines(app, &app->top, app->str, TEXT_LEFT + 40, y, TEXTCOLOR_BODY);
}

static void DrawType(LegDexSections *app)
{
    int type = app->types[app->args->cursor[LEGDEX_TAB_TYPES]];

    MessageLoader_GetString(app->typeNames, type, app->str);
    DrawTopHeader(app, app->str);

    int y = HEADER_H + 2;
    DrawStrip(app, LegDexSections_Text_Attacking, y);
    y += LINE_H;
    y = DrawMatchupLine(app, y, type, TRUE, TYPE_MULTI_SUPER_EFF, LegDexSections_Text_SuperEffective);
    y = DrawMatchupLine(app, y, type, TRUE, TYPE_MULTI_NOT_VERY_EFF, LegDexSections_Text_NotVeryEffective);
    y = DrawMatchupLine(app, y, type, TRUE, TYPE_MULTI_IMMUNE, LegDexSections_Text_NoEffect);

    y += 2;
    if (y + LINE_H <= SCREEN_H) {
        DrawStrip(app, LegDexSections_Text_Defending, y);
    }

    y += LINE_H;
    y = DrawMatchupLine(app, y, type, FALSE, TYPE_MULTI_SUPER_EFF, LegDexSections_Text_SuperEffective);
    y = DrawMatchupLine(app, y, type, FALSE, TYPE_MULTI_NOT_VERY_EFF, LegDexSections_Text_NotVeryEffective);
    DrawMatchupLine(app, y, type, FALSE, TYPE_MULTI_IMMUNE, LegDexSections_Text_NoEffect);
}

static void DrawAbility(LegDexSections *app)
{
    int ability = app->abilityOrder[app->args->cursor[LEGDEX_TAB_ABILITIES]];

    MessageLoader_GetString(app->abilityNames, ability, app->str);
    DrawTopHeader(app, app->str);

    MessageLoader_GetString(app->abilityDescriptions, ability, app->str);
    int y = PrintLines(app, &app->top, app->str, TEXT_LEFT, HEADER_H + 4, TEXTCOLOR_BODY);

    y += 4;
    DrawStrip(app, LegDexSections_Text_HoldersTitle, y);
    y += LINE_H + 2;

    int start = sLegDexAbilityHolderStart[ability];
    int end = sLegDexAbilityHolderStart[ability + 1];

    if (start == end) {
        PrintEntry(app, &app->top, LegDexSections_Text_NoHolders, TEXT_LEFT, y, TEXTCOLOR_BODY);
        return;
    }

    int lineWidth = 0;
    String_Clear(app->str);

    for (int i = start; i < end; i++) {
        String_Clear(app->str2);
        AppendHolderName(app, app->str2, sLegDexAbilityHolders[i].species, sLegDexAbilityHolders[i].form);
        AppendListItem(app->str, app->str2, &lineWidth, TEXT_RIGHT - TEXT_LEFT, i == start);
    }

    int numLines = String_NumLines(app->str);
    int numPages = (numLines + HOLDER_LINES - 1) / HOLDER_LINES;

    if (app->holderPage >= numPages) {
        app->holderPage = 0;
    }

    for (int i = 0; i < HOLDER_LINES; i++) {
        int lineNum = app->holderPage * HOLDER_LINES + i;

        if (lineNum >= numLines) {
            break;
        }

        String_CopyLineNum(app->line, app->str, lineNum);
        Print(&app->top, app->line, TEXT_LEFT, y + i * LINE_H, TEXTCOLOR_BODY);
    }

    if (numPages > 1) {
        PrintEntry(app, &app->top, LegDexSections_Text_MoreHolders, 192, SCREEN_H - LINE_H, TEXTCOLOR_BODY);
    }
}

static void DrawListRow(LegDexSections *app, int tab, int index, int y, TextColor color)
{
    String_Clear(app->str);

    switch (tab) {
    case LEGDEX_TAB_POKEMON:
        AppendText(app, app->str, LegDexSections_Text_PokemonList);
        break;
    case LEGDEX_TAB_MEGA: {
        const LegDexSpeciesForm *mega = &sLegDexMegas[index];

        String_AppendChar(app->str, CHAR_HASH);
        AppendNumber(app, app->str, mega->species, 3, PADDING_MODE_ZEROES);
        String_AppendChar(app->str, CHAR_SPACE);

        if (MegaUnlocked(app, mega->species)) {
            AppendMegaName(app, app->str, mega->species, mega->form, FALSE);
        } else {
            AppendText(app, app->str, LegDexSections_Text_Unknown);
        }
        break;
    }
    case LEGDEX_TAB_TYPES:
        MessageLoader_GetString(app->typeNames, app->types[index], app->str);
        break;
    case LEGDEX_TAB_ABILITIES:
        MessageLoader_GetString(app->abilityNames, app->abilityOrder[index], app->str);
        break;
    }

    Print(&app->bottom, app->str, 12, y, color);
}

static void DrawBottom(LegDexSections *app)
{
    static const u16 tabNames[LEGDEX_TAB_COUNT] = {
        LegDexSections_Text_TabPokemon,
        LegDexSections_Text_TabMega,
        LegDexSections_Text_TabTypes,
        LegDexSections_Text_TabAbilities,
    };
    int tab = app->args->tab;
    int tabW = SCREEN_W / LEGDEX_TAB_COUNT;

    Window_FillTilemap(&app->bottom, COL_CREAM);

    // Tabs
    for (int i = 0; i < LEGDEX_TAB_COUNT; i++) {
        BOOL selected = i == tab;

        Window_FillRectWithColor(&app->bottom, selected ? COL_DARK_GOLD : COL_LIGHT_GOLD, i * tabW, 0, tabW, TAB_H);
        Window_FillRectWithColor(&app->bottom, COL_GOLD, i * tabW + tabW - 1, 0, 1, TAB_H);
        MessageLoader_GetString(app->text, tabNames[i], app->str);

        int textW = Font_CalcStringWidth(FONT_SYSTEM, app->str, 0);
        Print(&app->bottom, app->str, i * tabW + (tabW - textW) / 2, 4, selected ? TEXTCOLOR_HEADER : TEXTCOLOR_TAB);
    }

    Window_FillRectWithColor(&app->bottom, COL_DARK_GOLD, 0, TAB_H - 2, SCREEN_W, 2);

    DrawList(app);

    // Controls
    u32 footer = tab == LEGDEX_TAB_POKEMON ? LegDexSections_Text_FooterHome
        : tab == LEGDEX_TAB_ABILITIES      ? LegDexSections_Text_FooterAbilities
                                           : LegDexSections_Text_FooterList;

    Window_FillRectWithColor(&app->bottom, COL_DARK_GOLD, 0, FOOTER_Y, SCREEN_W, SCREEN_H - FOOTER_Y);
    PrintEntry(app, &app->bottom, footer, 6, FOOTER_Y, TEXTCOLOR_HEADER);
}

static void DrawListRowAt(LegDexSections *app, int row)
{
    int tab = app->args->tab;
    int index = app->args->scroll[tab] + row;
    int y = LIST_Y + row * ROW_H;

    Window_FillRectWithColor(&app->bottom, COL_CREAM, 0, y, SCREEN_W - 10, ROW_H);

    if (index >= ListCount(app, tab)) {
        return;
    }

    if (index == app->args->cursor[tab]) {
        Window_FillRectWithColor(&app->bottom, COL_HIGHLIGHT, 4, y, SCREEN_W - 16, ROW_H);
        Window_FillRectWithColor(&app->bottom, COL_DARK_GOLD, 4, y, 3, ROW_H);
        DrawListRow(app, tab, index, y, TEXTCOLOR_HIGHLIGHT);
    } else {
        DrawListRow(app, tab, index, y, TEXTCOLOR_BODY);
    }
}

// The list rows and the scroll bar
static void DrawList(LegDexSections *app)
{
    int tab = app->args->tab;
    int count = ListCount(app, tab);
    int scroll = app->args->scroll[tab];

    for (int row = 0; row < LIST_ROWS; row++) {
        DrawListRowAt(app, row);
    }

    // Scroll bar
    Window_FillRectWithColor(&app->bottom, COL_CREAM, SCREEN_W - 10, LIST_Y, 10, LIST_ROWS * ROW_H);

    if (count > LIST_ROWS) {
        int barH = LIST_ROWS * ROW_H;
        int thumbH = barH * LIST_ROWS / count;
        int thumbY = LIST_Y + (barH - thumbH) * scroll / (count - LIST_ROWS);

        Window_FillRectWithColor(&app->bottom, COL_LIGHT_GOLD, SCREEN_W - 8, LIST_Y, 4, barH);
        Window_FillRectWithColor(&app->bottom, COL_DARK_GOLD, SCREEN_W - 8, thumbY, 4, thumbH < 4 ? 4 : thumbH);
    }
}

static void DrawTop(LegDexSections *app)
{
    HideSprite(app);

    switch (app->args->tab) {
    case LEGDEX_TAB_MEGA:
        DrawMega(app);
        break;
    case LEGDEX_TAB_TYPES:
        DrawType(app);
        break;
    case LEGDEX_TAB_ABILITIES:
        DrawAbility(app);
        break;
    default:
        DrawHome(app);
        break;
    }

}

static void Redraw(LegDexSections *app)
{
    DrawTop(app);
    DrawBottom(app);
    Window_CopyToVRAM(&app->top);
    Window_CopyToVRAM(&app->bottom);
}

// After the cursor moved from `oldCursor`: only the rows that changed, or the list when it scrolled
static void RedrawCursor(LegDexSections *app, int oldCursor, int oldScroll)
{
    int tab = app->args->tab;

    DrawTop(app);

    if (app->args->scroll[tab] != oldScroll) {
        DrawList(app);
    } else {
        DrawListRowAt(app, oldCursor - oldScroll);
        DrawListRowAt(app, app->args->cursor[tab] - oldScroll);
    }

    Window_CopyToVRAM(&app->top);
    Window_CopyToVRAM(&app->bottom);
}
