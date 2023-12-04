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
use core::ffi::c_void;
use numtoa::NumToA;
use static_assertions::assert_eq_size;

#[no_mangle]
pub fn yuzu_print(string: &str) {
    output_debug_string(string.as_ptr(), string.len());
}

#[no_mangle]
pub fn yuzu_print_number(num: usize, base: usize) {
    let mut buffer = [0u8; 20]; // I doubt we'll be printing numbers greater than 1 quintillion
    yuzu_print(num.numtoa_str(base.into(), &mut buffer));
}

#[no_mangle]
pub fn output_debug_string(string: *const u8, length: usize) {
    unsafe {
        asm!("stp x0, x1, [sp, #-0x10]!");
        asm!("mov x0, {0}", in(reg) string);
        asm!("mov x1, {0}", in(reg) length);
        asm!("svc #39");
        asm!("ldp x0, x1, [sp], #0x10");
    }
}
