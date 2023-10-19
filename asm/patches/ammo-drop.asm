; Check if param2 means arrows, bombs, and deku seeds should drop
; onlyif ammo_availability == useful or ammo_availability == plentiful
.offset 0x08b9464c
mov w8, #14
bl additions_jumptable
b.eq 0x08b9507c ; return

; onlyif ammo_availability == scarce
.offset 0x08b9464c
mov w8, #15
bl additions_jumptable
nop
; b.eq 0x08b9507c ; return

; .offset 0x08eca458
; mov w8, #14
; bl additions_jumptable
