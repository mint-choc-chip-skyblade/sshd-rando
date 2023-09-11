; Start using subsdk8 0x500 bytes into the .text section
; Please leave 0x1000 bytes for this landingpad

.offset 0x360A5500
cmp w8, #0
b.eq handle_custom_item_get

ret ; this should never be reached

; ends at 0x360A6500
