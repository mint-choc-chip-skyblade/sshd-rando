#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::flag;
use crate::math;
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

// Core actor stuff
// ActorObjectBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBase {
    pub vtable:   *mut ActorObjectBasevtable,
    pub basebase: ActorBaseBasemembers,
    pub members:  ActorObjectBasemembers,
}
assert_eq_size!([u8; 0x410], ActorObjectBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBasevtable {
    pub base:                      ActorBasevtable,
    pub get_actor_list_element:    extern "C" fn() -> u64,
    pub can_be_linked_to_wood_tag: extern "C" fn() -> bool,
    pub do_drop:                   extern "C" fn() -> bool,
}
assert_eq_size!([u8; 0xF8], ActorObjectBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBasemembers {
    pub base:               ActorBasemembers,
    pub y_offset_maybe:     f32,
    pub _0:                 [u8; 20],
    pub target_fi_text_id1: u32,
    pub target_fi_text_id2: u32,
    pub pos_copy1:          math::Vec3f,
    pub pos_copy2:          math::Vec3f,
    pub pos_copy3:          math::Vec3f,
    pub rot_copy:           math::Vec3s,
    pub _1:                 u16,
    pub forward_speed:      f32,
    pub gravity_accel:      f32,
    pub gravity:            f32,
    pub velocity:           math::Vec3f,
    pub world_matrix:       [u8; 0x30],
    pub bounding_box:       [u8; 0x18],
    pub culling_distance:   f32,
    pub aabb_addon:         f32,
    pub object_actor_flags: u32,
    pub _2:                 f32,
    pub _3:                 [u8; 4],
    pub _4:                 f32,
    pub _5:                 [u8; 28],
    pub some_pos_copy:      math::Vec3f,
    pub _6:                 [u8; 12],
    pub _7:                 math::Vec3f,
    pub _8:                 [u8; 12],
    pub starting_pos:       math::Vec3f,
    pub starting_angle:     math::Vec3s,
    pub _9:                 [u8; 6],
    pub actor_carry:        [u8; 0xCC],
    pub _10:                [u8; 0x8C],
}
assert_eq_size!([u8; 0x348], ActorObjectBasemembers);

// ActorBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBase {
    pub vtable:  *mut ActorBasevtable,
    pub base:    ActorBaseBasemembers,
    pub members: ActorBasemembers,
}
assert_eq_size!([u8; 0x190], ActorBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBasevtable {
    pub base:                    ActorBaseBasevtable,
    pub actor_init1:             extern "C" fn(*mut ActorObjectBase),
    pub actor_init2:             extern "C" fn(*mut ActorObjectBase),
    pub actor_update:            extern "C" fn(*mut ActorObjectBase),
    pub actor_update_in_event:   extern "C" fn(*mut ActorObjectBase),
    pub _0:                      extern "C" fn(*mut ActorObjectBase),
    pub _1:                      extern "C" fn(*mut ActorObjectBase),
    pub copy_pos_rot:            extern "C" fn(*mut ActorObjectBase),
    pub get_current_actor_event: extern "C" fn(*mut ActorObjectBase) -> u32,
    pub update_actor_properties: extern "C" fn(*mut ActorObjectBase),
    pub perform_interaction:     extern "C" fn(*mut ActorObjectBase),
}
assert_eq_size!([u8; 0xE0], ActorBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBasemembers {
    pub base_properties:  u64,
    pub _0:               [u8; 22],
    pub obj_name_ptr:     u64,
    pub _1:               [u8; 34],
    pub sound_mgr:        u64,
    pub sound_pos_ptr:    *mut math::Vec3f,
    pub pos_copy:         math::Vec3f,
    pub param2:           u32,
    pub rot_copy:         math::Vec3s,
    pub _2:               u16,
    pub room_id_copy:     u8,
    pub _3:               u8,
    pub subtype:          u8,
    pub _4:               u8,
    pub rot:              math::Vec3s,
    pub _5:               u16,
    pub pos:              math::Vec3f,
    pub scale:            math::Vec3f,
    pub actor_properties: u32,
    pub _6:               [u8; 28],
    pub roomid:           u8,
    pub actor_sub_type:   u8,
    pub _7:               [u8; 18],
}
assert_eq_size!([u8; 0xC8], ActorBasemembers);

// ActorBaseBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBase {
    pub vtable:          *mut ActorBaseBasevtable,
    pub members:         ActorBaseBasemembers,
    pub base_properties: u64,
}
assert_eq_size!([u8; 0xD0], ActorBaseBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBasevtable {
    pub init:                  extern "C" fn(*mut ActorBaseBase),
    pub pre_init:              extern "C" fn(*mut ActorBaseBase),
    pub post_init:             extern "C" fn(*mut ActorBaseBase),
    pub destroy:               extern "C" fn(*mut ActorBaseBase),
    pub pre_destroy:           extern "C" fn(*mut ActorBaseBase),
    pub post_destroy:          extern "C" fn(*mut ActorBaseBase),
    pub base_update:           extern "C" fn(*mut ActorBaseBase),
    pub pre_update:            extern "C" fn(*mut ActorBaseBase),
    pub post_update:           extern "C" fn(*mut ActorBaseBase),
    pub draw:                  extern "C" fn(*mut ActorBaseBase),
    pub pre_draw:              extern "C" fn(*mut ActorBaseBase),
    pub post_draw:             extern "C" fn(*mut ActorBaseBase),
    pub delete_ready:          extern "C" fn(*mut ActorBaseBase),
    pub create_heap:           extern "C" fn(*mut ActorBaseBase),
    pub create_heap2:          extern "C" fn(*mut ActorBaseBase),
    pub init_models:           extern "C" fn(*mut ActorBaseBase),
    pub dtor:                  extern "C" fn(*mut ActorBaseBase),
    pub dtor_with_actor_heaps: extern "C" fn(*mut ActorBaseBase),
}
assert_eq_size!([u8; 0x90], ActorBaseBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBasemembers {
    pub members: ActorBaseBasemembersnovtable,
    pub vtable:  *mut ActorBaseBasevtable,
}
assert_eq_size!([u8; 0xC0], ActorBaseBasemembers);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBasemembersnovtable {
    pub unique_actor_index:      u32,
    pub param1:                  u32,
    pub actorid:                 u16,
    pub life_cycle:              u8,
    pub signal_for_init:         bool,
    pub signal_for_delete:       bool,
    pub signal_for_retry_create: bool,
    pub group_type:              u8,
    pub proc_control:            u8,
    pub actor_mgr:               [u8; 0x80],
    pub _0:                      u64,
    pub actor_list_mgr:          [u8; 0x10],
    pub heap:                    u64,
    pub base_properties:         u32,
    pub _1:                      u32,
}
assert_eq_size!([u8; 0xB8], ActorBaseBasemembersnovtable);

// Actors
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcItem {
    pub base:                    ActorObjectBase,
    pub itemid:                  u16,
    pub _0:                      [u8; 6],
    pub item_model_ptr:          u64,
    pub _1:                      [u8; 2784],
    pub actor_list_element:      u32,
    pub _2:                      [u8; 816],
    pub freestanding_y_offset:   f32,
    pub _3:                      [u8; 44],
    pub final_determined_itemid: u16,
    pub _4:                      [u8; 10],
    pub prevent_drop:            u8,
    pub _5:                      [u8; 3],
    pub no_longer_waiting:       u8,
    pub _6:                      [u8; 19],
}
assert_eq_size!([u8; 4744], dAcItem);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOlightLine {
    pub base:                  ActorObjectBase,
    pub _0:                    [u8; 0x989],
    pub light_shaft_activated: bool,
    pub _1:                    [u8; 6],
    pub light_shaft_index:     u32,
    pub _2:                    [u8; 4],
}
assert_eq_size!([u8; 0xDA8], dAcOlightLine);

// Stage stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dStageMgr {
    pub _0:                               [u8; 0x1000C],
    pub set_in_actually_trigger_entrance: u8,
    pub _1:                               [u8; 11],
}
assert_eq_size!([u8; 0x10018], dStageMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct GameReloader {
    pub _0:                       [u8; 0x350],
    pub reload_trigger:           u16,
    pub _1:                       [u8; 0x52],
    pub speed_after_reload:       f32,
    pub stamina_after_reload:     u32,
    pub item_to_use_after_reload: u8,
    pub beedle_shop_spawn_state:  u8,
    pub action_index:             u16,
    pub area_type:                u8,
    pub _2:                       [u8; 0x5],
    pub is_reloading:             u8,
    pub prevent_set_respawn_info: u8,
    pub count_down_after_spawn:   u8,
}
assert_eq_size!([u8; 0x3B9], GameReloader);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut savefile::FileMgr;
    static DUNGEONFLAG_MGR: *mut flag::DungeonflagMgr;
    static mut STATIC_DUNGEONFLAGS: [u16; 8];
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
#[no_mangle]
pub fn fix_freestanding_item_y_offset() {
    unsafe {
        let mut item_actor: *mut dAcItem;
        asm!("mov {0}, x19", out(reg) item_actor);

        let actor_param1 = (*item_actor).base.basebase.members.param1;

        if (actor_param1 >> 9) & 0x1 == 0 {
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

            (*item_actor).freestanding_y_offset = y_offset;

            if use_default_scaling {
                (*item_actor).base.members.base.rot.y |= 1;
            } else {
                (*item_actor).base.members.base.rot.y &= 0xFFFE;
            }
        }

        // Replaced instruction
        asm!("mov w0, w20");
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

        return (*item_actor).final_determined_itemid;
    }
}
