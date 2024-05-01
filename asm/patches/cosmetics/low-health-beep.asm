; onlyif low_health_beeping_speed == no_beeping_or_flashing
.offset 0x7100ac1738
b 0x7100ac1878

; onlyif low_health_beeping_speed == no_beeping
.offset 0x7100ac1754
b 0x7100ac1878

; onlyif low_health_beeping_speed == no_beeping
.offset 0x7100ac1794
nop
b 0x7100ac1878

; onlyif low_health_beeping_speed == very_fast
.offset 0x7100ac1798
mov w8, #1

; onlyif low_health_beeping_speed == fast
.offset 0x7100ac1798
mov w8, #2

; onlyif low_health_beeping_speed == slow
.offset 0x7100ac1798
mov w8, #6

; onlyif low_health_beeping_speed == very_slow
.offset 0x7100ac1798
mov w8, #12
