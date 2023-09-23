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
.offset 0x084eba98
orr w19, w1, #0x200 ; the 9th bit (zero-indexed)


; Always act like Baby Rattle

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
