#include "macros/btlcmd.inc"


// Mega / Legendary Mega Evolution at the start of the turn. Before this runs,
// BattleSystem_PrepareMegaEvolution has set the battler's form and types, put its new ability in
// BTLVAR_CALC_TEMP, and put the first of its two animations in BTLVAR_SCRIPT_TEMP
// (BATTLE_ANIMATION_MEGA_EVOLVE or BATTLE_ANIMATION_LEGENDARY_MEGA_EVOLVE).
// Like subscript_form_change, but the Mega animation replaces the mosaic: part 1 plays, the form
// changes, then part 2 (the _REVEAL animation right after it) plays. With Battle Scene: OFF both
// animations are skipped and the form simply changes. Stats are recalculated in the party Pokemon
// when the ability update is synced, and the battler reloads the new stats.
_000:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_RECALC_MON_STATS
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_MSG_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_SUBSTITUTE, _NoSubstituteIn
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_SUB_OUT
    Wait 
    RestoreSprite BTLSCR_MSG_TEMP
    Wait 
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_SUB_IN
    Wait 

_NoSubstituteIn:
    PlayBattleAnimationFromVar BTLSCR_MSG_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    ChangeForm BTLSCR_MSG_TEMP
    UpdateVar OPCODE_ADD, BTLVAR_SCRIPT_TEMP, 1
    PlayBattleAnimationFromVar BTLSCR_MSG_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    // {0} transformed!
    PrintMessage BattleStrings_Text_PokemonTransformed_Ally, TAG_NICKNAME, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_MSG_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_SUBSTITUTE, _NoSubstituteOut
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_SUB_OUT
    Wait 
    RefreshSprite BTLSCR_MSG_TEMP
    Wait 
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_SUB_IN
    Wait 

_NoSubstituteOut:
    RefreshMonData BTLSCR_MSG_BATTLER_TEMP
    End 
