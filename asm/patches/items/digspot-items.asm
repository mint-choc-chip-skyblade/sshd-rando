; Always set digspot sceneflag, even if it's not a key piece.
.offset 0x71008eed2c
nop
nop

.offset 0x71008ef8a8 ; dAcOsoil::update
ldrb w0, [x19, #0x12F] ; load FF 00 00 00 from param2 (the patched itemid)

.offset 0x71008ed32c ; dAcOsoil::stateSoilUpdate
ldrb w0, [x19, #0x12F] ; load FF 00 00 00 from param2 (the patched itemid)


; handle traps
.offset 0x71008ef93c ; dAcOsoil::update
mov w8, #53
bl additions_jumptable

.offset 0x71008ed3c0
mov w8, #53
bl additions_jumptable
