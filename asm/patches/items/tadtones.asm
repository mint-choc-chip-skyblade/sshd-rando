; Modify STORYFLAG_DEFINITIONS to allow flag 953 to be a counter
; STATIC_STORYFLAGS[index] = 805a9b7e
; shiftMask uses 7 lsb for the counter (max value of 128)
; shiftMask >> 4 = 0 so:
; Story Flag #953 (0x03B9) - 805A9B7E 0x01 to 805A9B7E 0x40 on the story flag sheet
.offset 0x710164e342
.byte 0x53 ; index
.byte 0x7  ; shiftMask

; Allow tadtone dowsing after getting hasCollectedAllTadtones flag
; TODO: CHECK
.offset 0x7100b6dc78
mov w0, #0xffff

; Show Tadtone Scroll even after getting Water Dragon's Reward
.offset 0x7100ccccd8
mov w0, wzr

; Always play tadtone minigame music in Flooded Faron Woods
.offset 0x7100f39f24
nop

; Don't overwrite the tadtone's z-rotation with 0 so that we can use it for the itemid
.offset 0x7100773f14
nop

; Replace the one use of z-rotation with 0
.offset 0x7100772d18
mov w9, wzr

; Still init tadtone actors even if hasCollectedAllTadtones flag is set
.offset 0x7100773a40
nop

; Give tadtone's randomized item when in various possible states
.offset 0x7100770564
mov x0, x19
mov w8, #69
bl additions_jumptable

.offset 0x7100771838
mov x0, x19
mov w8, #69
bl additions_jumptable
nop

.offset 0x710077234c
mov x0, x19
mov w8, #69
bl additions_jumptable
nop

.offset 0x7100772560
mov x0, x19
mov w8, #69
bl additions_jumptable
nop

; Always init the tadtone minigame even if we've collected all tadtone group items
.offset 0x7100e50ef8
b 0x7100e50f04

; Check the custom tadtone counter instead of the vanilla storyflag to start the
; tadtones cutscene.
.offset 0x7100e510c8
mov w8, #70
bl additions_jumptable ; pointer to dTgClefGame is already in x0
mov x19, x0 ; move dTgClefGame pointer into expected register
cmp w1, #1 ; If we've collected all tadtones and haven't played the song event yet, then branch to it
b.eq 0x7100e512e0
; Replaced code now comes next
ldrb w8, [x0, #0x22c]
cbz w8, 0x7100e51100
b 0x7100e513bc ; Otherwise, branch to the end of the function
nop
nop
nop
nop
nop
