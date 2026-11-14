#include "macros/btlanimcmd.inc"

.data

// Legendary Mega Evolution, part 2 of 2 (BATTLE_ANIMATION_LEGENDARY_MEGA_EVOLVE_REVEAL), played right
// after the form change: the golden sphere BURSTS around the new form, then the REVEAL (cry and a
// shower of golden sparkles and coins). Restores everything part 1 changed.
L_0:
    // 6. BURST (second half): the new form appears as the sphere bursts into golden particles
    LoadParticleResource 0, status_effect_spa
    LoadParticleResource 1, pay_day_spa
    Func_HideBattler BATTLE_ANIM_ATTACKER, FALSE
    PlaySoundEffectL SEQ_SE_DP_BOWA3_sseq
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 3, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_YELLOW2, 10, 2
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 16, 0, BATTLE_COLOR_WHITE
    WaitForAnimTasks

    // 7. REVEAL: the cry plays while golden sparkles and coins shower down around the Pokemon
    PlayPokemonCry 0, -117, 127
    CreateEmitter 1, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    PlaySoundEffectL SEQ_SE_DP_REAPOKE_sseq
    PlayLoopedSoundEffectL SEQ_SE_DP_W006_sseq, 8, 2
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_YELLOW, 5, 0
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_ORANGE, 4, 0
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
