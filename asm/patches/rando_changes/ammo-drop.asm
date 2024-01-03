; Check if param2 means arrows, bombs, and deku seeds should drop
; onlyif ammo_availability == useful or ammo_availability == plentiful
.offset 0x7100b9464c
mov w8, #14
bl additions_jumptable
b.eq 0x7100b9507c ; return

; onlyif ammo_availability == scarce
.offset 0x7100b9464c
mov w8, #15
bl additions_jumptable
