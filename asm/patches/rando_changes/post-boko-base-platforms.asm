; Spawn lava river platforms in Eldin if
; Boko Base has been completed
.offset 0x7100e90ab8
mov x19, x0 ; code afterwards expects pointer in x19
mov w8, #30
bl additions_jumptable
cmp x0, #1
b.ne 0x7100e90ba8
nop
nop
nop
nop
