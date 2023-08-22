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
; dAcNpcSenpaiAMotherLOD_c::ctor starts at:  0x08659ab0
; dAcNpcSenpaiAMotherLOD_c::init ends at:    0x0865a080
; Total available space (bytes):                  0x5D0
; Total available space (bytes):                   1488 (decimal)
; Total available instructions:                     372 (decimal)
; 
; Please update this:
; Total space used (bytes):                           0
; Total instructions used:                            0


