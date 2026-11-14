#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (505_heal_pulse) by tools/scripts/convert_gen5_anims.py

L_0:
    LoadParticleResource 0, gen5_particle_676_spa
    PlayPannedSoundEffect SEQ_SE_DP_W234_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W234_sseq, BATTLE_SOUND_PAN_LEFT, 15
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x421f, 5, 0
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 15
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
