.offset 0x712e0a7500
ldrb w22, [x27, #0x10b] ; replaced instruction (get sceneflag)
cmp w22, #0xFF
b.eq not_set_flag

; x24 is overwritten after this
mov x24, #0x1988 ; get dAcEbc->bokoHasSmallKey offset
ldrb w24, [x19, x24] ; get dAcEbc->bokoHasSmallKey
cmp w24, #1

not_set_flag:
ret
