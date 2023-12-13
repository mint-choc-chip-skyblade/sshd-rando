; Setup traps (change itemids) in dAcItem::stateWaitForceGetDemoUpdate
.offset 0x71004df298
mov w8, #28
bl additions_jumptable

; Setup traps (change itemids) in dAcItem::stateWaitGetDemoUpdate
.offset 0x71004def10
mov w8, #28
bl additions_jumptable

; Setup traps (change itemids) in dAcItem::stateWaitTBoxGetDemoUpdate
.offset 0x71004dfc4c
mov w8, #28
bl additions_jumptable

; Setup traps in handleType3
.offset 0x710050d8c8
mov w8, #24
bl additions_jumptable

; Setup traps in tboxs
.offset 0x7100b0b7f4
mov w8, #26
bl additions_jumptable


; Check for traps when spawning actors
.offset 0x7100f14514
mov w8, #25
bl additions_jumptable


; Prevent events clearing trap effects
.offset 0x7100ac055c
mov w8, #27
bl additions_jumptable
mov w8, w0
nop

; Prevent events from blocking trap effects
; .offset 0x7100ac0964
; mov w8, #27
; bl additions_jumptable
; mov w8, w0
; nop

; .offset 0x7100ac0904
; mov w8, #27
; bl additions_jumptable
; mov w8, w0
; nop
; 
; .offset 0x7100ac0aec
; mov w8, #27
; bl additions_jumptable
; mov w8, w0
; nop
