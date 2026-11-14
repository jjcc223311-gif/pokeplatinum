// wonder_room: the Black 2 animation is background / camera only (not convertible), so this is
// trick_room's animation.
#include "macros/btlanimcmd.inc"

L_0:
    SetVar BATTLE_ANIM_VAR_BG_MOVE_STEP_X, 0
    SetVar BATTLE_ANIM_VAR_BG_MOVE_STEP_Y, 0
    SetVar BATTLE_ANIM_VAR_BG_ANIM_MODE, 0
    SetVar BATTLE_ANIM_VAR_BG_SCREEN_MODE, 0
    SetVar BATTLE_ANIM_VAR_BG_BLEND_TYPE, 1
    SwitchBg 57, BATTLE_BG_SWITCH_MODE_BLEND
    PlayDelayedSoundEffectC SEQ_SE_DP_061_sseq, 2
    WaitForBgSwitch
    Delay 60
    SetVar BATTLE_ANIM_VAR_BG_MOVE_STEP_X, 0
    SetVar BATTLE_ANIM_VAR_BG_MOVE_STEP_Y, 0
    SetVar BATTLE_ANIM_VAR_BG_ANIM_MODE, 0
    SetVar BATTLE_ANIM_VAR_BG_SCREEN_MODE, 0
    SetVar BATTLE_ANIM_VAR_BG_BLEND_TYPE, 2
    RestoreBg 57, BATTLE_BG_SWITCH_MODE_BLEND
    WaitForBgSwitch
    End
