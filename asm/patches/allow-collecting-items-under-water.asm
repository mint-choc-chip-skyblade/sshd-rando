; in item get func 1
.offset 0x084df098
mov w9, w8
mov w8, #16
bl additions_jumptable
tbnz w8, #2, 0x084df0b8 ; don't set event name if anim index == 4

.offset 0x084df0b4
nop ; don't set default item get eventFlags


; in item get func 2
.offset 0x084df2c0
mov w9, w8
mov w8, #16
bl additions_jumptable
tbnz w8, #2, 0x084df0b8 ; don't set event name if anim index == 4

.offset 0x084df2dc
mov w24, w25 ; move returned event flags into correct register
