#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (512_acrobatics) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W013B_sseq, BATTLE_SOUND_PAN_LEFT
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 16
    PlayDelayedSoundEffect SEQ_SE_DP_W013B_sseq, BATTLE_SOUND_PAN_RIGHT, 15
    PlayDelayedSoundEffect SEQ_SE_DP_W013B_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    LoadParticleResource 0, gen5_particle_682_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 12
    Delay 20
    PlayDelayedSoundEffect SEQ_SE_DP_W013B_sseq, BATTLE_SOUND_PAN_LEFT, 15
    Delay 20
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
