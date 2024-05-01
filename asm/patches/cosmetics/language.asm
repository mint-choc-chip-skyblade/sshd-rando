; Always take the same lang path
.offset 0x710105eb88
b 0x710105edd8

; onlyif language == chinese
; .offset 0x710105edd8
; mov w8, #4
; mov w9, #7

; onlyif language == dutch
.offset 0x710105edd8
mov w8, #2
mov w9, #6

; onlyif language == french_fr
.offset 0x710105edd8
mov w8, #2
mov w9, #3

; onlyif language == french_us
.offset 0x710105edd8
mov w8, #1
mov w9, #3

; onlyif language == german
.offset 0x710105edd8
mov w8, #2
mov w9, #2

; onlyif language == italian
.offset 0x710105edd8
mov w8, #2
mov w9, #5

; onlyif language == japanese
; .offset 0x710105edd8
; mov w8, #0
; mov w9, #0

; onlyif language == korean
; .offset 0x710105edd8
; mov w8, #3
; mov w9, #9

; onlyif language == russian
; .offset 0x710105edd8
; mov w8, #5
; mov w9, #10

; onlyif language == spanish_es
.offset 0x710105edd8
mov w8, #2
mov w9, #4

; onlyif language == spanish_us
.offset 0x710105edd8
mov w8, #1
mov w9, #4

; onlyif language == taiwanese
; .offset 0x710105edd8
; mov w8, #6
; mov w9, #8

; onlyif language == english_gb
.offset 0x710105edd8
mov w8, #2
mov w9, #1

; onlyif language == english_us
.offset 0x710105edd8
mov w8, #1
mov w9, #1
