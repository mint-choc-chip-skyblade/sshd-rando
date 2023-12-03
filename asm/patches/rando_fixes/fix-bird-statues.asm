; Don't remove bird statues from landing map after Levias
.offset 0x7100c5b0cc
mov x0, #0x0

; Change HD progression storyflag for inner FS bird statue
.offset 0x71013a2530
.short -1 ; rando beaten FS storyflag

; Change HD progression storyflag for Temple of Time bird statue
.offset 0x71013a25c8
.short -1 ; rando exit out of LMF for first time storyflag
