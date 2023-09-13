#![no_std]
#![feature(split_array)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use core::ffi::c_ushort;

mod structs;

// IMPORTANT: when using vanilla code, the start point must be declared in original-symbols.yaml
// and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut structs::FileMgr;
    static DUNGEONFLAG_MGR: *mut structs::DungeonflagMgr;
    static mut STATIC_STORYFLAGS: [c_ushort; 128usize];
    static mut STATIC_SCENEFLAGS: [c_ushort; 8usize];
    static mut STATIC_TEMPFLAGS: [c_ushort; 4usize];
    static mut STATIC_ZONEFLAGS: [[c_ushort; 4usize]; 63usize];
    static mut STATIC_ITEMFLAGS: [c_ushort; 64usize];
    static mut STATIC_DUNGEONFLAGS: [c_ushort; 8usize];
}

// IMPORTANT: when adding functions here that need to get called from the game, add `#[no_mangle]`
// and add a .global *symbolname* to additions/rust-additions.asm

// #[no_mangle]
// pub fn test() -> u32 {
//     return 69u32;
// }

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

        if itemid >= 25 && itemid <= 27 {
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

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
