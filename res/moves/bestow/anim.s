#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (516_bestow) by tools/scripts/convert_gen5_anims.py

L_0:
    Delay 30
    PlayPannedSoundEffect SEQ_SE_DP_W204_sseq, BATTLE_SOUND_PAN_LEFT
    Delay 10
    LoadParticleResource 0, gen5_particle_686_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 0, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 20
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W204_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
