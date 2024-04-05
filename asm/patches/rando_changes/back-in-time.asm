; patches the doSoftReset function to check if the player is holding the L
; button and sets RESPAWN_TYPE to 3 if so
; 
; onlyif enable_back_in_time == on
.offset 0x7100deab18
mov w8, #50
bl additions_jumptable
