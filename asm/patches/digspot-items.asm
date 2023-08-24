; Always set digspot sceneflag, even if it's not a key piece.
.offset 0x088eed2c
nop
nop

.offset 0x088ef8a8
ldrb w0, [x19, #0x12F] ; load FF 00 00 00 from param2 (the patched itemid)

.offset 0x088ed32c
ldrb w0, [x19, #0x12F] ; load FF 00 00 00 from param2 (the patched itemid)
