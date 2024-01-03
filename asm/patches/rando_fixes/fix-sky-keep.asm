; Set Stone of Trials placed flag when opening Sky Keep
.offset 0x710098312c
b 0x7100659ac0


; Fix Sky Keep dungeon exit
.offset 0x7100e419c0
mov w8, #11

.offset 0x7100e419f0
bl additions_jumptable
