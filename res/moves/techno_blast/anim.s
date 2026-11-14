#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (546_techno_blast) by tools/scripts/convert_gen5_anims.py

L_0:
    Delay 20
    Delay 30
    PlayPannedSoundEffect SEQ_SE_DP_W161_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W161_sseq, BATTLE_SOUND_PAN_LEFT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W161_sseq, BATTLE_SOUND_PAN_LEFT, 55
    PlayDelayedSoundEffect SEQ_SE_DP_W161_sseq, BATTLE_SOUND_PAN_LEFT, 65
    LoadParticleResource 0, gen5_particle_715_spa
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 70
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveEmitterA2BLinear 4, 0, 0, 0, 12, 64, EMITTER_ANIMATION_MODE_ATK_TO_DEF
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W161_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W465_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
