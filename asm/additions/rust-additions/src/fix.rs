#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::lyt;
use crate::minigame;
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
    static LOFTWING_PTR: *mut player::dBird;

    static STORYFLAG_MGR: *mut flag::FlagMgr;
    static SCENEFLAG_MGR: *mut flag::SceneflagMgr;

    static mut CURRENT_STAGE_NAME: [u8; 8];

    static LYT_MSG_WINDOW: *mut lyt::dLytMsgWindow;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn strlen(string: *mut u8) -> u64;
    fn strncmp(dest: *mut u8, src: *mut u8, size: u64) -> u64;
    fn dAcOlightLine__inUpdate(light_pillar_actor: *mut actor::dAcOlightLine, unk: u64);
    fn dAcOrdinaryNpc__update(npc: *mut c_void) -> u64;
    fn dAcNpcSkn2__addInteractionTarget(horwell: *mut c_void, some_val: u32);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
#[no_mangle]
pub fn fix_item_get() {
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

        let current_action = (*PLAYER_PTR).current_action;

        // If in water or sliding, allow immediate item gets
        if ((*PLAYER_PTR).action_flags >> 18) & 0x1 == 1
            || current_action == player::PLAYER_ACTIONS::SLIDING
        {
            // debug::debug_print_num("action_flags: ", (*PLAYER_PTR).action_flags);
            asm!("mov w25, #0"); // allow collecting items in non-vanilla ways

            // If should be a big item get animation, make it a small one
            // Big item gets don't work properly under water :(
            if item_animation_index == 1 && current_action != player::PLAYER_ACTIONS::SLIDING {
                asm!("mov w8, #0");
            }
        }
    }
}

#[no_mangle]
pub fn fix_items_in_sand_piles() {
    unsafe {
        let param1: u32;
        asm!(
            "ldr {0:w}, [x19, #0xc]",
            out(reg) param1,
        );

        let sceneflag = param1 >> 10 & 0xFF;

        // Only trap items in sand piles on Skyloft and if they have the
        // sceneflag for the Item in Bird's Nest check
        if &CURRENT_STAGE_NAME[..5] == b"F000\0" && sceneflag == 13 {
            asm!("mov w8, #1");
        } else {
            asm!("mov w8, #0");
        }

        asm!("cmp w8, #1");
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
    unsafe {
        let mut subtypeBitfield: u8;
        asm!(
            "ldrb {0:w}, [x23, #0xce]",
            out(reg) subtypeBitfield,
        );

        // If not Sandship stone
        if (subtypeBitfield & 2) == 0 {
            asm!(
                "mov w8, #0",
                "strb w8, [x23, #0xba]", // playFirstTimeCS
                "strb w8, [x23, #0xc1]", // isFirstStone
            );
        }

        // Replaced instructions
        asm!(
            "mov w9, #0xc2960000",
            "mov w8, {0:w}",
            in(reg) subtypeBitfield,
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
        dAcNpcSkn2__addInteractionTarget(horwell, 2);

        // Replaced instructions
        dAcOrdinaryNpc__update(horwell);
        asm!("ldr x8,[x19, #0xb60]");
    }
}

#[no_mangle]
pub fn is_kikwi_found(dont_care: *mut c_void, found_storyflag: u16) -> bool {
    unsafe {
        if &CURRENT_STAGE_NAME[..5] == b"F100\0" {
            return flag::check_storyflag(found_storyflag) == 1;
        } else {
            return true;
        }
    }
}

#[no_mangle]
pub fn fix_ammo_counts(collected_item: flag::ITEMFLAGS) {
    // Reset ammo counts to zero if we collect ammo, but don't
    // have the item which corresponds to using the ammo
    match collected_item {
        // Bombs
        flag::ITEMFLAGS::FIVE_BOMBS | flag::ITEMFLAGS::TEN_BOMBS => {
            if flag::check_itemflag(flag::ITEMFLAGS::BOMB_BAG) == 0 {
                flag::set_itemflag_or_counter_to_value(flag::ITEMFLAGS::BOMB_COUNTER, 0);
            }
        },
        // Arrows
        flag::ITEMFLAGS::SINGLE_ARROW | flag::ITEMFLAGS::BUNDLE_OF_ARROWS => {
            if flag::check_itemflag(flag::ITEMFLAGS::BOW) == 0 {
                flag::set_itemflag_or_counter_to_value(flag::ITEMFLAGS::ARROW_COUNTER, 0);
            }
        },
        // Deku Seeds
        flag::ITEMFLAGS::FIVE_DEKU_SEEDS | flag::ITEMFLAGS::TEN_DEKU_SEEDS => {
            if flag::check_itemflag(flag::ITEMFLAGS::SLINGSHOT) == 0 {
                flag::set_itemflag_or_counter_to_value(flag::ITEMFLAGS::DEKU_SEED_COUNTER, 0);
            }
        },
        _ => {},
    }
}

#[no_mangle]
pub fn apply_loftwing_speed_override() {
    unsafe {
        if (&CURRENT_STAGE_NAME[..5] == b"F023\0"
            && flag::check_storyflag(368) == 1 // Pumpkin Soup delivered to rainbow island
            && flag::check_storyflag(200) == 0) // Levias defeated
            || minigame::MinigameState::SpiralChargeTutorial.is_current()
        {
            if (*LOFTWING_PTR).obj_base_members.forward_speed > 80.0 {
                (*LOFTWING_PTR).obj_base_members.forward_speed = 80.0;
            }
        }
    }
}

#[no_mangle]
pub fn check_for_botg_itemflag_for_light_tower(param1: u64, param2: u64, param3: u64) {
    unsafe {
        let actor: *mut c_void;
        asm!("mov {0:x}, x19", out(reg) actor);

        if flag::check_itemflag(flag::ITEMFLAGS::BALLAD_OF_THE_GODDESS) == 1 {
            asm!("mov w8, 1");
        } else {
            asm!("mov w8, wzr");
        }

        // Replaced instructions
        asm!("mov x0, {0:x}", in(reg) param1);
        asm!("mov x2, {0:x}", in(reg) param3);
        asm!("mov x1, {0:x}", "mov w3, wzr", "mov x4, xzr", in(reg) actor);
    }
}

#[no_mangle]
pub fn set_skyloft_thunderhead_sceneflag() {
    if unsafe { (*SCENEFLAG_MGR).sceneindex } == 0 {
        flag::set_local_sceneflag(29);
    }

    flag::set_global_sceneflag(0, 29);
}

// prevent_pyrup_fire_when_underground1
#[no_mangle]
pub fn not_should_pyrup_breathe_fire(player: *mut player::dPlayer) -> bool {
    unsafe {
        if !((*(*player).vtable).is_recovering_related)(player) && !is_player_in_tunnel() {
            return false;
        }
        return true;
    }
}

#[no_mangle]
pub fn prevent_pyrup_fire_when_underground2(some_value: i16) -> bool {
    unsafe {
        let mut should_prevent_fire = true;

        if !is_player_in_tunnel() {
            should_prevent_fire = false;

            // Replaced instructions
            asm!("strh {0:w}, [x19, #0x1d6]", "strh {0:w}, [x19, #0x13e]", in(reg) some_value);
        }

        return should_prevent_fire;
    }
}

#[no_mangle]
pub fn is_player_in_tunnel() -> bool {
    let current_action = unsafe { (*PLAYER_PTR).current_action };

    if current_action == player::PLAYER_ACTIONS::ATTACK_CRAWL
        || current_action == player::PLAYER_ACTIONS::DAMAGE_CRAWL
        || current_action == player::PLAYER_ACTIONS::CRAWLSPACE
    {
        return true;
    }

    return false;
}
