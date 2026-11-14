#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (480_storm_throw) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_W233_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W233_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_W233_sseq, BATTLE_SOUND_PAN_RIGHT, 73
    PlayDelayedSoundEffect SEQ_SE_DP_W233_sseq, BATTLE_SOUND_PAN_RIGHT, 77
    LoadParticleResource 0, gen5_particle_655_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 45
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
