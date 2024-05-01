#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::color;
use crate::debug;
use crate::input;

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

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ReloadColorFader {
    pub _0:             [u8; 0x14],
    pub current_state:  u32,
    pub unk:            u32,
    pub previous_state: u32,
    pub _1:             [u8; 0x65],
    pub other_state:    u8,
}
assert_eq_size!([u8; 0x86], ReloadColorFader);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static BOOT_PTR: *mut c_void;
    static mut RESPAWN_TYPE: u8;
    static dSystem: *mut c_void;
    static reload_color_fader: *mut ReloadColorFader;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn do_soft_reset(fader: *mut ReloadColorFader);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn main_loop_inject() -> *mut c_void {
    unsafe {
        if (input::check_button_held(input::BUTTON_INPUTS::LEFT_STICK_BUTTON)
            && input::check_button_held(input::BUTTON_INPUTS::A_BUTTON)
            && input::check_button_held(input::BUTTON_INPUTS::R_BUTTON))
        {
            (*reload_color_fader).other_state = 1;
            (*reload_color_fader).previous_state = (*reload_color_fader).current_state;
            (*reload_color_fader).current_state = 1;
            do_soft_reset(reload_color_fader);
        }

        color::handle_colors();

        return dSystem;
    }
}

#[no_mangle]
pub fn activate_back_in_time(param1: *mut c_void) -> *mut c_void {
    // This is patched into the do_soft_reset function
    unsafe {
        if input::check_button_held(input::BUTTON_INPUTS::L_BUTTON) {
            RESPAWN_TYPE = 3;
        }

        // Replaced instructions
        asm!("mov x8, {0:x}", in(reg) BOOT_PTR);

        return param1;
    }
}
