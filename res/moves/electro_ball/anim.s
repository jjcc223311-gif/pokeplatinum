#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (486_electro_ball) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_661_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    PlayPannedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_LEFT, 70
    Delay 70
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W255_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
