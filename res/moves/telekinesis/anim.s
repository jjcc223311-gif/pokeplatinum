#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (477_telekinesis) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 1, 0, 0x7fff, 12, 0
    LoadParticleResource 0, gen5_particle_367_spa
    PlayPannedSoundEffect SEQ_SE_DP_W006_sseq, BATTLE_SOUND_PAN_LEFT
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W213_sseq, BATTLE_SOUND_PAN_RIGHT
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
