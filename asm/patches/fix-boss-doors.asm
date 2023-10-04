; Have boss doors check for boss defeat storyflags
; instead of dungeon defeat storyflags to be openable
; in reverse. This modofies a data array that holds
; storyflags in 4-byte elements
.offset 0x09398550
.word 0x53  ; Defeated Ghirahim 1
.word 0x7   ; Defeated Scaldera
.word 0x32C ; Defeated Moldarach
.word 0x288 ; Defeated Koloktos
.word 0x54  ; Defeated Ghirahim 2
.word 0x3A5 ; Defeated Tentalus