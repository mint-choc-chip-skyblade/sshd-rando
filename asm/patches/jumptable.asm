; Since the additional instruction space is so far away, a jumptable is needed
; to allow branching to this space only using one instruction.
; 
; If you have the space, it is preferred that you don't use this jumptable.
; 
; Ideally, this should only be used when there is no other choice because this
; jumptable is using the slice of unused space at the end of the vanilla
; game's code and there's really not a lot of it ^^'
; 
; 
; End of vanilla game code:      0x7101060950
; Start of .rodata section:      0x7101061000
; Total available space (bytes): 0x6B0
; Total available space (bytes): 1712 (decimal)
; Total available instructions:  428 (decimal)
; 
; Please update this:
; Total space used (bytes):      0x98
; Total instructions used:       26

; startflags
.offset 0x7101060950
mov w8, #2
b additions_jumptable

; Set Stone of Trials placed flag
.offset 0x7101060958
mov w8, #8
b additions_jumptable

; Hide spawnable chest after demo appear
; Create dAcTbox::stateDemoAppearLeave function
.offset 0x7101060960
mov w8, #36
b additions_jumptable

; End Pumpkin Archery early by hitting the bell
.offset 0x7101060968
mov w8, #42
b additions_jumptable

; TgReact overwrite checkParam2OnDestroy function calls
.offset 0x7101060970
mov w8, #43
b additions_jumptable

; load custom bzs
.offset 0x7101060978
mov w8, #82
b additions_jumptable

; use custom bzs
.offset 0x7101060980
mov w8, #83
b additions_jumptable

; Load arcs from romfs/Object/NX where possible
; prefer_object_folder_for_models
.offset 0x7101060988
mov w8, #95
b additions_jumptable

; Actually branches to the rust additions landingpad
; additions_jumptable
.offset 0x7101060FE0 ; uses 10 instructions
b 0x712e0a5500
