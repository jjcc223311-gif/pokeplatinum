#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (502_ally_switch) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER
    PlayDelayedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER, 16
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 32
    PlayPannedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER
    PlayDelayedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER, 12
    PlayDelayedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER, 24
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 36
    PlayPannedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_CENTER
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 32
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    End
