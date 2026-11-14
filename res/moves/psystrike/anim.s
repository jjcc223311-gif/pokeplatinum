#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (540_psystrike) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_709_spa
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 30
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_RIGHT, 70
    PlayDelayedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_RIGHT, 77
    PlayDelayedSoundEffect SEQ_SE_DP_480_sseq, BATTLE_SOUND_PAN_RIGHT, 84
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Delay 50
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
