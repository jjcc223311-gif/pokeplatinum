#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (513_reflect_type) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_683_spa
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x7fff, 8, 0
    PlayPannedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_RIGHT, 29
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    WaitForAnimTasks
    PlayDelayedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_LEFT, 20
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 30
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x7fff, 8, 0
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
