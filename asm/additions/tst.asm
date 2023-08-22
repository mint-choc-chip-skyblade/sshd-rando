; start of rando subsdk
; subsdk1 offset = 0x359ff500
; actual offset = (0x359ff500 + (0x360a5000 - 0x359ff000))
; = (subsdk additions offset + (start of rando subsdk - start of subsdk1))

.offset 0x360a5500
mov w0, #20
mov x16, #0x32FC
movk x16, #0x084E, LSL #16
br x16