#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (550_bolt_strike) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W120_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W120_sseq, BATTLE_SOUND_PAN_LEFT, 45
    PlayDelayedSoundEffect SEQ_SE_DP_W120_sseq, BATTLE_SOUND_PAN_LEFT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W120_sseq, BATTLE_SOUND_PAN_LEFT, 80
    PlayDelayedSoundEffect SEQ_SE_DP_W017_sseq, BATTLE_SOUND_PAN_LEFT, 130
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x3ff, 8, 0
    LoadParticleResource 0, gen5_particle_723_spa
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 9, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 7, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 60
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 10
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W120_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Func_FadeBattlerSprite BATTLE_ANIM_DEFENDER, 1, 0, 0x3ff, 8, 0
    CreateEmitter 0, 8, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 6, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 1
    Delay 20
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 20
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
