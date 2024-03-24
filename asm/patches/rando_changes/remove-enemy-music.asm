; branch past the code that cuts off the bgm with enemy drums
; onlyif remove_enemy_music == on
.offset 0x7100f7fd5c
b 0x7100f7fdf0

; onlyif remove_enemy_music == on
.offset 0x71001d7874
b 0x71001d7900
