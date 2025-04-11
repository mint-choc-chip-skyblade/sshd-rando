; Remove help_index bounds check
.offset 0x7100c4060c
nop
nop

; New help_index bounds check
; Slightly later in the code to allow the stack to be properly maintained
; (gotta love LTO messing things up -_-)
.offset 0x7100c40648
mov w8, #90
bl additions_jumptable
nop

; Set numeric and string args for help menu info
.offset 0x7100c406bc
mov w8, #87
bl additions_jumptable
b 0x7100c408ec

; Left-justify the text
.offset 0x7100c40ec4
mov w8, #88
bl additions_jumptable

; Allow multiple help boxes when pressing dpad right
; This adds additional checks to the vanilla check to see if the player
; pressed dpad right (to close the help menu).
; dpad right now cycles between 3 sets of help information (can be increased)
; dpad left closes the menu as does dpad right after the final help is shown
.offset 0x7100c3fed4
mov w8, #89
bl additions_jumptable
cmp w0, #1
b.eq 0x7100c402bc ; ret, don't close window
b.gt 0x7100c4004c ; 2+ -> close window
; 0 -> continue as normal
