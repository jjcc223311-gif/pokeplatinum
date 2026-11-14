#include "macros/btlcmd.inc"


// Zen Mode Darmanitan and Meloetta (after Relic Song) change form in battle. Before this runs,
// BattleSystem_PrepareBattleFormChange has set the battler's form and types and put its ability
// (unchanged) in BTLVAR_CALC_TEMP. Syncing the ability recalculates the party Pokemon's stats for
// the new form; the battler then reloads them.
_000:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_RECALC_MON_STATS
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    Call BATTLE_SUBSCRIPT_FORM_CHANGE
    RefreshMonData BTLSCR_MSG_BATTLER_TEMP
    End 
