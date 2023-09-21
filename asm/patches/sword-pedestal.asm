; Replace setting the Goddess Sword item flag with
; setting a custom story flag to trigger the items
; from pulling the Goddess Sword

; The nops after the bl stop the Goddess Sword text
; and fanfare from playing
.offset 0x08a1759c
mov w8, #3
bl 0x0865a070
nop
nop
nop
nop
nop
nop
nop