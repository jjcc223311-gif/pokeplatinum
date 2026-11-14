#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (519_fire_pledge) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_689_spa
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 28
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 28
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 55
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 55
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 15
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 15
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 10, 0
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 15
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
