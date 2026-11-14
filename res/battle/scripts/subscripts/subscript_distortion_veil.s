#include "macros/btlcmd.inc"


// Distortion Veil halved the first damaging hit BTLVAR_MSG_BATTLER_TEMP took since switching in
_000:
    // {0}’s {1} softened the blow!
    PrintMessage BattleStrings_Text_PokemonsAbilitySoftenedTheBlow_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
