; Patches nighttime Rupin so his night market choices cycle in a loop without
; needing to sleep to a new night or rely on rng to get new choices
;
; The event flow has been changed so that the "make_actor_do_something" flow
; can be repeatedly triggered. Each time this happens,
; dAcNpcDouguyaNight::doEventFlowAction is called with command 8.
;
; The following asm patches the command 8 case to replace the code which
; forces the choices to remain the same until a new night (and relies on rng)
; to instead loop through the choices sequentially.
.offset 0x7100584dd0
; x8 contains a pointer to the storyflag_mgr vtable
ldr x8,[x8, #0x50] ; get the get_flag_or_counter function
mov w1, #0x28C ; night market flag
blr x8
cmp w0, #0

; put the new night market value into w2
; value decrements and rolls over from 0 to 4, then -1
b.ne rupin_increment
mov w2, #4

rupin_increment:
sub w2, w0, #1

ldr x0, [x20, #0x1f0] ; get pointer to the storyflag_mgr in x0
mov w1, #0x28C ; flag
ldr x8, [x0]
ldr x8,[x8, #0x48] ; get the set_flag_or_counter_to_value function
blr x8

; skips 31 instructions
b 0x7100584e80



; Patches nighttime Strich to behave the same as Rupin, above.
.offset 0x71005b6db0
; x8 contains a pointer to the storyflag_mgr vtable
ldr x8,[x8, #0x50] ; get the get_flag_or_counter function
mov w1, #0x28C ; night market flag
blr x8
cmp w0, #0

; put the new night market value into w2
; value decrements and rolls over from 0 to 4, then -1
b.ne strich_increment
mov w2, #4

strich_increment:
sub w2, w0, #1

ldr x0, [x20, #0x1f0] ; get pointer to the storyflag_mgr in x0
mov w1, #0x28C ; flag
ldr x8, [x0]
ldr x8,[x8, #0x48] ; get the set_flag_or_counter_to_value function
blr x8

; skips 31 instructions
b 0x71005b6e60
