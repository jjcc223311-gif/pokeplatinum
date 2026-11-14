#include "macros/btlcmd.inc"

// Smack Down (after the hit): an airborne target is grounded

_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_CUR_HP, 0, _end
    TrySmackDown BTLSCR_SIDE_EFFECT_MON, _end
    PrintMessage BattleStrings_Text_PokemonFellStraightDown_Ally, TAG_NICKNAME, BTLSCR_SIDE_EFFECT_MON
    Wait 
    WaitButtonABTime 30

_end:
    End 
