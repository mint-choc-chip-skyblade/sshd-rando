; Unlock Iron Shield
.offset 0x710164054c
.short 0xFFFF

; Unlock Sacred Shield
.offset 0x71016405a0
.short 0xFFFF

; Unlock Small Seed Satchel
.offset 0x7101640648
.short 0xFFFF

; Unlock Small Quiver
.offset 0x710164069c
.short 0xFFFF

; Unlock Small Bomb Bag
.offset 0x71016406f0
.short 0xFFFF


; Rotate shop items
.offset 0x7100b0595c
mov w8, #66
bl additions_jumptable

; Set shop item height
.offset 0x7100afff98
mov w8, #67
bl additions_jumptable
