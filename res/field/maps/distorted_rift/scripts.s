#include "macros/scrcmd.inc"
#include "constants/distorted_rift.h"
#include "res/text/bank/distorted_rift.h"


    ScriptEntry DistortedRift_OnTransition
    ScriptEntry DistortedRift_Portal
    ScriptEntry DistortedRift_Legendary
    ScriptEntry DistortedRift_OnLoad
    ScriptEntryEnd

DistortedRift_OnTransition:
    InitPersistedMapFeaturesForDistortionWorld
    DistortedRift RIFT_CMD_SET_GFX, VAR_RESULT
    End

DistortedRift_OnLoad:
    GoToIfSet FLAG_MAP_LOCAL_REMOVE_OBJECT, DistortedRift_RemoveLegendary
    End

DistortedRift_RemoveLegendary:
    RemoveObject DIST_WORLD_MAP_OBJECT_RIFT_LEGENDARY
    End

DistortedRift_Portal:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    Message DistortedRift_Text_LeapIntoPortal
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, DistortedRift_GoToTurnbackCave
    CloseMessage
    ReleaseAll
    End

DistortedRift_GoToTurnbackCave:
    BufferPlayerName 0
    Message DistortedRift_Text_PlayerLeaptIntoPortal
    CloseMessage
    PlaySE SEQ_SE_PL_SYUWA_sseq
    SetPartyGiratinaForm GIRATINA_FORM_ALTERED
    FadeScreenOut
    WaitFadeScreen
    Warp MAP_HEADER_TURNBACK_CAVE_GIRATINA_ROOM, 11, 15, DIR_SOUTH
    FadeScreenIn
    WaitFadeScreen
    End

// One encounter per visit: the Pokemon is gone after the battle whatever the result. Only a
// capture removes it from the pool (RIFT_CMD_MARK_CAUGHT).
DistortedRift_Legendary:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    WaitSE SE_CONFIRM_sseq_3
    SetVar VAR_0x8004, RIFT_POOL_LEVEL
    GoToIfNe VAR_RIFT_SPECIES, SPECIES_ARCEUS, DistortedRift_LegendaryCry
    SetVar VAR_0x8004, RIFT_ARCEUS_LEVEL
    Message DistortedRift_Text_ArceusDescends
    CloseMessage
DistortedRift_LegendaryCry:
    PlayCry VAR_RIFT_SPECIES
    WaitCry
    SetFlag FLAG_RIFT_LEGENDARY_GONE
    SetFlag FLAG_MAP_LOCAL_REMOVE_OBJECT
    StartLegendaryBattle VAR_RIFT_SPECIES, VAR_0x8004
    ClearFlag FLAG_MAP_LOCAL_REMOVE_OBJECT
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, DistortedRift_BlackOut
    CheckDidNotCapture VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, DistortedRift_Vanished
    DistortedRift RIFT_CMD_MARK_CAUGHT, VAR_RESULT
    ReleaseAll
    End

DistortedRift_Vanished:
    BufferSpeciesNameFromVar 0, VAR_RIFT_SPECIES, 0, 0
    Message DistortedRift_Text_VanishedIntoTheVoid
    WaitButton
    CloseMessage
    ReleaseAll
    End

DistortedRift_BlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

    .balign 4, 0
