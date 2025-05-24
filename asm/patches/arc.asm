; Allocate more space for ArcMgr entries
.offset 0x7100e3b600
mov w1, #0x8988 ; ArcEntry[400] -> 0x58 * 400 = 0x8980, + 0x8 for some pointer ArcEntryTable

.offset 0x7100e3b618
mov w10, #0x8988

.offset 0x7100e3b610
mov w8, #400 ; upped from 200


; Allocate more space for StageArcMgr entries
; 
; This sucks cos the vanilla game allocates *exactly* enough entries to accommodate
; all of the rooms in Sandship. Which means the extra entry needed to load the bzs.arc
; that rando adds isn't there and the game crashes trying to find an arc which doesn't exist.
; 
; In theory, only one extra entry needs to be added
; but even numbers are nice and safety is even nicer.
.offset 0x7100e3b2ac
mov w1, #0x6e8 ; ArcEntry[20] -> 0x58 * 20 = 0x6e0, + 0x8 for some pointer ArcEntryTable

.offset 0x7100e3b2bc
mov w8, #20 ; upped from 18


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


; Load stage arcs from romfs/ModReplace where possible
; Unfortunately necessary jumptable usage ;-;
.offset 0x7100b8c3e4
bl 0x7100659af0

; Load general arcs from romfs/ModReplace where possible
.offset 0x7100deb2cc
mov w8, #96 // replaced instructions / function setup
bl additions_jumptable
mov w8, #97 // prefer_modreplace_for_general_arcs
bl additions_jumptable
cbnz w0, 0x7100deb604 ; return 1
nop
