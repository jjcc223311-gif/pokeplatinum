#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (537_steamroller) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W011_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    PlayDelayedSoundEffect SEQ_SE_DP_W036_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    LoadParticleResource 0, gen5_particle_706_spa
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 24
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
