#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::flag;
use crate::math;

use core::arch::asm;
use core::ffi::{c_char, c_void};
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
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn spawnDrop(
        itemid: flag::ITEMFLAGS,
        roomid: u32,
        pos: *mut math::Vec3f,
        rot: *mut math::Vec3s,
    );
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Ammo pots
#[no_mangle]
pub extern "C" fn drop_arrows_bombs_seeds(
    param2_s0x18: u8,
    roomid: u32,
    pos: *mut math::Vec3f,
    param4: u32,
    param5: *mut c_void,
) {
    unsafe {
        // 0xFE is the custom id being used to drop arrows, bombs, and seeds.
        // Should set the eq flag for comparison after this addtion.
        if param2_s0x18 == 0xFE {
            if flag::check_itemflag(flag::ITEMFLAGS::BOW) != 0 {
                spawnDrop(
                    flag::ITEMFLAGS::BUNDLE_OF_ARROWS,
                    roomid,
                    pos,
                    &mut math::Vec3s::default() as *mut math::Vec3s,
                );
            }

            if flag::check_itemflag(flag::ITEMFLAGS::BOMB_BAG) != 0 {
                spawnDrop(
                    flag::ITEMFLAGS::TEN_BOMBS,
                    roomid,
                    pos,
                    &mut math::Vec3s::default() as *mut math::Vec3s,
                );
            }

            if flag::check_itemflag(flag::ITEMFLAGS::SLINGSHOT) != 0 {
                spawnDrop(
                    flag::ITEMFLAGS::FIVE_DEKU_SEEDS, // 10 doesn't work for some reason
                    roomid,
                    pos,
                    &mut math::Vec3s::default() as *mut math::Vec3s,
                );
            }
        }

        // Replaced instructions
        asm!(
            "mov w25, #0x660d",
            "movk w25, #0x19, LSL #16",
            "mul x10, x9, x25",
            "mov w3, {0:w}",
            in(reg) param4,
        );
    }
}

#[no_mangle]
pub extern "C" fn drop_nothing(param2_s0x18: u8) {
    unsafe {
        // if should drop seeds, arrows, or bombs
        if param2_s0x18 == 0xB || param2_s0x18 == 0xC || param2_s0x18 == 0xD {
            asm!("mov w0, #0x0"); // 0x0 -> nothing, 0xFF -> green rupee
        }

        // Replaced instructions
        asm!(
            "mov w25, #0x660d",
            "movk w25, #0x19, LSL #16",
            "mul x10, x9, x25",
        );
    }
}
