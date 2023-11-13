; Ignore Faron Trial completion status for Goddess Walls
.offset 0x08948344 ; 0x7100944344
nop

; Ignore Ballad of the Goddess itemflag check in Goddess Wall init
; This gets checked later so that you don't need to reload the area
; to be able to activate Goddess Walls
.offset 0x0894838c ; 0x710094438c
nop

; Add check for Ballad in stateWaitHarpUpdate
.offset 0x08940ca0 ; 0x710093cca0
mov w8, #17
bl additions_jumptable
nop
nop
nop


; Change flags stopping butterflies from spawning
.offset 0x08e6d298 ; 0x7100e69298
mov w1, #9 ; replace Faron Trial / Scale flag with Harp flag

.offset 0x08e6d31c ; 0x7100e6931c
nop ; remove check for imp 1 defeated


; Trial butterflies
.offset 0x08e6d538 ; 0x7100e69538
mov w1, #919 ; Faron Trial completed rando storyflag

.offset 0x08e6d560 ; 0x7100e69560
mov w1, #920 ; Eldin Trial completed rando storyflag

.offset 0x08e6d588 ; 0x7100e69588
mov w1, #921 ; Lanayru Trial completed rando storyflag

.offset 0x08e6d668 ; 0x7100e69668
mov w1, #922 ; Hylia Trial completed rando storyflag
