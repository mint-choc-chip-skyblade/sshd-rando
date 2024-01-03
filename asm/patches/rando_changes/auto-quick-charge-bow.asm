; Always allow using L to nock an arrow
.offset 0x7100a5f668
nop

; Holding L automatically quick charges the bow
.offset 0x7100a60578
mov w8, #0x2006
