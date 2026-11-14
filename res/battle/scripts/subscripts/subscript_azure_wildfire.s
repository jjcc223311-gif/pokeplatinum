#include "macros/btlcmd.inc"


// Azure Wildfire: its first burn on a foe this battle restores 1/4 max HP (BTLVAR_HP_CALC_TEMP,
// 0 if already at full HP) and raises its Speed 1 stage. BTLVAR_MSG_BATTLER_TEMP = the user.
_000:
    CompareVarToValue OPCODE_EQU, BTLVAR_HP_CALC_TEMP, 0, _speed
    Call BATTLE_SUBSCRIPT_ABILITY_HP_RESTORE_GRADUAL

_speed:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_TYPE, SIDE_EFFECT_TYPE_ABILITY
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_MSG_BATTLER_TEMP
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_SPEED_UP_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    End 
