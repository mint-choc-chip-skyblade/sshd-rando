; Change flag checked for in harp tutorial from GoT raised to tutorial completed
.offset 0x71005fde74
mov w1, #343 ; have played the song with The Old One

; Only prevent the harp tutorial if you've already done it
.offset 0x71005fdf40
mov w1, #343
