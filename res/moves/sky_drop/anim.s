#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (507_sky_drop) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    Delay 8
    PlayPannedSoundEffect SEQ_SE_DP_W054_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W327_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    LoadParticleResource 0, gen5_particle_460_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 30
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    PlayPannedSoundEffect SEQ_SE_DP_W327_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W327_sseq, BATTLE_SOUND_PAN_RIGHT, 12
    PlayDelayedSoundEffect SEQ_SE_DP_W327_sseq, BATTLE_SOUND_PAN_RIGHT, 24
    PlayDelayedSoundEffect SEQ_SE_DP_W327_sseq, BATTLE_SOUND_PAN_RIGHT, 36
    Delay 10
    LoadParticleResource 1, gen5_particle_184_spa
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 1, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 1, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 1, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 48
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
