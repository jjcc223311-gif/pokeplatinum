#include "macros/btlcmd.inc"


// Rime Caller: the controller has already started 5 turns of hail.
_000:
    PlayBattleAnimation BTLSCR_PLAYER, BATTLE_ANIMATION_WEATHER_HAIL
    Wait 
    WaitButtonABTime 15
    // {0}’s {1} whipped up a hailstorm!
    PrintMessage BattleStrings_Text_PokemonsAbilityWhippedUpAHailstorm_Ally, TAG_NICKNAME_ABILITY, BTLSCR_MSG_TEMP, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 
