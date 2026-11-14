#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (508_shift_gear) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_LEFT, 5
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_LEFT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W231_sseq, BATTLE_SOUND_PAN_LEFT, 40
    LoadParticleResource 0, gen5_particle_678_spa
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 36
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
