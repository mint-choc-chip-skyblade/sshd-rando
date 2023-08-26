; Don't drop the AC boko item on death in the update function.
.offset 0x082cb768
b 0x082cb820

; Don't set sceneflag on boko death if boko has a small key.
.offset 0x082c98c4
mov x22, #0x1988 ; get dAcEbc->bokoHasSmallKey offset
ldrb w22, [x27, x22] ; get dAcEbc->bokoHasSmallKey
cbnz w22, 0x082c9918

; Get item id to give from boko and put it in the register that will become
; param1 of the dAcItem actor from the boko.
.offset 0x082bbeec
ldrb w2, [x19, #0x12C] ; load 00 00 00 FF from param2 (the patched itemid)

; Get item id to give from boko and put it in the register that will become
; param1 of the dAcItem actor from the boko.
.offset 0x082bb8f4
ldrb w2, [x19, #0x12C] ; load 00 00 00 FF from param2 (the patched itemid)
