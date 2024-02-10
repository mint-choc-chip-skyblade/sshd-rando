; All savefiles created with the rando are
; Hero Mode files. So settings here are checked
; and replaced with normal mode behavior if necessary

; Air Meter normal mode depletion rate
; onlyif faster_air_meter_depletion == off
.offset 0x7100a59340
lsl w8, w25, 0

; Spawn Heart Flowers
; onlyif spawn_hearts == on
.offset 0x71004ae98c
mov w0, 0

; Heart Spawns
; onlyif spawn_hearts == on
.offset 0x71004e4568
mov w0, 0

; Spawn Hearts from pots?
; onlyif spawn_hearts == on
.offset 0x7100b948a8
mov w0, 0

; Heart Spawn related
; onlyif spawn_hearts == on
.offset 0x7100e8e4d0
mov w0, 0

; Skyward Strike Spin Attack Power/Range
; onlyif upgraded_skyward_strike == off
.offset 0x7100a726cc
mov w0, 0

; Skyward Strike Slash Power/Range
; onlyif upgraded_skyward_strike == off
.offset 0x7100ad4408
mov w0, 0

; Skyward Strike Charge Speed
; onlyif upgraded_skyward_strike == off
.offset 0x7100de5a80
mov w0, 0

; Multiply by our own damage multiplier instead.
; The instruction that loads the multiplier into w8
; is set in asmpatchhandler.py
.offset 0x7100a6ce7c
mul w21, w21, w8
