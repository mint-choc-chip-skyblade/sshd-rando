; Check for BotG before allowing to open the thunderhead
.offset 0x710092bed8
mov w8, #60
bl additions_jumptable
cbz w8, 0x710092bee8

; Don't play the thunderhead opening cs if skip_harp_playing is on
; This softlocks the player after the cutscene plays otherwise :p
; onlyif skip_harp_playing == on
.offset 0x71008398fc
b 0x71008399dc
