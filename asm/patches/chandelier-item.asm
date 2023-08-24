; Patch chandelier heart piece
.offset 0x08768694
ldrb w9, [x19, 0xD] ; load 00 00 FF 00 from param1 (the patched itemid)

; Force itemsubtype 9 (rearrange vanilla instruction order)
and w8, w8, #0x3fc00
orr w1, w8, w9
movk w1, #9, LSL #16 ; itemsubtype9


; Patch chandelier heart piece it another place xD
.offset 0x08768770
ldrb w9, [x19, 0xD] ; load 00 00 FF 00 from param1 (the patched itemid)

; Force itemsubtype 9 (swaps vanilla instruction order)
orr w1, w8, w9
movk w1, #9, LSL #16 ; itemsubtype9


; Allow bonking down chandelier during Levias quest.
.offset 0x08767160
b 0x087671d0 ; branch over storyflag checks
