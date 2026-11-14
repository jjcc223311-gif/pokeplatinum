#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (555_snarl) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W103_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W054_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_732_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 40
    PlayDelayedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_RIGHT, 15
    PlayDelayedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
