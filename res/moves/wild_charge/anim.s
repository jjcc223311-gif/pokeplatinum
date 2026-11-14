#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (528_wild_charge) by tools/scripts/convert_gen5_anims.py

L_0:
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x32d6, 14, 0
    LoadParticleResource 0, gen5_particle_379_spa
    PlayPannedSoundEffect SEQ_SE_DP_W209_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W006_sseq, BATTLE_SOUND_PAN_LEFT, 75
    PlayDelayedSoundEffect SEQ_SE_DP_W006_sseq, BATTLE_SOUND_PAN_LEFT, 105
    PlayDelayedSoundEffect SEQ_SE_DP_W209_sseq, BATTLE_SOUND_PAN_LEFT, 70
    PlayDelayedSoundEffect SEQ_SE_DP_W209_sseq, BATTLE_SOUND_PAN_LEFT, 100
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 30
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    Func_Shake 2, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    Delay 12
    PlayPannedSoundEffect SEQ_SE_DP_W209_sseq, BATTLE_SOUND_PAN_RIGHT
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 4, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 5, EMITTER_CB_SET_POS_TO_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
