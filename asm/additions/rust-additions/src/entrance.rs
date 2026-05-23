#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::math;
use crate::player;
use crate::savefile;

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
pub struct dTgSceneChange {
    pub base:              actor::dAcBase,
    pub mTriggerMatrix:    math::Matrix,
    pub mScenLink:         u8,
    pub mScenType:         u8,
    pub mPathIndex:        u8,
    pub mEnabledSceneflag: u8,
    pub mEnableStoryflag:  u16,
    pub mDisableStoryflag: u16,
    pub unk1:              u8,
    pub unk2:              u8,
    pub unk3:              u8,
    pub unk4:              u8,
    pub mVec:              math::Vec3f,
}
assert_eq_size!([u8; 0x1D8], dTgSceneChange);

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
    static PLAYER_PTR: *mut player::dPlayer;
    static FILE_MGR: *mut savefile::FileMgr;
    static STORYFLAG_MGR: *mut flag::FlagMgr;
    static STAGE_MGR: *mut actor::dStageMgr;
    static FANFARE_SOUND_MGR: *mut c_void;

    static mut GAME_RELOADER_PTR: *mut actor::GameReloader;

    static mut RESPAWN_TYPE: u8;
    static mut CURRENT_STAGE_NAME: [u8; 8];
    static mut CURRENT_STAGE_SUFFIX: [u8; 4];
    static mut CURRENT_FADE_FRAMES: u16;
    static mut CURRENT_ROOM: u8;
    static mut CURRENT_TRIAL: u8;
    static mut CURRENT_LAYER: u8;
    static mut CURRENT_ENTRANCE: u8;
    static mut CURRENT_NIGHT: u8;
    static mut CURRENT_UNK: u8;
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
    static mut TRAP_ID: u8;

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

    fn playFanfareMaybe(soundMgr: *mut c_void, soundIndex: u16) -> u64;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
// When checking/setting stage info in this function be sure to use
// all of the NEXT_* variables as this function gets called right after
// those have been assigned.
#[no_mangle]
pub extern "C" fn handle_er_cases() {
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
            debug::debug_print(c"Should be night".as_ptr());

            if next_stage_is_valid_at_night() {
                debug::debug_print(c"Next stage is valid at night: NEXT_NIGHT = 1".as_ptr());
                NEXT_NIGHT = 1;
            } else {
                debug::debug_print(c"Next stage is NOT valid at night: NEXT_NIGHT = 0".as_ptr());
                NEXT_NIGHT = 0;
            }
        } else {
            debug::debug_print(c"Should not be night".as_ptr());
            NEXT_NIGHT = 0;
        }

        // Stop trap music. If health is zero, this gets handled
        // already and this would cut off the game over music instead
        if (TRAP_ID == 2 || TRAP_ID == 3) && (*FILE_MGR).FA.current_health != 0 {
            playFanfareMaybe(FANFARE_SOUND_MGR, 0xFFFF);
        }

        // Replaced code sets these
        (*GAME_RELOADER_PTR).item_to_use_after_reload = 0xFF;
        (*GAME_RELOADER_PTR).beedle_shop_spawn_state = 0;
        (*GAME_RELOADER_PTR).action_index = 0xFF;
    }
}

#[no_mangle]
pub extern "C" fn next_stage_is_valid_at_night() -> bool {
    unsafe {
        if (&NEXT_STAGE_NAME[..5] == b"D000\0" || // Waterfall Cave
            &NEXT_STAGE_NAME[..5] == b"S000\0" || // The Goddess's Silent Realm
            (
                &NEXT_STAGE_NAME[..2] == b"F0"      && // Non-surface stage
                &NEXT_STAGE_NAME[..6] != b"F010r\0" && // Not Isle of Songs (works but looks weird)
                &NEXT_STAGE_NAME[..6] != b"F019r\0"    // Not Bamboo Island (Peater disappears?)
                // &NEXT_STAGE_NAME[..6] != b"F004r\0" // Not Bazaar (works but Sparrot isn't there)
            ))
        {
            return true;
        }
    }

    return false;
}

// When checking stage info in this function be sure to use
// all of the CURRENT_* variables
#[no_mangle]
pub extern "C" fn handle_er_action_states() {
    unsafe {
        // Prevent x14 getting clobbered. The vanilla game code does this at
        // 0x7100e10bd8 but that's too late. This is needed to allow this
        // function to call other functions (like flag::check_itemflag).
        asm!("mov x22, x14");

        if &CURRENT_STAGE_NAME[..5] == b"F210\0" && CURRENT_ENTRANCE == 0 {
            // Force the player to be diving when loading into the Mogma Turf skydive
            // entrance. Ensures the player always has access to the skydive chest (and
            // other pillars).
            (*GAME_RELOADER_PTR).action_index = 0x13;

            // By default, the game sets the respawn info at the top of the fall into Mogma
            // Turf. If the player dies due to the fall (either due to low health or OHKO),
            // they then respawn at the top of the fall but not in the diving state. This
            // can cause an infinite death loop if the player doesn't have the sailcloth.
            if flag::check_itemflag(flag::ITEMFLAGS::SAILCLOTH) == 0 {
                (*GAME_RELOADER_PTR).prevent_set_respawn_info = 1;
            }
        }

        // Replaced code sets this
        ACTOR_PARAM_SCALE = 0;
    }
}

#[no_mangle]
pub extern "C" fn warp_to_start() -> bool {
    unsafe {
        // Don't warp if in boss rush
        if flag::check_storyflag(530) != 0 || flag::check_storyflag(531) != 0 {
            return false;
        }

        let start_info = &*(&WARP_TO_START_INFO as *const WarpToStartInfo);

        // Make sure the night storyflag remains in-sync with the actual time of day
        if start_info.night == 0 {
            flag::unset_storyflag(737);
        } else {
            flag::set_storyflag(737);
        }

        GameReloader__actuallyTriggerEntrance(
            STAGE_MGR,
            start_info.room,
            start_info.layer,
            start_info.entrance,
            start_info.night.into(),
            0,
            0,
            0xF,
            0xFF,
        );

        (*STAGE_MGR).set_in_actually_trigger_entrance = 0;

        NEXT_STAGE_NAME = (*start_info).stage_name;
        NEXT_ROOM = (*start_info).room;
        NEXT_LAYER = (*start_info).layer;
        NEXT_ENTRANCE = (*start_info).entrance;
        NEXT_NIGHT = (*start_info).night;

        if (*GAME_RELOADER_PTR).reload_trigger == 0x2BF {
            (*GAME_RELOADER_PTR).reload_trigger = 5;
        }

        // Just to be extra safe (fixes some issues with Fi warp)
        handle_er_cases();
        return true;
    }
}

#[no_mangle]
pub extern "C" fn fix_sky_keep_exit(
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

#[no_mangle]
pub extern "C" fn require_sword_to_enter_trial_gate() -> bool {
    unsafe {
        let scen_link: u8;
        asm!("ldrb {0:w}, [x23, #0x4]", out(reg) scen_link);

        if scen_link == 0xFF || flag::check_itemflag(flag::ITEMFLAGS::PRACTICE_SWORD) == 0 {
            return false;
        }

        return true;
    }
}

#[no_mangle]
pub extern "C" fn require_sword_to_enter_sacred_realm(
    sceneflag_mgr: *mut c_void,
    roomid: u32,
    sceneflag: u32,
) -> bool {
    if flag::check_itemflag(flag::ITEMFLAGS::PRACTICE_SWORD) == 0
        || flag::check_local_sceneflag(sceneflag) != 0
    {
        return false;
    }
    return true;
}

#[no_mangle]
pub extern "C" fn allow_saving_respawn_info_on_new_file_start() {
    unsafe {
        // Storyflag 1201 is the "can use amiibo" flag.
        // This is used as a check for setting the respawn info and forcing an
        // autosave when starting a new game file.
        if flag::check_storyflag(1201) == 0 {
            (*GAME_RELOADER_PTR).prevent_set_respawn_info = 0;
        }

        // Replaced instructions
        CURRENT_STAGE_NAME = *b"\0\0\0\0\0\0\0\0";
        CURRENT_ROOM = 0;
    }
}

#[no_mangle]
pub extern "C" fn allow_autosave_on_new_file_start(param1: u64) -> u64 {
    unsafe {
        let mut w21: u32;
        asm!("mov {0:w}, w21", out(reg) w21);

        // If flag 1201 isn't set, this must be the 1st time loading a new game file.
        // Exclude layer 28 so the game doesn't autosave on the titlescreen.
        if flag::check_storyflag(1201) == 0 && CURRENT_LAYER != 28 {
            flag::set_storyflag(1201);
            // Commit the flag so that the game doesn't autosave when loading an autosave
            // made when starting a new game file.
            ((*(*STORYFLAG_MGR).funcs).do_commit)(STORYFLAG_MGR);
            w21 = 0;
            asm!("mov w8, #1");
        } else if &CURRENT_STAGE_NAME[..5] == b"F210\0"
            && CURRENT_ENTRANCE == 0
            && flag::check_itemflag(flag::ITEMFLAGS::SAILCLOTH) == 0
        {
            asm!("mov w8, #0");
        } else if (*GAME_RELOADER_PTR).is_reloading != 0 {
            // vanilla case
            asm!("mov w8, #1");
        } else {
            asm!("mov w8, #0");
        }

        asm!("mov w21, {0:w}", in(reg) w21);

        return param1;
    }
}

#[no_mangle]
pub extern "C" fn voidout_near_skyloft_or_light_pillars_without_sailcloth(
    player: *mut player::dPlayer,
    scen_link: u8,
    path_index: u8,
    scen_type: u8,
) {
    unsafe {
        // SCEN type 5 == "landing on skyloft"
        // SCEN type 9 == "entering light pillar"
        if (scen_type == 5 || scen_type == 9)
            && flag::check_itemflag(flag::ITEMFLAGS::SAILCLOTH) == 0
        {
            // Triggers a voidout.
            ((*(*PLAYER_PTR).vtable).can_handle_gameover)(PLAYER_PTR, 1, 0, 0);
        } else {
            ((*(*player).vtable).trigger_scen_change)(player, scen_link, path_index, scen_type);
        }
    }
}
