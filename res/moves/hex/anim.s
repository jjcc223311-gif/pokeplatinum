#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (506_hex) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    PlayPannedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_LEFT
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_677_spa
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayDelayedSoundEffect SEQ_SE_DP_W028_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    PlayPannedSoundEffect SEQ_SE_DP_W028_sseq, BATTLE_SOUND_PAN_RIGHT
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
