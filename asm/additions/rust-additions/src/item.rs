#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::event;
use crate::fix;
use crate::flag;
use crate::math;
use crate::player;
use crate::savefile;
use crate::settings;

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

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcItem {
    pub base:                    actor::dAcOBase,
    pub itemid:                  u16,
    pub _0:                      [u8; 6],
    pub item_model_ptr:          *mut itemModel,
    pub _1:                      [u8; 2784],
    pub actor_list_element:      u32,
    pub _2:                      [u8; 816],
    pub freestanding_y_offset:   f32,
    pub _3:                      [u8; 32],
    pub rot_increment:           math::Vec3s,
    pub model_rot:               math::Vec3s,
    pub final_determined_itemid: u16,
    pub _4:                      [u8; 9],
    pub prevent_timed_despawn:   u8,
    pub prevent_drop:            u8,
    pub _5:                      [u8; 3],
    pub no_longer_waiting:       u8,
    pub _6:                      [u8; 19],
}
assert_eq_size!([u8; 0x1288], dAcItem);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct itemModel {
    pub vtable: *mut itemModelVtable,
}
assert_eq_size!([u8; 0x8], itemModel);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct itemModelVtable {
    pub _0:               [u8; 0x28],
    pub set_local_matrix:
        extern "C" fn(item_model_ptr: *mut itemModel, world_matrix: *const c_void),
}
assert_eq_size!([u8; 0x30], itemModelVtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcTbox {
    pub base:                         actor::dAcOBase,
    pub mdlAnmChr_c:                  [u8; 0xB8],
    pub _0:                           [u8; 0x12E8],
    pub state_mgr:                    [u8; 0x70],
    pub _1:                           [u8; 0xA8],
    pub dowsing_target:               [u8; 0x28],
    pub goddess_chest_dowsing_target: [u8; 0x28],
    pub register_dowsing_target:      [u8; 0x10],
    pub unregister_dowsing_target:    [u8; 0x10],
    pub _2:                           [u8; 0x40],
    pub anim_completion_amount:       f32,
    pub _3:                           [u8; 0x14],
    pub itemid_0x1ff:                 flag::ITEMFLAGS,
    pub item_model_index:             u16,
    pub chest_opened:                 u8,
    pub spawn_sceneflag:              u8,
    pub set_sceneflag:                u8,
    pub chestflag:                    u8,
    pub unk:                          u8,
    pub chest_subtype:                u8,
    pub _4:                           [u8; 2],
    pub is_chest_opened_related:      u8,
    pub _5:                           [u8; 4],
    pub do_obstructed_check:          bool,
    pub _6:                           [u8; 6],
}
assert_eq_size!([u8; 0x19A8], dAcTbox);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static PLAYER_PTR: *mut player::dPlayer;

    static FILE_MGR: *mut savefile::FileMgr;
    static ROOM_MGR: *mut actor::RoomMgr;
    static HARP_RELATED: *mut event::HarpRelated;

    static DUNGEONFLAG_MGR: *mut flag::DungeonflagMgr;
    static SCENEFLAG_MGR: *mut flag::SceneflagMgr;

    static mut STATIC_DUNGEONFLAGS: [u16; 8];
    static mut CURRENT_STAGE_NAME: [u8; 8];

    static EQUIPPED_SWORD: u8;
    static mut ITEM_GET_BOTTLE_POUCH_SLOT: u32;
    static mut NUMBER_OF_ITEMS: u32;

    static mut SQUIRRELS_CAUGHT_THIS_PLAY_SESSION: bool;

    static RANDOMIZER_SETTINGS: settings::RandomizerSettings;
    static mut dAcOWarp__StateGateOpen: c_void;
    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn sinf(x: f32) -> f32;
    fn cosf(x: f32) -> f32;
    fn getRotFromDegrees(deg: f32) -> u16;
    fn dAcItem__determineFinalItemid(itemid: u64) -> u64;
    fn dAcOmusasabi__stateWaitEnter();
    fn checkParam2OnDestroy(
        param2_s0x18: u8,
        roomid: u32,
        pos: *mut math::Vec3f,
        param_4: u32,
        param_5: *mut c_void,
    ) -> u32;
    fn getArcModelFromName(
        arc_table: *mut c_void,
        model_name: *const c_char,
        model_path: *const c_char,
    ) -> u64;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
#[no_mangle]
pub fn give_item(itemid: u8) {
    give_item_with_sceneflag(itemid, 0xFF);
}

#[no_mangle]
pub fn give_item_with_sceneflag(itemid: u8, sceneflag: u8) -> *mut dAcItem {
    unsafe {
        NUMBER_OF_ITEMS = 0;
        ITEM_GET_BOTTLE_POUCH_SLOT = 0xFFFFFFFF;

        let new_itemid = dAcItem__determineFinalItemid(itemid as u64);
        let param1: u32 = (new_itemid as u32) | (sceneflag as u32) << 10 | 0x580000;

        let item_actor: *mut dAcItem = actor::spawn_actor(
            actor::ACTORID::ITEM,
            (*ROOM_MGR).roomid.into(),
            param1,
            core::ptr::null_mut(),
            core::ptr::null_mut(),
            core::ptr::null_mut(),
            0xFFFFFFFF,
        ) as *mut dAcItem;

        ITEM_GET_BOTTLE_POUCH_SLOT = 0xFFFFFFFF;
        NUMBER_OF_ITEMS = 0;

        return item_actor;
    }
}

#[no_mangle]
pub fn init_appearing_chest_subtype(tbox: *mut dAcTbox) -> *mut dAcTbox {
    unsafe {
        let param1 = (*tbox).base.basebase.members.param1;
        let spawn_sceneflag = (param1 >> 0x14) & 0xFF;

        if spawn_sceneflag != 0xFF && flag::check_local_sceneflag(spawn_sceneflag.into()) == 0 {
            (*tbox).chest_subtype = 0;
        } else {
            (*tbox).chest_subtype = ((param1 >> 4) & 0x3) as u8;
        }

        // Replaced instructions
        asm!("mov w8, #0x1995", "mov w1, #0xFFFFFFFF");
        return tbox;
    }
}

#[no_mangle]
pub fn spawn_appeared_chest(tbox: *mut dAcTbox) -> *mut dAcTbox {
    unsafe {
        let w9_bkp: u32;
        asm!("mov {0:w}, w9", out(reg) w9_bkp);
        asm!("mov x19, {0:x}", in(reg) tbox);

        if 0.910 > (*tbox).anim_completion_amount && (*tbox).anim_completion_amount > 0.905 {
            let mut new_param1 = (*tbox).base.basebase.members.param1;

            let current_pos = (*tbox).base.members.base.pos;
            let new_pos: *mut math::Vec3f = &mut math::Vec3f {
                x: current_pos.x,
                y: current_pos.y,
                z: current_pos.z,
            } as *mut math::Vec3f;

            let current_rot = (*tbox).base.members.base.rot;
            let new_rot: *mut math::Vec3s = &mut math::Vec3s {
                x: 0xFF00 | (*tbox).set_sceneflag as u16,
                y: current_rot.y,
                z: (((*tbox).chestflag as u16) << 9) | ((*tbox).itemid_0x1ff as u16),
            } as *mut math::Vec3s;

            let new_scale: *mut math::Vec3f = &mut math::Vec3f {
                x: 1.0,
                y: 1.0,
                z: 1.0,
            } as *mut math::Vec3f;

            actor::spawn_actor(
                actor::ACTORID::TBOX,
                (*ROOM_MGR).roomid.into(),
                new_param1,
                new_pos,
                new_rot,
                new_scale,
                (*tbox).base.members.base.param2,
            );
        }

        asm!("ldr w8, [{0:x}, #0x1988]", in(reg) tbox);
        asm!("mov w9, {0:w}", in(reg) w9_bkp);
        return tbox;
    }
}

#[no_mangle]
pub fn hide_appearing_chest(tbox: *mut dAcTbox) {
    unsafe {
        (*tbox).base.members.base.pos.y = (*tbox).base.members.base.pos.y - 10000.0;
    }
}

#[no_mangle]
pub fn handle_crest_hit_give_item(crest_actor: *mut actor::dAcOSwSwordBeam) {
    unsafe {
        // Reset position so that we don't void out before getting the items
        let position = math::Vec3f {
            x: 0.0,
            y: 0.0,
            z: 304.0,
        };
        (*PLAYER_PTR).obj_base_members.base.pos = position;

        // Goddess Sword Reward
        if flag::check_local_sceneflag(50) == 0 {
            let goddess_sword_reward: u8 =
                ((*crest_actor).base.basebase.members.param1 >> 0x18) as u8;
            give_item(goddess_sword_reward);
            flag::set_local_sceneflag(50);
        }
        if (EQUIPPED_SWORD < 2) {
            return;
        }

        // Longsword Reward
        if flag::check_local_sceneflag(51) == 0 {
            let longsword_reward: u8 = ((*crest_actor).base.basebase.members.param1 >> 0x10) as u8;
            give_item(longsword_reward);
            flag::set_local_sceneflag(51);
        }
        if (EQUIPPED_SWORD < 3) {
            return;
        }

        // White Sword Reward
        if flag::check_local_sceneflag(52) == 0 {
            let whitesword_reward: u8 = ((*crest_actor).base.members.base.param2 >> 0x18) as u8;
            give_item(whitesword_reward);
            flag::set_local_sceneflag(52);
        }
    }
}

#[no_mangle]
pub fn handle_custom_item_get(item_actor: *mut dAcItem) -> u16 {
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

        // Get necessary params for setting a custom flag if this item has one
        let (flag, sceneindex, flag_space_trigger, original_itemid) =
            unpack_custom_item_params(item_actor);

        if flag != 0x7F {
            // Use different flag spaces depending on the value of the
            // flag_space_trigger
            match flag_space_trigger {
                0 => flag::set_global_sceneflag(sceneindex as u16, flag as u16),
                1 => flag::set_global_dungeonflag(sceneindex as u16, flag as u16),
                _ => {},
            }
        }

        return (*item_actor).final_determined_itemid;
    }
}

// Unpacks our custom item params into separate variables
#[no_mangle]
pub fn unpack_custom_item_params(item_actor: *mut dAcItem) -> (u32, u32, u32, u32) {
    unsafe {
        let param2: u32 = (*item_actor).base.members.base.param2;
        let flag: u32 = (param2 & (0x00007F00)) >> 8;
        let mut sceneindex: u32 = (param2 & (0x00018000)) >> 15;
        let flag_space_trigger: u32 = (param2 & (0x00020000)) >> 17;
        let mut original_itemid: u32 = (param2 & (0x00FC0000)) >> 18;

        // Transform the scene index into one of the unused ones
        match sceneindex {
            0 => sceneindex = 6,
            1 => sceneindex = 13,
            2 => sceneindex = 16,
            3 => sceneindex = 19,
            _ => {},
        }

        // Transform the original_itemid into its proper itemid
        match original_itemid {
            1 => original_itemid = 42, // Stamina Fruit
            2 => original_itemid = 2,  // Green Rupee
            3 => original_itemid = 3,  // Blue Rupee
            4 => original_itemid = 4,  // Red Rupee
            5 => original_itemid = 34, // Rupoor
            _ => {},
        }

        return (flag, sceneindex, flag_space_trigger, original_itemid);
    }
}

#[no_mangle]
pub fn check_and_modify_item_actor(item_actor: *mut dAcItem) {
    unsafe {
        // Get necessary params for checking if this item has a custom flag
        let (flag, sceneindex, flag_space_trigger, original_itemid) =
            unpack_custom_item_params(item_actor);

        // Don't do anything for conveyor spawned stamina fruit in LMF
        let current_item = (*item_actor).base.basebase.members.param1 & 0x1FF;
        if current_item == 42 && &CURRENT_STAGE_NAME[..4] == b"D300" {
            (*item_actor).base.basebase.members.param1 |= 0x200;
            return;
        }

        // Force a textbox for every item
        (*item_actor).base.basebase.members.param1 &= !0x200u32;

        // If the item isn't a trap and it's a minor item, don't force a textbox
        if ((*item_actor).base.members.base.param2 >> 4) & 0xF == 0xF {
            match current_item {
                // Green | Blue | Red Rupee | Heart, Arrows | Bombs, Stamina, Tears, Light Fruit |
                // Seeds | Uncommon | Rare Treasure | Bugs | Treasures
                2 | 3 | 4 | 6..=8 | 40..=47 | 57 | 60 | 63 | 64 | 141..=152 | 161..=176 => {
                    (*item_actor).base.basebase.members.param1 |= 0x200;
                },
                _ => {},
            }
        }

        // Despawn the item if it's one of the stamina fruit on LMF that
        // shouldn't exist until the dungeon has been raised. Actors are
        // identified by Z position
        let zPos: f32 = (*item_actor).base.members.base.pos.z;
        if (&CURRENT_STAGE_NAME[..5] == b"F300\0"
            && flag::check_storyflag(8) == 0 // LMF is not raised
            && (zPos == 46.531517028808594 || zPos == 105.0 || zPos == 3495.85009765625))
        {
            // Set itemid to 0 which despawns it later in the init function
            (*item_actor).base.basebase.members.param1 &= !0x1FF;
        }

        // Check if the flag is on
        let mut flag_is_on = 0;
        match flag_space_trigger {
            0 => flag_is_on = flag::check_global_sceneflag(sceneindex as u16, flag as u16),
            1 => flag_is_on = flag::check_global_dungeonflag(sceneindex as u16, flag as u16),
            _ => {},
        }

        // If we have a custom flag and it's been set, revert this item back to what
        // it originally was
        if flag != 0x7F && flag_is_on != 0 {
            (*item_actor).base.basebase.members.param1 &= !0x1FF;
            (*item_actor).base.basebase.members.param1 |= original_itemid;
            // Set bit 9 for no textbox
            (*item_actor).base.basebase.members.param1 |= 0x200;
        // Otherwise, if we have a custom flag, potentially fix
        // the horizontal offset if necessary
        } else if (flag != 0x7F) {
            fix_freestanding_item_horizontal_offset(item_actor);
        }

        // Fix the y offset if necessary
        fix_freestanding_item_y_offset(item_actor);

        // Replaced Code
        if (((*item_actor).base.basebase.members.param1 >> 10) & 0xFF) == 0xFF {
            asm!("mov x19, #1");
            asm!("cmp x19, #1");
        }
        asm!("mov x19, {0}", in(reg) item_actor);
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
pub fn give_squirrel_item(musasabi_tag: *mut actor::dTgMusasabi) {
    unsafe {
        if SQUIRRELS_CAUGHT_THIS_PLAY_SESSION && (*musasabi_tag).unused == 0 {
            let itemid: u8 = ((*musasabi_tag).base.members.param2 & 0xFF) as u8;
            let sceneflag: u8 = ((*musasabi_tag).base.members.param2 >> 8 & 0xFF) as u8;

            if sceneflag != u8::MAX && flag::check_local_sceneflag(sceneflag as u32) == 0 {
                give_item_with_sceneflag(itemid, sceneflag);
            } else {
                give_item(flag::ITEMFLAGS::RED_RUPEE as u8);
            }

            // Keep track of if the item has alreeady been given
            (*musasabi_tag).unused = 1;
        }

        SQUIRRELS_CAUGHT_THIS_PLAY_SESSION = false;

        // Replaced instructions
        let current_action: player::PLAYER_ACTIONS = (*PLAYER_PTR).current_action;

        if current_action != player::PLAYER_ACTIONS::FREE_FALL
            && current_action != player::PLAYER_ACTIONS::USING_SAILCLOTH
        {
            (*musasabi_tag).has_spawned_squirrels = false;
        }
    }
}

#[no_mangle]
pub fn tgreact_spawn_custom_item(
    mut param2_s0x18: u8,
    roomid: u32,
    pos: *mut math::Vec3f,
    param_4: u32,
    param_5: *mut c_void,
) -> u32 {
    unsafe {
        let tgreact: *mut actor::dAcOBase;
        asm!("mov {0:x}, x19", out(reg) tgreact);

        let tgreact_param1: u32 = (*tgreact).basebase.members.param1;
        let param2 = (*tgreact).members.base.param2;

        if (param2 >> 8) & 0x3FF != 0x3FF {
            let flag: u32 = (param2 & (0x00007F00)) >> 8;

            let mut sceneindex: u32 = (param2 & (0x00018000)) >> 15;
            match sceneindex {
                0 => sceneindex = 6,
                1 => sceneindex = 13,
                2 => sceneindex = 16,
                3 => sceneindex = 19,
                _ => {},
            }

            let flag_space_trigger: u32 = (param2 & (0x00020000)) >> 17;

            // Check if the flag is on
            let mut flag_is_on = 0;
            match flag_space_trigger {
                0 => flag_is_on = flag::check_global_sceneflag(sceneindex as u16, flag as u16),
                1 => flag_is_on = flag::check_global_dungeonflag(sceneindex as u16, flag as u16),
                _ => {},
            }

            let new_itemid = dAcItem__determineFinalItemid(((tgreact_param1 >> 8) & 0xFF) as u64);

            // If the tgreact would give hearts in vanilla and the randomized item is a
            // heart, behave like the flag has already been set. This allows 3
            // hearts to spawn instead
            if flag_is_on == 0 && (((param2 >> 24) & 0xFF) != 6 || new_itemid != 6) {
                let item_actor_param1: u32 = (new_itemid as u32) | 0xFF1FFE00;

                let mut actor_pos = (*tgreact).members.base.pos;
                let actor_pos_ptr: *mut math::Vec3f = &mut actor_pos as *mut math::Vec3f;

                let mut facing_angle = (*tgreact).members.base.rot.y;

                if facing_angle == 0 {
                    facing_angle = (*PLAYER_PTR).obj_base_members.base.rot.y - 0x8000;
                }

                let mut item_rot = math::Vec3s {
                    x: 0,
                    y: facing_angle,
                    z: 0,
                };
                let item_rot_ptr: *mut math::Vec3s = &mut item_rot as *mut math::Vec3s;

                let trapid = (param2 >> 19) & 0xF;

                let item_actor: *mut dAcItem = actor::spawn_actor(
                    actor::ACTORID::ITEM,
                    roomid,
                    item_actor_param1,
                    actor_pos_ptr,
                    item_rot_ptr,
                    core::ptr::null_mut(),
                    0xFF00000F | (param2 & 0x3FF00) | (trapid << 4),
                ) as *mut dAcItem;

                let mut forward_speed = 0.0;
                let mut velocity_y = 0.0;

                if (param2 >> 18) & 1 == 1 {
                    forward_speed = 12.0;
                    velocity_y = 19.5;
                }

                // Give items that are normally Deku Seeds a bit of an extra push xD
                if ((param2 >> 24) & 0xFF) == 0x0D {
                    forward_speed += 2.0;
                    velocity_y += 3.0;
                }

                (*item_actor).base.members.forward_speed = forward_speed;
                (*item_actor).base.members.velocity.x = 0.0;
                (*item_actor).base.members.velocity.y = velocity_y;
                (*item_actor).base.members.velocity.z = 0.0;
                (*item_actor).prevent_timed_despawn = 1;
                param2_s0x18 = 0xFF;
                (*tgreact).members.base.param2 |= 0x3FF00;
            }
        }

        if param2_s0x18 == 0xFF {
            return 1; // force hidden item jingle to play
        }

        if flag::check_local_sceneflag(tgreact_param1 & 0xFF) == 0 {
            flag::set_local_sceneflag(tgreact_param1 & 0xFF);

            return checkParam2OnDestroy(param2_s0x18, roomid, pos, param_4, param_5);
        }

        return 0;
    }
}

#[no_mangle]
pub fn academy_bell_give_custom_item() {
    unsafe {
        let bell_actor: *mut actor::dAcObell;
        asm!("mov {0:x}, x19", out(reg) bell_actor);

        let itemid = (*bell_actor).base.basebase.members.param1 & 0xFF;
        let param1 = 0x19FC00 | itemid; // item will set sceneflag 127 on collection
        asm!("mov w1, {0:w}", in(reg) param1);

        // Replaced instructions
        asm!("mov w4, #0xFFFFFFFF", "mov w5, wzr");
    }
}

#[no_mangle]
pub fn check_bucha_local_sceneflag(flag: u32) -> u16 {
    unsafe {
        if &CURRENT_STAGE_NAME[..5] == b"F100\0" {
            return flag::check_local_sceneflag(flag);
        }
        return 1;
    }
}

#[no_mangle]
pub fn check_stage_on_bucha_interaction(param1: u64) -> u64 {
    unsafe {
        if &CURRENT_STAGE_NAME[..5] != b"F100\0" {
            asm!("add lr, lr, #0x234");
        }

        // Replaced intructions
        asm!(
            "mov x19, {0:x}",
            "mov w8, #0x2651",
            in(reg) param1,
        );
        return param1;
    }
}

#[no_mangle]
pub fn fix_bottle_items_from_npcs(param1: u64, param2: u64, param3: u32) {
    unsafe {
        if flag::check_storyflag(894) == 0 {
            ITEM_GET_BOTTLE_POUCH_SLOT = 0xFFFFFFFF;
        }

        // Replaced instructions
        asm!("mov w0, #0x281", "mov w3, #2", "mov x1, {0:x}", "mov w2, {1:w}", in(reg) param2, in(reg) param3);
    }
}

#[no_mangle]
pub fn rotate_freestanding_items(item_actor: *mut dAcItem) {
    unsafe {
        // Spin items if not a stamina fruit
        if (*item_actor).itemid != 42 {
            (*item_actor).rot_increment.x = getRotFromDegrees(1.5);
        }
    }
}

#[no_mangle]
pub fn fix_freestanding_item_y_offset(item_actor: *mut dAcItem) {
    unsafe {
        let actor_param1 = (*item_actor).base.basebase.members.param1;

        if (*item_actor).itemid != 42 {
            let mut use_default_scaling = false;
            let mut y_offset = 0.0f32;
            let item_rot = (*item_actor).base.members.base.rot;

            // Item id
            match dAcItem__determineFinalItemid((actor_param1 & 0x1FF).into()) {
                // Sword + Sailcloth | Harp | Digging Mitts | Scattershot | Beedle's Insect Cage | Ancient Flower | Sot | Songs
                9..=15 | 16 | 56 | 105 | 159 | 166 | 180 | 186..=193 => y_offset = 20.0,
                // Bow | Iron Bow | Sacred Bow | Sea Chart | Wooden Shield | Hylian Shield
                19 | 90 | 91 | 98 | 116 | 125 => y_offset = 23.0,
                // Clawshots | Spiral Charge | Mogma Mitts | Life Tree Seedling
                20 | 21 | 99 | 197 => y_offset = 25.0,
                // AC BK | FS BK
                25 | 26 => y_offset = 30.0,
                // SSH BK, ET Key, SV BK, ET BK | Amber Tablet
                27..=30 | 99 | 179 => y_offset = 24.0,
                // LMF BK
                31 => y_offset = 27.0,
                // Crystal Pack | 5 Bombs | 10 Bombs | Single Crystal | Beetle | Pouch | Pouch Expansion | Small Bomb Bag | Big Bug Net | Eldin Ore
                35 | 40 | 41 | 48 | 53 | 112 | 113 | 134 | 140 | 165 => y_offset = 18.0,
                // Bellows | Bug Net | Bomb Bag
                49 | 71 | 92 => y_offset = 26.0,
                36          // Glittering Spores
                | 52        // Slingshot
                | 54        // Bottle of Water
                | 55        // Mushroom Spores
                | 65        // Guardian Potion
                | 66        // Guardian Potion+
                | 68        // Water Dragon's Scale
                | 70        // Bug Medal
                | 74        // Sacred Water
                | 78        // Heart Potion
                | 79        // Heart Potion+
                | 81        // Heart Potion++
                | 84        // Stamina Potion
                | 85        // Stamina Potion+
                | 86        // Air Potion
                | 87        // Air Potion+
                | 88        // Fairy in a Bottle
                | 100..=104 // Medals
                | 108..=111 // Wallets
                | 114       // Life Medal
                | 126       // Revitalizing Potion
                | 127       // Revitalizing Potion+
                | 153       // Empty Bottle
                | 161..=164 // Treasures
                | 167..=170 // Treasures
                | 172..=174 // Treasures
                | 178       // Ruby Tablet
                | 194       // Revitalizing Potion++
                | 195       // Hot Pumpkin Soup
                | 196       // Cold Pumpkin Soup
                | 198       // Life Tree Fruit
                | 199 => y_offset = 16.0,
                // Seeds | Uncommon | Rare Treasure
                57 | 60 | 63 | 64 => y_offset = 15.0,
                // Beetle Upgrades
                75..=77 => y_offset = 10.0,
                // Heart Container
                93 => use_default_scaling = true,
                // Triforces
                95..=97 => {
                    y_offset = 24.0;
                    use_default_scaling = true;
                },
                // Seed Satchel | Golden Skull
                128 | 175 => y_offset = 14.0,
                // Map | Quiver | Whip | Emerald Tablet | Maps
                50 | 131 | 137 | 177 | 207..=213 => y_offset = 19.0,
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

            // Only apply the offset if the item isn't tilted
            if item_rot.x < 0x2000 || item_rot.x > 0xE000 {
                (*item_actor).freestanding_y_offset = y_offset;
            }

            if use_default_scaling {
                (*item_actor).base.members.base.rot.y |= 1;
            } else {
                (*item_actor).base.members.base.rot.y &= 0xFFFE;
            }
        }
    }
}

#[no_mangle]
pub fn fix_freestanding_item_horizontal_offset(item_actor: *mut dAcItem) {
    unsafe {
        // If the item is facing sideways, apply a horizontal offset (i.e. stamina
        // fruit on walls) and rotate the item if necessary
        let item_rot = (*item_actor).base.members.base.rot;
        if item_rot.x > 0x2000 && item_rot.x < 0xE000 {
            let actor_param1 = (*item_actor).base.basebase.members.param1;
            let mut h_offset = 0.0f32;
            let mut angle_change_x = 0u16;
            let mut angle_change_y = 0u16;
            let mut angle_change_z = 0u16;

            // Item id
            match actor_param1 & 0x1FF {
                // Rupees
                2 | 3 | 4 | 32 | 33 | 34 => h_offset = 20.0,
                // Progressive Sword
                9..=14 => {
                    h_offset = 7.0;
                    angle_change_x = 0xD900;
                    angle_change_y = 0xF400;
                    angle_change_z = 0xF600;
                },
                // Goddess's Harp | All Songs
                16 | 186..=193 => {
                    h_offset = 17.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x2500;
                    angle_change_z = 0x0800;
                },
                // Progressive Bow
                19 | 90 | 91 => h_offset = 17.0,
                // Clawshots
                20 => {
                    h_offset = 25.0;
                    angle_change_x = 0x0500;
                    angle_change_y = 0x2400;
                },
                // Spiral Charge
                21 => {
                    h_offset = 27.0;
                    angle_change_y = 0x3000;
                    angle_change_z = 0x0300;
                },
                // AC BK
                25 => {
                    h_offset = 50.0;
                    angle_change_x = 0xEF00;
                },
                // FS BK | SV BK
                26 | 29 => h_offset = 40.0,
                // SSH BK
                27 => h_offset = 47.0,
                // Key Piece
                28 => {
                    h_offset = 10.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x2000;
                    angle_change_z = 0x0800;
                },
                // ET BK
                30 => h_offset = 60.0,
                // LMF BK | Small Seed Satchel | Whip
                31 | 128 | 137 => h_offset = 25.0,
                // Gratitude Crystal Pack | Single Crystal
                35 | 48 => h_offset = 28.0,
                // 5 Bombs | 10 Bombs
                40 | 41 => {
                    h_offset = 20.0;
                    angle_change_y = 0x1600;
                },
                // Gust Bellows
                49 => {
                    h_offset = 35.0;
                    angle_change_x = 0x1100;
                    angle_change_z = 0x2000;
                },
                // Progressive Slingshot
                52 | 105 => {
                    h_offset = 30.0;
                    angle_change_x = 0x1000;
                    angle_change_z = 0x1000;
                },
                // Progressive Beetle
                53 | 75..=77 => {
                    h_offset = 40.0;
                    angle_change_x = 0xE000;
                    angle_change_y = 0xCB00;
                    angle_change_z = 0xB000;
                },
                // Progressive Mitts
                56 | 99 => {
                    h_offset = 45.0;
                    angle_change_y = 0xE800;
                },
                // Water Dragon Scale | Sea Chart
                68 | 98 => h_offset = 15.0,
                // Bug Medal | Life Medal
                70 | 114 => {
                    h_offset = 15.0;
                    angle_change_x = 0x0A80;
                },
                // Progressive Bug Net
                71 | 140 => {
                    h_offset = 30.0;
                    angle_change_x = 0x1000;
                    angle_change_y = 0xE800;
                    angle_change_z = 0x2000;
                },
                // Bomb Bag
                92 => h_offset = 45.0,
                // Heart Container | Progressive Pouch | Life Tree Fruit
                93 | 112 | 113 | 198 => h_offset = 35.0,
                // Heart Piece
                94 => h_offset = 40.0,
                // Triforce Pieces
                95..=97 => h_offset = 75.0,
                // Heart Medal | Rupee Medal | Treasure Medal | Potion Medal | Cursed Medal
                100..=104 => {
                    h_offset = 15.0;
                    angle_change_y = 0x4000;
                    angle_change_z = 0x0A00;
                },
                36          // Glittering Spores
                | 54        // Bottle of Water
                | 55        // Mushroom Spores
                | 65        // Guardian Potion
                | 66        // Guardian Potion+
                | 74        // Sacred Water
                | 78        // Heart Potion
                | 79        // Heart Potion+
                | 81        // Heart Potion++
                | 84        // Stamina Potion
                | 85        // Stamina Potion+
                | 86        // Air Potion
                | 87        // Air Potion+
                | 88        // Fairy in a Bottle
                | 108..=111 // Wallets
                | 126       // Revitalizing Potion
                | 127       // Revitalizing Potion+
                | 153       // Empty Bottle
                | 163       // Tumbleweed
                | 194       // Revitalizing Potion++
                | 195       // Hot Pumpkin Soup
                | 196       // Cold Pumpkin Soup
                | 199 => h_offset = 20.0, // Extra Wallet
                // Wooden Shield | Hylian Shield
                116 | 125 => {
                    h_offset = 25.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x2400;
                    angle_change_z = 0x1000;
                },
                // Small Quiver
                131 => {
                    h_offset = 25.0;
                    angle_change_x = 0x1000;
                    angle_change_z = 0x1000;
                },
                // Small Bomb Bag
                134 => h_offset = 30.0,
                // Fireshield Earrings
                138 => h_offset = 20.0,
                // Cawlin's Letter
                158 => {
                    h_offset = 15.0;
                    angle_change_y = 0x2000;
                },
                // Beedle's Insect Cage
                159 => {
                    h_offset = 40.0;
                    angle_change_y = 0x2000;
                },
                // Rattle
                160 => {
                    h_offset = 25.0;
                    angle_change_y = 0xE000;
                },
                // Seeds | All Treasures
                57 | 60 | 63 | 64 | 165..=176 => h_offset = 25.0,
                // Tablets
                177..=179 => {
                    h_offset = 10.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x2000;
                    angle_change_z = 0x0800;
                },
                // Stone of Trials
                180 => {
                    h_offset = 20.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x2000;
                    angle_change_z = 0x0800;
                },
                // Small Keys
                1 | 200..=206 => {
                    h_offset = 5.0;
                    angle_change_x = 0x0C00;
                    angle_change_y = 0x1000;
                    angle_change_z = 0x0600;
                },
                // Maps
                50 | 207..=213 => {
                    h_offset = 30.0;
                    angle_change_x = 0x0800;
                    angle_change_y = 0x1000;
                    angle_change_z = 0x0800;
                },
                _ => h_offset = 0.0,
            }

            // Use trigonometry to figure out the horizontal offsets
            // Assume items are tilted on the x rotation and turned with the
            // y rotation to get whatever angle they have. If they're rotated with z
            // change it accordingly
            let mut facing_angle = item_rot.y;
            if facing_angle == 0 {
                facing_angle = 0 - item_rot.z;
                (*item_actor).base.members.base.rot.y = facing_angle;
                (*item_actor).base.members.base.rot.z = 0;
            }
            let facing_angle_radians: f32 = (facing_angle as f32 / 65535 as f32) * 2.0 * 3.14159;
            let xOffset = sinf(facing_angle_radians) * h_offset;
            let zOffset = cosf(facing_angle_radians) * h_offset;
            (*item_actor).base.members.base.pos.x += xOffset;
            (*item_actor).base.members.base.pos.z += zOffset;
            (*item_actor).base.members.base.rot.x = 0;
            (*item_actor).base.members.base.rot.x += angle_change_x;
            (*item_actor).base.members.base.rot.y += angle_change_y;
            (*item_actor).base.members.base.rot.z += angle_change_z;
        }
    }
}

#[no_mangle]
pub fn check_and_open_trial_gates(collected_item: flag::ITEMFLAGS) {
    unsafe {
        // Don't try to open any trial gates if the setting isn't on
        if RANDOMIZER_SETTINGS.skip_harp_playing == 0 {
            return;
        }

        // Return early if we aren't collecting any relevant items
        let relevant_items = [
            flag::ITEMFLAGS::GODDESS_HARP,
            flag::ITEMFLAGS::FARORE_COURAGE,
            flag::ITEMFLAGS::NAYRU_WISDOM,
            flag::ITEMFLAGS::DIN_POWER,
            flag::ITEMFLAGS::FARON_SONG_OF_THE_HERO_PART,
            flag::ITEMFLAGS::SONG_OF_THE_HERO,
        ];
        if !relevant_items.iter().any(|&item| item == collected_item) {
            return;
        }

        let mut open_trial_gate = false;
        // If we have the Goddess Harp and the appropriate song, set
        // the scene flag for the trial gate being open. If we're in
        // the scene index where the trial is, set the flag locally
        // and then try to find the trial gate actor and open it.
        if flag::check_itemflag(flag::ITEMFLAGS::GODDESS_HARP) == 1 {
            if flag::check_itemflag(flag::ITEMFLAGS::FARORE_COURAGE) == 1 {
                if (*SCENEFLAG_MGR).sceneindex == 1 {
                    flag::set_local_sceneflag(17);
                    open_trial_gate = true;
                } else {
                    flag::set_global_sceneflag(1, 17);
                }
            }
            if flag::check_itemflag(flag::ITEMFLAGS::NAYRU_WISDOM) == 1 {
                if (*SCENEFLAG_MGR).sceneindex == 7 {
                    flag::set_local_sceneflag(91);
                    open_trial_gate = true;
                } else {
                    flag::set_global_sceneflag(7, 91);
                }
            }
            if flag::check_itemflag(flag::ITEMFLAGS::DIN_POWER) == 1 {
                if (*SCENEFLAG_MGR).sceneindex == 4 {
                    flag::set_local_sceneflag(70);
                    open_trial_gate = true;
                } else {
                    flag::set_global_sceneflag(4, 70);
                }
            }
            if flag::check_itemflag(flag::ITEMFLAGS::SONG_OF_THE_HERO) == 1 {
                if (*SCENEFLAG_MGR).sceneindex == 0 {
                    flag::set_local_sceneflag(69);
                    open_trial_gate = true;
                } else {
                    flag::set_global_sceneflag(0, 69);
                }
            }
        }

        // Open the trial gate if we're potentially on the same stage as the one that
        // we're opening
        if open_trial_gate {
            // Try to find the trial gate actor
            let mut trial_gate_actor =
                actor::find_actor_by_type(actor::ACTORID::OBJ_WARP, core::ptr::null_mut())
                    as *mut actor::dAcOWarp;
            // If it exists, change it's state to open
            if trial_gate_actor != core::ptr::null_mut() {
                ((*(*trial_gate_actor).state_mgr.vtable).change_state)(
                    &mut (*trial_gate_actor).state_mgr as *mut actor::StateMgr,
                    &mut dAcOWarp__StateGateOpen as *mut c_void,
                );
            }
        }
    }
}

#[no_mangle]
pub fn after_item_collection_hook(collected_item: flag::ITEMFLAGS) -> flag::ITEMFLAGS {
    unsafe {
        fix::fix_ammo_counts(collected_item);
        check_and_open_trial_gates(collected_item);

        // Replaced code
        asm!("mov w8, {0:w}", in(reg) ((collected_item as u16) - 2));

        return collected_item;
    }
}

#[no_mangle]
pub fn resolve_progressive_item_models(model_name: *const c_char, item_id: u16) -> *const c_char {
    unsafe {
        match item_id {
            // Progressive Bow
            19 => {
                if flag::check_itemflag(flag::ITEMFLAGS::BOW) == 0 {
                    return cstr!("GetBowA").as_ptr();
                }
                if flag::check_itemflag(flag::ITEMFLAGS::IRON_BOW) == 0 {
                    return cstr!("GetBowB").as_ptr();
                }
                return cstr!("GetBowC").as_ptr();
            },
            // Progressive Slingshot
            52 => {
                if flag::check_itemflag(flag::ITEMFLAGS::SLINGSHOT) == 0 {
                    return cstr!("GetPachinkoA").as_ptr();
                }
                return cstr!("GetPachinkoB").as_ptr();
            },
            // Progressive Beetle
            53 => {
                if flag::check_itemflag(flag::ITEMFLAGS::BEETLE) == 0 {
                    return cstr!("GetBeetleA").as_ptr();
                }
                if flag::check_itemflag(flag::ITEMFLAGS::HOOK_BEETLE) == 0 {
                    return cstr!("GetBeetleB").as_ptr();
                }
                if flag::check_itemflag(flag::ITEMFLAGS::QUICK_BEETLE) == 0 {
                    return cstr!("GetBeetleC").as_ptr();
                }
                return cstr!("GetBeetleD").as_ptr();
            },
            // Progressive Mitts
            56 => {
                if flag::check_itemflag(flag::ITEMFLAGS::DIGGING_MITTS) == 0 {
                    return cstr!("GetMoleGloveA").as_ptr();
                }
                return cstr!("GetMoleGloveB").as_ptr();
            },
            // Progressive Bug Net
            71 => {
                if flag::check_itemflag(flag::ITEMFLAGS::BUG_NET) == 0 {
                    return cstr!("GetNetA").as_ptr();
                }
                return cstr!("GetNetB").as_ptr();
            },
            // Progressive Wallet
            108 => {
                if flag::check_itemflag(flag::ITEMFLAGS::MEDIUM_WALLET) == 0 {
                    return cstr!("GetPurseB").as_ptr();
                }
                if flag::check_itemflag(flag::ITEMFLAGS::BIG_WALLET) == 0 {
                    return cstr!("GetPurseC").as_ptr();
                }
                if flag::check_itemflag(flag::ITEMFLAGS::GIANT_WALLET) == 0 {
                    return cstr!("GetPurseD").as_ptr();
                }
                return cstr!("GetPurseE").as_ptr();
            },
            _ => {
                return model_name;
            },
        }
    }
}

#[no_mangle]
pub fn get_arc_model_from_item(
    arc_table: *mut c_void,
    model_name: *const c_char,
    item_id: u16,
) -> u64 {
    unsafe {
        let initial_model_name = match item_id {
            214 => cstr!("Onp").as_ptr(),
            215 => cstr!("DesertRobot").as_ptr(),
            _ => model_name,
        };

        let resolved_model_name = resolve_progressive_item_models(initial_model_name, item_id);

        return getArcModelFromName(
            arc_table,
            resolved_model_name,
            cstr!("g3d/model.brres").as_ptr(),
        );
    }
}

#[no_mangle]
pub fn get_item_model_name_ptr(model_name: *const c_char, item_id: u16) -> *const c_char {
    unsafe {
        let initial_model_name = match item_id {
            214 => cstr!("OnpB").as_ptr(),
            215 => cstr!("DesertRobot").as_ptr(),
            _ => model_name,
        };

        let resolved_model_name = resolve_progressive_item_models(initial_model_name, item_id);

        // Replaced code
        asm!("mov x1, {0:x}", in(reg) item_id);
        asm!("cmp x1, #0x1C");

        return resolved_model_name;
    }
}

#[no_mangle]
pub fn change_model_scale(item_actor: *mut dAcItem, world_matrix: *const c_void) {
    unsafe {
        let mut scale = match (*item_actor).final_determined_itemid {
            214 => 0.5f32, // Tadtone
            215 => 0.3f32, // Scrapper
            _ => 1.0f32,
        };

        // Hacky fix for treasures being really smol
        // The y_offsets here aren't in the same scale as
        let mut multiplier = 1.0;

        let itemid = (*item_actor).final_determined_itemid;
        match itemid {
            // Bird Feather, Tumbleweed, Amber Relic, Dusk Relic, Blue Bird Feather, Goddess Plume
            162 | 163 | 167 | 168 | 174 | 176 => {
                multiplier = 2.0;
            },
            // Ancient Flower
            166 => {
                multiplier = 1.5;
            },
            _ => {},
        };

        if ((*item_actor).base.members.base.param2 >> 4) & 0xF == 0xF {
            if (*item_actor).freestanding_y_offset <= 20.0 {
                (*item_actor).freestanding_y_offset *= multiplier;
            }
            scale *= multiplier;
        }

        (*item_actor).base.members.base.scale.x *= scale;
        (*item_actor).base.members.base.scale.y *= scale;
        (*item_actor).base.members.base.scale.z *= scale;

        // Replaced code
        ((*(*(*item_actor).item_model_ptr).vtable).set_local_matrix)(
            (*item_actor).item_model_ptr,
            world_matrix,
        );
    }
}
