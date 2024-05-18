; Give randomized item in init function
.offset 0x71005c204c
ldrb w0, [x19, #0x12D] ; load 00 00 FF 00 from param2 (the patched itemid)
; let the vanilla function get called

.offset 0x71005c2054
; setup param1
mov w2, #0x3000 ; set sceneflag 12 on collection
bfxil w2, w0, #0x0, #0x9

; branch over 7 unused instructions
b 0x71005c207c ; this instruction space is used for the dAcItem__spawnRandoItemWithParams custom function


; Give randomized item in update function
.offset 0x71005c4e24 ; starts 1 instruction back to prevent self getting overwritten
nop
ldrb w0, [x19, #0x12D] ; load 00 00 FF 00 from param2 (the patched itemid)
; let the vanilla function get called

.offset 0x71005c4e30
; setup param1
mov w2, #0x3000 ; set sceneflag 12 on collection
movk w2, #0x0, LSL #16
bfxil w2, w0, #0x0, #0x9

; replaced instruction
ldrsb w19, [x19, #0x17c]

nop ; 6 nops
nop
nop
nop
nop
nop



; handle traps
; these patches are quite far away from when the item actually gets created
; but will still always get called
; in dAcNpcKyuiElder::init
.offset 0x71005c1ef0
mov w8, #52
bl additions_jumptable

.offset 0x71005c20b0
nop ; don't overwrite dAcBase::param2

; in dAcNpcKyuiElder::spawnSlingshot??
.offset 0x71005c4cc8
mov w8, #52
bl additions_jumptable

.offset 0x71005c4e90
nop ; don't overwrite dAcBase::param2



; Replace check for slingshot item with a sceneflag check for the Kikwi Elder's Reward

; In function that checks each of the Kikwi storyflags
.offset 0x71005c2e7c
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w11, #0x2 ; replaced instruction
mov w8, w0 ; move result into w8
nop ; 6 nops
nop
nop
nop
nop
nop

.offset 0x71005c2d94
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w8, w0 ; move result into w8
nop ; 7 nops
nop
nop
nop
nop
nop
nop


; In changeStateAfterGettingSlingshot function??
.offset 0x71005c5260
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w8, w0 ; move result into w8
nop ; 7 nops
nop
nop
nop
nop
nop
nop


; In function that switches to post item get event for Bucha?
.offset 0x71005c11a8
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w8, w0 ; move result into w8
nop ; 7 nops
nop
nop
nop
nop
nop
nop

.offset 0x71005c1ad4
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w8, w0 ; move result into w8
nop ; 7 nops
nop
nop
nop
nop
nop
nop

.offset 0x71005c1240
nop ; remove branch to getSaveFlagSpace
mov w0, #12 ; sceneflag 12
mov w8, #12 ; branch to addition 12
bl additions_jumptable
mov w8, w0 ; move result into w8
nop ; 7 nops
nop
nop
nop
nop
nop
nop


; Check current stage in dAcNpcKyuiElder::performInteraction
.offset 0x71005c2c78
mov w8, #55

.offset 0x71005c2c80
bl additions_jumptable
