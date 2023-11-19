; Rocks
; Don't play event when blowing up rocks
.offset 0x08737a64
mov w8, #0xFF


; Logs
; Don't play event when pushing logs
.offset 0x088440e8
mov x19, x0 ; move self into x19 early

.offset 0x088440f4
add x0, x0, #0x1000 ; add offset to w0 instead of in the strb
strb w11, [x0, #0x3FD]

mov w9, #0xFF ; use now free w9 to store -1 for the event index

.offset 0x08844104
strb w9, [x0, #0x3FC] ; store new event index


; Ropes
; Don't play event when knocking down ivy ropes
.offset 0x088154e8
mov w8, #0xFF


; Arrow Switches
; DOESN'T WORK
; don't play event when shooting arrow switches (eyes)
; .offset 0x086f5aac
; mov w8, #0xFF

; Don't open collection screen when getting treasures/gratitude crystals
.offset 0x08bf0590
b 0x08bf0674 ; skip to the end of the function

; Timeshift Stones
; Don't play first time timeshift stone cutscenes
.offset 0x0897eabc ; 0x710097aabc
mov w8, #18
bl additions_jumptable

; Always set isFirstStone to false
.offset 0x0897eadc ; 0x710097aadc
strb wzr, [x23, #0xc1]
