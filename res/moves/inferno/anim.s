#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (517_inferno) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_687_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 25
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 75
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 100
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 125
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 16
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 10, 0
    Delay 16
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 16
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1c, 10, 0
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
