#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (544_gear_grind) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT, 5
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT, 25
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_RIGHT, 54
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_RIGHT, 76
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_RIGHT, 75
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_RIGHT, 80
    LoadParticleResource 0, gen5_particle_713_spa
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 10, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 60
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 3
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 36
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
