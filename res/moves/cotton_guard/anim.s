#include "macros/btlanimcmd.inc"

// Converted from the Black 2 animation (538_cotton_guard) by tools/scripts/convert_gen5_anims.py

L_0:
    PlayPannedSoundEffect SEQ_SE_DP_W464_sseq, BATTLE_SOUND_PAN_LEFT
    PlayPannedSoundEffect SEQ_SE_DP_W199_sseq, BATTLE_SOUND_PAN_LEFT
    PlayDelayedSoundEffect SEQ_SE_DP_W199_sseq, BATTLE_SOUND_PAN_LEFT, 50
    PlayDelayedSoundEffect SEQ_SE_DP_W199_sseq, BATTLE_SOUND_PAN_LEFT, 62
    PlayDelayedSoundEffect SEQ_SE_DP_W199_sseq, BATTLE_SOUND_PAN_LEFT, 70
    PlayDelayedSoundEffect SEQ_SE_DP_W199_sseq, BATTLE_SOUND_PAN_LEFT, 78
    LoadParticleResource 0, gen5_particle_707_spa
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    End
