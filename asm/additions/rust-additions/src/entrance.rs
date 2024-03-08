#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
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

// Fi warp stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct WarpToStartInfo {
    pub stage_name: [u8; 8],
    pub room:       u8,
    pub layer:      u8,
    pub entrance:   u8,
    pub night:      u8,
}
assert_eq_size!([u8; 12], WarpToStartInfo);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static STAGE_MGR: *mut actor::dStageMgr;

    static mut GAME_RELOADER_PTR: *mut actor::GameReloader;

    static mut RESPAWN_TYPE: u8;
    static mut CURRENT_STAGE_NAME: [u8; 8];
    static mut CURRENT_STAGE_SUFFIX: [u8; 4];
    static mut CURRENT_FADE_FRAMES: u16;
    static mut CURRENT_ROOM: u8;
    static mut CURRENT_LAYER: u8;
    static mut CURRENT_ENTRANCE: u8;
    static mut CURRENT_NIGHT: u8;
    static mut CURRENT_SOMETHING: u8;
    static mut NEXT_STAGE_NAME: [u8; 8];
    static mut NEXT_STAGE_SUFFIX: [u8; 4];
    static mut NEXT_TRANSITION_FADE_FRAMES: u16;
    static mut NEXT_ROOM: u8;
    static mut NEXT_LAYER: u8;
    static mut NEXT_ENTRANCE: u8;
    static mut NEXT_NIGHT: u8;
    static mut NEXT_TRIAL: u8;
    static mut NEXT_UNK: u8;
    static mut CURRENT_LAYER_COPY: u8;

    static mut ACTOR_PARAM_SCALE: u64;

    // Custom
    static WARP_TO_START_INFO: WarpToStartInfo;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn GameReloader__triggerExit(
        game_reloader: *mut actor::GameReloader,
        current_room: u32,
        exit_index: u32,
        force_night: u32,
        force_trial: u32,
    );
    fn GameReloader__triggerEntrance(
        game_reloader: *mut actor::GameReloader,
        stage_name: *mut [u8; 7],
        room: u32,
        layer: u32,
        entrance: u32,
        forced_night: u32,
        forced_trial: u32,
        transition_type: u32,
        transition_fade_frames: u16,
        unk10: u32,
        unk11: u32,
    );
    fn GameReloader__actuallyTriggerEntrance(
        stage_mgr: *mut actor::dStageMgr,
        room: u8,
        layer: u8,
        entrance: u8,
        forced_night: u32,
        forced_trial: u32,
        transition_type: u32,
        transition_fade_frames: u16,
        param_9: u8,
    );
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
// When checking/setting stage info in this function be sure to use
// all of the NEXT_* variables as this function gets called right after
// those have been assigned.
#[no_mangle]
pub fn handle_er_cases() {
    unsafe {
        // Enforce a max speed after reloading
        // Prevents you running off high ledges from non-vanilla exits
        if (*GAME_RELOADER_PTR).speed_after_reload > 30f32 {
            (*GAME_RELOADER_PTR).speed_after_reload = 30f32;
        }

        // If we're spawning from Sky Keep, but Sky Keep hasn't appeared yet,
        // instead spawn near the statue
        if &NEXT_STAGE_NAME[..5] == b"F000\0"
            && NEXT_ENTRANCE == 53
            && flag::check_storyflag(22) == 0
        {
            NEXT_ENTRANCE = 52
        }

        // // If we're spawning from LMF and it hasn't been raised,
        // // instead spawn in front of where the dungeon entrance would be
        if &NEXT_STAGE_NAME[..5] == b"F300\0" && NEXT_ENTRANCE == 5 && flag::check_storyflag(8) == 0
        {
            NEXT_ENTRANCE = 19;
        }

        // If we're spawning in Lanayru Desert/Mines through the minecart entrance,
        // make sure that a timeshift stone that makes the minecart move is active
        if ((&NEXT_STAGE_NAME[..5] == b"F300\0" && NEXT_ENTRANCE == 2)
            || (&NEXT_STAGE_NAME[..7] == b"F300_1\0" && NEXT_ENTRANCE == 1))
            && (flag::check_global_sceneflag(7, 113) == 0
                && flag::check_global_sceneflag(7, 114) == 0)
        {
            // Unset all other timeshift stones in the scene
            for flag in (115..=124).chain([108, 111]) {
                flag::unset_global_sceneflag(7, flag);
            }
            // Set the last timeshift stone in mines
            flag::set_global_sceneflag(7, 113);
        }

        // If we're about to enter a stage that should have the silent realm effect
        // set it. Otherwise unset it
        if NEXT_STAGE_NAME[0] == b'S' || &NEXT_STAGE_NAME[..7] == b"D003_8\0" {
            NEXT_TRIAL = 1;
        } else {
            NEXT_TRIAL = 0;
        }

        // Force NEXT_NIGHT to day (storyflag keeps the night state stored)
        // If it should be night time, check if the entrance is valid at night
        // check_storyflag(899) can only be true if natural_night_connections is off
        if (flag::check_storyflag(899) != 0 || NEXT_NIGHT == 1) {
            // debug::debug_print("Should be night");

            if next_stage_is_valid_at_night() {
                // debug::debug_print("Next stage is valid at night: NEXT_NIGHT = 1");
                NEXT_NIGHT = 1;
            } else {
                // debug::debug_print("Next stage is NOT valid at night: NEXT_NIGHT = 0");
                NEXT_NIGHT = 0;
            }
        } else {
            // debug::debug_print("Should not be night");
            NEXT_NIGHT = 0;
        }

        // Replaced code sets these
        (*GAME_RELOADER_PTR).item_to_use_after_reload = 0xFF;
        (*GAME_RELOADER_PTR).beedle_shop_spawn_state = 0;
        (*GAME_RELOADER_PTR).action_index = 0xFF;
        (*GAME_RELOADER_PTR).area_type = 0xFF;
    }
}

#[no_mangle]
pub fn next_stage_is_valid_at_night() -> bool {
    unsafe {
        if (&NEXT_STAGE_NAME[..2] == b"F0" &&      // Non-surface stage
            &NEXT_STAGE_NAME[..6] != b"F004r\0" && // Not Bazaar
            &NEXT_STAGE_NAME[..6] != b"F010r\0" && // Not Isle of Songs
            &NEXT_STAGE_NAME[..6] != b"F019r\0" && // Not Bamboo Island
            &NEXT_STAGE_NAME[..3] != b"F02"   ||   // Not Sky/Thunderhead
            (
                &NEXT_STAGE_NAME[..5] == b"F020\0" && // Sky stage
                (
                    NEXT_ENTRANCE == 0  || // Beedle's Island
                    NEXT_ENTRANCE == 22 || // Lumpy West Door
                    NEXT_ENTRANCE == 23 || // Lumpy East Door
                    NEXT_ENTRANCE == 24    // Lumpy Back Door
                )
            ) ||
            // Waterfall Cave
            &NEXT_STAGE_NAME[..5] == b"D000\0" ||
            // The Goddess's Silent Realm
            &NEXT_STAGE_NAME[..5] == b"S000\0")
        {
            return true;
        }
    }

    return false;
}

// When checking stage info in this function be sure to use
// all of the CURRENT_* variables
#[no_mangle]
pub fn handle_er_action_states() {
    unsafe {
        // If we're spawning in the mogma turf dive entrance,
        // set Link to always be diving regardless of how he
        // previously entered
        if &CURRENT_STAGE_NAME[..5] == b"F210\0" && CURRENT_ENTRANCE == 0 {
            (*GAME_RELOADER_PTR).action_index = 0x13;
        }

        // Replaced code sets this
        ACTOR_PARAM_SCALE = 0;
    }
}

#[no_mangle]
pub fn warp_to_start() {
    unsafe {
        let start_info = &*(&WARP_TO_START_INFO as *const WarpToStartInfo);

        GameReloader__actuallyTriggerEntrance(
            STAGE_MGR,
            (*start_info).room.into(),
            (*start_info).layer.into(),
            (*start_info).entrance.into(),
            (*start_info).night.into(),
            0,
            0,
            0xF,
            0xFF,
        );

        (*STAGE_MGR).set_in_actually_trigger_entrance = 0;

        NEXT_STAGE_NAME = (*start_info).stage_name; // *b"F001r\0\0\0";

        if (*GAME_RELOADER_PTR).reload_trigger == 0x2BF {
            (*GAME_RELOADER_PTR).reload_trigger = 5;
        }

        // Just to be extra safe (fixes some issues with Fi warp)
        handle_er_cases();
    }
}

#[no_mangle]
pub fn fix_sky_keep_exit(
    game_reloader: *mut actor::GameReloader,
    stage_name: *mut [u8; 7],
    room: u32,
    layer: u32,
    entrance: u32,
    forced_night: u32,
    forced_trial: u32,
    transition_type: u32,
    mut transition_fade_frames: u16,
    unk10: u32,
    mut unk11: u32,
) {
    unsafe {
        if &(*stage_name)[..5] == b"F000\0" {
            // Use bzs exit when leaving the dungeon (makes ER work properly)
            GameReloader__triggerExit(game_reloader, 0, 1, 2, 2);
        } else {
            // Replaced instructions
            transition_fade_frames = 0xF;
            unk11 = 0xFF;
            GameReloader__triggerEntrance(
                game_reloader,
                stage_name,
                room,
                layer,
                entrance,
                forced_night,
                forced_trial,
                transition_type,
                transition_fade_frames,
                unk10,
                unk11,
            );
        }
    }
}
