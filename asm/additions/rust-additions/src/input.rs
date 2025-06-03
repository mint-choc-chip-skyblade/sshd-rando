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

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct InputMgr {
    pub vtable: *mut InputMgr__vtable,
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct InputMgr__vtable {
    pub _0:                        [u8; 0x20],
    pub check_button_held_down:    extern "C" fn(*mut InputMgr, BUTTON_INPUTS) -> bool,
    pub check_button_held_up:      extern "C" fn(*mut InputMgr, BUTTON_INPUTS) -> bool,
    pub check_button_pressed_down: extern "C" fn(*mut InputMgr, BUTTON_INPUTS) -> bool,
    pub check_button_pressed_up:   extern "C" fn(*mut InputMgr, BUTTON_INPUTS) -> bool,
}

#[repr(u32)]
#[derive(Copy, Clone, Hash, PartialEq, Eq)]
pub enum BUTTON_INPUTS {
    DPAD_LEFT_BUTTON   = 0x1,
    DPAD_RIGHT_BUTTON  = 0x2,
    DPAD_DOWN_BUTTON   = 0x4,
    DPAD_UP_BUTTON     = 0x8,
    PLUS_BUTTON        = 0x10,
    Y_BUTTON           = 0x100,
    X_BUTTON           = 0x200,
    B_BUTTON           = 0x400,
    A_BUTTON           = 0x800,
    MINUS_BUTTON       = 0x1000,
    ZL_BUTTON          = 0x2000,
    L_BUTTON           = 0x4000,
    LEFT_STICK_BUTTON  = 0x10000,
    RIGHT_STICK_BUTTON = 0x20000,
    R_BUTTON           = 0x40000,
    ZR_BUTTON          = 0x80000,
    RIGHT_STICK_UP     = 0x100000,
    RIGHT_STICK_DOWN   = 0x200000,
    RIGHT_STICK_LEFT   = 0x400000,
    RIGHT_STICK_RIGHT  = 0x800000,
    LEFT_STICK_UP      = 0x1000000,
    LEFT_STICK_DOWN    = 0x2000000,
    LEFT_STICK_LEFT    = 0x4000000,
    LEFT_STICK_RIGHT   = 0x8000000,
}

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static INPUT_MGR: *mut InputMgr;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub extern "C" fn check_button_held_down(button: BUTTON_INPUTS) -> bool {
    unsafe {
        return ((*(*INPUT_MGR).vtable).check_button_held_down)(INPUT_MGR, button);
    }
}

#[no_mangle]
pub extern "C" fn check_button_held_up(button: BUTTON_INPUTS) -> bool {
    unsafe {
        return ((*(*INPUT_MGR).vtable).check_button_held_up)(INPUT_MGR, button);
    }
}

#[no_mangle]
pub extern "C" fn check_button_pressed_down(button: BUTTON_INPUTS) -> bool {
    unsafe {
        return ((*(*INPUT_MGR).vtable).check_button_pressed_down)(INPUT_MGR, button);
    }
}

#[no_mangle]
pub extern "C" fn check_button_pressed_up(button: BUTTON_INPUTS) -> bool {
    unsafe {
        return ((*(*INPUT_MGR).vtable).check_button_pressed_up)(INPUT_MGR, button);
    }
}
