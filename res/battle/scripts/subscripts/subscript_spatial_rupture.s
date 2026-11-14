#include "macros/btlcmd.inc"


// BTLVAR_MSG_BATTLER_TEMP's Spatial Rupture let its move go through Protect / Detect
_000:
    // {0}’s {1} pierced the protection!
    PrintMessage BattleStrings_Text_PokemonsAbilityPiercedTheProtection_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
