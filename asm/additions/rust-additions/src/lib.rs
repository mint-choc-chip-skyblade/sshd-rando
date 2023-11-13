#![no_std]
#![feature(split_array)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use core::arch::asm;
use core::ffi::c_void;
use core::str;
use numtoa::NumToA;

mod structs;

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static PLAYER_PTR: *mut structs::Player;

    static FILE_MGR: *mut structs::FileMgr;
    static HARP_RELATED: *mut structs::HarpRelated;

    static STORYFLAG_MGR: *mut structs::FlagMgr;
    static ITEMFLAG_MGR: *mut structs::FlagMgr;
    static SCENEFLAG_MGR: *mut c_void;
    static DUNGEONFLAG_MGR: *mut structs::DungeonflagMgr;

    static mut STATIC_STORYFLAGS: [u16; 128];
    static mut STATIC_SCENEFLAGS: [u16; 8];
    static mut STATIC_TEMPFLAGS: [u16; 4];
    static mut STATIC_ZONEFLAGS: [[u16; 4]; 63];
    static mut STATIC_ITEMFLAGS: [u16; 64];
    static mut STATIC_DUNGEONFLAGS: [u16; 8];

    static mut GAME_RELOADER: *mut structs::GameReloader;
    static mut RESPAWN_TYPE: u8;
    static mut CURRENT_STAGE_NAME: [u8; 7];
    static mut CURRENT_STAGE_SUFFIX: [u8; 3];
    static mut CURRENT_FADE_FRAMES: u16;
    static mut CURRENT_ROOM: u8;
    static mut CURRENT_LAYER: u8;
    static mut CURRENT_ENTRANCE: u8;
    static mut CURRENT_NIGHT: u8;
    static mut CURRENT_SOMETHING: u8;
    static mut NEXT_STAGE_NAME: [u8; 7];
    static mut NEXT_STAGE_SUFFIX: [u8; 3];
    static mut NEXT_FADE_FRAMES: u16;
    static mut NEXT_ROOM: u8;
    static mut NEXT_LAYER: u8;
    static mut NEXT_ENTRANCE: u8;
    static mut NEXT_NIGHT: u8;
    static mut NEXT_TRIAL: u8;
    static mut NEXT_SOMETHING: u8;
    static mut CURRENT_LAYER_COPY: u8;

    static mut ACTOR_PARAM_SCALE: u64;
    static mut ACTOR_PARAM_ROT: *mut structs::Vec3s;
    static mut ACTORBASE_PARAM2: u32;

    static mut BASEBASE_ACTOR_PARAM1: u32;
    static mut BASEBASE_GROUP_TYPE: u8;

    static ACTOR_ALLOCATOR_DEFINITIONS: u64; // [*const u64; 701];

    static STARTFLAGS: [u16; 1000];

    fn strlen(string: *mut u8) -> u64;
    fn strncmp(dest: *mut u8, src: *mut u8, size: u64) -> u64;
    fn GameReloader__triggerExit(
        gameReloader: *mut structs::GameReloader,
        currentRoom: u32,
        exitIndex: u32,
        forceNight: u32,
        forceTrial: u32,
    );
    fn GameReloader__triggerEntrance(
        gameReloader: *mut structs::GameReloader,
        stageName: *mut [u8; 7],
        room: u32,
        layer: u32,
        entrance: u32,
        forcedNight: u32,
        forcedTrial: u32,
        transitionType: u32,
        transitionFadeFrames: u16,
        unk10: u32,
        unk11: u32,
    );
    fn SceneflagMgr__setFlag(sceneflagMgr: *mut c_void, roomid: u32, flag: u32);
    fn SceneflagMgr__unsetFlag(sceneflagMgr: *mut c_void, roomid: u32, flag: u32);
    fn SceneflagMgr__checkFlag(sceneflagMgr: *mut c_void, roomid: u32, flag: u32) -> u16;
    fn spawnDrop(
        itemid: structs::ITEMFLAGS,
        roomid: u32,
        pos: *mut structs::Vec3f,
        rot: *mut structs::Vec3s,
    );
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

// Flags
// Storyflags
#[no_mangle]
pub fn set_storyflag(flag: u16) {
    unsafe {
        ((*(*STORYFLAG_MGR).funcs).setFlag)(STORYFLAG_MGR, flag);
    };
}

#[no_mangle]
pub fn unset_storyflag(flag: u16) {
    unsafe {
        ((*(*STORYFLAG_MGR).funcs).unsetFlag)(STORYFLAG_MGR, flag);
    };
}

#[no_mangle]
pub fn check_storyflag(flag: u16) -> u32 {
    unsafe {
        return ((*(*STORYFLAG_MGR).funcs).getFlagOrCounter)(STORYFLAG_MGR, flag);
    }
}

// Sceneflags (local)
#[no_mangle]
pub fn set_local_sceneflag(flag: u32) {
    unsafe {
        return SceneflagMgr__setFlag(SCENEFLAG_MGR, 0, flag);
    }
}

#[no_mangle]
pub fn unset_local_sceneflag(flag: u32) {
    unsafe {
        return SceneflagMgr__unsetFlag(SCENEFLAG_MGR, 0, flag);
    }
}

#[no_mangle]
pub fn check_local_sceneflag(flag: u32) -> u16 {
    unsafe {
        return SceneflagMgr__checkFlag(SCENEFLAG_MGR, 0, flag);
    }
}

// Sceneflags (global)
#[no_mangle]
pub fn set_global_sceneflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

#[no_mangle]
pub fn unset_global_sceneflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] &= !(1 << lower_flag);
    }
}

#[no_mangle]
pub fn check_global_sceneflag(sceneindex: u16, flag: u16) -> u16 {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        return ((*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] >> lower_flag)
            & 0x1;
    }
}

// Dungeonflags (global)
#[no_mangle]
pub fn set_global_dungeonflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.dungeonflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

// Itemflags
#[no_mangle]
pub fn set_itemflag(flag: structs::ITEMFLAGS) {
    unsafe {
        ((*(*ITEMFLAG_MGR).funcs).setFlag)(ITEMFLAG_MGR, flag as u16);
    }
}

#[no_mangle]
pub fn unset_itemflag(flag: structs::ITEMFLAGS) {
    unsafe {
        ((*(*ITEMFLAG_MGR).funcs).unsetFlag)(ITEMFLAG_MGR, flag as u16);
    }
}

#[no_mangle]
pub fn check_itemflag(flag: structs::ITEMFLAGS) -> u32 {
    unsafe {
        return ((*(*ITEMFLAG_MGR).funcs).getFlagOrCounter)(ITEMFLAG_MGR, flag as u16);
    }
}

// Misc flag funcs
#[no_mangle]
pub fn set_goddess_sword_pulled_story_flag() {
    // Set story flag 951 (Raised Goddess Sword in Goddess Statue).
    set_storyflag(951);
}

#[no_mangle]
pub fn set_stone_of_trials_placed_flag(
    gameReloader: *mut structs::GameReloader,
    currentRoom: u32,
    exitIndex: u32,
    forceNight: u32,
    forceTrial: u32,
) {
    unsafe {
        GameReloader__triggerExit(gameReloader, currentRoom, exitIndex, forceNight, forceTrial)
    }

    set_storyflag(22); // 22 == Stone of Trials placed storyflag
}

#[no_mangle]
pub fn check_night_storyflag() -> bool {
    return check_storyflag(899) != 0; // 899 == day/night flag
}

#[no_mangle]
pub fn update_day_night_storyflag() {
    // yuzu_print("Updating night flag");

    unsafe {
        // 899 == day/night storyflag
        if NEXT_NIGHT == 1 {
            // yuzu_print("Setting night flag");
            set_storyflag(899);
        } else {
            // yuzu_print("Unsetting night flag");
            unset_storyflag(899);
        }

        ((*(*STORYFLAG_MGR).funcs).doCommit)(STORYFLAG_MGR);

        // Replaced instruction
        NEXT_SOMETHING = 0xFF;
    }

    return;
}

#[no_mangle]
pub fn patch_freestanding_item_fields(
    actorid: u16,
    unk: u64,
    actor_param1: u32,
    actor_group_type: u8,
) {
    // dAcItem actor id && is rando patched item
    if actorid == 0x281 && (actor_param1 >> 9) & 0x1 == 0 {
        let mut use_default_scaling = false;
        let mut y_offset = 0.0f32;

        // Item id
        match actor_param1 & 0x1FF {
            // Sword | Harp | Mitts | Beedle's Insect Cage | Sot | Songs
            10 | 16 | 56 | 159 | 180 | 186..=193 => y_offset = 20.0,
            // Bow | Sea Chart | Wooden Shield | Hylian Shield
            19 | 98 | 116 | 125 => y_offset = 23.0,
            // Clawshots | Spiral Charge
            20 | 21 => y_offset = 25.0,
            // AC BK | FS BK
            25 | 26 => y_offset = 30.0,
            // SSH BK, ET Key, SV BK, ET BK | Amber Tablet
            27..=30 | 179 => y_offset = 24.0,
            // LMF BK
            31 => y_offset = 27.0,
            // Crystal Pack | 5 Bombs | 10 Bombs | Single Crystal | Beetle | Pouch | Small Bomb Bag | Eldin Ore
            35 | 40 | 41 | 48 | 53 | 112 | 134 | 165 => y_offset = 18.0,
            // Bellows | Bug Net | Bomb Bag
            49 | 71 | 92 => y_offset = 26.0,
            52          // Slingshot
            | 68        // Water Dragon's Scale
            | 100..=104 // Medals
            | 108       // Wallets
            | 114       // Life Medal
            | 153       // Empty Bottle
            | 161..=164 // Treasures
            | 166..=170 // Treasures
            | 172..=174 // Treasures
            | 178       // Ruby Tablet
            | 198       // Life Tree Fruit
            | 199 => y_offset = 16.0,
            // Semi-rare | Rare Treasure
            63 | 64 => y_offset = 15.0,
            // Heart Container
            93 => use_default_scaling = true,
            95..=97 => {
                y_offset = 24.0;
                use_default_scaling = true;
            },
            // Seed Satchel | Golden Skull
            128 | 175 => y_offset = 14.0,
            // Quiver | Whip | Emerald Tablet | Maps
            131 | 137 | 177 | 207..=213 => y_offset = 19.0,
            // Earrings
            138 => y_offset = 6.0,
            // Letter | Monster Horn
            158 | 171 => y_offset = 12.0,
            // Rattle
            160 => {
                y_offset = 5.0;
                use_default_scaling = true;
            },
            // Goddess Plume
            176 => y_offset = 17.0,
            _ => y_offset = 0.0,
        }

        let y_offset_as_hex = f32::to_bits(y_offset) >> 16;

        unsafe {
            ACTORBASE_PARAM2 &= 0xFF0000FF; // Clear space for y-offset
            ACTORBASE_PARAM2 |= (y_offset_as_hex << 0x8) as u32;

            // Patch whether to use default scaling into angley.
            // angley is used for the actual rotation of the item but we use
            // the lsb so it shouldn't make a noticeable
            // difference.

            if ACTOR_PARAM_ROT != core::ptr::null_mut() {
                if use_default_scaling {
                    (*ACTOR_PARAM_ROT).y |= 1;
                } else {
                    (*ACTOR_PARAM_ROT).y &= 0xFFFE;
                }
            }
        }
    }

    unsafe {
        // Replaced instructions
        asm!("mov x8, {0}", in(reg) &ACTOR_ALLOCATOR_DEFINITIONS);
    }
}

#[no_mangle]
pub fn fix_freestanding_item_y_offset() {
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

// When checking/setting stage info in this function be sure to use
// all of the NEXT_* variables as this function gets called right after
// those have been assigned.
#[no_mangle]
pub fn handle_er_cases() {
    unsafe {
        // Enforce a max speed after reloading
        // Prevents you running off high ledges from non-vanilla exits
        if (*GAME_RELOADER).speed_after_reload > 30f32 {
            (*GAME_RELOADER).speed_after_reload = 30f32;
        }

        // If we're spawning from Sky Keep, but Sky Keep hasn't appeared yet,
        // instead spawn near the statue
        if &NEXT_STAGE_NAME[..5] == b"F000\0" && NEXT_ENTRANCE == 53 && check_storyflag(22) == 0 {
            NEXT_ENTRANCE = 52
        }

        // // If we're spawning from LMF and it hasn't been raised,
        // // instead spawn in front of where the dungeon entrance would be
        if &NEXT_STAGE_NAME[..5] == b"F300\0" && NEXT_ENTRANCE == 5 && check_storyflag(8) == 0 {
            NEXT_ENTRANCE = 19;
        }

        // If we're spawning in Lanayru Desert/Mines through the minecart entrance,
        // make sure that a timeshift stone that makes the minecart move is active
        if ((&NEXT_STAGE_NAME[..5] == b"F300\0" && NEXT_ENTRANCE == 2)
            || (&NEXT_STAGE_NAME[..7] == b"F300_1\0" && NEXT_ENTRANCE == 1))
            && (check_global_sceneflag(7, 113) == 0 && check_global_sceneflag(7, 114) == 0)
        {
            // Unset all other timeshift stones in the scene
            for flag in (115..=124).chain([108, 111]) {
                unset_global_sceneflag(7, flag);
            }
            // Set the last timeshift stone in mines
            set_global_sceneflag(7, 113);
        }

        // If we're about to enter a stage that should have the silent realm effect
        // set it. Otherwise unset it
        if NEXT_STAGE_NAME[0] == b'S' || &NEXT_STAGE_NAME == b"D003_8\0" {
            NEXT_TRIAL = 1;
        } else {
            NEXT_TRIAL = 0;
        }

        // Force NEXT_NIGHT to day (storyflag keeps the night state stored)
        // If it should be night time, check if the entrance is valid at night
        // check_storyflag(899) can only be true if natural_night_connections is off
        if (check_storyflag(899) != 0 || NEXT_NIGHT == 1) {
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
        (*GAME_RELOADER).item_to_use_after_reload = 0xFF;
        (*GAME_RELOADER).beedle_shop_spawn_state = 0xFF;
        (*GAME_RELOADER).action_index = 0xFF;
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
            (*GAME_RELOADER).action_index = 0x13;
        }

        // Replaced code sets this
        ACTOR_PARAM_SCALE = 0;
    }
}

#[no_mangle]
pub fn fix_sky_keep_exit(
    gameReloader: *mut structs::GameReloader,
    stageName: *mut [u8; 7],
    room: u32,
    layer: u32,
    entrance: u32,
    forcedNight: u32,
    forcedTrial: u32,
    transitionType: u32,
    mut transitionFadeFrames: u16,
    unk10: u32,
    mut unk11: u32,
) {
    unsafe {
        if &(*stageName)[..5] == b"F000\0" {
            // Use bzs exit when leaving the dungeon (makes ER work properly)
            GameReloader__triggerExit(gameReloader, 0, 1, 2, 2);
        } else {
            // Replaced instructions
            transitionFadeFrames = 0xF;
            unk11 = 0xFF;
            GameReloader__triggerEntrance(
                gameReloader,
                stageName,
                room,
                layer,
                entrance,
                forcedNight,
                forcedTrial,
                transitionType,
                transitionFadeFrames,
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
            return ((*(*STORYFLAG_MGR).funcs).getFlagOrCounter)(STORYFLAG_MGR, 152);
        }

        return 1u32;
    }
}

#[no_mangle]
pub fn drop_arrows_bombs_seeds(
    param2_s0x18: u8,
    roomid: u32,
    pos: *mut structs::Vec3f,
    param4: u32,
    param5: *mut c_void,
) {
    unsafe {
        // 0xFE is the custom id being used to drop arrows, bombs, and seeds.
        // Should set the eq flag for comparison after this addtion.
        if param2_s0x18 == 0xFE {
            if check_itemflag(structs::ITEMFLAGS::BOW) != 0 {
                spawnDrop(
                    structs::ITEMFLAGS::BUNDLE_OF_ARROWS,
                    roomid,
                    pos,
                    &mut structs::Vec3s::default() as *mut structs::Vec3s,
                );
            }

            if check_itemflag(structs::ITEMFLAGS::BOMB_BAG) != 0 {
                spawnDrop(
                    structs::ITEMFLAGS::TEN_BOMBS,
                    roomid,
                    pos,
                    &mut structs::Vec3s::default() as *mut structs::Vec3s,
                );
            }

            if check_itemflag(structs::ITEMFLAGS::SLINGSHOT) != 0 {
                spawnDrop(
                    structs::ITEMFLAGS::FIVE_DEKU_SEEDS, // 10 doesn't work for some reason
                    roomid,
                    pos,
                    &mut structs::Vec3s::default() as *mut structs::Vec3s,
                );
            }
        }

        // Replaced instructions
        asm!(
            "mov w25, #0x660d",
            "movk w25, #0x19, LSL #16",
            "mul x10, x9, x25",
            "mov w3, {0:w}",
            in(reg) param4,
        );
    }
}

#[no_mangle]
pub fn drop_nothing(param2_s0x18: u8) {
    unsafe {
        // if should drop seeds, arrows, or bombs
        if param2_s0x18 == 0xB || param2_s0x18 == 0xC || param2_s0x18 == 0xD {
            asm!("mov w0, #0x0"); // 0x0 -> nothing, 0xFF -> green rupee
        }

        // Replaced instructions
        asm!(
            "mov w25, #0x660d",
            "movk w25, #0x19, LSL #16",
            "mul x10, x9, x25",
        );
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
            yuzu_print_number((*PLAYER_PTR).action_flags, 16);
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
        if (*HARP_RELATED).someCheckForContinuousStrumming == 0
            || (*HARP_RELATED).someOtherHarpThing != 0
        {
            // Additional check for BotG
            if check_itemflag(structs::ITEMFLAGS::BALLAD_OF_THE_GODDESS) == 1 {
                return true;
            }
        }

        return false;
    }
}

// Will output a string to Yuzu's log.
// In Yuzu go to Emulation > Configure > Debug and
// enter this into the global log filter:
// *:Error Debug.Emulated:Trace
// Also be sure to check the "Show Log in Console" Option
// to see the output statements in real time

pub fn yuzu_print(string: &str) {
    output_debug_string(string.as_ptr(), string.len());
}

pub fn yuzu_print_number<T: NumToA<T>>(num: T, base: T) {
    let mut buffer = [0u8; 20]; // I doubt we'll be printing numbers greater than 1 quintillion
    yuzu_print(num.numtoa_str(base, &mut buffer)); // print in base 10
}

pub fn output_debug_string(string: *const u8, length: usize) {
    unsafe {
        asm!("mov x0, {0}", in(reg) string);
        asm!("mov x1, {0}", in(reg) length);
        asm!("svc #39");
    }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
