.offset 0x712e5da03c
b 0x712e0a5164

; in align(12)
.offset 0x712e0a5164
ldr x0, [x19, #0x28] ; _IO_write_ptr
bl 0x712e6047e0 ; strlen
b 0x712e0a5188

; in align(8)
.offset 0x712e0a5188
mov w1, w0
b 0x712e0a51b4

; in align(12)
.offset 0x712e0a51b4
; get the string ptr again as strlen overwrote it
ldr x0, [x19, #0x28] ; _IO_write_ptr
ldrb w8, [x0] ; first byte of string
b 0x712e0a52d8

; in align(8)
.offset 0x712e0a52d8
cmp w8, #62
b 0x712e0a52e4

; in align(12)
.offset 0x712e0a52e4
b.ne 0x712e0a56c8 ; go back to normal code
svc #39 ; OutputPrintString
b 0x712e0a56c8 ; go back to normal code

; in align(8)
.offset 0x712e0a56c8
ldr x8, [x19, #0x28] ; _IO_write_ptr
b 0x712e5da040 ; back to vfprintf


; Remove nvwsi-post prints
.offset 0x712e4c7b90
nop

.offset 0x712e4c7c08
nop
