; read and use the tbox subtype from param1
.offset 0x08b0d09c
ldr w9, [x19, #0xc] ; get param1
ubfx w10, w9, #0x4, #0x2 ; param1 >> 4 & 0x3 (shift right by 4 bits and uses the next 2 bits)

.offset 0x08b0d0a8
nop ; remove use of ITEM_TO_TBOX_SUBTYPE

; branch to jumptable
.offset 0x08b107fc
b 0x08659ab0
; b 0x08004818

; .offset 0x08004818
; b 0x360A0000
; mov x16, #0x360A5500
; br x16
; b 0x360a5500
