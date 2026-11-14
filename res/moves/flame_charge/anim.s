#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (488_flame_charge) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_LEFT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_LEFT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_LEFT, 100
    PlayDelayedSoundEffect SEQ_SE_DP_W172_sseq, BATTLE_SOUND_PAN_LEFT, 130
    LoadParticleResource 0, gen5_particle_663_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x1f, 8, 0
    Delay 120
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    Delay 20
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
