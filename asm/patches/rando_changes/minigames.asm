; Prevent dying in certain minigames with high damage multipliers
.offset 0x7100a6d04c
mov w0, w21 ; move final health into function arg 1
mov w8, #39
bl additions_jumptable
mov w21, w1

; End Pumpkin Archery Early by hitting the bell
.offset 0x710072884c
bl 0x7100659ad0


; Minigame win condition changes

; ; Pumpkin Archery Guaranteed Win
; onlyif minigame_difficulty == guaranteed_win
.offset 0x7100604724
b 0x7100604744

; Pumpkin Archery Easy
; onlyif minigame_difficulty == easy
.offset 0x7100604724
cmp w8, #399
; onlyif minigame_difficulty == easy
.offset 0x710060472c
cmp w8, #149
; onlyif minigame_difficulty == easy
.offset 0x7100604738
cmp w8, #9

; Pumpkin Archery Hard
; onlyif minigame_difficulty == hard
.offset 0x7100604724
cmp w8, #799
; onlyif minigame_difficulty == hard
.offset 0x710060472c
cmp w8, #599
; onlyif minigame_difficulty == hard
.offset 0x7100604738
cmp w8, #399
