; Always show the skip prompt (needs to be visible before you can skip)
.offset 0x7100b767a4
nop

; Allow holding minus to skip cutscenes
.offset 0x7100b76704
ldr x8, [x8, #0x40]
