; Call custom trigger entrance stuff
.offset 0x71000289a8
mov w8, #21
bl additions_jumptable
b 0x7100028a3c ; Skip vanilla trigger entrance stuff
