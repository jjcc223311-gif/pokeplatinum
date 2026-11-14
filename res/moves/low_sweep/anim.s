#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (490_low_sweep) by tools/scripts/convert_gen5_anims.py

L_0:
    Delay 20
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_007_sseq, BATTLE_SOUND_PAN_LEFT
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 20
    LoadParticleResource 0, gen5_particle_189_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_007_sseq, BATTLE_SOUND_PAN_RIGHT
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
