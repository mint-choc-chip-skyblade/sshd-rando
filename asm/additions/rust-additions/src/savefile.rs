#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::math;

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

// FileMgr/SaveFile stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FileMgr {
    pub all_save_files: u64,
    pub save_tails:     u64,
    pub FA:             SaveFile,
    pub FB:             SaveFile,
    pub _0:             [u8; 36],
    pub amiibo_pos:     math::Vec3f,
    pub amiibo_stage:   u64,
    pub _1:             [u8; 8740],
    pub game_options:   u8,
    pub _2:             [u8; 793],
    pub prevent_commit: bool,
    pub _3:             u8,
}
assert_eq_size!([u8; 52488], FileMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SaveFile {
    pub save_time:                 u64, // size is a guess
    pub unk:                       u64,
    pub _0:                        [u8; 1968],
    pub pouch_items:               [i32; 8],
    pub item_check_items:          [i32; 60],
    pub padding_maybe:             u32,
    pub player_name:               [u16; 8],
    pub storyflags:                [u16; 128],
    pub itemflags:                 [u16; 64],
    pub dungeonflags:              [[u16; 8]; 26],
    pub _1:                        [u8; 3680],
    pub sceneflags:                [[u16; 8]; 26],
    pub _2:                        [u8; 4960],
    pub enemy_kill_counters:       [u16; 100],
    pub hit_by_enemy_counters:     [u16; 100],
    pub tempflags:                 [u16; 4],
    pub zoneflags:                 [[u16; 4]; 63],
    pub stage_object_flags:        [u16; 4096],
    pub _3:                        [u8; 14],
    pub health_capacity:           u16,
    pub some_health_related_thing: u16,
    pub current_health:            u16,
    pub _4:                        [u8; 148],
    pub skykeep_room_layout:       [u8; 9],
    pub unk21413:                  u8,
    pub unk21414:                  u8,
    pub current_layer:             u8,
    pub unk21416:                  u8,
    pub unk21417:                  u8,
    pub unk21418:                  u8,
    pub current_entrance:          u8,
    pub unk21420:                  u8,
    pub is_new_file:               bool,
    pub selected_b_wheel_slot:     u8,
    pub unk21423:                  u8,
    pub selected_pouch_slot:       u8,
    pub selected_dowsing_slot:     u8,
    pub unk21426:                  u8,
    pub unk21427:                  u8,
    pub current_night:             u8,
    pub is_auto_save:              u8,
    pub unkfiller5:                [u8; 10],
}
assert_eq_size!([u8; 21440], SaveFile);

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
