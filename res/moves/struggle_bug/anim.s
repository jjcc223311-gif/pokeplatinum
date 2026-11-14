#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (522_struggle_bug) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W255_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W405_sseq, BATTLE_SOUND_PAN_LEFT, 30
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 10
    LoadParticleResource 0, gen5_particle_693_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    LoadParticleResource 1, gen5_particle_425_spa
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W405_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W405_sseq, BATTLE_SOUND_PAN_RIGHT, 5
    PlayDelayedSoundEffect SEQ_SE_DP_W405_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayPannedSoundEffect SEQ_SE_DP_W405_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
