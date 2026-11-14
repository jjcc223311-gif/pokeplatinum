#include "macros/btlcmd.inc"


_000:
    Gen5MoveEffect GEN5_EFFECT_QUASH, _other
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    PrintMessage BattleStrings_Text_PokemonsMoveWasPostponed_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    End 

_other:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 
