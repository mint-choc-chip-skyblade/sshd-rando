; Overwrite checkParam2OnDestroy function calls
.offset 0x7100e8d3c0
bl 0x7101060970
.offset 0x7100e8d5b8
bl 0x7101060970

; Still init dTgReaction if sceneflag is set
.offset 0x7100e8e518
nop

; Don't check sceneflag in update either
.offset 0x7100e8ec78
mov w0, #0
