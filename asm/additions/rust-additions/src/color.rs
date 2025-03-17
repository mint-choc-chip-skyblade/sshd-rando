#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::lyt;

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
    static LYT_PAUSE_DISP: *mut lyt::dLytPauseDisp;
    static mut COLOR_CHANGE_DELAY: u8;
    static SKY_CLOUD_COLORS: u32;

    static mut CURRENT_SKY_COLOR: u32;
    static mut DAYTIME_SKY_COLOR: u32;
    static mut NIGHTTIME_SKY_COLOR: u32;
    static mut DEMISE_SKY_COLOR: u32;
    static mut TITLESCREEN_SKY_COLOR: u32;
    static mut HYLIA_SKY_COLOR: u32;
    static mut THUNDERHEAD_SKY_COLOR: u32;
    static mut FILESELECT_SKY_COLOR: u32;

    static mut CURRENT_CLOUD_COLOR: u32;
    static mut DAYTIME_CLOUD_COLOR: u32;
    static mut NIGHTTIME_CLOUD_COLOR: u32;
    static mut DEMISE_CLOUD_COLOR: u32;
    static mut TITLESCREEN_CLOUD_COLOR: u32;
    static mut HYLIA_CLOUD_COLOR: u32;
    static mut THUNDERHEAD_CLOUD_COLOR: u32;
    static mut FILESELECT_CLOUD_COLOR: u32;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn memcpy(dest: *mut c_void, src: *mut c_void, size: u32);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn init_rainbow_colors(memcpy_dest: *mut c_void, memcpy_src: *mut c_void) {
    unsafe {
        // Replaced instructions
        memcpy(memcpy_dest, memcpy_src, 0x28A0);

        // if daytime_sky_color == rainbow
        if SKY_CLOUD_COLORS & 0xFF == 11 {
            DAYTIME_SKY_COLOR = 0xFF7373FF;
            TITLESCREEN_SKY_COLOR = 0xFF7373FF;
            THUNDERHEAD_SKY_COLOR = 0xFF7373FF;
            FILESELECT_SKY_COLOR = 0xFF7373FF;
        }
        // if nighttime_sky_color == rainbow
        if (SKY_CLOUD_COLORS >> 8) & 0xFF == 11 {
            NIGHTTIME_SKY_COLOR = 0xFF7373FF;
            DEMISE_SKY_COLOR = 0xFF7373FF;
            HYLIA_SKY_COLOR = 0xFF7373FF;
        }
        // if daytime_cloud_color == rainbow
        if (SKY_CLOUD_COLORS >> 16) & 0xFF == 11 {
            DAYTIME_CLOUD_COLOR = 0xFF73FF73;
            TITLESCREEN_CLOUD_COLOR = 0xFF73FF73;
            THUNDERHEAD_CLOUD_COLOR = 0xFF73FF73;
            FILESELECT_CLOUD_COLOR = 0xFF73FF73;
        }
        // if nighttime_cloud_color == rainbow
        if (SKY_CLOUD_COLORS >> 24) & 0xFF == 11 {
            NIGHTTIME_CLOUD_COLOR = 0xFF73FF73;
            DEMISE_CLOUD_COLOR = 0xFF73FF73;
            HYLIA_CLOUD_COLOR = 0xFF73FF73;
        }
    }
}

#[no_mangle]
pub fn handle_colors() {
    unsafe {
        // update the color change delay
        if COLOR_CHANGE_DELAY == 0 {
            COLOR_CHANGE_DELAY += 4;
        }
        COLOR_CHANGE_DELAY -= 1;

        let mut color = get_color_from_index(SKY_CLOUD_COLORS & 0xFF, DAYTIME_SKY_COLOR);
        if color != 0 {
            DAYTIME_SKY_COLOR = color;
            TITLESCREEN_SKY_COLOR = DAYTIME_SKY_COLOR;
            THUNDERHEAD_SKY_COLOR = DAYTIME_SKY_COLOR;
            FILESELECT_SKY_COLOR = DAYTIME_SKY_COLOR;
        }
        color = get_color_from_index((SKY_CLOUD_COLORS >> 8) & 0xFF, NIGHTTIME_SKY_COLOR);
        if color != 0 {
            NIGHTTIME_SKY_COLOR = color;
            DEMISE_SKY_COLOR = NIGHTTIME_SKY_COLOR;
            HYLIA_SKY_COLOR = NIGHTTIME_SKY_COLOR;
        }

        color = get_color_from_index((SKY_CLOUD_COLORS >> 16) & 0xFF, DAYTIME_CLOUD_COLOR);
        if color != 0 {
            DAYTIME_CLOUD_COLOR = color;
            TITLESCREEN_CLOUD_COLOR = DAYTIME_CLOUD_COLOR;
            THUNDERHEAD_CLOUD_COLOR = DAYTIME_CLOUD_COLOR;
            FILESELECT_CLOUD_COLOR = DAYTIME_CLOUD_COLOR;
        }
        color = get_color_from_index((SKY_CLOUD_COLORS >> 24) & 0xFF, NIGHTTIME_CLOUD_COLOR);
        if color != 0 {
            NIGHTTIME_CLOUD_COLOR = color;
            DEMISE_CLOUD_COLOR = NIGHTTIME_CLOUD_COLOR;
            HYLIA_CLOUD_COLOR = NIGHTTIME_CLOUD_COLOR;
        }
    }
}

#[no_mangle]
pub fn get_color_from_index(color_index: u32, color: u32) -> u32 {
    match color_index {
        1 => return 0xFFFFCD9C,  // Blue (9C,CD,FF)
        2 => return 0xFFB5F0A3,  // Green (A3,F0,B5)
        3 => return 0xFFB0F9FF,  // Yellow (FF,F9,B0)
        4 => return 0xFFB3D2FF,  // Orange (FF,D2,B3)
        5 => return 0xFFA9A3FE,  // Red (FE,A3,A9)
        6 => return 0xFFFEBBE2,  // Purple (E2,BB,FE)
        7 => return 0xFFECB7FF,  // Pink (FF,B7,EC)
        8 => return 0xFFEEEEEE,  // White (EE,EE,EE)
        9 => return 0xFF201010,  // Black (10,10,20)
        10 => return 0xFF787878, // Grey (78,78,78)
        11 => return rainbow_color_fade(color),
        _ => return 0,
    }
}

#[no_mangle]
pub fn rainbow_color_fade(color: u32) -> u32 {
    unsafe {
        // Yep, this is a stupid way to check if the game is paused ^^'
        if COLOR_CHANGE_DELAY == 0 && LYT_PAUSE_DISP == core::ptr::null_mut() {
            let mut prev_r: u32 = color & 0xFF;
            let mut prev_g: u32 = (color >> 8) & 0xFF;
            let mut prev_b: u32 = (color >> 16) & 0xFF;

            if prev_r > 115 && prev_b == 115 {
                prev_r -= 1;
                prev_g += 1;
            }
            if prev_g > 115 && prev_r == 115 {
                prev_g -= 1;
                prev_b += 1;
            }
            if prev_b > 115 && prev_g == 115 {
                prev_b -= 1;
                prev_r += 1;
            }

            return (0xFF << 24) + (prev_b << 16) + (prev_g << 8) + prev_r;
        }

        return color;
    }
}
