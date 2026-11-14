#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (503_scald) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_674_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    PlayPannedSoundEffect SEQ_SE_DP_W145C_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_LEFT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 70
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 40
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 8, 0
    Delay 10
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
