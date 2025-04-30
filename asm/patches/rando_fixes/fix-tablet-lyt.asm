; Override tablet counting code
.offset 0x7100d78428
mov w8, #92
bl additions_jumptable
mov w22, w0
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

; Change the keyframe used to hide the tablets
; when the player has at least one triforce
.offset 0x7100d78a88
mov x9, #0x40E00000 ; 7.0, was 0x40400000 -> 3.0
movk x9, #0x40E0, LSL #48
