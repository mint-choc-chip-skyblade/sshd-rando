; Don't change talking entrypoint for Fledge after delivering the barrel to Henya

; In stateSearchObjUpdate
.offset 0x7100563c10
b 0x7100563ce0

; In vtable func
.offset 0x71005685f8
nop

; In setVelocityZeroNoReturn5 (obviously an incorrect name ^^')
.offset 0x7100567b4c
nop
nop
nop
nop
nop
nop
nop

; In dAcNpcCeLady::update
.offset 0x710056cac4
nop

; In dAcOBarrel_c::stateGrabUpUpdate
.offset 0x7100717a6c
b 0x7100717bdc ; creates a lot of free instruction space

; In dAcOtubo::stateGrabUpdate
.offset 0x71009b85c8
b 0x71009b8738
