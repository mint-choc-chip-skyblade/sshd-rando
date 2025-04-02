; Sceneflag 7x10 (52) is set on item collection. This patch changes the vanilla itemflag check for
; the Life Tree Fruit and instead checks for the collection sceneflag.
.offset 0x71007da734
; call check_local_sceneflag(52)
mov w0, #52
mov w8, #79
bl additions_jumptable
cmp w0, #0
b 0x71007da778 ; 13 nops

; spawn item on tree
.offset 0x71007daa84
mov w8, #80
bl additions_jumptable

; .offset 0x71007d993c
; nop

; Allow planting seedling if the player already has the fruit
.offset 0x71007b81dc
nop
.offset 0x71007b80c0
nop
.offset 0x71007b837c
nop
