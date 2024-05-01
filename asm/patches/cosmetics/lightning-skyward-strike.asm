; onlyif lightning_skyward_strike == on
.offset 0x7100ad4988
b 0x7100ad550c

; I don't think this actually does anything cos of the above patch
; onlyif lightning_skyward_strike == on
.offset 0x7100ad49c0
nop

; onlyif lightning_skyward_strike == on
.offset 0x7100add420
mov x9, #0x63B
movk x9, #0x63B, LSL #16

; onlyif lightning_skyward_strike == on
.offset 0x7100add430
movk x9, #0x63B, LSL #32
movk x9, #0x63B, LSL #48

; onlyif lightning_skyward_strike == on
.offset 0x7100ad4518
b 0x7100ad4568

; onlyif lightning_skyward_strike == on
.offset 0x7100ad4548
b 0x7100ad4578

; onlyif lightning_skyward_strike == on
.offset 0x7100ad4a60
nop

; onlyif lightning_skyward_strike == on
.offset 0x7100a726f0
mov w2, #0x8AE
