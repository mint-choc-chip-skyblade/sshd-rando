; in dAcNpcBBRvl::shouldSpawnGroose?
; always return true if not in boss rush
.offset 0x7100557720
nop

; in dAcNpcBBRvl::shouldNotSpawnGroose?
; always return false if not in boss rush
.offset 0x7100557a7c
nop

; in dAcNpcBBRvl::init2
; always act like LEARNT_FARON_SOTH (16) storyflag is false
.offset 0x710054f860
mov w0, #0

; in dAcNpcBBRvl::stateShootF3DemoUpdate
; always act like LEARNT_FARON_SOTH (16) storyflag is false
.offset 0x7100542668
mov w0, #0
.offset 0x710054275c
mov w0, #0
.offset 0x71005449f0
mov w0, #0
