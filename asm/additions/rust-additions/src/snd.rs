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

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SoundMgrs {
    pub vtable: *mut SoundMgrsVtable,
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SoundMgrsVtable {
    pub _0:  [u8; 0x48],
    pub fn9: extern "C" fn(*mut SoundMgrs, i32, u64, u64),
}

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static SOUND_MGRS: *mut SoundMgrs;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn load_additional_sfx(sound_mgrs: u64, sound_id: i32) {
    unsafe {
        // Replaced instructions
        ((*(*SOUND_MGRS).vtable).fn9)(SOUND_MGRS, sound_id, 0, 0);

        /// 576 is the sound ID for GRP_D301_L1 which has the heart container
        /// sound
        ((*(*SOUND_MGRS).vtable).fn9)(SOUND_MGRS, 576, 0, 0);

        /// 545 is the sound ID for GRP_B210_L14 which has the ancient tablet
        /// sound
        ((*(*SOUND_MGRS).vtable).fn9)(SOUND_MGRS, 545, 0, 0);
    }
}

#[no_mangle]
pub fn assign_item_textbox_collection_sfx(
    fanfare_sound_mgr: *mut c_void,
    item_being_collected: flag::ITEMFLAGS,
) -> *mut c_void {
    unsafe {
        let mut sfx_id = match item_being_collected {
            flag::ITEMFLAGS::SPIRIT_VESSEL => 0x1528,
            flag::ITEMFLAGS::HEART_CONTAINER => 0x152E,
            flag::ITEMFLAGS::EMERALD_TABLET
            | flag::ITEMFLAGS::RUBY_TABLET
            | flag::ITEMFLAGS::AMBER_TABLET => 0x1882,
            flag::ITEMFLAGS::TEAR_OF_FARORE
            | flag::ITEMFLAGS::TEAR_OF_DIN
            | flag::ITEMFLAGS::TEAR_OF_NAYRU
            | flag::ITEMFLAGS::SACRED_TEAR => 0x1529,
            _ => 0,
        };

        // Move sfx_id into the correct register
        asm!("mov w1, {0:w}", in(reg) sfx_id);

        return fanfare_sound_mgr;
    }
}
