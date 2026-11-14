#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (559_fusion_bolt) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_LEFT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_LEFT, 80
    PlayDelayedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_RIGHT, 130
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x5980, 12, 0
    LoadParticleResource 0, gen5_particle_737_spa
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 30
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 40
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 80
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    PlayPannedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_KAMI_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    Delay 15
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x5980, 12, 0
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    Delay 26
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
