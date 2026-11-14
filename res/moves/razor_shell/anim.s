#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (534_razor_shell) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_703_spa
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT, 8
    PlayDelayedSoundEffect SEQ_SE_DP_W043_sseq, BATTLE_SOUND_PAN_RIGHT, 12
    PlayDelayedSoundEffect SEQ_SE_DP_W015_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
