; search 2
; .offset 0x08d3c300
; mov w0, #1

.offset 0x08d3c2fc
ldr x8, [x8, #0x20] ; check for b-butten *held* instead

.offset 0x08d3c39c
mov w0, #1
.offset 0x08d3c184
mov w0, #1
.offset 0x08d3c424
mov w0, #1
.offset 0x08d3c460
mov w0, #1

; search 3
; Make 1st textbox instantly appear
.offset 0x08d3b9e0
mov w0, #1

; search 4
; penultimate textbox stuff
; .offset 0x08d3cc80
; mov w0, #1

.offset 0x08d3cc7c
ldr x8, [x8, #0x20] ; check for b-butten *held* instead

.offset 0x08d3cd4c
mov w0, #1
.offset 0x08d3cb2c
mov w0, #1
.offset 0x08d3cbbc
mov w0, #1
.offset 0x08d3ca34
mov w0, #1