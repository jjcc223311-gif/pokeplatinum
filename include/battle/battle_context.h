#ifndef POKEPLATINUM_BATTLE_BATTLE_CONTEXT_H
#define POKEPLATINUM_BATTLE_BATTLE_CONTEXT_H

#include "constants/battle.h"
#include "constants/pokemon.h"

#include "struct_decls/battle_system.h"
#include "struct_decls/font_oam.h"

#include "battle/ai_context.h"
#include "battle/battle_mon.h"
#include "battle_anim/struct_ball_rotation_decl.h"

#include "char_transfer.h"
#include "sprite_system.h"

typedef struct BattleContext BattleContext;

typedef struct BattleMessage {
    u8 commandCode;
    u8 tags;
    u16 id;
    int params[6];
    int digits;
    int battler;
} BattleMessage;

typedef struct FieldConditions {
    u32 weatherTurns;
    u8 futureSightTurns[MAX_BATTLERS];
    u8 wishTurns[MAX_BATTLERS];
    u16 futureSightMove[MAX_BATTLERS];
    int futureSightAttacker[MAX_BATTLERS];
    s32 futureSightDamage[MAX_BATTLERS];
    u8 wishTarget[MAX_BATTLERS];
} FieldConditions;

typedef struct SideConditions {
    u32 reflectUser : 2;
    u32 reflectTurns : 3;
    u32 lightScreenUser : 2;
    u32 lightScreenTurns : 3;
    u32 mistUser : 2;
    u32 mistTurns : 3;
    u32 safeguardUser : 2;
    u32 safeguardTurns : 3;
    u32 followMe : 1;
    u32 followMeUser : 2;
    u32 knockedOffItemsMask : 6;
    u32 padding00_1D : 3;

    u32 spikesLayers : 2;
    u32 toxicSpikesLayers : 2;
    u32 padding04_04 : 28;
} SideConditions;

typedef struct TurnFlags {
    u32 struggling : 1;
    u32 ppDecremented : 1;
    u32 protecting : 1;
    u32 helpingHand : 1;
    u32 magicCoat : 1;
    u32 snatching : 1;
    u32 roosting : 1;
    u32 fleeing : 2;
    u32 enduring : 1;
    u32 padding00_0A : 22;

    int physicalDamageTakenFrom[MAX_BATTLERS];
    int physicalDamageLastAttacker;
    int physicalDamageAttackerMask;

    int specialDamageTakenFrom[MAX_BATTLERS];
    int specialDamageLastAttacker;
    int specialDamageAttackerMask;

    int lastDamageTaken;
    int lastAttacker;
    int assuranceDamageMask;
} TurnFlags;

typedef struct SelfTurnFlags {
    u32 skipPressureCheck : 1;
    u32 lightningRodActivated : 1;
    u32 stormDrainActivated : 1;
    u32 moldBreakerActivated : 1;
    u32 trickRoomActivated : 1;
    u32 focusItemActivated : 1;
    u32 repeatedMoveCount : 3;
    u32 padding00_09 : 23;

    int physicalDamageTaken;
    int physicalDamageLastAttacker;
    int specialDamageTaken;
    int specialDamageLastAttacker;
    int statusFlags;
    int shellBellDamageDealt;
} SelfTurnFlags;

typedef struct MoveFailFlags {
    u32 paralyzed : 1;
    u32 noEffect : 1;
    u32 imprisoned : 1;
    u32 infatuated : 1;
    u32 disabled : 1;
    u32 taunted : 1;
    u32 flinched : 1;
    u32 confused : 1;
    u32 gravity : 1;
    u32 healBlocked : 1;
    u32 padding00_0A : 22;
} MoveFailFlags;

typedef struct BattleScriptTaskData {
    BattleSystem *battleSys;
    BattleContext *battleCtx;
    BallRotation *ballRotation;
    ManagedSprite *sprites[2];
    FontOAM *fontOAM;
    CharTransferAllocation charTransferAllocation;
    int flag;
    int seqNum;
    int ball;
    int tmpData[8];
    void *tmpPtr[2];
} BattleScriptTaskData;

struct BattleContext {
    u8 curCommandState[MAX_BATTLERS];
    u8 nextCommandState[MAX_BATTLERS];

    int command;
    int commandNext;

    int fieldConditionCheckState;
    int fieldConditionCheckTemp;
    int monConditionCheckState;
    int monConditionCheckTemp;
    int sideConditionCheckState;
    int sideConditionCheckTemp;
    int turnStartCheckState;
    int turnStartCheckTemp;
    int afterMoveHitCheckState;
    int afterMoveHitCheckTemp;
    int afterMoveMessageType;
    int afterMoveMessageState;
    int afterMoveEffectState;

    int afterMoveEffectTemp;
    int beforeMoveCheckState;
    int tryMoveCheckState;
    int statusCheckState;
    int abilityCheckState;
    int switchInCheckState;
    int vanishedCheckTemp;

    int padding0060;

    int attacker;
    int attackerTemp;
    int defender;
    int defenderTemp;
    int faintedMon;
    int switchedMon;
    int switchedMonTemp;
    int abilityMon;
    int magicCoatMon;
    int sideEffectType;
    int sideEffectParam;
    int sideEffectFlags;
    int sideEffectMon;
    int lastBattlerId;

    int gainedExp;
    int sharedExp;
    int modernSharedExp;
    u32 sideGetExpMask[2];

    enum NarcID scriptNarc;
    int scriptFile;
    int scriptCursor;
    int scriptStackPointer;
    enum NarcID scriptStackNarc[BATTLE_SCRIPT_STACK_MAX];
    int scriptStackFile[BATTLE_SCRIPT_STACK_MAX];
    int scriptStackCursor[BATTLE_SCRIPT_STACK_MAX];

    int turnOrderCounter;
    int waitCounter;

    BattleMessage msgBuffer;
    int msgBattlerTemp;
    int msgAttacker;
    int msgDefender;
    int msgMoveTemp;
    int msgItemTemp;
    int msgAbilityTemp;
    int msgTemp;
    int calcTemp;
    int scriptTemp;

    u32 battlerStatusFlags[MAX_BATTLERS];
    u32 payDayCount;
    int totalTurns;
    int totalFainted[MAX_BATTLERS];
    int totalDamage[MAX_BATTLERS];
    int meFirstTurnOrder;

    BattleScriptTaskData *taskData;
    void *tmpData;

    u32 fieldConditionsMask;
    FieldConditions fieldConditions;

    u32 sideConditionsMask[NUM_BATTLE_SIDES];
    SideConditions sideConditions[NUM_BATTLE_SIDES];

    TurnFlags turnFlags[MAX_BATTLERS];
    SelfTurnFlags selfTurnFlags[MAX_BATTLERS];
    MoveFailFlags moveFailFlags[MAX_BATTLERS];

    AIContext aiContext; // has the move and item data tables
    u32 *aiScriptTemp;
    u32 aiScriptCursor;

    u32 battleStatusMask;
    u32 battleStatusMask2;

    int damage;
    int hitDamage;
    int criticalBoosts;
    int criticalMul;
    int movePower;
    int powerMul;
    int hpCalcTemp;
    int moveType;
    int moveEffectChance;
    int prizeMoneyMul;
    u32 moveStatusFlags;
    u32 sideEffectDirectFlags;
    u32 sideEffectIndirectFlags;
    u32 sideEffectAbilityFlags;
    u8 multiHitCounter;
    u8 multiHitNumHits;
    u8 battlerCounter;
    u8 beatUpCounter;

    BOOL multiHitLoop;
    u32 multiHitCheckFlags;
    u32 multiHitAccuracyCheck;

    u32 clearVolatileStatus[MAX_BATTLERS];

    u8 selectedPartySlot[MAX_BATTLERS];
    u8 switchedPartySlot[MAX_BATTLERS];
    u8 aiSwitchedPartySlot[MAX_BATTLERS];

    u32 battlerActions[MAX_BATTLERS][MAX_BATTLE_ACTIONS];
    u8 battlerActionOrder[MAX_BATTLERS];
    u8 monSpeedOrder[MAX_BATTLERS];
    u32 monSpeedValues[MAX_BATTLERS];

    u8 ioQueue[MAX_LINK_BATTLERS][MAX_BATTLERS][BATTLE_IO_QUEUE_SIZE];
    u8 ioBuffer[MAX_BATTLERS][BATTLE_IO_BUFFER_SIZE];
    int battleScript[BATTLE_SCRIPT_SIZE_MAX];

    BattleMon battleMons[MAX_BATTLERS];

    u32 moveTemp;
    u32 moveCur;
    u32 movePrev;
    u32 moveLockedInto[MAX_BATTLERS];
    u16 moveProtect[MAX_BATTLERS];
    u16 moveHit[MAX_BATTLERS];
    u16 moveHitBattler[MAX_BATTLERS];
    u16 moveHitType[MAX_BATTLERS];
    u16 movePrevByBattler[MAX_BATTLERS];
    u16 moveCopied[MAX_BATTLERS];
    u16 moveCopiedHit[MAX_BATTLERS][MAX_BATTLERS];
    u16 moveSketched[MAX_BATTLERS];
    u16 moveSelected[MAX_BATTLERS];
    u16 moveSlot[MAX_BATTLERS];
    u16 conversion2Move[MAX_BATTLERS];
    u16 conversion2Battler[MAX_BATTLERS];
    u16 conversion2Type[MAX_BATTLERS];
    u16 metronomeMove[MAX_BATTLERS];

    int storedDamage[MAX_BATTLERS];
    int lastHitByBattler[MAX_BATTLERS];
    int battlerSpeedTemp;
    u8 battlersSwitchingMask;
    u8 levelUpMons;
    u16 padding310A;

    u16 speedRand[MAX_BATTLERS];

    int flingTemp;
    int flingScript;

    u8 safariCatchStage;
    u8 safariEscapeCount;
    u8 runAttempts;
    u8 battleEndFlag;

    u8 magnitude;
    u8 fieldWeatherChecked;
    s16 hpTemp;

    u16 recycleItem[MAX_BATTLERS];

    u8 partyOrder[MAX_BATTLERS][MAX_PARTY_SIZE];

    BOOL expJinglePlayed;

    int linkBattleTimeout;

    u8 recordedCommandFlags[MAX_BATTLERS];

    int waitingBattlers;

    // Mega / Legendary Mega Evolution (player only)
    u8 megaRequested[MAX_BATTLERS]; // TRUE while the Mega button is on (form chosen by the Mega Rock); set ONLY by the Mega button, consumed at the start of the turn
    u8 legendaryRequested[MAX_BATTLERS]; // TRUE while the Legendary button is on; set ONLY by the Legendary button
    u8 megaEvolvedMask; // player party slots that have Mega Evolved this battle (once per Pokemon)
    u8 legendaryEvolvedMask; // player party slots that have Legendary Mega Evolved this battle
    u8 legendaryUsed; // Legendary Mega Evolution is once per battle for the whole team
    // Legendary Mega abilities with a charge / counter for the current stay (cleared on switch-in)
    u8 crosswireCharged[MAX_BATTLERS]; // Crosswire: an Electric hit landed
    u8 cannonSalvoCount[MAX_BATTLERS]; // Cannon Salvo: special hits landed (0-2)
    u8 rubyConduitCharged[MAX_BATTLERS]; // Ruby Conduit: took a damaging hit
    u8 royalParryUsed[MAX_BATTLERS]; // Royal Parry: already parried a contact hit
    int abilityChargeTurn[MAX_BATTLERS]; // turn the attacker's charges were last updated (once per move)
    u8 magicBounceReflected; // Magic Bounce already reflected the current move (cleared each action)
    u8 rimeCallerUsedMask[MAX_BATTLERS];
    int sideFaintedTurn[2]; // Retaliate: turn (totalTurns + 1) a Pokemon on that side last fainted
    int echoedVoiceTurn;    // Echoed Voice: turn it was last used, and how many turns in a row
    u8 echoedVoiceCount;
    u8 smackedDown[MAX_BATTLERS];      // Smack Down: grounded until it switches out
    int telekinesisUntil[MAX_BATTLERS]; // Telekinesis: last turn (totalTurns + 1) it floats
    int wideGuardTurn[2];  // Wide Guard / Quick Guard: turn (totalTurns + 1) the side is protected
    int quickGuardTurn[2];
    int wonderRoomUntil;   // Wonder Room / Magic Room: last turn they are active (0 = off)
    int magicRoomUntil;
    int fusionFlareTurn;   // Fusion Flare / Fusion Bolt: turn each was last used
    int fusionBoltTurn;
    u8 defiantPending[MAX_BATTLERS]; // Defiant: Attack +2 is due after the current move
    u8 relicSongPending[MAX_BATTLERS]; // Meloetta used Relic Song: switch Aria / Pirouette Forme
    // Once-per-battle Legendary Mega abilities: party slots (per battler's trainer) that used them
    u8 fossilCitadelUsedMask[MAX_BATTLERS];
    u8 dunePursuitUsedMask[MAX_BATTLERS];
    u8 auraConvergeUsedMask[MAX_BATTLERS];
    u8 timeLockUsedMask[MAX_BATTLERS];
    u8 azureWildfireUsedMask[MAX_BATTLERS];
    u8 distortionGateUsedMask[MAX_BATTLERS];
    u8 prismaticGraceUsedMask[MAX_BATTLERS];
    u8 seismicBreakerUsedMask[MAX_BATTLERS];
    u8 thirdEyeCurseUsedMask[MAX_BATTLERS];
    u8 omenWingsUsedMask[MAX_BATTLERS];
    u8 prismaticGracePending[MAX_BATTLERS]; // cure + heal after the current move
    u8 venomLeveragePending[MAX_BATTLERS]; // lower the poisoned foe's Defense after the current move
    u8 venomLeverageTarget[MAX_BATTLERS];
    u8 seismicBreakerPending[MAX_BATTLERS]; // show the message after the current move
    u8 omenWingsPending[MAX_BATTLERS]; // raise Attack / Speed in the next switch-in checks
    u8 wakeRunnerUsed[MAX_BATTLERS]; // this stay
    u8 emperorMantleState[MAX_BATTLERS]; // this stay: 0 waiting for a Fire hit, 1 next Fighting move +1 priority, 2 used
    u8 azureWildfirePending[MAX_BATTLERS]; // Azure Wildfire: heal + Speed after the current move
    u8 gildedClawsUsed[MAX_BATTLERS]; // Gilded Claws: first contact hit made this stay
    u8 siegeReservoirState[MAX_BATTLERS]; // Siege Reservoir this stay: 0 waiting, 1 heal at turn end, 2 done // Rime Caller: party slots (per battler's trainer) that already called hail
    // Trainer (enemy) Mega / Legendary Mega Evolution, from the Coal Badge on. Indexed by the
    // trainer's first battler (BattleSystem_TrainerMegaKey); bits = party slots.
    u8 trainerMegaRollMask[MAX_BATTLERS]; // 50% roll won: Mega 2 (form 28)
    u8 trainerLegendaryRollMask[MAX_BATTLERS]; // 50% roll won: Legendary 2 (form 31)
    u8 trainerMegaRockGivenMask[MAX_BATTLERS]; // had no item and was given a Mega Rock for this battle
    u8 trainerMegaEvolvedMask[MAX_BATTLERS];
    u8 trainerLegendaryEvolvedMask[MAX_BATTLERS];
    u8 trainerLegendaryUsed[MAX_BATTLERS]; // once per battle per trainer
    int trainerMegaTurn[MAX_BATTLERS]; // per battler: turn it Mega Evolved (Legendary waits a turn)
    u8 megaSwitchInCheck; // run the switch-in checks after a Mega Evolution (new entry abilities)
    u32 megaTrickRoomBefore; // Trick Room bits before this turn's Mega Evolutions
    u8 formChangedMask; // player party slots whose original form/ability are saved below,
    u8 megaRevertForm[MAX_PARTY_SIZE]; // to be restored when the battle ends
    u16 megaRevertAbility[MAX_PARTY_SIZE];

    u32 battleProgressFlag : 1;
    u32 padding3154_01 : 31;
};

#endif // POKEPLATINUM_BATTLE_BATTLE_CONTEXT_H
