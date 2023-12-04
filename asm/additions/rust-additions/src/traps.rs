#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::event;
use crate::flag;
use crate::player;
use crate::savefile;

use core::arch::asm;
use core::ffi::c_void;
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
    static PLAYER_PTR: *mut player::dPlayer;

    static FILE_MGR: *mut savefile::FileMgr;
    static EVENT_MGR: *mut event::EventMgr;
    static FANFARE_SOUND_MGR: *mut c_void;

    // Custom symbols
    static mut TRAP_ID: u8;
    static mut TRAP_DURATION: u16;

    // Functions
    fn playFanfareMaybe(soundMgr: *mut c_void, soundIndex: u16) -> u64;

}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Traps
#[no_mangle]
pub fn setup_traps(item_actor: *mut actor::dAcItem) -> u16 {
    unsafe {
        // Is trap if one of 0x000000C0 is unset
        let trapid = ((*item_actor).base.members.base.param2 & 0xC0) >> 6;

        if trapid != 3 {
            // Set itemid to a rupoor for the frowny face and sound
            (*item_actor).itemid = 34;
            (*item_actor).final_determined_itemid = 34;

            match trapid {
                0 => {
                    TRAP_ID = 0;
                    TRAP_DURATION = 255;
                },
                1 => {
                    TRAP_ID = 1;
                },
                _ => (),
            }
        } else {
            // Just to be sure, reset the trap values
            TRAP_ID = u8::MAX;
            TRAP_DURATION = 0;
        }

        return (*item_actor).final_determined_itemid;
    }
}

#[no_mangle]
pub fn update_traps() {
    unsafe {
        match TRAP_ID {
            0 => {
                (*PLAYER_PTR).burn_timer = 32;
                (*PLAYER_PTR).shock_effect_timer = 32;
                (*PLAYER_PTR).cursed_timer = 32;
                (*PLAYER_PTR).shit_smell_timer = 32;
                (*PLAYER_PTR).sheild_burn_timer = 32;
                TRAP_DURATION = 256;
            },
            1 => {
                (*FILE_MGR).FA.current_health = 1;
                (*PLAYER_PTR).stamina_amount = 0;
                (*PLAYER_PTR).stamina_recovery_timer = 64;
                flag::set_storyflag(565); // z button bipping
                flag::set_storyflag(566); // c button bipping
                flag::set_storyflag(567); // map button bipping
                flag::set_storyflag(568); // pouch button bipping
                flag::set_storyflag(569); // b button bipping
                flag::set_storyflag(570); // interface selection bipping
                flag::set_storyflag(571); // gear button bipping
                flag::set_storyflag(818); // dowsing button bipping
                flag::set_storyflag(832); // help button bipping
                playFanfareMaybe(FANFARE_SOUND_MGR, 0x15C2);
            },
            _ => (),
        }

        TRAP_ID = u8::MAX;
    }
}

#[no_mangle]
pub fn handle_effect_timers() -> u32 {
    unsafe {
        // If in event, clear status effects
        if EVENT_MGR != core::ptr::null_mut() && (*EVENT_MGR).probably_state != 0 {
            // But if the cause is a trap, don't clear them
            if TRAP_DURATION > 0 {
                return 0;
            }

            return 1;
        }

        if TRAP_DURATION > 0 {
            TRAP_DURATION -= 1;

            if (*PLAYER_PTR).burn_timer == 0 {
                (*PLAYER_PTR).burn_timer = 32;
                (*PLAYER_PTR).shock_effect_timer = 32;
                (*PLAYER_PTR).cursed_timer = 32;
                (*PLAYER_PTR).shit_smell_timer = 32;
                (*PLAYER_PTR).sheild_burn_timer = 32;
            }
        }

        return 0;
    }
}
