; Prevent Trial Gates from closing even if the flag
; to close them is set

; Faron Trial Gate
.offset 0x71009dd088
nop

.offset 0x71009d93f8
nop

; Eldin Trial Gate
.offset 0x71009dd0b0
nop

.offset 0x71009d9420
nop

; Lanayru Trial Gate
.offset 0x71009dd0d8
nop

.offset 0x71009d9448
nop

; Skyloft Trial Gate
.offset 0x71009dd110
b 0x71009dd0e8

.offset 0x71009d9474
b 0x71009d94f8

; Skip over dAcOWarp::stateGateClearUpdate
.offset 0x71009d986c
b 0x71009d9930

; Load the itemid in from the trial gate params1 >> 0x18
.offset 0x71009d80d0
ldr w0, [x0, #0xC]
lsr w0, w0, #0x18
b 0x71009d80f8

; Check to see if we should give the trial reward
.offset 0x71009d81e0
mov w8, #41
bl additions_jumptable

; Don't allow thrusting a sword into a trial gate if
; the player doesn't actually have a sword
.offset 0x71009d94f8
mov w8, #58
bl additions_jumptable
cbz w0, 0x71009d9534

; fix pouch items not working properly from trial gates :p
.offset 0x71009d8104
nop

; Skip branching away from generating a glow around an item if it isn't a tear
.offset 0x71004e5bd4
nop

; Set the tear subtype (which determines the glow color) using our custom function
.offset 0x71004e5c3c
nop ; Skip a branching away from the code if the item isn't a tear
mov w0, w8
mov w8, #68
bl additions_jumptable
cmp w0, #3
b.hi 0x71004e5e28 ; If we returned greater than 3, don't generate a glow
mov w8, w0 ; move the tear subtype back into the register the code expects
b 0x71004e5c90 ; Branch to the code which spawns in the glow actor