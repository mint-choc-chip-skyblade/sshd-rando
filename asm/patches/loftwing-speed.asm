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


; Spawn Tornados further away
.offset 0x08e9be14 ; 0x7100e97e14
; w9 already has 0x8000 at LSL #0
movk w9, #0x469c, LSL #16 ; 12000.0 -> 20032.0

; Increase Tornado culling distance
; Uses instructions that inits parts of the worldMatrix to 0.0
; Since this data is being inited and doesn't have a value yet, it's alraedy zero
.offset 0x089876a0 ; 0x71009836a0
movz w8, #0x47df, LSL #16 ; 114176.0 arbitrarily large value to stop despawn - taken from SD

.offset 0x089876a8 ; 0x71009836a8
str w8, [x19, #0x23c] ; store new culling distance value
