#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (524_frost_breath) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    LoadParticleResource 0, gen5_particle_694_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 0, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 1, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 30
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x7fff, 6, 0
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 60
    PlayDelayedSoundEffect SEQ_SE_DP_W016B_sseq, BATTLE_SOUND_PAN_RIGHT, 100
    PlayDelayedSoundEffect SEQ_SE_DP_W043_sseq, BATTLE_SOUND_PAN_RIGHT, 180
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 195
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
