#![no_std]
#![feature(ptr_from_ref)]
#![feature(split_array)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]
#![deny(clippy::no_mangle_with_rust_abi)]
#![deny(improper_ctypes)]
#![deny(improper_ctypes_definitions)]

use core::arch::asm;
use core::ffi::{c_char, c_void};
use core::str;
use static_assertions::assert_eq_size;

mod actor;
mod ammo;
mod color;
mod debug;
mod entrance;
mod event;
mod fix;
mod flag;
mod input;
mod item;
mod lyt;
mod mainloop;
mod math;
mod mem;
mod minigame;
mod player;
mod rng;
mod savefile;
mod settings;
mod shop;
mod snd;
mod traps;

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
    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
