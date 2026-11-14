#include "macros/btlcmd.inc"


// Distortion Gate: the controller has already reset the attacker's positive stat stages.
// BTLVAR_MSG_BATTLER_TEMP = the Distortion Gate user (the defender).
_000:
    // {0}’s {1} erased {2}’s boosts!
    PrintMessage BattleStrings_Text_PokemonsAbilityErasedPokemonsBoosts_AllyAlly, TAG_NICKNAME_ABILITY_NICKNAME, BTLSCR_DEFENDER, BTLSCR_DEFENDER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    End 
