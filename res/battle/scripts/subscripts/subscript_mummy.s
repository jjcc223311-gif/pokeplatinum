#include "macros/btlcmd.inc"

// Mummy: the attacker's ability became Mummy (set in BattleSystem_TriggerAbilityOnHit)

_000:
    // {0} acquired {1}!
    PrintMessage BattleStrings_Text_PokemonAcquiredAbility_Ally, TAG_NICKNAME_ABILITY, BTLSCR_ATTACKER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    End 
