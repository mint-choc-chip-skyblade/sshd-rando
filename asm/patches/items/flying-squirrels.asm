; Test spawn item from tag
.offset 0x7100e88274
mov w8, #29
bl additions_jumptable

; Don't give item from dAcOmusasabi actors, this is handled by dTgMusasabi now
.offset 0x71008634bc
nop
.offset 0x7100863da0
nop
