#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (547_relic_song) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W047_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_720_spa
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 6
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 2, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 5, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 6, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 7, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 8, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 9, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 10, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 6
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 11, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 10
    Delay 40
    PlayPannedSoundEffect SEQ_SE_DP_W255_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W255_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
