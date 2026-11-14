#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (473_psyshock) by tools/scripts/convert_gen5_anims.py

L_0:
    WaitForAnimTasks
    PlayPannedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_LEFT, 6
    PlayDelayedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_LEFT, 12
    PlayDelayedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_LEFT, 18
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, 12, 0, 3
    Func_MoveBattler BATTLE_ANIM_BATTLER_SPRITE_ATTACKER, -12, 0, 3
    Delay 20
    PlayPannedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_RIGHT
    PlayDelayedSoundEffect SEQ_SE_DP_W060C_sseq, BATTLE_SOUND_PAN_RIGHT, 25
    LoadParticleResource 0, gen5_particle_650_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 45
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    Delay 10
    Delay 60
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
