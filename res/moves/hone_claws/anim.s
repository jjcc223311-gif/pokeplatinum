#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (468_hone_claws) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_648_spa
    PlayPannedSoundEffect SEQ_SE_DP_W014_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_LEFT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W014_sseq, BATTLE_SOUND_PAN_LEFT, 20
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_LEFT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_W014_sseq, BATTLE_SOUND_PAN_LEFT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_LEFT, 50
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
