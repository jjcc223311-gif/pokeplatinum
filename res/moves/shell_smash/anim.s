#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (504_shell_smash) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayDelayedSoundEffect SEQ_SE_DP_W179_sseq, BATTLE_SOUND_PAN_LEFT, 20
    WaitForAnimTasks
    LoadParticleResource 0, gen5_particle_675_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 10
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 10
    PlayPannedSoundEffect SEQ_SE_DP_W155_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W043_sseq, BATTLE_SOUND_PAN_LEFT, 5
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
