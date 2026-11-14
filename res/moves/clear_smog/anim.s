#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (499_clear_smog) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W109_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_671_spa
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 0, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    WaitForAnimTasks
    Delay 20
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W109_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
