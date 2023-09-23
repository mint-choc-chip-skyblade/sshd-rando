; Change the comparison when loading
; Link's tunic textures from b.eq to b.ne

; onlyif tunic_swap == on
.offset 0x08ab5930
b.ne 0x08ab7b58