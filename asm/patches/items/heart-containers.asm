; in dAcOItemHeartContainer::stateFallUpdate
.offset 0x710080cce0
ldrb w0, [x19, 0xe] ; get rando item id from param1 >> 16 & 0xFF

; in dAcOItemHeartContainer::stateWaitGetUpdate
.offset 0x710080d65c
ldrb w0, [x19, 0xe] ; get rando item id from param1 >> 16 & 0xFF

; in dAcOItemHeartContainer::stateWaitGetQuakeUpdate
.offset 0x710080da3c
ldrb w0, [x19, 0xe] ; get rando item id from param1 >> 16 & 0xFF

