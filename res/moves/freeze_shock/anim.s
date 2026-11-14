#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (553_freeze_shock) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_025_sseq, BATTLE_SOUND_PAN_LEFT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_025_sseq, BATTLE_SOUND_PAN_LEFT, 20
    LoadParticleResource 0, gen5_particle_726_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
