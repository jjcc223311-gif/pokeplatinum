#include "macros/btlanimcmd.inc"

.data

// Mega Evolution, part 2 of 2 (BATTLE_ANIMATION_MEGA_EVOLVE_REVEAL), played right after the form
// change: the sphere BURSTS into particles around the new Mega form, then the REVEAL (cry and
// falling rainbow sparkles). Restores everything part 1 changed (hidden sprite, white background).
L_0:
    // 6. BURST (second half): the new form appears as the sphere bursts
    LoadParticleResource 0, status_effect_spa
    LoadParticleResource 1, wish_spa
    Func_HideBattler BATTLE_ANIM_ATTACKER, FALSE
    PlaySoundEffectL SEQ_SE_DP_BOWA3_sseq
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 6, 0
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 16, 0, BATTLE_COLOR_WHITE
    WaitForAnimTasks

    // 7. REVEAL: the cry plays while rainbow sparkles fall around the Pokemon
    PlayPokemonCry 0, -117, 127
    CreateEmitter 1, 2, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 1, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    PlaySoundEffectL SEQ_SE_DP_REAPOKE_sseq
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_RED, 4, 0
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_YELLOW1, 4, 0
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
