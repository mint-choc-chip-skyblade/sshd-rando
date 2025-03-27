; Allocate more space for ArcMgr entries
.offset 0x7100e3b600
mov w1, #0x8988 ; ArcEntry[400] -> 0x58 * 400 = 0x8980, + 0x8 for some pointer ArcEntryTable

.offset 0x7100e3b618
mov w10, #0x8988

.offset 0x7100e3b610
mov w8, #400 ; upped from 200


; hopefully fix memory leak by checking if filename already has an arcEntry
.offset 0x7100ed7d80
mov x4, x19
mov w8, #81
bl additions_jumptable
strb w23, [x22, x0]

; Load custom bzs.arc
; uses the jumptable cos the vanilla instructions are a mess
.offset 0x7100e13354
b 0x7100659ae0

; Use custom bzs.arc when trying to load vanilla bzs
.offset 0x7100deb9a4
bl 0x7100659ae8
