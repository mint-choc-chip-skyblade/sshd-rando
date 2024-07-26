.offset 0x712e5db03c
b 0x712e0a6164

; in align(12)
.offset 0x712e0a6164
ldr x0, [x19, #0x28] ; _IO_write_ptr
bl 0x712e6147e0 ; strlen
b 0x712e0a6188

; in align(8)
.offset 0x712e0a6188
mov w1, w0
b 0x712e0a61b4

; in align(12)
.offset 0x712e0a61b4
ldr x0, [x19, #0x28] ; _IO_write_ptr
svc #39 ; OutputPrintString
b 0x712e0a62d8

; in align(8)
.offset 0x712e0a62d8
ldr x8, [x19, #0x28] ; _IO_write_ptr
b 0x712e5db040 ; back to vfprintf


; Remove nvwsi-post prints
.offset 0x712e4c8b90
nop

.offset 0x712e4c8c08
nop
