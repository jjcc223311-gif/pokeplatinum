#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (545_searing_shot) by tools/scripts/convert_gen5_anims.py

L_0:
    Delay 10
    PlayPannedSoundEffect SEQ_SE_DP_W179_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_LEFT, 55
    LoadParticleResource 0, gen5_particle_714_spa
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x1f, 10, 0
    Delay 40
    Delay 40
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W088_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 10
    PlayDelayedSoundEffect SEQ_SE_DP_W088_sseq, BATTLE_SOUND_PAN_RIGHT, 20
    PlayDelayedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_RIGHT, 30
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x1f, 10, 0
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
