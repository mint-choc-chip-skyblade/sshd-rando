.offset 0x7100e1683c
mov w8, #54
bl additions_jumptable



; Clouds
;
; Don't overwrite the cloud colour every frame
; This is done in the mainloop now
;; .offset 0x7100ba81d0
;; nop

; Sets the starting colour of the clouds
;; .offset 0x710000df08
;; mov x8, #0xFFFF ; r = 0xFF, g = 0x73, b = 0x73, rgb(255, 115, 115)
;; movk x8, #0xFFFF, LSL #16


; Sky
;
; Don't overwrite the sky colour every frame
; This is done in the mainloop now
; .offset 0x7100ba8260
; nop
;; .offset 0x7100ba8258
;; mov w12, #0xFF00
;; movk w12, #0xFF00, LSL #16

; .offset 0x710000df10
; nop
; nop
; movk x8, #0xFF00, LSL #32 ; r = 0x73, g = 0xFF, b = 0x73, rgb(115, 255, 115)
; movk x8, #0xFF00, LSL #48

; .offset 0x7100ba8258
; mov w12, #0x7DF3
; movk w12, #0xFFE9, LSL #16
