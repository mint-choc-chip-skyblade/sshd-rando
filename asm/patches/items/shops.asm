; Unlock Iron Shield
.offset 0x710164054c
.short 0xFFFF

; Unlock Sacred Shield
.offset 0x71016405a0
.short 0xFFFF

; Unlock Small Seed Satchel
.offset 0x7101640648
.short 0xFFFF

; Unlock Small Quiver
.offset 0x710164069c
.short 0xFFFF

; Unlock Small Bomb Bag
.offset 0x71016406f0
.short 0xFFFF


; Rotate shop items
.offset 0x7100b0595c
mov w8, #66
bl additions_jumptable

; Set shop item height
.offset 0x7100afff98
mov w8, #67
bl additions_jumptable

; Init dAcShopSample__Subclasses based on their shop_index instead of the item
; being sold. The vanilla game checks the shop_index and behaves correctly for
; the vanilla item that's placed there. Rando breaks the assumptions made so
; the init is changed as follows:
; 
; * shop_indexes 30+ are unchanged (Luv's potion shop)
; * shop_indexes 20, 21, and 22 are vanilla pouches and the vanilla game
; increments a storyflag counter to keep track of the chain. This works in
; rando too so force these shop_indexes to always behave like vanilla (ignore
; the checks for what item is being sold)
; * all others get treated like the vanilla extra wallet shop sample. This
; gets heavily modified below. The vanilla game already has storyflags for the
; vanilla Life Medal and Heart Piece shop samples so those will be reused. The
; remaining shop samples behave specifically for their vanilla items so
; storyflags will be given to them so they will behave consistently for rando.
.offset 0x7100b01f0c
; sold out
cmp w9, #0x7F
b.eq 0x7100b01fc4
; init Luv's potion shop
cmp w9, #30 ; w9 holds the shop_index
b.ge 0x7100b022c0
cmp w9, #20 ; Beedle 300R
b.eq 0x7100b023a8
cmp w9, #21 ; Beedle 600R
b.eq 0x7100b025f8
cmp w9, #22 ; Beedle 1200R
b.eq 0x7100b0256c
b 0x7100b02054 ; otherwise, got to vanilla extra wallet init

; Keep shop_index when creating subclass
.offset 0x7100b02064
mov w20, w9
.offset 0x7100b020cc
mov w8, w20

; Set sold out storyflag when giving item
; and ignore the extra wallet storyflag counter
.offset 0x7100b042d4
mov w8, #68
bl additions_jumptable
b 0x7100b042f4

; Don't increment vanilla extra wallet storyflag counter
.offset 0x7100b043dc
b 0x7100b04400

; Check sold out storyflag to show correct item on the shop sample
.offset 0x7100b04220
; x0 has the dAcShopSample__Subclass so get the shop_index from it
ldrh w0, [x0, #8]
mov w8, #69
b additions_jumptable
