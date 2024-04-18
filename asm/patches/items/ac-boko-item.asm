; Don't drop the AC boko item on death in the update function.
.offset 0x71002cb768
b 0x71002cb820

; Don't set sceneflag on boko death if boko has a small key.
.offset 0x71002c98c4
mov w8, #1
bl additions_jumptable

; .offset 0x71002c98c4
; mov x22, #0x1988 ; get dAcEbc->bokoHasSmallKey offset
; ldrb w22, [x27, x22] ; get dAcEbc->bokoHasSmallKey
; cbnz w22, 0x71002c9918

; Get item id to give from boko and put it in the register that will become
; param1 of the dAcItem actor from the boko.
.offset 0x71002bbeec
ldrb w2, [x19, #0x12C] ; load 00 00 00 FF from param2 (the patched itemid)

; handle traps
.offset 0x71002bbefc
mov w8, #53
bl additions_jumptable

; Get item id to give from boko and put it in the register that will become
; param1 of the dAcItem actor from the boko.
.offset 0x71002bb8f4
ldrb w2, [x19, #0x12C] ; load 00 00 00 FF from param2 (the patched itemid)

; handle traps
.offset 0x71002bb904
mov w8, #53
bl additions_jumptable
