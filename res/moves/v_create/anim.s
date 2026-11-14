#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (557_v_create) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W360_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_LEFT, 65
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_LEFT, 65
    PlayDelayedSoundEffect SEQ_SE_DP_W017_sseq, BATTLE_SOUND_PAN_LEFT, 140
    LoadParticleResource 0, gen5_particle_734_spa
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 12, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 13, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x12, 10, 0
    Delay 120
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    Delay 10
    Delay 2
    PlayPannedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W052_sseq, BATTLE_SOUND_PAN_RIGHT, 15
    Delay 2
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 10, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 11, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x12, 10, 0
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 30
    Delay 10
    Delay 2
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
