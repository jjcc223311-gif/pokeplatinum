#include "macros/btlcmd.inc"


_000:
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_HELD_ITEM, 0, _skip
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 20

_skip:
    CalcCrit 
    CalcDamage 
    End 
