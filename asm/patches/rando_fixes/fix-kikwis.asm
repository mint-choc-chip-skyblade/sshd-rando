; in vtable func
.offset 0x71005beb80
b 0x71005beb90 ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005beb9c
mov w8, #40
bl additions_jumptable


; in some unk func
.offset 0x71005bd2f4
b 0x71005bd330 ; skip 14 instructions


; in dAcNpcKyuiElder::init
.offset 0x71005c1b14
b 0x71005c1b28 ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005c1b30
mov w8, #40
bl additions_jumptable


; in dAcNpcKyuiElder::update
.offset 0x71005c2c14
nop ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005c2c20
mov w8, #40
bl additions_jumptable


; in dAcNpcKyuiElder::performInteraction
.offset 0x71005c2d5c
nop ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005c2d68
mov w8, #40
bl additions_jumptable

.offset 0x71005c2e4c
nop ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005c2e58
mov w8, #40
bl additions_jumptable


; in dAcNpcKyuiElder::changeStateAfterGettingSlingshot
.offset 0x71005c5210
nop ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005c5220
mov w8, #40
bl additions_jumptable


; in dAcNpcKyuiFirst::getForwardSpeedForNextFrame?
.offset 0x71005ca450
nop ; ignore storyflag bound check
; check if kikwi is found / is not in F100
.offset 0x71005ca460
mov w8, #40
bl additions_jumptable
