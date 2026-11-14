#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (554_ice_burn) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_025_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_025_sseq, BATTLE_SOUND_PAN_LEFT
    LoadParticleResource 0, gen5_particle_730_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 6
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 4
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
