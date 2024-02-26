; Overwrite checkParam2OnDestroy function calls
; onlyif hidden_item_shuffle == on
.offset 0x7100e8d3c0
bl 0x7100659ad0
; onlyif hidden_item_shuffle == on
.offset 0x7100e8d5b8
bl 0x7100659ad0

; Still init dTgReaction if sceneflag is set
; onlyif hidden_item_shuffle == on
.offset 0x7100e8e518
nop

; Don't check sceneflag in update either
.offset 0x7100e8ec78
mov w0, #0
