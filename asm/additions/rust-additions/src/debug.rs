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
use core::ffi::{c_char, c_double, c_void};
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
    static mut DEBUG_PRINTABLE_STRING: [c_char; 64];
    static mut DEBUG_PRINTABLE_STRING_ARG: [c_char; 64];
    static mut DEBUG_BUFFER: [c_char; 64];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn strlen_const(string: *const c_char) -> u64;
    fn strcat(dest: *const c_char, src: *const c_char) -> *const c_char;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
extern "C" fn __fill_debug_string(string: *const c_char, character: c_char) {
    let string_as_array = string as *mut [c_char; 64];
    let mut char_counter = 0;

    unsafe {
        for c in *string_as_array {
            (*string_as_array)[char_counter] = character;
            char_counter += 1;
        }
    }
}

#[no_mangle]
extern "C" fn __setup_debug_strings(debug_string: *const c_char, string_arg: *const c_char) {
    unsafe {
        __fill_debug_string(DEBUG_PRINTABLE_STRING.as_ptr(), 0);
        __fill_debug_string(DEBUG_PRINTABLE_STRING_ARG.as_ptr(), 0);
        __fill_debug_string(DEBUG_BUFFER.as_ptr(), 0);

        // Starts string with "> "
        DEBUG_PRINTABLE_STRING[0] = 62;
        DEBUG_PRINTABLE_STRING[1] = 32;

        strcat(DEBUG_PRINTABLE_STRING.as_ptr(), debug_string);
        let len_debug_string = strlen_const(DEBUG_PRINTABLE_STRING.as_ptr()) as usize;

        if !string_arg.is_null() && len_debug_string < 63 {
            strcat(DEBUG_PRINTABLE_STRING_ARG.as_ptr(), string_arg);
            let len_string_arg = strlen_const(DEBUG_PRINTABLE_STRING_ARG.as_ptr()) as usize;
            __fill_debug_string(DEBUG_PRINTABLE_STRING_ARG[len_string_arg..].as_ptr(), 0);

            if len_debug_string + len_string_arg > 63 {
                let num_overflow_chars = (len_debug_string + len_string_arg) - 63;
                __fill_debug_string(
                    DEBUG_PRINTABLE_STRING_ARG[len_string_arg - num_overflow_chars..].as_ptr(),
                    0,
                );
            }

            DEBUG_PRINTABLE_STRING[len_debug_string + 1] = 0;
            return;
        }

        __fill_debug_string(DEBUG_PRINTABLE_STRING[len_debug_string..].as_ptr(), 32);
        DEBUG_PRINTABLE_STRING[63] = 0;
    }
}

#[no_mangle]
pub extern "C" fn debug_print(debug_string: *const c_char) {
    // e.g. debug::debug_print(c"Test string".as_ptr());

    unsafe {
        __setup_debug_strings(debug_string, core::ptr::null_mut());
        debugPrint_128(DEBUG_BUFFER.as_ptr(), DEBUG_PRINTABLE_STRING.as_ptr());
    }
}

#[no_mangle]
pub extern "C" fn debug_print_str(debug_string: *const c_char, string_arg: *const c_char) {
    // e.g. debug::debug_print_str(c"custom model name: %s".as_ptr(),
    // c"DesertRobot".as_ptr());

    unsafe {
        __setup_debug_strings(debug_string, string_arg);
        debugPrint_128(
            DEBUG_BUFFER.as_ptr(),
            DEBUG_PRINTABLE_STRING.as_ptr(),
            DEBUG_PRINTABLE_STRING_ARG.as_ptr(),
        );
    }
}
#[no_mangle]
pub extern "C" fn debug_print_num(debug_string: *const c_char, number: usize) {
    // e.g. debug::debug_print_num(c"param1: %d".as_ptr(), param1 as usize);

    unsafe {
        __setup_debug_strings(debug_string, core::ptr::null_mut());
        debugPrint_128(
            DEBUG_BUFFER.as_ptr(),
            DEBUG_PRINTABLE_STRING.as_ptr(),
            number,
        );
    }
}

#[no_mangle]
pub extern "C" fn debug_print_float(debug_string: *const c_char, float: f32) {
    // e.g. debug::debug_print_float(c"param1: %f".as_ptr(), param1 as f32);

    unsafe {
        __setup_debug_strings(debug_string, core::ptr::null_mut());
        debugPrint_128(
            DEBUG_BUFFER.as_ptr(),
            DEBUG_PRINTABLE_STRING.as_ptr(),
            float as c_double,
        );
    }
}
