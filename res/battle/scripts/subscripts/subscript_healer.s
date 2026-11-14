#include "macros/btlcmd.inc"


// Healer: cures its partner's status condition. BTLSCR_MSG_BATTLER_TEMP is the Pokemon with Healer,
// BTLSCR_SIDE_EFFECT_MON its partner, BTLVAR_MSG_TEMP the condition (MSGCOND_*).
_000:
    UpdateMonData OPCODE_SET, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_STATUS, MON_CONDITION_NONE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_NIGHTMARE
    // {0}’s {1} cured its {2} status!
    PrintMessage BattleStrings_Text_PokemonsAbilityCuredItsStatus_Ally, TAG_NICKNAME_ABILITY_STATUS, BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_TEMP
    Wait 
    SetHealthBoxStatusIcon BTLSCR_SIDE_EFFECT_MON, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30
    End 
