; Fix freestanding item y offset at end of dAcItem::init
.offset 0x71004e5f94
bl 0x7100659ab8

.offset 0x71004e8f7c
b 0x71004e8f94


; Increase freestanding item size only if there's no default value already
.offset 0x71004e5128
ldr x10, [x19, #0xC] ; get param1
tbnz w10, #9, 0x71004e486c ; keep default value if not rando-patched item

ldrh w10, [x19, #0x13E] ; get rotation y
tbnz w10, #0, 0x71004e486c ; keep default value if default scale bit is set

b 0x71004e4864 ; act like slingshot for rando-patched items

; Change slingshot scale size (reused for rando-patched items)
.offset 0x71004ea2c8
fmov s0, 0x40000000 ; 2.0


; Prevent spawned items acting like rando-patched items
.offset 0x71004eba84 ; store actorParam1Base early to save instructions later
orr w19, w1, #0x200 ; the 9th bit (zero-indexed)
mov w21, w0

.offset 0x71004eba98 ; the instruction that was replaced above
and w0, w1, #0x1FF

; Use freed space in bucha to create a new function header for dAcItem__spawnRandoItemWithParams
; Copied from dAcItem__spawnItemWithParams (0x71004eba70)
.offset 0x71005c2060
stp x24, x23, [sp, #-0x40]!
stp x22, x21, [sp, #0x10]
stp x20, x19, [sp, #0x20]
stp x29, x30, [sp, #0x30]
add x29, sp, #0x30
mov w19, w1 ; don't change bit 9 (allows for rando patched *spawned* items)
b 0x71004eba88 ; branch to the rest of dAcItem__spawnItemWithParams


; Always act like Rattle

; dAcItem::init
.offset 0x71004e4e54
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004e4e94 ; check if is patched freestanding item

.offset 0x71004e4e08
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004e4e8c ; check if is patched freestanding item


; some dAcItem func (when spawned from things like trees?)
.offset 0x71004e3ab0
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004e39f4 ; check if is patched freestanding item

; dAcItem carry/beetle funcs
.offset 0x71004de294
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004de2a4 ; check if is patched freestanding item

.offset 0x71004de448
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004de458 ; check if is patched freestanding item


; dAcItem::stateWaitEnter
.offset 0x71004db344
ldr w8, [x19, #0xC] ; put param1 in w8
tbnz w8, #9, 0x71004db358 ; check if is patched freestanding item (this case is inverted)

.offset 0x71004dd078
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004dd088 ; check if is patched freestanding item


; some dAcItem sound effect func
; .offset 0x71004e310c
; ldr w8, [x19, #0xC] ; put param1 in w8
; tbz w8, #9, 0x71004e31c8 ; check if is patched freestanding item


; Make all items able to be picked up by beetle
.offset 0x71004e3788
b.hi 0x71004e37a8 ; branch over checks to prevent being picked up by beetle

.offset 0x71004e37a4
nop



; Fix spawned items that shouldn't have textboxes
; LMF conveyor stamina fruits
.offset 0x7100e50318
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Player shot arrows
.offset 0x710002b1dc
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x710002bccc
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Boko shot arrows
.offset 0x71002ce808
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71002d7b94
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Some arrow thing?
.offset 0x7100a7d988
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Lizalfos Tails
.offset 0x71003ac274
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71003ac348
mov w8, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71003ac550
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Heart Flowers
.offset 0x71004ac154
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71004ac2c8
mov w8, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71004ad6dc
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Treasures
.offset 0x71006f0ad8
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71006f0b7c
mov w8, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Ancient Flowers
.offset 0x71007cdbf8
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x71007cdf3c
mov w2, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

; Insects
.offset 0x7100a97b18
mov w9, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x7100a97a28
mov w10, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)

.offset 0x7100a97acc
mov w10, #0xfe00 ; from 0xfc00 (sets bit 9 of param1)
