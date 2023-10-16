; Patch dAcItem fields to fix y-offsets and scaling
.offset 0x08f14514
mov w8, #13
bl 0x0865a070

; Fix freestanding item y offset at end of dAcItem::init
.offset 0x084e5f94
bl 0x08659ab8

.offset 0x084e8f7c
b 0x084e8f94


; Increase freestanding item size only if there's no default value already
.offset 0x084e5128
ldr x10, [x19, #0xC] ; get param1
tbnz w10, #9, 0x084e486c ; keep default value if not rando-patched item

ldrh w10, [x19, #0x13E] ; get rotation y
tbnz w10, #0, 0x084e486c ; keep default value if default scale bit is set

b 0x084e4864 ; act like slingshot for rando-patched items

; Change slingshot scale size (reused for rando-patched items)
.offset 0x084ea2c8
fmov s0, 0x40000000 ; 2.0


; Prevent spawned items acting like rando-patched items
.offset 0x084eba84 ; store actorParam1Base early to save instructions later
orr w19, w1, #0x200 ; the 9th bit (zero-indexed)
mov w21, w0

.offset 0x084eba98 ; the instruction that was replaced above
and w0, w1, #0x1FF

; Use freed space in bucha to create a new function header for dAcItem__spawnRandoItemWithParams
; Copied from dAcItem__spawnItemWithParams (0x084eba70)
.offset 0x085c2060
stp x24, x23, [sp, #-0x40]!
stp x22, x21, [sp, #0x10]
stp x20, x19, [sp, #0x20]
stp x29, x30, [sp, #0x30]
add x29, sp, #0x30
mov w19, w1 ; don't change bit 9 (allows for rando patched *spawned* items)
b 0x084eba88 ; branch to the rest of dAcItem__spawnItemWithParams


; Always act like Rattle

; dAcItem::init
.offset 0x084e4e54
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084e4e94 ; check if is patched freestanding item

.offset 0x084e4e08
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084e4e8c ; check if is patched freestanding item


; some dAcItem func (when spawned from things like trees?)
.offset 0x084e3ab0
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084e39f4 ; check if is patched freestanding item

; dAcItem carry/beetle funcs
.offset 0x084de294
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084de2a4 ; check if is patched freestanding item

.offset 0x084de448
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084de458 ; check if is patched freestanding item


; dAcItem::stateWaitEnter
.offset 0x084db344
ldr w8, [x19, #0xC] ; put param1 in w8
tbnz w8, #9, 0x084db358 ; check if is patched freestanding item (this case is inverted)

.offset 0x084dd078
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084dd088 ; check if is patched freestanding item


; some dAcItem sound effect func
.offset 0x084e310c
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x084e31c8 ; check if is patched freestanding item


; Make all items able to be picked up by beetle
.offset 0x084e3788
b.hi 0x084e37a8 ; branch over checks to prevent being picked up by beetle

.offset 0x084e37a4
nop
