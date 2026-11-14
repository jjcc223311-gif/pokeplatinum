#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (527_electroweb) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_697_spa
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayDelayedSoundEffect SEQ_SE_DP_W085_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W085_sseq, BATTLE_SOUND_PAN_RIGHT, 60
    PlayDelayedSoundEffect SEQ_SE_DP_W085_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    Delay 1
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
