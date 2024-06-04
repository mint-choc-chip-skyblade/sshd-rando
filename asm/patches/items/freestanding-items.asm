.offset 0x71004e8f7c
b 0x71004e8f94


; Always let triforces fall when bonked
.offset 0x71004dc09c
mov w8, #3 ; -> branch over code that prevents triforces falling

; Allow Triforces and Heart Pieces to be whippable
.offset 0x71004e4dd8
nop ; heart piece check -> false
mov w9, #3 ; triforce check -> false

.offset 0x71004e3620
mov w10, w11 ; triforce check -> false

.offset 0x71004e4e14
b 0x71004e4ea0 ; heart piece check -> false


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

.offset 0x71004ea2e8
mov w8, #62
b additions_jumptable


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
; Special case for items in sand piles
.offset 0x71004db340
mov w8, #33
bl additions_jumptable

.offset 0x71004dd078
ldr w8, [x19, #0xC] ; put param1 in w8
tbz w8, #9, 0x71004dd088 ; check if is patched freestanding item


; Make all items able to be picked up by beetle
.offset 0x71004e3788
b.hi 0x71004e37a8 ; branch over checks to prevent being picked up by beetle

.offset 0x71004e37a4
nop

; Rando patches for dAcItem::Init
.offset 0x71004e44ac
mov w8, #23
bl additions_jumptable


; Make freestanding items spin
.offset 0x71004eb0b0
mov w8, #32
b additions_jumptable
.offset 0x71004e49ec
add x9, x9, #0xb0 ; use above func for other default case


; Prevent picking up Skyview Temple - Item behind Bars
; with a Skyward Spin Attack
; Also use this to remove textboxes from common items
.offset 0x71004e621c
mov x0, x19
mov w8, #61
bl additions_jumptable
