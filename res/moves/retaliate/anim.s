#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (514_retaliate) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W207_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W207_sseq, BATTLE_SOUND_PAN_LEFT, 40
    LoadParticleResource 0, gen5_particle_684_spa
    WaitForAnimTasks
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W026_sseq, BATTLE_SOUND_PAN_LEFT
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 16
    PlayPannedSoundEffect SEQ_SE_DP_W207_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W207_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W207_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
