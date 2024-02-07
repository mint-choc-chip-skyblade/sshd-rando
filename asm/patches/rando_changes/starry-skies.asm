; After handling daytime stuff, also run the nighttime code (stars!)
; onlyif starry_skies == on
.offset 0x7100ec3858
b 0x7100ec2dd0

; The sun is specifically kept becauses the camera (x22) isn't overwritten
; HDR is lucky in that the assembler didn't reuse this register, unlike SDR
; where the camera (r14) was reused


; Remove weird camera culling on Skyloft and The Sky
; onlyif starry_skies == on
.offset 0x7100ec3238
b 0x7100ec3344 ; removes a lot of instructions
