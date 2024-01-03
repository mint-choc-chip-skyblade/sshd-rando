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

; Skip setting the sceneflag for the IoS crest
; but still set it for all the other crests
.offset 0x710092eca8
b 0x710092ed1c ; return
