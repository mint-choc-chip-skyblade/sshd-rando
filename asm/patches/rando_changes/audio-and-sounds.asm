; Load additional sound files by patching the code
; which loads the GRP_FAN_TIMECHANGE sound file
.offset 0x7100f7dc2c
mov w8, #66
bl additions_jumptable

; Forces the GRP_FAN_TIMECHANGE sound file to always be loaded
.offset 0x7100f7d684
nop
.offset 0x7100f7d690
nop
.offset 0x7100f7d6a8
nop


; Get custom sfx when item textbox is displayed
.offset 0x7100a3b820
mov w1, w8 ; backup ref to ITEMFLAG_TO_GIVE_IN_EVENT
mov w8, #67
bl additions_jumptable
cbz w1, 0x7100a3b878 ; continue with vanilla sfx if sfx_id == 0

; don't overwrite sfx_id with the vanilla heart container sound
.offset 0x7100a3b838
nop


; Randomize Music
.offset 0x7100df53f0
mov w8, #94
bl additions_jumptable
