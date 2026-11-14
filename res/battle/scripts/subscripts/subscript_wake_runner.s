#include "macros/btlcmd.inc"


// Wake Runner: the controller has already cleared the hazards on the user's side.
_000:
    // {0}’s {1} washed away the hazards!
    PrintMessage BattleStrings_Text_PokemonsAbilityWashedAwayTheHazards_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
