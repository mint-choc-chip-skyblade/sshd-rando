; Patch the total number of gratitude crystals
; into numeric arg 1 when collecting a gratitude
; crystal or pack
.offset 0x71004e2584
mov w8, #22
bl additions_jumptable
