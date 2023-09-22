; Replace setting the Goddess Sword item flag with
; setting a custom story flag to trigger the items
; from pulling the Goddess Sword

.offset 0x08a1759c
mov w8, #3
bl 0x0865a070
nop ; don't call the debug(?) function when setting itemflags
nop

; Remove Goddess Sword textbox after pulling the Goddess Sword
.offset 0x08a494e4
mov w2, #0xff ; -1 (don't show a textbox after the event)