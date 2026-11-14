#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (558_fusion_flare) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_LEFT, 60
    PlayDelayedSoundEffect SEQ_SE_DP_W411_sseq, BATTLE_SOUND_PAN_LEFT, 70
    LoadParticleResource 0, gen5_particle_735_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x1f, 8, 0
    Delay 20
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 60
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 15
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayPannedSoundEffect SEQ_SE_DP_W053_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 8, 0
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
