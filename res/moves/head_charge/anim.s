#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (543_head_charge) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_LEFT, 10
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W029_sseq, BATTLE_SOUND_PAN_RIGHT, 5
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    LoadParticleResource 0, gen5_particle_712_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 40
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
