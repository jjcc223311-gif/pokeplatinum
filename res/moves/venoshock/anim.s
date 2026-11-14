#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (474_venoshock) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_651_spa
    PlayPannedSoundEffect SEQ_SE_DP_W145B_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W145B_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W145B_sseq, BATTLE_SOUND_PAN_RIGHT, 70
    PlayPannedSoundEffect SEQ_SE_DP_W145B_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 40
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
