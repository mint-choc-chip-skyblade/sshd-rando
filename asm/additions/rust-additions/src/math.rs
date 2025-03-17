#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;

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

#[repr(C)]
#[derive(Copy, Clone, Default)]
pub struct Vec3f {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}
assert_eq_size!([u8; 12], Vec3f);

#[repr(C)]
#[derive(Copy, Clone, Default)]
pub struct Vec3s {
    pub x: u16,
    pub y: u16,
    pub z: u16,
}
assert_eq_size!([u8; 6], Vec3s);

#[repr(C)]
#[derive(Copy, Clone, Default)]
pub struct Matrix {
    pub xx: f32,
    pub xy: f32,
    pub xz: f32,
    pub xw: f32,
    pub yx: f32,
    pub yy: f32,
    pub yz: f32,
    pub yw: f32,
    pub zx: f32,
    pub zy: f32,
    pub zz: f32,
    pub zw: f32,
}
assert_eq_size!([u8; 0x30], Matrix);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

////////////////////////
// ADD FUNCTIONS HERE //
////////////////////////
