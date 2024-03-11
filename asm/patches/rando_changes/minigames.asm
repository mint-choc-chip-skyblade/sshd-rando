; Prevent dying in certain minigames with high damage multipliers
.offset 0x7100a6d04c
mov w0, w21 ; move final health into function arg 1
mov w8, #39
bl additions_jumptable
mov w21, w1

; End Pumpkin Archery Early by hitting the bell
.offset 0x710072884c
bl 0x7100659ad0