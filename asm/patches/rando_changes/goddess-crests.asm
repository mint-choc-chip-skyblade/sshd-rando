; Allow obtaining the last Isle of Songs reward with
; white sword or higher
.offset 0x710092e730
b.ge 0x710092e754

; Branch to our custom item give code
.offset 0x7100930844
mov x0, x19
mov w8, #13
bl additions_jumptable
b 0x710093086c ; cancel song giving cutscene

; Skip setting the sceneflag normally as we set it
; in our custom function
.offset 0x710092ed18
nop