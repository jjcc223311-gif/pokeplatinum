#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (521_volt_switch) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W028_sseq, BATTLE_SOUND_PAN_LEFT, 70
    LoadParticleResource 0, gen5_particle_692_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 60
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 3, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 20
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W082_sseq, BATTLE_SOUND_PAN_RIGHT
    Delay 20
    Delay 20
    Delay 10
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
