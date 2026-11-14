#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (552_fiery_dance) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W436_sseq, BATTLE_SOUND_PAN_RIGHT
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 8, 0
    LoadParticleResource 0, gen5_particle_725_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    PlayPannedSoundEffect SEQ_SE_DP_W436_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W436_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W436_sseq, BATTLE_SOUND_PAN_RIGHT, 80
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 60
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 50
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
