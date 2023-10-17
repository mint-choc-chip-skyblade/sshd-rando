; Check if param2 means arrows, bombs, and deku seeds should drop
.offset 0x08b9464c
mov w8, #14
bl additions_jumptable
b.eq 0x08b9507c ; return

; .offset 0x08eca458
; mov w8, #14
; bl additions_jumptable
