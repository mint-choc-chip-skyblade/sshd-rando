; Assign model index for new items
.offset 0x71013a0d84
; Small Keys
.2byte 0 ; SV Small Key         (200)
.2byte 0 ; LMF Small Key        (201)
.2byte 0 ; AC Small Key         (202)
.2byte 0 ; FS Small Key         (203)
.2byte 0 ; SSH Small Key        (204)
.2byte 0 ; SK Small Key         (205)
.2byte 0 ; Caves Small Key      (206)

; Maps
.2byte 0x2B ; SV Map            (207)
.2byte 0x2B ; ET Map            (208)
.2byte 0x2B ; LMF Map           (209)
.2byte 0x2B ; AC Map            (210)
.2byte 0x2B ; FS Map            (211)
.2byte 0x2B ; SSH Map           (212)
.2byte 0x2B ; SK Map            (213)

.2byte 0xA7 ; Group of Tadtones (214)
.2byte 0xA7 ; Scrapper          (215)
.2byte 0xA7 ; Unused            (216)
.2byte 0xA7 ; Unused            (217)
.2byte 0xA7 ; Unused            (218)
.2byte 0xA7 ; Unused            (219)
.2byte 0xA7 ; Unused            (220)
.2byte 0xA7 ; Unused            (221)
.2byte 0xA7 ; Unused            (222)
.2byte 0xA7 ; Unused            (223)
.2byte 0xA7 ; Unused            (224)
.2byte 0xA7 ; Unused            (225)
.2byte 0xA7 ; Unused            (226)
.2byte 0xA7 ; Unused            (227)
.2byte 0xA7 ; Unused            (228)
.2byte 0xA7 ; Unused            (229)
.2byte 0xA7 ; Unused            (230)
.2byte 0xA7 ; Unused            (231)
.2byte 0xA7 ; Unused            (232)
.2byte 0xA7 ; Unused            (233)
.2byte 0xA7 ; Unused            (234)
.2byte 0xA7 ; Unused            (235)
.2byte 0xA7 ; Unused            (236)
.2byte 0xA7 ; Unused            (237)
.2byte 0xA7 ; Unused            (238)
.2byte 0xA7 ; Unused            (239)
.2byte 0x1D ; Trap              (240)
.2byte 0x1D ; Trap              (241)
.2byte 0x1D ; Trap              (242)
.2byte 0x1D ; Trap              (243)
.2byte 0x1D ; Trap              (244)
.2byte 0x1D ; Trap              (245)
.2byte 0x1D ; Trap              (246)
.2byte 0x1D ; Trap              (247)
.2byte 0x1D ; Trap              (248)
.2byte 0x1D ; Trap              (249)
.2byte 0x1D ; Trap              (250)
.2byte 0x1D ; Trap              (251)
.2byte 0x1D ; Trap              (252)
.2byte 0x1D ; Trap              (253)
.2byte 0x1D ; Trap              (254)


; Assign item get animation
; the good game SS is, it assumes the best default and crashes :p
.offset 0x710137af0c
.int 0      ; SV Small Key      (200)
.int 0      ; LMF Small Key     (201)
.int 0      ; AC Small Key      (202)
.int 0      ; FS Small Key      (203)
.int 0      ; SSH Small Key     (204)
.int 0      ; SK Small Key      (205)
.int 0      ; Caves Small Key   (206)
.int 0x1000 ; SV Map            (207)
.int 0x1000 ; ET Map            (208)
.int 0x1000 ; LMF Map           (209)
.int 0x1000 ; AC Map            (210)
.int 0x1000 ; FS Map            (211)
.int 0x1000 ; SSH Map           (212)
.int 0x1000 ; SK Map            (213)
.int 0      ; Group of Tadtones (214)
.int 0x1000 ; Scrapper          (215)
.int 0      ; Unused            (216)
.int 0      ; Unused            (217)
.int 0      ; Unused            (218)
.int 0      ; Unused            (219)
.int 0      ; Unused            (220)
.int 0      ; Unused            (221)
.int 0      ; Unused            (222)
.int 0      ; Unused            (223)
.int 0      ; Unused            (224)
.int 0      ; Unused            (225)
.int 0      ; Unused            (226)
.int 0      ; Unused            (227)
.int 0      ; Unused            (228)
.int 0      ; Unused            (229)
.int 0      ; Unused            (230)
.int 0      ; Unused            (231)
.int 0      ; Unused            (232)
.int 0      ; Unused            (233)
.int 0      ; Unused            (234)
.int 0      ; Unused            (235)
.int 0      ; Unused            (236)
.int 0      ; Unused            (237)
.int 0      ; Unused            (238)
.int 0      ; Unused            (239)
.int 0x2000 ; Trap              (240)
.int 0x2000 ; Trap              (241)
.int 0x2000 ; Trap              (242)
.int 0x2000 ; Trap              (243)
.int 0x2000 ; Trap              (244)
.int 0x2000 ; Trap              (245)
.int 0x2000 ; Trap              (246)
.int 0x2000 ; Trap              (247)
.int 0x2000 ; Trap              (248)
.int 0x2000 ; Trap              (249)
.int 0x2000 ; Trap              (250)
.int 0x2000 ; Trap              (251)
.int 0x2000 ; Trap              (252)
.int 0x2000 ; Trap              (253)
.int 0x2000 ; Trap              (254)


.offset 0x71004e0d04
mov w8, #0
bl additions_jumptable

; Don't allow items to set dungeonflags
; Could be used to allow tears to be placed anywhere
; .offset 0x71004e335c
; nop


; Only set dungeonflags from items if the item is a trial tear
.offset 0x71004e33b4
cmp w8, #43 ; 1st tear item
b.lt 0x71004e3360 ; pretend like it's not a dungeonflag item
cmp w8, #46 ; last tear item
b.gt 0x71004e3360 ; pretend like it's not a dungeonflag item
b 0x71004e3454 ; continue on to set dungeonflag
