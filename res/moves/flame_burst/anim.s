#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (481_flame_burst) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_656_spa
    PlayPannedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 12
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 4
    PlayPannedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 8, 0
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
