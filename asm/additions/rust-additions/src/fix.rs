#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::lyt;
use crate::player;

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

//////////////////////
// ADD STRUCTS HERE //
//////////////////////

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static PLAYER_PTR: *mut player::dPlayer;

    static STORYFLAG_MGR: *mut flag::FlagMgr;

    static mut CURRENT_STAGE_NAME: [u8; 8];

    static LYT_MSG_WINDOW: *mut lyt::dLytMsgWindow;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn strlen(string: *mut u8) -> u64;
    fn strncmp(dest: *mut u8, src: *mut u8, size: u64) -> u64;
    fn dAcOlightLine__inUpdate(light_pillar_actor: *mut actor::dAcOlightLine, unk: u64);
    fn dAcOrdinaryNpc__update(npc: *mut c_void) -> u64;
    fn dAcNpcSkn2__addInteractionTarget(horwell: *mut c_void);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
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
            // debug::debug_print_num("action_flags: ", (*PLAYER_PTR).action_flags);
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
pub fn update_crystal_count(itemid: u32) {
    unsafe {
        let mut count: u32 = flag::check_itemflag(flag::ITEMFLAGS::CRYSTAL_PACK_COUNTER);

        // Increase counter depending on the itemid.
        // The counter hasn't increased with the value of the itemid yet
        // so we have to add it manually here
        match itemid {
            0x23 => count += 5, // Crystal Pack
            0x30 => count += 1, // Single Crystal
            _ => count += 0,
        }

        // Update numeric arg 1 with the proper count
        if (itemid == 0x23 || itemid == 0x30) {
            (*(*LYT_MSG_WINDOW).text_mgr).numeric_args[1] = count;
        }

        asm!("mov w0, {0:w}", in(reg) itemid); // Restore w0 back to itemid

        // Replaced instructions
        asm!("and w8, w0, #0xffff", "cmp w8, #0x1c");
    }
}

#[no_mangle]
pub fn horwell_always_interactable(horwell: *mut c_void) {
    unsafe {
        dAcNpcSkn2__addInteractionTarget(horwell);

        // Replaced instructions
        dAcOrdinaryNpc__update(horwell);
        asm!("ldr x8,[x19, #0xb60]");
    }
}
