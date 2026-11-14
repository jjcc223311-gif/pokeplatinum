#include "macros/btlcmd.inc"


_000:
    CheckSynchronoise _fail
    CalcCrit 
    CalcDamage 
    End 

_fail:
    PrintAttackMessage 
    Wait 
    WaitButtonABTime 30
    // {0} wasn’t affected!
    PrintMessage BattleStrings_Text_PokemonWasntAffected_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_NO_MORE_WORK
    End 
