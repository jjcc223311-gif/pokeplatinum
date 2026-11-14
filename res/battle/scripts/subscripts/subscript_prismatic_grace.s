#include "macros/btlcmd.inc"


// Prismatic Grace: cure the status an opposing move just gave it (BTLVAR_MSG_TEMP = which status,
// for the message) and restore BTLVAR_HP_CALC_TEMP HP (0 at full HP). BTLVAR_MSG_BATTLER_TEMP = user.
_000:
    UpdateMonData OPCODE_SET, BTLSCR_MSG_TEMP, BATTLEMON_STATUS, MON_CONDITION_NONE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_MSG_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_NIGHTMARE
    // {0}’s {1} cured its {2} status!
    PrintMessage BattleStrings_Text_PokemonsAbilityCuredItsStatus_Ally, TAG_NICKNAME_ABILITY_STATUS, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_TEMP
    Wait 
    SetHealthBoxStatusIcon BTLSCR_MSG_TEMP, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30
    CompareVarToValue OPCODE_EQU, BTLVAR_HP_CALC_TEMP, 0, _end
    Call BATTLE_SUBSCRIPT_ABILITY_HP_RESTORE_GRADUAL

_end:
    End 
