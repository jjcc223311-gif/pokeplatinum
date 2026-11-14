#include "macros/btlcmd.inc"

// Cursed Body: the attacker's move was disabled (set in BattleSystem_TriggerAbilityOnHit)

_000:
    // {0}’s {1} was disabled!
    PrintMessage BattleStrings_Text_PokemonsMoveWasDisabled_Ally, TAG_NICKNAME_MOVE, BTLSCR_ATTACKER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 
