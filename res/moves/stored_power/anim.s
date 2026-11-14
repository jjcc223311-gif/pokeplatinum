#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (500_stored_power) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_181_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_181_sseq, BATTLE_SOUND_PAN_LEFT, 42
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x1f, 10, 0
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_672_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
