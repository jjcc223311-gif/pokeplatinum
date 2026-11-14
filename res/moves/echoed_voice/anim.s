#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (497_echoed_voice) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W103_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_212_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    LoadParticleResource 1, gen5_particle_669_spa
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 40
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
