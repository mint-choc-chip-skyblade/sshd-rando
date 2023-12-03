; Setup traps (change itemids) in dAcItem::stateWaitForceGetDemoUpdate
.offset 0x71004df298
mov w8, #13
bl additions_jumptable

; Setup traps (change itemids) in dAcItem::stateWaitGetDemoUpdate
.offset 0x71004def10
mov w8, #13
bl additions_jumptable


; Prevent events clearing trap effects
.offset 0x7100ac055c
mov w8, #23
bl additions_jumptable
mov w8, w0
nop

; Prevent events from blocking trap effects
; .offset 0x7100ac0964
; mov w8, #23
; bl additions_jumptable
; mov w8, w0
; nop

; .offset 0x7100ac0904
; mov w8, #23
; bl additions_jumptable
; mov w8, w0
; nop
; 
; .offset 0x7100ac0aec
; mov w8, #23
; bl additions_jumptable
; mov w8, w0
; nop
