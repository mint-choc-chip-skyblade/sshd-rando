; Deactivate air vents if the player doesn't have the Sailcloth
.offset 0x71009f6e3c
mov w8, #99
b additions_jumptable

; Require Sailcloth to fly to the sky from bird statues
.offset 0x7100d88730
mov w8, #100
bl additions_jumptable
nop

; Trigger voidout if the player approaches loadzones that visually use the
; Sailcloth if they don't actually have it yet.
; In dTgSceneChange_c::update
.offset 0x7100e93524
mov w8, #101
bl additions_jumptable
