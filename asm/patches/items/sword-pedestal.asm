; Replace setting the Goddess Sword item flag with
; setting a custom story flag to trigger the items
; from pulling the Goddess Sword

; Goddess Sword checks

.offset 0x7100a1759c
mov w8, #3
bl additions_jumptable
nop ; don't call the debug(?) function when setting itemflags
nop

; Remove Goddess Sword textbox after pulling the sword
.offset 0x7100a494e4
mov w2, #0xff ; -1 (don't show a textbox after the event)


; Only spawn sword if you haven't already gotten the checks
.offset 0x71008c4528 ; in init
mov w1, #951 ; storyflag for goddess statue sword checks

.offset 0x71008c5268 ; in update
mov w1, #951 ; storyflag for goddess statue sword checks

.offset 0x71008c3af4 ; in some state change
mov w1, #951 ; storyflag for goddess statue sword checks


; True Master Sword check

; Set the Boko Base storyflag that restricts the use of the sword before the pull event. This
; means that all the vanilla code which checks that flag doesn't need to be painstakingly sifted
; through to make sure it all behaves perfectly for the rando.
.offset 0x71008c4fbc
mov w8, #76
bl additions_jumptable

; Remove True Master Sword textbox after pulling the sword
.offset 0x7100a17588
; mov w2, #0xFF ; -1 (don't show a textbox after the event)
mov w8, #77
bl additions_jumptable


; As the restricted sword flag only gets set when the player tries to pull the sword, the code
; which spawns the sword needs to be updated to check for the custom rando flag that only sets
; after collecting the check instead
.offset 0x71008c4504 ; in init
mov w1, #952 ; storyflag for boko base sword check
.offset 0x71008c450c
cmp w0, #1

.offset 0x71008c5244 ; in update
mov w1, #952 ; storyflag for boko base sword check
.offset 0x71008c524c
cmp w0, #1

.offset 0x71008c3ad0 ; in some state change
mov w1, #952 ; storyflag for boko base sword check
.offset 0x71008c3ad8
cmp w0, #1


; Fix Boko Base sword model.
; 
; The game hardcodes the Goddess Statue sword to always be the Goddess Sword. However, for some
; reason, the game is programmed to use the player's currently equipped sword when in Boko Base.
; This wouldn't be a big issue in SDR but the code in HDR has been optimised to hell and back and
; is a complete mess to follow.
; 
; The general idea is that the sword models are all loaded into memory in the same location. In
; dPlayer::initSwordModels, the code abuses this fact and loads the model from a fixed address +
; an offset based on the equipped sword. In the sword pedestal code, the game can just pull the
; model data from the player struct. However, because the desired behaviour is to always show TMS,
; the following two patches must re-create the behaviour found in dPlayer::initSwordModels.

.offset 0x71008c46bc
mov w2, w8 ; put sword_type in w2
mov w8, #78
bl additions_jumptable
str x0, [x19, #0x478]
b 0x71008c4714
