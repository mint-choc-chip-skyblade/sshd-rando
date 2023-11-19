; Don't remove bird statues from landing map after Levias
.offset 0x08c5b0cc
mov x0, #0x0

; Change HD progression storyflag for inner FS bird statue
.offset 0x093a2530 ; 0x710139e530
.short 901 ; rando beaten FS storyflag

; Change HD progression storyflag for Temple of Time bird statue
.offset 0x093a25c8 ; 0x710139e5c8
.short 935 ; rando exit out of LMF for first time storyflag
