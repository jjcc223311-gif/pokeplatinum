#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (526_work_up) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W048_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W077_sseq, BATTLE_SOUND_PAN_LEFT, 50
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x1ff, 8, 0
    LoadParticleResource 0, gen5_particle_696_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
