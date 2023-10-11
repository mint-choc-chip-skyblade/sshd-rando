; Set Stone of Trials placed flag when opening Sky Keep
.offset 0x0898312c
b 0x08659ac0


; Fix Sky Keep dungeon exit
.offset 0x08e419c0
mov w8, #11

.offset 0x08e419f0
bl 0x0865a070
