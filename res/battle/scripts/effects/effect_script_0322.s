#include "macros/btlcmd.inc"


_000:
    Gen5MoveEffect GEN5_EFFECT_MAGIC_ROOM, _other
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_MagicRoomStarted, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

_other:
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_MagicRoomEnded, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 
