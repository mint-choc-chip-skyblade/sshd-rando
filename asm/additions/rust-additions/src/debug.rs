// This is a special file for allowing debug prints
// to yuzu's console.

// Will output a string to Yuzu's log.
//
// In Yuzu go to Emulation > Configure > Debug and
// enter this into the global log filter:
// *:Error Debug.Emulated:Trace
//
// Also be sure to check the "Show Log in Console" Option
// to see the output statements in real time.

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
    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn debug_print(string: *const c_char) {
    // e.g. debug_print(cstr!("Test string").as_ptr());

    unsafe {
        let buffer: [c_char; 128] = [0; 128];
        debugPrint_128(buffer.as_ptr(), string);
    }
}

#[no_mangle]
pub fn debug_print_str(string: *const c_char, string_arg: *const c_char) {
    // e.g. debug_print_str(cstr!("custom model name: %s").as_ptr(),
    // cstr!("DesertRobot").as_ptr());

    unsafe {
        let buffer: [c_char; 128] = [0; 128];
        debugPrint_128(buffer.as_ptr(), string, string_arg);
    }
}

#[no_mangle]
pub fn debug_print_num(string: *const c_char, number: usize) {
    // e.g. debug_print_num(cstr!("param1: %d").as_ptr(), param1 as usize);

    unsafe {
        let buffer: [c_char; 128] = [0; 128];
        debugPrint_128(buffer.as_ptr(), string, number);
    }
}
