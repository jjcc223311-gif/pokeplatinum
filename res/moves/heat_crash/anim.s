#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (535_heat_crash) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_704_spa
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT, 15
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 10, 0
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
