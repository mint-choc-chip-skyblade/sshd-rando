; branch past the code that cuts off the bgm with enemy drums
; onlyif remove_enemy_music == on
.offset 0x7100f7fd5c
b 0x7100f7fdf0

; remove vulnerable interrupting music in tentalus fight
; onlyif remove_enemy_music == on
.offset 0x71001d7874
b 0x71001d7900

; remove vulnerable interrupting music in scaldera fight
; onlyif remove_enemy_music == on
.offset 0x7100231318
b 0x710023135c
; onlyif remove_enemy_music == on
.offset 0x71002317e4
b 0x7100231828
; onlyif remove_enemy_music == on
.offset 0x71002319a4
b 0x71002319e8
; onlyif remove_enemy_music == on
.offset 0x71002327c4
b 0x7100232808
