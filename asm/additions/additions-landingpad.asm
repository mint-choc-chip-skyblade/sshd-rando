; Start using subsdk8 0x500 bytes into the .text section
; Please leave 0x1000 bytes for this landingpad

.offset 0x360A5500

; custom item gets
cmp w8, #0
b.eq handle_custom_item_get

; don't set AC boko flag on death
cmp w8, #1
b.eq 0x360A9000

; startflags
cmp w8, #2
b.eq handle_startflags

; set goddess sword pulled scene flag
cmp w8, #3
b.eq set_goddess_sword_pulled_story_flag

; freestanding item y offset
cmp w8, #4
b.eq fix_freestanding_item_y_offset

; fix sandship boat
cmp w8, #5
b.eq fix_sandship_boat

ret ; this should never be reached

; ends at 0x360A6500
