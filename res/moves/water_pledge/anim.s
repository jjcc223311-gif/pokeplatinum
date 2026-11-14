#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (518_water_pledge) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_688_spa
    PlayPannedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT, 80
    PlayPannedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_RIGHT, 80
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
