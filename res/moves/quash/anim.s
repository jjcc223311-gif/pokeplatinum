#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (511_quash) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W118_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W054_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W020_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W020_sseq, BATTLE_SOUND_PAN_RIGHT, 60
    LoadParticleResource 0, gen5_particle_681_spa
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
