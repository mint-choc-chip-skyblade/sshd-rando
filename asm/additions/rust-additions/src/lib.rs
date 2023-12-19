#![no_std]
#![feature(ptr_from_ref)]
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
mod entrance;
mod event;
mod fix;
mod flag;
mod item;
mod lyt;
mod math;
mod player;
mod savefile;
mod traps;
mod yuzu;

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
    static PLAYER_PTR: *mut player::dPlayer;

    static FILE_MGR: *mut savefile::FileMgr;
    static HARP_RELATED: *mut event::HarpRelated;
    static STAGE_MGR: *mut actor::dStageMgr;
    static EVENT_MGR: *mut event::EventMgr;
    static CURRENT_ACTOR_EVENT_FLOW_MGR: *mut event::ActorEventFlowMgr;

    static STORYFLAG_MGR: *mut flag::FlagMgr;
    static ITEMFLAG_MGR: *mut flag::FlagMgr;
    static SCENEFLAG_MGR: *mut flag::SceneflagMgr;
    static DUNGEONFLAG_MGR: *mut flag::DungeonflagMgr;

    static mut STATIC_STORYFLAGS: [u16; 128];
    static mut STATIC_SCENEFLAGS: [u16; 8];
    static mut STATIC_TEMPFLAGS: [u16; 4];
    static mut STATIC_ZONEFLAGS: [[u16; 4]; 63];
    static mut STATIC_ITEMFLAGS: [u16; 64];
    static mut STATIC_DUNGEONFLAGS: [u16; 8];

    static mut ACTOR_PARAM_SCALE: u64;
    static mut ACTOR_PARAM_ROT: *mut math::Vec3s;
    static mut ACTORBASE_PARAM2: u32;
    static mut ACTORBASE_SUBTYPE: u8;

    static mut ACTOR_STAGE_OBJECT_FLAG: u16;
    static mut ACTOR_VIEW_CLIP_INDEX: u8;
    static mut ACTOR_OBJECT_INFO_PTR: u64;

    static mut BASEBASE_ACTOR_PARAM1: u32;
    static mut BASEBASE_GROUP_TYPE: u8;

    // Custom symbols
    static mut TRAP_ID: u8;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Custom Event Flow stuff
#[no_mangle]
pub fn custom_event_commands(
    actor_event_flow_mgr: *mut event::ActorEventFlowMgr,
    p_event_flow_element: *const event::EventFlowElement,
) {
    let event_flow_element = unsafe { &*p_event_flow_element };
    match event_flow_element.param3 {
        // Fi Warp
        70 => entrance::warp_to_start(),
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

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
