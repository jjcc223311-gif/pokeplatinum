#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (476_rage_powder) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_653_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_RIGHT, 50
    Delay 30
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1e, 8, 0
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
