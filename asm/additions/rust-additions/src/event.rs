#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::entrance;
use crate::fix;
use crate::flag;
use crate::lyt;
use crate::minigame;
use crate::traps;

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

// Event
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct EventMgr {
    pub _0:             [u8; 0x10],
    pub event_owner:    [u8; 0x18],
    pub linked_actor:   [u8; 0x18],
    pub _1:             [u8; 8],
    pub actual_event:   Event,
    pub _2:             [u8; 0x160],
    pub event:          Event,
    pub probably_state: u32,
    pub state_flags:    u32,
    pub skipflag:       u16,
    pub _3:             [u8; 14],
}
assert_eq_size!([u8; 0x260], EventMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct Event {
    pub vtable:         u64,
    pub eventid:        u32,
    pub event_flags:    u32,
    pub roomid:         i32,
    pub tool_dataid:    i32,
    pub event_name:     [u8; 32],
    pub event_zev_data: u64,
    pub callbackFn1:    u64,
    pub callbackFn2:    u64,
}
assert_eq_size!([u8; 0x50], Event);

// Harp stuff
// Not sure what this stuff is all about
// Used to keep vanilla checks for isPlayingHarp (see SD for more details)
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct HarpRelated {
    pub unk:                                 [u8; 0x30],
    pub some_check_for_continuous_strumming: u64,
    pub unk1:                                [u8; 0x22],
    pub some_other_harp_thing:               u8,
}

// Event Flow stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorEventFlowMgr {
    pub vtable:                     u64,
    pub msbf_info:                  u64,
    pub current_flow_index:         u32,
    pub _0:                         [u8; 12],
    pub result_from_previous_check: u32,
    pub current_text_label_name:    [u8; 32],
    pub _1:                         [u8; 12],
    pub next_flow_delay_timer:      u32,
    pub another_flow_element:       EventFlowElement,
    pub _2:                         [u8; 12],
}
assert_eq_size!([u8; 0x70], ActorEventFlowMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct EventFlowElement {
    pub typ:     u8,
    pub subtype: u8,
    pub pad:     u16,
    pub param2:  u16, // 6.5 hrs went into finding out that these are reversed ...
    pub param1:  u16,
    pub next:    u16,
    pub param3:  u16,
    pub param4:  u16,
    pub param5:  u16,
}
// Long story, turns out that the game stores param1 and 2 in a single u32
// field. This works fine in SD, however, HD has the reverse endianness. So,
// these two params2 get reversed and that's how I lost over 6 hours of my life
// ;-;
assert_eq_size!([u8; 0x10], EventFlowElement);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    // Custom symbols
    static mut TRAP_ID: u8;

    static STORYFLAG_MGR: *mut flag::FlagMgr;
    static LYT_MSG_WINDOW: *mut lyt::dLytMsgWindow;

    static mut CURRENT_STAGE_NAME: [u8; 8];

    static mut GODDESS_SWORD_RES: [u8; 0xA0000];
    static mut TRUE_MASTER_SWORD_RES: [u8; 0xA0000];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn parseBRRES(res_data: u64);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub extern "C" fn custom_event_commands(
    actor_event_flow_mgr: *mut ActorEventFlowMgr,
    p_event_flow_element: *const EventFlowElement,
) {
    let mut event_flow_element = unsafe { &*p_event_flow_element };
    match event_flow_element.param3 {
        // Fi Warp
        70 => unsafe {
            (*actor_event_flow_mgr).result_from_previous_check = entrance::warp_to_start() as u32
        },
        // Get trap type
        71 => unsafe {
            if TRAP_ID != u8::MAX {
                (*actor_event_flow_mgr).result_from_previous_check = 1;
            } else {
                (*actor_event_flow_mgr).result_from_previous_check = 0;
            }
        },
        72 => traps::update_traps(),
        73 => fix::set_skyloft_thunderhead_sceneflag(),
        74 => flag::increment_tadtone_counter(),
        75 => unsafe {
            let tadtone_groups_left = 17 - flag::check_storyflag(953);

            // Set numeric arg 0 to number of tadtones left. This will display the number
            // of remaining tadtones in the textbox for the item give.
            (*(*LYT_MSG_WINDOW).text_mgr).numeric_args[0] = tadtone_groups_left;

            // Set result from previous check to number of tadtones left. If this is 0, it
            // will show the item give textbox for collecting all the tadtones.
            (*actor_event_flow_mgr).result_from_previous_check = tadtone_groups_left;
        },
        76 => minigame::boss_rush_backup_flags(event_flow_element.param1),
        77 => minigame::boss_rush_restore_flags(),
        _ => (),
    }

    unsafe {
        asm!(
            "mov x0, {0:x}",
            "mov x1, {1:x}",
            // Replaced instructions
            "ldrh w8, [x1, #0xa]",
            "mov w21, #1",
            in(reg) actor_event_flow_mgr,
            in(reg) p_event_flow_element,
        );
    }
}

#[no_mangle]
#[warn(improper_ctypes_definitions)]
pub extern "C" fn check_tadtone_counter_before_song_event(
    tadtone_minigame_actor: *mut actor::dTgClefGame,
) -> (*mut actor::dTgClefGame, u32) {
    let collected_tadtone_groups = flag::check_storyflag(953);
    let vanilla_tadtones_completed_flag = flag::check_storyflag(18);

    // If we've collected all 17 tadtone groups and haven't played the cutscene
    // yet, then play the cutscene
    if collected_tadtone_groups == 17 && vanilla_tadtones_completed_flag == 0 {
        unsafe {
            (*tadtone_minigame_actor).delay_before_starting_event = 0;
        }
        return (tadtone_minigame_actor, 1);
    }

    return (tadtone_minigame_actor, 0);
}

#[no_mangle]
pub extern "C" fn set_boko_base_restricted_sword_flag_before_event(param1: *mut c_void) {
    unsafe {
        if &CURRENT_STAGE_NAME[..7] == b"F201_2\0" {
            flag::set_storyflag(167);
        }
    }

    // Replaced instructions
    unsafe {
        asm!("mov x0, {0:x}", "mov w8, #1", "strb w8, [x0, #0xb5a]", in(reg) param1);
    }
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct unkstruct {
    pub unk0x0:  *mut c_void,
    pub unk0x8:  *mut c_void,
    pub unk0x10: extern "C" fn(*mut c_void, u32, u32),
}

#[no_mangle]
pub extern "C" fn remove_vanilla_tms_sword_pull_textbox(param1: *mut *mut unkstruct) {
    unsafe {
        ((*(*param1)).unk0x10)(param1 as *mut c_void, 0xFF, 3);
    }

    // Sets tboxflag 9 in sceneindex 5 (Boko Base / VS)
    flag::set_global_tboxflag(5, 9);

    // The vanilla textbox eventflow unsets these flags.
    flag::unset_storyflag(167); // Restricted sword
    flag::set_local_sceneflag(44);
}

#[no_mangle]
pub extern "C" fn fix_boko_base_sword_model(
    mut res_data: *mut c_void,
    mut model_name: *const c_char,
    sword_type: u8,
) {
    unsafe {
        if sword_type == 1 {
            res_data = TRUE_MASTER_SWORD_RES.as_ptr() as *mut c_void;
            model_name = c"EquipSwordMaster".as_ptr();
        } else {
            res_data = GODDESS_SWORD_RES.as_ptr() as *mut c_void;
            model_name = c"EquipSwordB".as_ptr();
        }

        asm!("mov x0, {0:x}", in(reg) res_data);
        asm!("mov x1, {0:x}", in(reg) model_name);
    }
}
