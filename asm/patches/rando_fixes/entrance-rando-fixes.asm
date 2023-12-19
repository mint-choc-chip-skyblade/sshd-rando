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
