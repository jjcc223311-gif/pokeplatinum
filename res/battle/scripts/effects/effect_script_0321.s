#include "macros/btlcmd.inc"


_000:
    Gen5MoveEffect GEN5_EFFECT_WONDER_ROOM, _other
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_WonderRoomStarted, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

_other:
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_WonderRoomEnded, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 
