; Reset the initial angles for the boss keys

; onlyif boss_key_puzzles == correct_orientation
.offset 0x7100007180
mov w8, #37
bl additions_jumptable
nop

; onlyif boss_key_puzzles == random_orientation
.offset 0x7100007180
mov w8, #38
bl additions_jumptable
nop