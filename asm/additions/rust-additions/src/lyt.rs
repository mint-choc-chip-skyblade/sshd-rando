#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::flag;

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

// Lyt stuff
#[repr(C, packed(1))]
pub struct dLytMsgWindow {
    pub _0:       [u8; 0xA90],
    pub text_mgr: *mut TextManagerMaybe,
}
assert_eq_size!([u8; 0xA98], dLytMsgWindow);

#[repr(C, packed(1))]
pub struct dLytPauseDisp {
    pub _0:        [u8; 0xC5E],
    pub is_paused: bool,
    pub _1:        [u8; 0x11],
}
assert_eq_size!([u8; 0xC70], dLytPauseDisp);

// Text stuff
#[repr(C, packed(1))]
pub struct TextManagerMaybe {
    pub _0:           [u8; 0x8AC],
    pub numeric_args: [u32; 5],
}
assert_eq_size!([u8; 0x8C0], TextManagerMaybe);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static mut CURRENT_STAGE_NAME: [u8; 8];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn set_top_dowsing_icon() -> u32 {
    unsafe {
        if &CURRENT_STAGE_NAME[..5] == b"F103\0" {
            return 0x11; // Tadtones
        }
        if flag::check_storyflag(271) != 0 {
            return 0x12; // Sandship
        }
        return 0x13; // Zelda
    }
}
