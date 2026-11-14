#include "macros/btlcmd.inc"


// Seismic Breaker: Reflect / Light Screen on the target's side were broken before the damage.
_000:
    // {0}’s {1} shattered the barriers!
    PrintMessage BattleStrings_Text_PokemonsAbilityShatteredTheBarriers_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
