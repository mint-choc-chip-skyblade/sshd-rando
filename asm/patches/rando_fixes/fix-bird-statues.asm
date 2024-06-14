; Don't remove bird statues from landing map after Levias
.offset 0x7100c5b0cc
mov x0, #0x0

; Change Sealed Grounds Statue to use its Scene Flag instead of the story flag
.offset 0x71013a247c
.word 0x00000000 ; Use scene flag
.short 0x000A    ; sealed grounds scene
.short 0x0023    ; flag number

; Change HD progression storyflag for Sealed Grounds Statue
.offset 0x71013a24cc
.word 0x00000000 ; Use scene flag
.short 0x000A    ; Sealed Grounds scene
.short 0x0023    ; flag number

; Change HD progression storyflag for Volcano Entry Statue
.offset 0x71013a2508
.short -1 ; flag number

; Change HD progression storyflag for inner FS bird statue
.offset 0x71013a2530
.short -1 ; rando beaten FS storyflag

; Change HD progression storyflag for Lanayru Mine Statue
.offset 0x71013a2598
.short -1 ; flag number

; Change HD progression storyflag for Temple of Time bird statue
.offset 0x71013a25c8
.short -1 ; rando exit out of LMF for first time storyflag

; Don't give great tree bird statue from storyflag
.offset 0x71013a24a8
.short -1

; Don't give lanayru gorge bird statue from storyflag
.offset 0x71013a25f0
.short -1
