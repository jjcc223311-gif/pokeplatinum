#include "macros/btlcmd.inc"


// Electric Surge: BattleSystem_TriggerEffectOnSwitch has already set (or refreshed) Electric
// Terrain for 5 turns.
_000:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_CHARGE
    PlayMoveAnimationOnMons BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait 
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_PLAYED_MOVE_ANIMATION
    // {0}’s {1} electrified the battlefield!
    PrintMessage BattleStrings_Text_PokemonsAbilityElectrifiedTheBattlefield_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    // An electric current ran across the battlefield!
    PrintMessage BattleStrings_Text_AnElectricCurrentRanAcrossTheBattlefield, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 
