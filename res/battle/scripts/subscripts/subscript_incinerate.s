#include "macros/btlcmd.inc"

// Incinerate (after the hit): the target's Berry is burned up

_000:
    CompareMonDataToValue OPCODE_LTE, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_HELD_ITEM, ITEM_CHERI_BERRY - 1, _end
    CompareMonDataToValue OPCODE_GT, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_HELD_ITEM, ITEM_ROWAP_BERRY, _end
    PrintMessage BattleStrings_Text_PokemonsBerryWasBurnedUp_Ally, TAG_NICKNAME_ITEM, BTLSCR_SIDE_EFFECT_MON, BTLSCR_SIDE_EFFECT_MON
    Wait 
    WaitButtonABTime 30
    UpdateMonData OPCODE_SET, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_HELD_ITEM, ITEM_NONE

_end:
    End 
