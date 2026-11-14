#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (520_grass_pledge) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_690_spa
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_211_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
