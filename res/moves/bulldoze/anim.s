#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (523_bulldoze) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W360_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W089_sseq, BATTLE_SOUND_PAN_LEFT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W089_sseq, BATTLE_SOUND_PAN_LEFT, 45
    PlayDelayedSoundEffect SEQ_SE_DP_W089_sseq, BATTLE_SOUND_PAN_LEFT, 55
    PlayPannedSoundEffect SEQ_SE_DP_W089_sseq, BATTLE_SOUND_PAN_LEFT
    Delay 20
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    End
