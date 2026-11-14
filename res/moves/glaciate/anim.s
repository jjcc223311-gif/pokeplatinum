#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (549_glaciate) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_LEFT, 20
    LoadParticleResource 0, gen5_particle_722_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 100
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 170
    PlayDelayedSoundEffect SEQ_SE_DP_W043_sseq, BATTLE_SOUND_PAN_RIGHT, 90
    Delay 30
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 40
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x7fff, 8, 0
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
