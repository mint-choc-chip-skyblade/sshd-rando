; Prevent Trial Gates from closing even if they flag
; to close them is set

; Faron Trial Gate
.offset 0x71009dd088
nop

.offset 0x71009d93f8
nop

; Eldin Trial Gate
.offset 0x71009dd0b0
nop

.offset 0x71009d9420
nop

; Lanayru Trial Gate
.offset 0x71009dd0d8
nop

.offset 0x71009d9448
nop

; Skyloft Trial Gate
.offset 0x71009dd110
b 0x71009dd0e8

.offset 0x71009d9474
b 0x71009d94f8

; Skip over dAcOWarp::stateGateClearUpdate
.offset 0x71009d986c
b 0x71009d9930