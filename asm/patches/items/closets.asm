; patch dAcOChest::eventUpdate to handle traps correctly
.offset 0x710076a41c
mov w8, #51
bl additions_jumptable

; fix pouch items not working properly from closets :p
.offset 0x710076a3ec
nop
