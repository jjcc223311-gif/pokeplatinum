#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (556_icicle_crash) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayDelayedSoundEffect SEQ_SE_DP_W419_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    PlayDelayedSoundEffect SEQ_SE_DP_W419_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W419_sseq, BATTLE_SOUND_PAN_RIGHT, 60
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_733_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Delay 6
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
