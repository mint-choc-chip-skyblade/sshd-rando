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




; High Dive Guaranteed Win
; Skip over landing tile calculations
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008b02ec
b 0x71008b031c

; Force landing tile to 4 (50 rupees)
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008b031c
mov w1, #4

; Force multipler to 10
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71007d15e4
mov w8, #10

; Don't increase multipler
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71007d1a78
nop

; Don't reset multipler
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71007d1b78
nop


; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008b0110
mov w8, #0 ; island rotation speed down from 750

; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008b01dc
ret ; don't change rotation speed


; In dAcOcannonCover::statePlayUpdate
; Update lyt with correct landing tile
; onlyif minigame_difficulty == guaranteed_win
.offset 0x7100759168
mov w9, #4 ; landing tile
str w9, [x8, #0x2c9c] ; make sure lyt updates rupee count

; In dAcOcannonCover::statePlayUpdate
; Force landing tile to 4 (50 rupees)
; onlyif minigame_difficulty == guaranteed_win
.offset 0x7100759178
mov w1, #4


; In dAcOrouletteIslandC::statePlayUpdate
; Update lyt with correct landing tile
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008aef7c
mov w9, #4 ; landing tile
str w9, [x8, #0x2c9c] ; make sure lyt updates rupee count

; In dAcOrouletteIslandC::statePlayUpdate
; Force landing tile to 4 (50 rupees)
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71008aef8c
mov w1, #4

; In dAcOfortuneRing::statePlayUpdate
; Update lyt with correct landing tile AND set value for rupee amount later
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71007d1e38
mov w14, #500
mov w15, #4
str w15, [x8, #0x2c9c] ; make sure lyt updates rupee count
; onlyif minigame_difficulty == guaranteed_win
.offset 0x71007d1ee0
str w14, [x22, #0x1610] ; w14 replaces xzr
str w15, [x22, #0x1614] ; w14 replaces xzr


; High Dive Easy
; onlyif minigame_difficulty == easy
.offset 0x71008b0110
mov w8, #325 ; island rotation speed down from 750

; High Dive Easy
; onlyif minigame_difficulty == hard
.offset 0x71008b0110
mov w8, #1500 ; island rotation speed up from 750
