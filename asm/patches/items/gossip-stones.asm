; Remove Imp1 requirement to spawn Gossip Stones
; onlyif gossip_stone_treasure_shuffle == on
.offset 0x71007fb024
nop

; Don't set the Gossip Stone sceneflag after it first appears
; The flag will be set when the player collects the randomized item instead
.offset 0x71007f6bfc
nop

; Skip over switch statement deciding which item to give
; Skip to getting pos and roomid
.offset 0x71007fb1e0
mov x5, x19
b 0x71007fb25c ; 0x71007fb244

; Skip over special behaviour for Goddess Plumes
.offset 0x71007fb264
b 0x71007fb350

; setup_gossip_stone_item_params
.offset 0x71007fb360
; add x3, sp, #0x8 ; vanilla instruction
mov w8, #98
bl additions_jumptable
nop
