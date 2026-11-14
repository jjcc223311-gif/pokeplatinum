#ifndef POKEPLATINUM_CONSTANTS_DISTORTED_RIFT_H
#define POKEPLATINUM_CONSTANTS_DISTORTED_RIFT_H

// ===== TEMPORARY TEST (set to 0 / remove when done testing the Distorted Rift) =====
// 1: Mom (Twinleaf Town) offers a warp to the Turnback Cave portal room, gives 3 Legend Mega
//    Rocks once, and offers to mark every Rift pool Pokemon as caught (to test the Arceus finale).
#define RIFT_TEMP_TEST 1

#define RIFT_POOL_LEVEL   70
#define RIFT_ARCEUS_LEVEL 80

// DistortedRift script command modes
#define RIFT_CMD_PICK            0 // pick this visit's Pokemon -> VAR_RIFT_SPECIES (and destVar); 0 = rift silent
#define RIFT_CMD_SET_GFX         1 // VAR_OBJ_GFX_ID_0 = overworld sprite of VAR_RIFT_SPECIES
#define RIFT_CMD_MARK_CAUGHT     2 // set the caught flag of VAR_RIFT_SPECIES
#define RIFT_CMD_DEBUG_CATCH_ALL 3 // TEMPORARY TEST: set every pool flag (not Arceus)
#define RIFT_CMD_COUNT_LEFT      4 // destVar = pool Pokemon not caught yet

#endif // POKEPLATINUM_CONSTANTS_DISTORTED_RIFT_H
