#include "macros/btlcmd.inc"

// Final Gambit (after the hit): the user faints

_000:
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, 0
    UpdateVar OPCODE_SET, BTLVAR_HP_CALC_TEMP, 32767
    UpdateHealthBar BTLSCR_ATTACKER
    Wait 
    End 
