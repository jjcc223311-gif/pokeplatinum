#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (531_heart_stamp) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_293_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W006_sseq, BATTLE_SOUND_PAN_RIGHT, 25
    PlayDelayedSoundEffect SEQ_SE_DP_293_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_700_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
