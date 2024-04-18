#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::event;
use crate::flag;
use crate::item;
use crate::math;
use crate::player;
use crate::savefile;

use core::arch::asm;
use core::ffi::{c_char, c_void};
use core::ptr::{from_ref, read_unaligned};
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

//////////////////////
// ADD STRUCTS HERE //
//////////////////////

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static PLAYER_PTR: *mut player::dPlayer;

    static FILE_MGR: *mut savefile::FileMgr;
    static ROOM_MGR: *mut actor::RoomMgr;
    static EVENT_MGR: *mut event::EventMgr;
    static FANFARE_SOUND_MGR: *mut c_void;

    static ITEMFLAG_MGR: *mut flag::FlagMgr;

    static ACTOR_ALLOCATOR_DEFINITIONS_PTR: *mut c_void;

    static mut ACTORBASE_PARAM2: u32;
    static mut ITEM_GET_BOTTLE_POUCH_SLOT: u32;

    // Custom symbols
    static mut TRAP_ID: u8;
    static mut NEXT_TRAP_ID: u8;
    static mut TRAP_DURATION: u16;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn playFanfareMaybe(soundMgr: *mut c_void, soundIndex: u16) -> u64;
    fn dPlayer__putItemAway(player: *mut player::dPlayer, unk1: u64, unk2: u64) -> i32;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Traps
#[no_mangle]
pub fn setup_traps(item_actor: *mut item::dAcItem) -> u16 {
    unsafe {
        // Is trap if one of 0x000000F0 is unset
        let trapid_bitmask = 0xF;
        let trapid = ((*item_actor).base.members.base.param2 >> 4) & trapid_bitmask;

        let is_trappable_item = ((*item_actor).base.members.base.param2 & 0xF) == 0xF;

        if trapid != trapid_bitmask && is_trappable_item {
            // Set itemid to a rupoor for the frowny face and sound
            (*item_actor).itemid = 34;
            (*item_actor).final_determined_itemid = 34;

            TRAP_ID = trapid as u8;

            if trapid == 0 {
                TRAP_DURATION = 255;
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
            // Burn trap
            0 => {
                (*PLAYER_PTR).burn_timer = 32;
                (*PLAYER_PTR).sheild_burn_timer = 32;
                TRAP_DURATION = 256;
            },
            // Curse trap
            1 => {
                (*PLAYER_PTR).cursed_timer = 512;
                TRAP_DURATION = 512;

                let item_being_used = (*PLAYER_PTR).item_being_used;

                if item_being_used != player::ITEM_BEING_USED::MITTS
                    || item_being_used != player::ITEM_BEING_USED::WATER_DRAGON_SCALE
                {
                    dPlayer__putItemAway(PLAYER_PTR, 0, 1);
                }
            },
            // Noise trap
            2 => {
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
            // Groose trap
            3 => {
                let player_pos = (*PLAYER_PTR).obj_base_members.base.pos;
                let actor_pos: *mut math::Vec3f = &mut math::Vec3f {
                    x: player_pos.x,
                    y: player_pos.y,
                    z: player_pos.z,
                } as *mut math::Vec3f;

                let actor_rot: *mut math::Vec3s = &mut math::Vec3s {
                    x: 0,
                    y: 0,
                    z: 10404, // talk_behaviour
                } as *mut math::Vec3s;

                let actor_scale: *mut math::Vec3f = &mut math::Vec3f {
                    x: 1.0,
                    y: 1.0,
                    z: 1.0,
                } as *mut math::Vec3f;

                actor::spawn_actor(
                    actor::ACTORID::NPC_RVL,
                    (*ROOM_MGR).roomid.into(),
                    0xFFFFFFFF,
                    actor_pos,
                    actor_rot,
                    actor_scale,
                    0xFFFFFFFF,
                );

                playFanfareMaybe(FANFARE_SOUND_MGR, 0x1705); // Groose's theme
            },
            // Health Trap
            4 => {
                (*FILE_MGR).FA.current_health = 1;
                (*PLAYER_PTR).stamina_amount = 0;
                (*PLAYER_PTR).something_we_use_for_stamina = 0x5A; // Make player exhausted?
                (*PLAYER_PTR).stamina_recovery_timer = 64;
            },
            _ => (),
        }

        // Only reset the trapid if the trap has an immediate effect
        if TRAP_DURATION == 0 {
            TRAP_ID = u8::MAX;
        }
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

            if TRAP_ID == 0 {
                if (*PLAYER_PTR).burn_timer == 0 {
                    (*PLAYER_PTR).burn_timer = 32;
                }
                if (*PLAYER_PTR).sheild_burn_timer == 0 {
                    (*PLAYER_PTR).sheild_burn_timer = 32;
                }
            } else if TRAP_ID == 1 {
                (*PLAYER_PTR).cursed_timer = 512;
            }
        } else {
            TRAP_ID = u8::MAX;
        }

        return 0;
    }
}

#[no_mangle]
pub fn npc_traps() {
    unsafe {
        let mut itemid: u16;
        let mut trapid: u8;
        asm!("ldr {0:w}, [x20, #0x4]", out(reg) itemid);

        // 11 cos signed numbers are bleh
        trapid = ((itemid >> 11) & 0xF) as u8;
        itemid &= 0x1FF;

        // NPC trapids are +1 in eventpatches.py to allow trapid != 0 so spawned NPC
        // items don't break
        if trapid != 0 {
            NEXT_TRAP_ID = trapid - 1;
        }

        // Replaced instructions
        asm!("mov w1, #0x9", "mov w2, {0:w}", in(reg) itemid);
    }
}

#[no_mangle]
pub fn fix_tbox_traps() {
    unsafe {
        let tbox_actor: *mut item::dAcTbox;
        asm!("mov {0:x}, x19", out(reg) tbox_actor);

        let trapid = (((*tbox_actor).base.members.base.param2 >> 28) & 0xF) as u8;

        if trapid != 0xF {
            // Force a rupoor model (otherwise, you get a trap with a big item get anim and
            // sound)
            asm!("mov w20, #34"); // set tbox itemid to rupoor
            NEXT_TRAP_ID = trapid;
        }

        // Replaced instructions
        let max = u32::MAX;
        ITEM_GET_BOTTLE_POUCH_SLOT = max;
        asm!("mov w25, {0:w}", in(reg) max);
    }
}

#[no_mangle]
pub fn spawned_actor_traps(
    actorid: actor::ACTORID,
    parent: *mut c_void,
    actor_param1: u32,
    actor_group_type: u8,
) {
    unsafe {
        if actorid == actor::ACTORID::ITEM && NEXT_TRAP_ID != u8::MAX {
            ACTORBASE_PARAM2 &= 0xFFFFFF0F;
            ACTORBASE_PARAM2 |= (NEXT_TRAP_ID << 4) as u32;
            NEXT_TRAP_ID = u8::MAX;
        }

        // Replaced instructions
        asm!("mov x8, {0:x}", in(reg) ACTOR_ALLOCATOR_DEFINITIONS_PTR);
    }
}

#[no_mangle]
pub fn handle_closet_traps(item_id: u32) -> u32 {
    unsafe {
        let closet_actor: *mut actor::dAcOBase;
        asm!("mov {0:x}, x19", out(reg) closet_actor);

        let trapid = ((*closet_actor).members.base.param2 >> 4) & 0xF;

        ACTORBASE_PARAM2 &= 0xFFFFFF0F;
        ACTORBASE_PARAM2 |= trapid << 4;

        return item_id;
    }
}
