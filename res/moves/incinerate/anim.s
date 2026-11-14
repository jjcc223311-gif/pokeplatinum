#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (510_incinerate) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_680_spa
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT, 40
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 10, 0
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 15
    Delay 20
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
