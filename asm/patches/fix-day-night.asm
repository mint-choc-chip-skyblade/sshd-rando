; Set/unset day/night storyflag
; onlyif natural_night_connections == off
.offset 0x0877e248
mov w8, #9

; onlyif natural_night_connections == off
.offset 0x0877e260
bl 0x0865a070


; Make it look like night when the night flag is set
; onlyif natural_night_connections == off
.offset 0x08ba521c
mov w0, #899 ; day/night storyflag
bl check_storyflag
cmp w0, #0x1
b.ne 0x08ba547c ; daytime
b 0x08ba5474 ; nighttime


; Overwrite night sky filter
; .offset 0x08ba5474
; movz x8, #0x111, LSL #32
