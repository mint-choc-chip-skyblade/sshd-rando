; hook into function that assigns NEXT_* stage info
; in actuallyTriggerEntrance
.offset 0x7100e2f1c0
mov w8, #6
bl additions_jumptable

; in triggerEntrance if actuallyTriggerEntrance isn't called
.offset 0x7100df8f7c
mov w8, #6
bl additions_jumptable

; Somewhere late enough that setting action states won't get overwritten
.offset 0x7100e10b6c
mov w8, #7
bl additions_jumptable

; Allow saving respawn info when starting a new file
.offset 0x7100df6a50
mov w8, #56
bl additions_jumptable


; Move branch to save instruction space
.offset 0x7100e177d8
b.ne 0x7100e1781c

; Combine checks for GAME_RELOADER_PTR->isReloading
.offset 0x7100e1781c
mov w21, #1
b 0x7100e1780c

; Checks GAME_RELOADER_PTR->isReloading *and* storyflag 1201 (amiibo) as a
; "is starting new game file" check.
.offset 0x7100e1780c
mov w8, #57
bl additions_jumptable
cbnz w8, 0x7100e17824
b 0x7100e17994
