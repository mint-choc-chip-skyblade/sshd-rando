#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::item;

use core::arch::asm;
use core::ffi::{c_char, c_void};
use cstr::cstr;
use static_assertions::assert_eq_size;

// repr(C) prevents rust from reordering struct fields.
// packed(1) prevents rust from aligning structs to the size of the largest
// field.

// Using u64 or 64bit pointers forces structs to be 8-byte aligned.
// The vanilla code seems to be 4-byte aligned. To make extra sure, used
// packed(1) to force the alignment to match what you define.

// Always add an assert_eq_size!() macro after defining a struct to ensure it's
// the size you expect it to be.

//////////////////////
// ADD STRUCTS HERE //
//////////////////////

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static MINIGAME_STATE: u32;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn prevent_minigame_death(final_health: i32) -> i32 {
    unsafe {
        let mut new_final_health = final_health;
        // Set final health to 1 if we're in the thrill digger or bug heaven minigames
        if new_final_health <= 0 && (MINIGAME_STATE == 3 || MINIGAME_STATE == 5) {
            new_final_health = 1;
        }

        // Replaced Code
        if flag::check_storyflag(166) == 0 {
            asm!("mov w0, 1");
        } else {
            asm!("mov w0, 0");
        }
        asm!("tst w0, #0xFFFF");

        return new_final_health;
    }
}

#[no_mangle]
pub fn try_end_pumpkin_archery(bell_actor: *mut actor::dAcOBell) -> *mut actor::dAcOBell {
    unsafe {
        if ((*bell_actor).field_0x860 & 1) == 1 {
            let npc_pcs = actor::find_actor_by_type(actor::ACTORID::NPC_PCS, core::ptr::null_mut())
                as *mut actor::dAcNpcPcs;
            if npc_pcs != core::ptr::null_mut() {
                (*npc_pcs).pumpkin_archery_timer = 0;
            }
            asm!("mov w8, #1")
        } else {
            asm!("mov w8, #0")
        }
    }

    return bell_actor;
}
