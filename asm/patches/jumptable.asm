; Since the additional instruction space is so far away, a jumptable is needed
; to allow branching to this space only using one instruction.
; 
; If you have the space, it is preferred that you don't use this jumptable.
; 
; Ideally, this should only be used when there is no other choice because this
; jumptable is overwriting an actor (dAcNpcSenpaiAMotherLOD_c) that is unused
; in rando.
; 
; For now, only the ctor and init functions are okay to be used. The ctor is
; first and is immediately followed by the init, so the space can be treated
; as one block of code. There are potentially other functions within this
; actor that can be used but more knowledge about this actor is needed before
; they can be used safely.
; 
; dAcNpcSenpaiAMotherLOD_c::ctor starts at:  0x7100659ab0
; dAcNpcSenpaiAMotherLOD_c::init ends at:    0x710065a080
; Total available space (bytes):                  0x5D0
; Total available space (bytes):                   1488 (decimal)
; Total available instructions:                     372 (decimal)
; 
; Please update this:
; Total space used (bytes):                          88
; Total instructions used:                           22

; startflags
.offset 0x7100659ab0
mov w8, #2
b additions_jumptable

; freestanding item y offset
.offset 0x7100659ab8
mov w8, #4
b additions_jumptable

; Set Stone of Trials placed flag
.offset 0x7100659ac0
mov w8, #8
b additions_jumptable

; Hide spawnable chest after demo appear
; Create dAcTbox::stateDemoAppearLeave function
.offset 0x7100659ac8
mov w8, #36
b additions_jumptable

; End Pumpkin Archery early by hitting the bell
.offset 0x7100659ad0
mov w8, #42
b additions_jumptable

.offset 0x7100659ad8
mov w8, #43
b additions_jumptable

; Actually branches to the rust additions landingpad
; additions_jumptable
.offset 0x710065a070 ; uses 10 instructions
b 0x712e0a5500
