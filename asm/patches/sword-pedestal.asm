; Replace setting the Goddess Sword item flag with
; setting a custom story flag to trigger the items
; from pulling the Goddess Sword

.offset 0x08a1759c
mov w8, #3
bl additions_jumptable
nop ; don't call the debug(?) function when setting itemflags
nop

; Remove Goddess Sword textbox after pulling the Goddess Sword
.offset 0x08a494e4
mov w2, #0xff ; -1 (don't show a textbox after the event)


; Only spawn sword if you haven't already gotten the checks
.offset 0x088c4528 ; in init
mov w1, #951 ; storyflag for goddess statue sword checks

.offset 0x088c5268 ; in update
mov w1, #951 ; storyflag for goddess statue sword checks

.offset 0x088c3af4 ; in some state change
mov w1, #951 ; storyflag for goddess statue sword checks
