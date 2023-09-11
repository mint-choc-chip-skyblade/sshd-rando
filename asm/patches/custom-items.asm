; Assign model index for new items
.offset 0x093a0d84
; Small Keys
.2byte 0 ; SV Small Key (200)
.2byte 0 ; LMF Small Key (201)
.2byte 0 ; AC Small Key (202)
.2byte 0 ; FS Small Key (203)
.2byte 0 ; SSH Small Key (204)
.2byte 0 ; SK Small Key (205)
.2byte 0 ; Caves Small Key (206)

; Maps
.2byte 0x2B ; SV Map (207)
.2byte 0x2B ; ET Map (208)
.2byte 0x2B ; LMF Map (209)
.2byte 0x2B ; AC Map (210)
.2byte 0x2B ; FS Map (211)
.2byte 0x2B ; SSH Map (212)
.2byte 0x2B ; SK Map (213)


; Assign item get animation
; the good game SS is, it assumes the best default and crashes :p
.offset 0x0937af0c
.int 0 ; SV Small Key      (200)
.int 0 ; LMF Small Key     (201)
.int 0 ; AC Small Key      (202)
.int 0 ; FS Small Key      (203)
.int 0 ; SSH Small Key     (204)
.int 0 ; SK Small Key      (205)
.int 0 ; Caves Small Key   (206)
.int 0x1000 ; SV Map       (207)
.int 0x1000 ; ET Map       (208)
.int 0x1000 ; LMF Map      (209)
.int 0x1000 ; AC Map       (210)
.int 0x1000 ; FS Map       (211)
.int 0x1000 ; SSH Map      (212)
.int 0x1000 ; SK Map       (213)
.int 0 ; Group of Tadtones (214)
.int 0x1000 ; Scrapper     (215)


.offset 0x084e0d04
mov w8, #0
bl 0x0865a070
