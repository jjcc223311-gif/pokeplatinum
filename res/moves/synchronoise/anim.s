#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (485_synchronoise) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_050_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W103_sseq, BATTLE_SOUND_PAN_LEFT, 20
    LoadParticleResource 0, gen5_particle_660_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 81
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 86
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 91
    PlayDelayedSoundEffect SEQ_SE_DP_W010_sseq, BATTLE_SOUND_PAN_RIGHT, 97
    Delay 50
    Delay 20
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
