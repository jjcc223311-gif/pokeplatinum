#include "macros/btlcmd.inc"


_000:
    // Ally Switch only works in double battles (swapping positions is not supported yet)
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 
