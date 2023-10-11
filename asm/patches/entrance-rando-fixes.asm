; hook into function that assigns NEXT_* stage info
; in actuallyTriggerEntrance
.offset 0x08e2f1c0
mov w8, #6
bl 0x0865a070

; in triggerEntrance if actuallyTriggerEntrance isn't called
.offset 0x08df8f7c
mov w8, #6
bl 0x0865a070

; Somewhere late enough that setting action states won't get overwritten
.offset 0x08e10b6c
mov w8, #7
bl 0x0865a070