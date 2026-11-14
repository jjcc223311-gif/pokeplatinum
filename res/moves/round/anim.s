#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (496_round) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_LEFT, 55
    PlayPannedSoundEffect SEQ_SE_DP_W047_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_668_spa
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x295e, 12, 0
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 2, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 5, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 6, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 7, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 8, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 9, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 10, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 11, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 12, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 13, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 1
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 14, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    WaitForAnimTasks
    Delay 5
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
