; in dAcItem::stateWaitGetDemoUpdate
.offset 0x71004df098
mov w9, w8
mov w8, #16
bl additions_jumptable
tbnz w8, #2, 0x71004df0b8 ; don't set event name if anim index == 4

.offset 0x71004df0b4
nop ; don't set default item get eventFlags


; in dAcItem::stateWaitForcedGetDemoUpdate
.offset 0x71004df2c0
mov w9, w8
mov w8, #16
bl additions_jumptable
tbnz w8, #2, 0x71004df0b8 ; don't set event name if anim index == 4

.offset 0x71004df2dc
mov w24, w25 ; move returned event flags into correct register
