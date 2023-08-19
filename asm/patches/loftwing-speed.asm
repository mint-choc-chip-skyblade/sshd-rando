; raise normal speed cap
.offset 0x08248720
mov w8, #0x43c80000 ; 80 -> 400.0

; speed comparisons
.offset 0x0824713c
mov w9, #0x43480000 ; 40.0 -> 200.0

.offset 0x08247150
mov w9, #0x43480000 ; 40.0 -> 200.0


; Prevent flapping from reducing speed
.offset 0x0824b64c
nop


; charge respawn rate / 10
; .offset 0x08248594
; mov w9, #15

; .offset 0x08247300
; mov w8, #5
