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



; Rickety Coaster Guaranteed Win
; onlyif minigame_difficulty == guaranteed_win
.offset 0x710059303c
mov w0, #3 ; best score
b 0x7100592ff8


; Rickety Coaster Easy
; Scary (easy) ret 3
; onlyif minigame_difficulty == easy
.offset 0x7100593114
mov w8, #35000 ; up from 30000

; Scary (easy) ret 2
; onlyif minigame_difficulty == easy
.offset 0x710059314c
mov w8, #40000 ; up from 35000

; Scary (easy) ret 1
; onlyif minigame_difficulty == easy
.offset 0x7100593158
mov w8, #45000 ; up from 40000

; Heartstopping (hard)
; This one has to be handled differently as the
; numbers are too big to just swap them out
; onlyif minigame_difficulty == easy
.offset 0x71005930bc
mov w8, #0x1170
movk w8, #1, LSL #16
cmp w19, w8
b.lt 0x7100593120 ; ret 3 if < 70000
mov w9, #5000
add w8, w8, w9
cmp w19, w8
b.le 0x7100593100 ; ret 2 if < 75000
add w8, w8, w9
; ret 1 if < 80000 else ret 0


; Rickety Coaster Hard
; Scary (easy) ret 3
; onlyif minigame_difficulty == hard
.offset 0x7100593114
mov w8, #29500 ; down from 30000

; Scary (easy) ret 2
; onlyif minigame_difficulty == hard
.offset 0x710059314c
mov w8, #30000 ; down from 35000

; Scary (easy) ret 1
; onlyif minigame_difficulty == hard
.offset 0x7100593158
mov w8, #35000 ; down from 40000

; Heartstopping (hard) ret 3
; onlyif minigame_difficulty == hard
.offset 0x71005930bc
mov w8, #62000 ; down from 65000

; Heartstopping (hard) ret 2
; onlyif minigame_difficulty == hard
.offset 0x71005930cc
mov w8, #65000 ; down from 70000

; Heartstopping (hard) ret 1
; onlyif minigame_difficulty == hard
.offset 0x71005930d8
mov w8, #0x1170
movk w8, #1, LSL #16 ; 70000, down from 75000
