; Assign model index for new items
.offset 0x71013a0d84
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
.offset 0x710137af0c
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
