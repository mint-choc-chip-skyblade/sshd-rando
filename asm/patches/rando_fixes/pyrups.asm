; Don't breathe fire while the player is underground
.offset 0x71003687ec
mov w8, #63
bl additions_jumptable

.offset 0x7100368d4c
mov w8, #63
bl additions_jumptable

.offset 0x7100367d28
mov w8, #63
bl additions_jumptable

.offset 0x7100367994
mov w8, #63
bl additions_jumptable

; separate patch for dAcEhidokari::stateWalkShellUpdate because it's ✨ unique ✨
.offset 0x710036833c
mov w8, #64
bl additions_jumptable
cbz w0, 0x7100368350
; the next 2 instructions ensure the state is NOT set to the fire one if w0 != 1
