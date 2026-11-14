#include "macros/btlanimcmd.inc"

.data

// Mega Evolution, part 1 of 2 (BATTLE_ANIMATION_MEGA_EVOLVE): CALL, SWIRL, FLASH, COCOON, CRACK and
// the start of the BURST. Ends with the screen white and the Pokemon hidden; subscript_mega_evolve
// then changes its form and plays part 2 (mega_evolve_reveal.s), which shows it again.
// The attacker is the Pokemon that Mega Evolves. Not played with Battle Scene: OFF.
// Timing: a sprite tint of alpha N takes about 2N frames. Shortened by ~3 s (about 180 frames)
// from the first version (kept in tools/mega_pack/_anim_backup/): fewer color pulses, shorter fades.
L_0:
    // 1. CALL: a bright flash on the player's side...
    PlaySoundEffectL SEQ_SE_DP_W043D_sseq
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 10, BATTLE_COLOR_WHITE
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 4, 0
    WaitForAnimTasks
    // ...the scene dims, and rainbow light streaks gather onto the Pokemon
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 9, BATTLE_COLOR_BLACK
    LoadParticleResource 0, charge_spa
    LoadParticleResource 1, focus_energy_spa
    PlayLoopedSoundEffectL SEQ_SE_DP_W062_sseq, 10, 2
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 0, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_RED, 3, 0
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_CYAN, 3, 0
    WaitForAnimTasks

    // 2. SWIRL: rainbow light spirals around the Pokemon, building up speed
    LoadParticleResource 2, hidden_power_spa
    PlaySoundEffectL SEQ_SE_DP_W179_sseq
    CreateEmitter 2, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    PlayLoopedSoundEffectL SEQ_SE_PL_KIRAKIRA_sseq, 10, 2
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_BLUE, 3, 0
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_PURPLE, 2, 0
    WaitForAnimTasks

    // 3. FLASH: full-screen white flash (the streaks and swirl finish under it)
    PlaySoundEffectC SEQ_SE_DP_W043_sseq
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 16, BATTLE_COLOR_WHITE
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 8, 2
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    UnloadParticleSystem 2

    // 4. COCOON: a glowing purple, shimmering energy sphere covers the Pokemon
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 9, BATTLE_COLOR_DARK_PURPLE
    LoadParticleResource 0, protect_spa
    PlaySoundEffectL SEQ_SE_DP_W115_sseq
    CreateEmitter 0, 0, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 2, 0, 0, 0
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_PURPLE, 5, 1
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_BLUE, 6, 0
    WaitForAnimTasks

    // 5. CRACK: the sphere shakes, with bright crack-like flickers
    LoadParticleResource 1, hit_2_spa
    PlaySoundEffectL SEQ_SE_DP_EGG01_sseq
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 4, 0
    WaitForAnimTasks
    PlaySoundEffectL SEQ_SE_DP_EGG01_sseq
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 4, 0, 1, 3, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 5, 0
    WaitForAnimTasks

    // 6. BURST (first half): white-out; the sphere is gone while the form changes
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 16, BATTLE_COLOR_WHITE
    Func_HideBattler BATTLE_ANIM_ATTACKER, TRUE
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
