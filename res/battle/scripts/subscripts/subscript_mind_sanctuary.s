#include "macros/btlcmd.inc"


// Mind Sanctuary: BattleSystem_TriggerEffectOnSwitch has already set Reflect and Light Screen on
// the side of BTLVAR_MSG_BATTLER_TEMP for 5 turns.
_000:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_REFLECT
    PlayMoveAnimationOnMons BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait 
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_PLAYED_MOVE_ANIMATION
    // {0}’s {1} put up a barrier!
    PrintMessage BattleStrings_Text_PokemonsAbilityPutUpABarrier_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
