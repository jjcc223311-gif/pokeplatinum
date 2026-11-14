#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (551_blue_flare) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    WaitForAnimTasks
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_724_spa
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 8
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 16
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 24
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT, 35
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 8, 0
    Delay 140
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 40
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 6
    Delay 30
    Delay 2
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
