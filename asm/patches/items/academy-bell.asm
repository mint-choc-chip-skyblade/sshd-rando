; Patch item given by academy bell
.offset 0x7100729398
mov w8, #44
.offset 0x71007293a4
bl additions_jumptable

; Prevent timed despawn
; Uses unnecessary code that zeros the new item's velocity
.offset 0x71007293b8
add x0, x0, #0x1000
; uses illicit knowledge that w4 keeps a 1 in its least sig bit
; prevents the spawned item from despawning
strb w4, [x0, #0x26f]
