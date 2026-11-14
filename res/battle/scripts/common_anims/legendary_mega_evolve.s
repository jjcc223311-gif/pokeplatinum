#include "macros/btlanimcmd.inc"

.data

// Legendary Mega Evolution, part 1 of 2 (BATTLE_ANIMATION_LEGENDARY_MEGA_EVOLVE): same sequence as
// mega_evolve.s, but golden (gold beams and particles, gold/amber sphere) and heavier: stronger
// shakes with the background shaking too, an extra crack and a slightly longer build-up. Ends with
// the screen white and the Pokemon hidden; part 2 is legendary_mega_evolve_reveal.s.
// Not played with Battle Scene: OFF. Shortened by ~3 s (about 180 frames) from the first version
// (kept in tools/mega_pack/_anim_backup/): fewer color pulses, shorter fades and cracks.
L_0:
    // 1. CALL: a bright golden flash on the player's side...
    PlaySoundEffectL SEQ_SE_DP_W043D_sseq
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 12, BATTLE_COLOR_LIGHT_YELLOW2
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_YELLOW2, 6, 0
    WaitForAnimTasks
    // ...the scene dims, and golden beams rain down and gather onto the Pokemon
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 10, BATTLE_COLOR_BLACK
    LoadParticleResource 0, morning_sun_spa
    LoadParticleResource 1, charge_spa
    PlayLoopedSoundEffectL SEQ_SE_DP_W062_sseq, 10, 2
    CreateEmitter 0, 0, EMITTER_CB_NONE
    CreateEmitter 0, 1, EMITTER_CB_NONE
    CreateEmitter 0, 2, EMITTER_CB_NONE
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    PlaySoundEffectL SEQ_SE_DP_W234_sseq
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_YELLOW, 4, 1
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_YELLOW1, 4, 1
    WaitForAnimTasks

    // 2. SWIRL: golden light and coin glints spiral around the Pokemon, building up speed
    LoadParticleResource 2, hidden_power_spa
    LoadParticleResource 3, pay_day_spa
    PlaySoundEffectL SEQ_SE_DP_W179_sseq
    CreateEmitter 2, 1, EMITTER_CB_SET_POS_TO_ATTACKER
    CreateEmitter 3, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    PlayLoopedSoundEffectL SEQ_SE_PL_KIRAKIRA_sseq, 9, 2
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_ORANGE, 4, 0
    WaitForAnimTasks
    CreateEmitter 3, 3, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_YELLOW, 3, 0
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_YELLOW1, 2, 0
    WaitForAnimTasks

    // 3. FLASH: full-screen white flash, held a little longer (the beams and swirl finish under it)
    PlaySoundEffectC SEQ_SE_DP_W043_sseq
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 16, BATTLE_COLOR_WHITE
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 10, 4
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    UnloadParticleSystem 2
    UnloadParticleSystem 3

    // 4. COCOON: a glowing gold/amber, shimmering energy sphere covers the Pokemon
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 10, BATTLE_COLOR_DARK_YELLOW
    LoadParticleResource 0, protect_spa
    PlaySoundEffectL SEQ_SE_DP_W115_sseq
    CreateEmitter 0, 0, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 2, 0, 0, 0
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_YELLOW, 8, 2
    WaitForAnimTasks
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_LIGHT_ORANGE, 8, 1
    WaitForAnimTasks

    // 5. CRACK: the sphere shakes hard, with bright crack-like flickers (one more than Mega)
    LoadParticleResource 1, hit_2_spa
    PlaySoundEffectL SEQ_SE_DP_EGG01_sseq
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 3, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 4, 0
    WaitForAnimTasks
    PlaySoundEffectL SEQ_SE_DP_EGG01_sseq
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 5, 0, 1, 3, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_ShakeBg 2, 2, 0, 3, 0
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 5, 0
    WaitForAnimTasks
    PlaySoundEffectL SEQ_SE_DP_EGG01_sseq
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_ATTACKER
    Func_Shake 6, 0, 1, 4, BATTLE_ANIM_BATTLER_SPRITE_ATTACKER
    Func_ShakeBg 4, 4, 0, 5, 0
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 1, BATTLE_COLOR_WHITE, 7, 0
    WaitForAnimTasks

    // 6. BURST (first half): white-out; the sphere is gone while the form changes
    Func_FadeBg FADE_BG_TYPE_BASE, 0, 0, 16, BATTLE_COLOR_WHITE
    Func_HideBattler BATTLE_ANIM_ATTACKER, TRUE
    WaitForAnimTasks
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End
