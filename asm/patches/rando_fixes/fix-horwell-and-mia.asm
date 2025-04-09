; make Horwell always interactable
.offset 0x7100661b30
mov w8, #31
bl additions_jumptable

; Control if Horwell spawns
.offset 0x7100660a10
mov w8, #84
bl additions_jumptable


; Control if Mia the remlit spawn
.offset 0x710041a744
mov w8, #85
bl additions_jumptable
