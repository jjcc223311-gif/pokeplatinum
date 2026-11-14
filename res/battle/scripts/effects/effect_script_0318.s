#include "macros/btlcmd.inc"


_000:
    Gen5MoveEffect GEN5_EFFECT_FUSION_BOLT, _hit

_hit:
    CalcCrit 
    CalcDamage 
    End 
