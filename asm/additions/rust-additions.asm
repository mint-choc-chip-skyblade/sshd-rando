; Start using subsdk8 0x500 bytes into the .text section
; 1st 0x500 bytes are left to make sure none of the subsdk setup is mangled
; The next 0x1000 bytes are reserved for the landingpad
; The next 0x500 bytes are reserved for additions not written in rust

; Custom rust functions need to be defined so that they can be correctly linked
; to the function calls in additions-landingpad.asm. Defining one of the rust
; symbols seems to define all of the rest which is nice ^^
.offset 0x712e0a7000
.global main_loop_inject
.type main_loop_inject, @function
