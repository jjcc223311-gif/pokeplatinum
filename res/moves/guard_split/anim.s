#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (470_guard_split) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_564_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 0, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 1, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 2, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    PlayPannedSoundEffect SEQ_SE_DP_W025B_sseq, BATTLE_SOUND_PAN_LEFT
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 5, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 6, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 7, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 8, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 9, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 10, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveEmitterA2BLinear 11, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_DEF_TO_ATK
    Delay 10
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
