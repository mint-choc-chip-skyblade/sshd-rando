; HANDLED IN CUSTOM FUNC NOW
; Read and use the tbox subtype from param1
; .offset 0x7100b0d09c
; ldr w9, [x19, #0xc] ; get param1
; ubfx w10, w9, #0x4, #0x2 ; param1 >> 4 & 0x3 (shift right by 4 bits and uses the next 2 bits)

.offset 0x7100b0d0a8
ldrb w10, [x27, #0x4] ; dAcTbox.chestSubtype
; nop ; remove use of ITEM_TO_TBOX_SUBTYPE


; Handle chest subtype for appearing chests
.offset 0x7100b0d048
mov w8, #34
bl additions_jumptable

; Don't show chest in dAcTbox::stateDemoAppearUpdate
.offset 0x7100b0a2d8
nop
nop
nop
nop

; .offset 0x7100b0a2e8
; Handle spawning chest at the correct animation frame
.offset 0x7100b0a200
ldrb w9, [x9, #0xd40] ; rearrange instructions
mov w8, #35
bl additions_jumptable

; Don't force chest scale 1.0 in dAcTbox::stateWaitOpenEnter
.offset 0x7100b0a6e4
nop
.offset 0x7100b0a6ec
nop

; Hide chest in dAcTbox::stateDemoAppearLeave
.offset 0x7100b0a6c4
b 0x7100659ac8 ; in custom jumptable
