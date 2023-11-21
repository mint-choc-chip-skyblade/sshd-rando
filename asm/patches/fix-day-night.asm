; Set/unset day/night storyflag
; onlyif natural_night_connections == off
.offset 0x710077e248
mov w8, #9

; onlyif natural_night_connections == off
.offset 0x710077e260
bl additions_jumptable


; Make it look like night when the night flag is set
; onlyif natural_night_connections == off
.offset 0x7100ba521c
mov w0, #899 ; day/night storyflag
bl check_storyflag
cmp w0, #0x1
b.ne 0x7100ba547c ; daytime
b 0x7100ba5474 ; nighttime


; Show moon instead of sun when the night flag is set
;
; Show moon
; onlyif natural_night_connections == off
.offset 0x7100ec20b0
mov w8, #10
bl additions_jumptable ; check day/night flag
cmp w0, #0x1
b.ne 0x7100ec290c ; daytime = no moon

; Show sun
; onlyif natural_night_connections == off
.offset 0x7100ec3c04
mov w8, #10
bl additions_jumptable ; check day/night flag
tbnz w0, #0x0, 0x7100ec3b60 ; night time = no sun


; Overwrite night sky filter
; .offset 0x7100ba5474
; movz x8, #0x111, LSL #32
