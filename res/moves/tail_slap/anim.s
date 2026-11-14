#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (541_tail_slap) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_710_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_030C_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_030C_sseq, BATTLE_SOUND_PAN_RIGHT
    Delay 10
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
