;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Allow calling Fi without a sword ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Don't check for equipped sword
.offset 0x7100a6ddfc
nop

; Don't check for skyward strike??
.offset 0x7100a6de14
nop

; Don't check for swordless due to boko base
.offset 0x7100a6de2c
nop
nop
nop
nop
nop

; Don't check for tunic
.offset 0x7100a6de50
nop
nop
nop

; Don't check for goddess sword
.offset 0x7100a6dfcc
nop
nop


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Allow calling Fi while in water ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Allow calling Fi even with the in water action flag set
.offset 0x7100a6dfd8
nop

; Not sure what this is but branches when in water
.offset 0x7100a6e000
nop

; Don't check in water action flag when also checking is in boat?
.offset 0x7100a6e06c
movk w9, #0xc3, LSL #16


; Allow calling Fi while on fire
.offset 0x7100a6de70
nop
nop
