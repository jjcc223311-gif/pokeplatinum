#include "macros/btlcmd.inc"


// Time Sovereign: BattleSystem_TriggerEffectOnSwitch has already set (or refreshed) Trick Room
// for 5 turns.
_000:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_TRICK_ROOM
    PlayMoveAnimationOnMons BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait 
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_PLAYED_MOVE_ANIMATION
    // {0}’s {1} twisted the dimensions!
    PrintMessage BattleStrings_Text_PokemonsAbilityTwistedTheDimensions_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
