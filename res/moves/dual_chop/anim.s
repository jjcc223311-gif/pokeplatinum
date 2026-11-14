#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (530_dual_chop) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_699_spa
    PlayPannedSoundEffect SEQ_SE_DP_W221B_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 11
    PlayDelayedSoundEffect SEQ_SE_DP_W221B_sseq, BATTLE_SOUND_PAN_RIGHT, 44
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Delay 20
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
