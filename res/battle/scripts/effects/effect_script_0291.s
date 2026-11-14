#include "macros/btlcmd.inc"


_000:
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_DEFENDER, BATTLEMON_STATUS, MON_CONDITION_ANY, _skip
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 20

_skip:
    CalcCrit 
    CalcDamage 
    End 
