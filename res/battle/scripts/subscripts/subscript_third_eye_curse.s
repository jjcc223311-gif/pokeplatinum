#include "macros/btlcmd.inc"


// Third-Eye Curse: the controller has already disabled the target's last move (BTLVAR_MSG_MOVE_TEMP)
// for 2 turns.
_000:
    // {0}’s {1} was disabled!
    PrintMessage BattleStrings_Text_PokemonsMoveWasDisabled_Ally, TAG_NICKNAME_MOVE, BTLSCR_DEFENDER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 
