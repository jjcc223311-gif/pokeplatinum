#include "macros/btlcmd.inc"


// Electric Terrain: the caller has already set FIELD_CONDITION_ELECTRIC_TERRAIN_INIT (5 turns).
_000:
    // An electric current ran across the battlefield!
    PrintMessage BattleStrings_Text_AnElectricCurrentRanAcrossTheBattlefield, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 
