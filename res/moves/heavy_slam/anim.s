#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (484_heavy_slam) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_LEFT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_LEFT, 30
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_659_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
