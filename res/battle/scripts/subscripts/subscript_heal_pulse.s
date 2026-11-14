#include "macros/btlcmd.inc"

// Heal Pulse: restores half of the target's max HP

_000:
    PrintAttackMessage 
    Wait 
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 2
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_DEFENDER
    Call BATTLE_SUBSCRIPT_RECOVER_HP
    End 
