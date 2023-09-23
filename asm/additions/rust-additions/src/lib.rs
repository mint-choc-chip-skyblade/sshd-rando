#![no_std]
#![feature(split_array)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use core::arch::asm;
use core::ffi::c_void;

mod structs;

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut structs::FileMgr;
    static STORYFLAG_MGR: *mut structs::FlagMgr;
    static ITEMFLAG_MGR: *mut structs::FlagMgr;
    static DUNGEONFLAG_MGR: *mut structs::DungeonflagMgr;
    static mut STATIC_STORYFLAGS: [u16; 128];
    static mut STATIC_SCENEFLAGS: [u16; 8];
    static mut STATIC_TEMPFLAGS: [u16; 4];
    static mut STATIC_ZONEFLAGS: [[u16; 4]; 63];
    static mut STATIC_ITEMFLAGS: [u16; 64];
    static mut STATIC_DUNGEONFLAGS: [u16; 8];
    static STARTFLAGS: [u16; 1000];
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
#[no_mangle]
pub fn handle_startflags() {
    unsafe {
        (*FILE_MGR).preventCommit = true;

        let mut delimiter_count = 0;

        for flag_ptr in STARTFLAGS.iter() {
            let mut flag = *flag_ptr;

            if flag == 0xFFFF {
                delimiter_count += 1;
                continue;
            }

            match delimiter_count {
                // Storyflags
                0 => {
                    ((*(*STORYFLAG_MGR).funcs).setFlag)(STORYFLAG_MGR, flag.into());
                },

                // Sceneflags
                1 => {
                    // flag = 0xFFSS where SS == sceneindex and FF == sceneflag
                    set_global_sceneflag(flag & 0xFF, flag >> 8);
                },

                // Itemflags
                2 => {
                    ((*(*ITEMFLAG_MGR).funcs).setFlag)(ITEMFLAG_MGR, flag.into());
                },

                // Dungeonflags
                3 => {
                    let sceneindex = flag & 0xFF;
                    flag = flag >> 8;

                    // Convert dungeonflag numbers to be like sceneflags
                    // Dungeonflags start offset by 1 due to an undefined value in the flag
                    // definitions.
                    if flag == 2 || flag == 3 || flag == 4 {
                        flag -= 1;
                    } else if flag == 12 {
                        // The rooms are defined before the boss key placed flag
                        flag = 7;
                    } else if flag == 16 {
                        flag = 8;
                    }

                    // flag = 0xFFSS where SS == sceneindex and FF == dungeonflag
                    set_global_dungeonflag(sceneindex, flag);
                },

                _ => {
                    break;
                },
            }
        }

        ((*(*STORYFLAG_MGR).funcs).doCommit)(STORYFLAG_MGR);
        ((*(*ITEMFLAG_MGR).funcs).doCommit)(ITEMFLAG_MGR);

        (*FILE_MGR).preventCommit = false;
    }
}

#[no_mangle]
fn set_global_sceneflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

#[no_mangle]
fn set_global_dungeonflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.dungeonflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

#[no_mangle]
pub fn handle_custom_item_get(item_actor: *mut structs::dAcItem) -> u16 {
    const BK_TO_FLAGINDEX: [usize; 7] = [
        12,  // AC BK - item id 25
        15,  // FS BK - item id 26
        18,  // SSH BK - item id 27
        255, // unused, shouldn't happen
        11,  // SV BK - item id 29
        14,  // ET - item id 30
        17,  // LMF - item id 31
    ];

    const SK_TO_FLAGINDEX: [usize; 7] = [
        11, // SV SK - item id 200
        17, // LMF SK - item id 201
        12, // AC SK - item id 202
        15, // FS SK - item id 203
        18, // SSH SK - item id 204
        20, // SK SK - item id 205
        9,  // Caves SK - item id 206
    ];

    const MAP_TO_FLAGINDEX: [usize; 7] = [
        11, // SV MAP - item id 207
        14, // ET MAP - item id 208
        17, // LMF MAP - item id 209
        12, // AC MAP - item id 210
        15, // FS MAP - item id 211
        18, // SSH MAP - item id 212
        20, // SK MAP - item id 213
    ];

    unsafe {
        let itemid = (*item_actor).itemid;

        let mut dungeon_item_mask = 0;

        if (itemid >= 25 && itemid <= 27) || (itemid >= 29 && itemid <= 31) {
            dungeon_item_mask = 0x80; // boss keys
        }

        if dungeon_item_mask == 0 {
            if itemid >= 200 && itemid <= 206 {
                dungeon_item_mask = 0x0F; // small keys
            }
        }

        if dungeon_item_mask == 0 {
            if itemid >= 207 && itemid <= 213 {
                dungeon_item_mask = 0x02; // maps
            }
        }

        if dungeon_item_mask != 0 {
            let current_scene_index = (*DUNGEONFLAG_MGR).sceneindex as usize;
            let mut dungeon_item_scene_index = 0xFF;

            if dungeon_item_mask == 0x80 {
                dungeon_item_scene_index = BK_TO_FLAGINDEX[(itemid - 25) as usize];
            }

            if dungeon_item_mask == 0x0F {
                dungeon_item_scene_index = SK_TO_FLAGINDEX[(itemid - 200) as usize];
            }

            if dungeon_item_mask == 0x02 {
                dungeon_item_scene_index = MAP_TO_FLAGINDEX[(itemid - 207) as usize];
            }

            // Set the local flag if the item is in its vanilla scene.
            if current_scene_index == dungeon_item_scene_index {
                if dungeon_item_mask != 0x0F {
                    STATIC_DUNGEONFLAGS[0] |= dungeon_item_mask;
                } else {
                    STATIC_DUNGEONFLAGS[1] += 1;
                }
            }
            // Otherwise, set the global flag.
            if dungeon_item_mask != 0x0F {
                (*FILE_MGR).FA.dungeonflags[dungeon_item_scene_index][0] |= dungeon_item_mask;
            } else {
                (*FILE_MGR).FA.dungeonflags[dungeon_item_scene_index][1] += 1;
            }
        }

        return (*item_actor).finalDeterminedItemID;
    }
}

#[no_mangle]
fn fix_freestanding_item_y_offset() {
    let mut item: *mut structs::dAcItem;

    unsafe {
        // Get param1 to check if the item needs its size changing.
        asm!("mov {0}, x19", out(reg) item);

        // Replaced instruction
        asm!("mov w0, w20");

        if (*item).base.baseBase.param1 >> 9 & 0x1 == 0 {
            let y_offset_as_hex = ((*item).base.members.base.param2 & 0x00FFFF00) << 8;
            let y_offset = f32::from_bits(y_offset_as_hex);

            (*item).freestandingYOffset = y_offset;
        }
    }
}

#[no_mangle]
fn storyflag_set_to_1(flag: u16) {
    unsafe {
        ((*(*STORYFLAG_MGR).funcs).setFlag)(STORYFLAG_MGR, flag);
    };
}

#[no_mangle]
fn set_goddess_sword_pulled_story_flag() {
    // Set story flag 951 (Raised Goddess Sword in Goddess Statue).
    storyflag_set_to_1(951);
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
