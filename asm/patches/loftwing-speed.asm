; Increase the normal loftwing speed cap.
.offset 0x08248720
mov w8, #0x43c80000 ; 80 -> 400.0

; Update speed comparisons to use larger values.
.offset 0x0824713c
mov w9, #0x43480000 ; 40.0 -> 200.0

.offset 0x08247150
mov w9, #0x43480000 ; 40.0 -> 200.0


; There's not enough space after the check for holding the b-button.
; Use the extra space freed up by removing the speed cap for flapping instead.
.offset 0x08248714
b 0x0824b644

; Prevent flapping from reducing speed and use the free space to help make
; loftwing braking behaves properly.
.offset 0x0824b63c
mov w1, #1 ; move vanilla instruction we want to keep out of the way
b 0x0824b650 ; branch over loftwing braking stuff

; Loftwing braking stuff.
; Moves the vanilla loftwing max speed into the correct register AND branches
; over the patch we make to increase the normal speed cap.
; .offset 0x0824b644
movz w8, #0x42a0, LSL #16 ; 80.0
b 0x08248724
nop ; prevent flapping from reducing speed


; charge respawn rate / 10
; .offset 0x08248594
; mov w9, #15

; .offset 0x08247300
; mov w8, #5
