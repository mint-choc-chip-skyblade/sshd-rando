#![no_std]
#![feature(split_array)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use core::arch::asm;
use core::ffi::c_void;
use core::str;
use static_assertions::assert_eq_size;

mod actor;
mod ammo;
mod event;
mod flag;
mod lyt;
mod math;
mod player;
mod savefile;
mod traps;
mod yuzu;

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
    static HARP_RELATED: *mut event::HarpRelated;
    static STAGE_MGR: *mut actor::dStageMgr;
    static EVENT_MGR: *mut event::EventMgr;

    static STORYFLAG_MGR: *mut flag::FlagMgr;
    static ITEMFLAG_MGR: *mut flag::FlagMgr;
    static SCENEFLAG_MGR: *mut flag::SceneflagMgr;
    static DUNGEONFLAG_MGR: *mut flag::DungeonflagMgr;

    static LYT_MSG_WINDOW: *mut lyt::dLytMsgWindow;

    static mut STATIC_STORYFLAGS: [u16; 128];
    static mut STATIC_SCENEFLAGS: [u16; 8];
    static mut STATIC_TEMPFLAGS: [u16; 4];
    static mut STATIC_ZONEFLAGS: [[u16; 4]; 63];
    static mut STATIC_ITEMFLAGS: [u16; 64];
    static mut STATIC_DUNGEONFLAGS: [u16; 8];

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
    static mut ACTOR_PARAM_ROT: *mut math::Vec3s;
    static mut ACTORBASE_PARAM2: u32;

    static mut BASEBASE_ACTOR_PARAM1: u32;
    static mut BASEBASE_GROUP_TYPE: u8;

    static ACTOR_ALLOCATOR_DEFINITIONS: u64; // [*const u64; 701];
    static CURRENT_ACTOR_EVENT_FLOW_MGR: *mut event::ActorEventFlowMgr;

    // Custom symbols
    static WARP_TO_START_INFO: WarpToStartInfo;
    static mut TRAP_ID: u8;
    static mut TRAP_DURATION: u16;

    // Functions
    fn strlen(string: *mut u8) -> u64;
    fn strncmp(dest: *mut u8, src: *mut u8, size: u64) -> u64;
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
    fn dAcOlightLine__inUpdate(light_pillar_actor: *mut actor::dAcOlightLine, unk: u64);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Entrance stuff

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
            // yuzu_print("Should be night");

            if next_stage_is_valid_at_night() {
                // yuzu_print("Next stage is valid at night: NEXT_NIGHT = 1");
                NEXT_NIGHT = 1;
            } else {
                // yuzu_print("Next stage is NOT valid at night: NEXT_NIGHT = 0");
                NEXT_NIGHT = 0;
            }
        } else {
            // yuzu_print("Should not be night");
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
            // Skyloft Silent Realm
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

// Custom Event Flow stuff
#[no_mangle]
pub fn custom_event_commands(
    actor_event_flow_mgr: *mut event::ActorEventFlowMgr,
    p_event_flow_element: *const event::EventFlowElement,
) {
    let event_flow_element = unsafe { &*p_event_flow_element };
    match event_flow_element.param3 {
        // Fi Warp
        70 => warp_to_start(),
        // Get trap type
        71 => unsafe {
            if TRAP_ID != u8::MAX {
                (*actor_event_flow_mgr).result_from_previous_check = 1;
            } else {
                (*actor_event_flow_mgr).result_from_previous_check = 0;
            }
        },
        72 => traps::update_traps(),
        _ => (),
    }

    unsafe {
        // Replaced instructions
        asm!("mov w21, #1", "cmp w8, #0x3f",);
    }
}

// Fixes
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

#[no_mangle]
pub fn fix_sandship_boat() -> u32 {
    unsafe {
        let current_stage_name = unsafe { &CURRENT_STAGE_NAME[..4] };

        if strlen(CURRENT_STAGE_NAME.as_mut_ptr()) == 4 && current_stage_name == b"F301" {
            // 152 == Skipper's Boat Timeshift Stone Hit
            return ((*(*STORYFLAG_MGR).funcs).get_flag_or_counter)(STORYFLAG_MGR, 152);
        }

        return 1u32;
    }
}

#[no_mangle]
pub fn fix_item_get_under_water() {
    unsafe {
        let mut item_animation_index: u8;

        asm!(
            "mov w8, w9", // put animation index back into w8
            "mov w25, #0x4", // default to not allowing immediate item gets
            "mov {0:w}, w9",
            out(reg) item_animation_index,
        );

        // Handle bounds check that was replaced
        if item_animation_index > 3 {
            asm!(
                "mov x20, xzr",
                "mov w8, #0x4", // used later to set event name to null
            );
            return;
        }

        // If in water, allow immediate item gets
        if ((*PLAYER_PTR).action_flags >> 18) & 0x1 == 1 {
            // yuzu_print_number((*PLAYER_PTR).action_flags, 16);
            asm!("mov w25, #0"); // allow collecting items under water

            // If should be a big item get animation, make it a small one
            // Big item gets don't work properly under water :(
            if item_animation_index == 1 {
                asm!("mov w8, #0");
            }
        }
    }
}

#[no_mangle]
pub fn activation_checks_for_goddess_walls() -> bool {
    unsafe {
        // Replaced code
        if (*HARP_RELATED).some_check_for_continuous_strumming == 0
            || (*HARP_RELATED).some_other_harp_thing != 0
        {
            // Additional check for BotG
            if flag::check_itemflag(flag::ITEMFLAGS::BALLAD_OF_THE_GODDESS) == 1 {
                return true;
            }
        }

        return false;
    }
}

#[no_mangle]
pub fn remove_timeshift_stone_cutscenes() {
    let mut param1: u32;

    unsafe {
        asm!(
            "ldr {0:w}, [x19, #0xc]",
            out(reg) param1,
        );

        let is_sandship_stone = param1 >> 10 & 0xFF == 1;

        // set value for playFirstTimeCutscene
        asm!(
            "strb {0:w}, [x23, #0xba]",
            in(reg) is_sandship_stone as u8,
        );
    }
}

#[no_mangle]
pub fn fix_light_pillars(light_pillar_actor: *mut actor::dAcOlightLine) {
    unsafe {
        let param1 = (*light_pillar_actor).base.basebase.members.param1;
        let storyflag = ((param1 >> 8) & 0xFF) as u16;

        if (flag::check_storyflag(storyflag) == 1) {
            (*light_pillar_actor).light_shaft_activated = true;
        }

        dAcOlightLine__inUpdate(light_pillar_actor, 1);
    }
}

#[no_mangle]
pub fn update_crystal_count(item: u32) {
    unsafe {
        let mut count: u32 = flag::check_itemflag(flag::ITEMFLAGS::CRYSTAL_PACK_COUNTER);

        // Increase counter depending on which item we got.
        // The counter hasn't increased with the value of the item yet
        // so we have to add it manually here
        match item {
            0x23 => count += 5, // Crystal Pack
            0x30 => count += 1, // Single Crystal
            _ => count += 0,
        }

        // Update numeric arg 1 with the proper count
        if (item == 0x23 || item == 0x30) {
            (*(*LYT_MSG_WINDOW).text_mgr).numeric_args[1] = count;
        }

        asm!("and w8, w0, #0xffff", "cmp w8, #0x1c");
    }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
