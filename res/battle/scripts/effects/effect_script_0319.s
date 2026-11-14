#include "macros/btlcmd.inc"


_000:
    Gen5MoveEffect GEN5_EFFECT_WIDE_GUARD, _other
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_WideGuardProtectedTheTeam, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

_other:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 
