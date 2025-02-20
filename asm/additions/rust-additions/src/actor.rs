#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::flag;
use crate::math;
use crate::rng;
use crate::savefile;

use core::arch::asm;
use core::ffi::{c_char, c_void};
use core::ptr::from_ref;
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

// Core actor stuff
// dAcOBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOBase {
    pub vtable:   *mut dAcOBasevtable,
    pub basebase: dBasemembers,
    pub members:  dAcOBasemembers,
}
assert_eq_size!([u8; 0x410], dAcOBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOBasevtable {
    pub base:                      dAcBasevtable,
    pub get_actor_list_element:    extern "C" fn() -> u64,
    pub can_be_linked_to_wood_tag: extern "C" fn() -> bool,
    pub do_drop:                   extern "C" fn() -> bool,
}
assert_eq_size!([u8; 0xF8], dAcOBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOBasemembers {
    pub base:               dAcBasemembers,
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
assert_eq_size!([u8; 0x348], dAcOBasemembers);

// dAcBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcBase {
    pub vtable:  *mut dAcBasevtable,
    pub base:    dBasemembers,
    pub members: dAcBasemembers,
}
assert_eq_size!([u8; 0x190], dAcBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcBasevtable {
    pub base:                    dBasevtable,
    pub actor_init1:             extern "C" fn(*mut dAcOBase),
    pub actor_init2:             extern "C" fn(*mut dAcOBase),
    pub actor_update:            extern "C" fn(*mut dAcOBase),
    pub actor_update_in_event:   extern "C" fn(*mut dAcOBase),
    pub _0:                      extern "C" fn(*mut dAcOBase),
    pub _1:                      extern "C" fn(*mut dAcOBase),
    pub copy_pos_rot:            extern "C" fn(*mut dAcOBase),
    pub get_current_actor_event: extern "C" fn(*mut dAcOBase) -> u32,
    pub update_actor_properties: extern "C" fn(*mut dAcOBase),
    pub perform_interaction:     extern "C" fn(*mut dAcOBase),
}
assert_eq_size!([u8; 0xE0], dAcBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcBasemembers {
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
assert_eq_size!([u8; 0xC8], dAcBasemembers);

// dBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dBase {
    pub vtable:          *mut dBasevtable,
    pub members:         dBasemembers,
    pub base_properties: u64,
}
assert_eq_size!([u8; 0xD0], dBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dBasevtable {
    pub init:                  extern "C" fn(*mut dBase),
    pub pre_init:              extern "C" fn(*mut dBase),
    pub post_init:             extern "C" fn(*mut dBase),
    pub destroy:               extern "C" fn(*mut dBase),
    pub pre_destroy:           extern "C" fn(*mut dBase),
    pub post_destroy:          extern "C" fn(*mut dBase),
    pub base_update:           extern "C" fn(*mut dBase),
    pub pre_update:            extern "C" fn(*mut dBase),
    pub post_update:           extern "C" fn(*mut dBase),
    pub draw:                  extern "C" fn(*mut dBase),
    pub pre_draw:              extern "C" fn(*mut dBase),
    pub post_draw:             extern "C" fn(*mut dBase),
    pub delete_ready:          extern "C" fn(*mut dBase),
    pub create_heap:           extern "C" fn(*mut dBase),
    pub create_heap2:          extern "C" fn(*mut dBase),
    pub init_models:           extern "C" fn(*mut dBase),
    pub dtor:                  extern "C" fn(*mut dBase),
    pub dtor_with_actor_heaps: extern "C" fn(*mut dBase),
}
assert_eq_size!([u8; 0x90], dBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dBasemembers {
    pub members: dBasemembersnovtable,
    pub vtable:  *mut dBasevtable,
}
assert_eq_size!([u8; 0xC0], dBasemembers);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dBasemembersnovtable {
    pub unique_actor_index:      u32,
    pub param1:                  u32,
    pub actorid:                 u16,
    pub life_cycle:              u8,
    pub signal_for_init:         bool,
    pub signal_for_delete:       bool,
    pub signal_for_retry_create: bool,
    pub group_type:              u8,
    pub proc_control:            u8,
    pub actor_mgr:               ActorMgr,
    pub _0:                      u64,
    pub actor_list_mgr:          [u8; 0x10],
    pub heap:                    u64,
    pub base_properties:         u32,
    pub _1:                      u32,
}
assert_eq_size!([u8; 0xB8], dBasemembersnovtable);

// ActorMgr stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorMgr {
    pub connect_node: ActorTreeNode,
    pub execute_node: ActorPriorityListNode,
    pub draw_node:    ActorPriorityListNode,
    pub search_node:  ActorListNode,
}
assert_eq_size!([u8; 0x80], ActorMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorTreeNode {
    pub tree_node: TreeNode,
    pub owner:     *mut dBase,
}
assert_eq_size!([u8; 0x28], ActorTreeNode);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct TreeNode {
    pub parent: *mut TreeNode,
    pub child:  *mut TreeNode,
    pub prev:   *mut TreeNode,
    pub next:   *mut TreeNode,
}
assert_eq_size!([u8; 0x20], TreeNode);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorPriorityListNode {
    pub node:      ActorListNode,
    pub order:     u16,
    pub new_order: u16,
    pub _0:        [u8; 4],
}
assert_eq_size!([u8; 0x20], ActorPriorityListNode);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorListNode {
    pub list_node: ListLink,
    pub owner:     *mut dAcBase,
}
assert_eq_size!([u8; 0x18], ActorListNode);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ListLink {
    pub prev: *mut ListLink,
    pub next: *mut ListLink,
}
assert_eq_size!([u8; 0x10], ListLink);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorTreeProcess {
    pub root:    *mut ActorTreeNode,
    pub prepare: [u8; 16], // TODO
}
assert_eq_size!([u8; 0x18], ActorTreeProcess);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct StateMgr__vtable {
    pub unk:                   u64,
    pub dtor:                  u64,
    pub initialize_state:      u64,
    pub execute_state:         u64,
    pub finalize_state:        u64,
    pub change_state:          extern "C" fn(*mut StateMgr, *mut c_void),
    pub refresh_state:         u64,
    pub get_state:             extern "C" fn(*mut StateMgr) -> *const c_void,
    pub get_new_state_id:      u64,
    pub get_current_state_id:  extern "C" fn(*mut StateMgr) -> i32,
    pub get_previous_state_id: u64,
}
assert_eq_size!([u8; 0x58], StateMgr__vtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct StateMgr {
    pub vtable:          *mut StateMgr__vtable,
    pub checker:         extern "C" fn(),
    pub factory:         extern "C" fn(),
    pub state_functions: u64,
    pub actor_reference: *mut dBase,
    pub current_state:   *mut ActorState,
    pub state_method:    [u8; 0x40],
}
assert_eq_size!([u8; 0x70], StateMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorState {
    pub vtable:       *mut ActorState__vtable,
    pub name:         *mut c_char,
    pub number:       u32,
    pub _0:           u32,
    pub state_enter:  [u8; 0x10], // ptmf
    pub state_update: [u8; 0x10], // ptmf
    pub state_leave:  [u8; 0x10], // ptmf
}
assert_eq_size!([u8; 0x48], ActorState);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorState__vtable {
    pub _0:                u64,
    pub dtor:              extern "C" fn(*mut ActorState),
    pub is_null:           extern "C" fn(*mut ActorState) -> bool,
    pub is_equal:          extern "C" fn(*mut ActorState, *mut ActorState) -> bool,
    pub operator_eq:       extern "C" fn(*mut ActorState, *mut ActorState) -> u32,
    pub operator_not_eq:   extern "C" fn(*mut ActorState, *mut ActorState) -> u32,
    pub is_same_name:      extern "C" fn(*mut ActorState, *mut ActorState) -> u32, /* return type guess */
    pub get_state_name:    extern "C" fn(*mut ActorState) -> *const c_char,
    pub get_state_number:  extern "C" fn(*mut ActorState) -> u32,
    pub call_enter_state:  extern "C" fn(),
    pub call_update_state: extern "C" fn(),
    pub call_leave_state:  extern "C" fn(),
}
assert_eq_size!([u8; 0x60], ActorState__vtable);

// Actors
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOlightLine {
    pub base:                  dAcOBase,
    pub _0:                    [u8; 0x989],
    pub light_shaft_activated: bool,
    pub _1:                    [u8; 6],
    pub light_shaft_index:     u32,
    pub _2:                    [u8; 4],
}
assert_eq_size!([u8; 0xDA8], dAcOlightLine);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOSwSwordBeam {
    pub base:                     dAcOBase,
    pub _0:                       [u8; 0xB90],
    pub state_mgr:                [u8; 0x70],
    pub _1:                       [u8; 0x4C],
    pub subtype:                  u8,
    pub sceneflag:                u8,
    pub _2:                       [u8; 3],
    pub spawned_from_other_actor: u8,
    pub _3:                       [u8; 6],
    pub cs_exitid:                i32,
    pub _4:                       [u8; 4],
}
assert_eq_size!([u8; 0x1070], dAcOSwSwordBeam);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcORockBoatMaybe {
    pub _0:            [u8; 0x4],
    pub param1:        u32,
    pub _1:            [u8; 0x1F8],
    pub spawnCooldown: u32,
    // TODO
}
assert_eq_size!([u8; 0x204], dAcORockBoatMaybe);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOWarp {
    pub base:                dAcOBase,
    pub _0:                  [u8; 0xAD8],
    pub state_mgr:           StateMgr,
    pub _1:                  [u8; 0x2EE],
    pub trial_index_bitmask: u8,
    pub _2:                  [u8; 0x15],
    pub trial_index:         u8,
    pub _3:                  [u8; 3],
    // TODO
}
assert_eq_size!([u8; 0x1260], dAcOWarp);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcObell {
    pub base:        dAcOBase,
    pub _0:          [u8; 0x450],
    pub field_0x860: u8,
    // TODO
}
assert_eq_size!([u8; 0x861], dAcObell);

// Tadtone
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOClef {
    pub base: dAcOBase,
    pub _0:   [u8; 0x5C8],
}
assert_eq_size!([u8; 0x9D8], dAcOClef);

// Tags
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dTgMusasabi {
    pub base:                      dAcBase,
    pub matrix1:                   math::Matrix,
    pub matrix2:                   math::Matrix,
    pub squirrel_count:            u8,
    pub unused:                    u8,
    pub some_countdown:            i16,
    pub param1_rshift4:            u16,
    pub has_spawned_squirrels:     bool,
    pub has_spawned_squirrels_LOD: bool,
}
assert_eq_size!([u8; 0x1F8], dTgMusasabi);

// Tadtone Minigame
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dTgClefGame {
    pub base:                        dAcBase,
    pub _0:                          [u8; 0x9B],
    pub delay_before_starting_event: u8,
    pub _1:                          [u8; 0x4],
}
assert_eq_size!([u8; 0x230], dTgClefGame);

// NPCs
// TODO: dAcOrdinaryNpc

// Fledge during Pumpkin Archery
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcNpcPcs {
    pub _0:                    [u8; 0x1650],
    pub pumpkin_archery_timer: u64,
    pub _1:                    [u8; 0x58],
}
assert_eq_size!([u8; 0x16B0], dAcNpcPcs);

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
pub struct RoomMgr {
    pub base:         dBase,
    pub _0:           [u8; 24],
    pub _1:           u64,
    pub roomPointers: [u64; 63], // actually [*mut Room; 63]
    pub _2:           [u8; 0x228C],
    pub roomid:       u8,
    pub _3:           [u8; 3],
}
assert_eq_size!([u8; 0x2578], RoomMgr);

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

#[repr(u16)]
#[derive(Copy, Clone, Hash, PartialEq, Eq)]
pub enum ACTORID {
    TITLE                         = 0x0,
    E3_TITLE                      = 0x1,
    E3_GAMEEND                    = 0x2,
    THPPLAYER                     = 0x3,
    GAME                          = 0x4,
    STAGE_MANAGER                 = 0x5,
    STAGE                         = 0x6,
    STAGE_SELECT                  = 0x7,
    VIEW_CLIP_TAG                 = 0x8,
    START_TAG                     = 0x9,
    MAP_AREA_TAG                  = 0xA,
    TRUCK_RAIL                    = 0xB,
    TAG_STREAM                    = 0xC,
    COL_BOMSLD                    = 0xD,
    OBJ_STAGE_KRAKEN              = 0xE,
    OBJ_STAGE_KRAKEN_PARTS        = 0xF,
    OBJ_TIME_STONE                = 0x10,
    OBJ_SW                        = 0x11,
    OBJ_BLOCK_ROPE                = 0x12,
    OBJ_PUSH_BLOCK                = 0x13,
    OBJ_KIBAKO                    = 0x14,
    OBJ_LOG                       = 0x15,
    OBJ_LOG_WATER                 = 0x16,
    OBJ_BELT_CVR                  = 0x17,
    OBJ_DRUM                      = 0x18,
    OBJ_BELT_OBSTACLE             = 0x19,
    OBJ_HIMO                      = 0x1A,
    OBJ_SPIDER_LINE               = 0x1B,
    OBJ_WIND                      = 0x1C,
    OBJ_WIND03                    = 0x1D,
    OBJ_WIND04                    = 0x1E,
    OBJ_TORNADO                   = 0x1F,
    OBJ_SWITCH_WALL               = 0x20,
    OBJ_TOWER_D101                = 0x21,
    OBJ_DOOR_DUNGEON_D200         = 0x22,
    OBJ_DOOR_DUNGEON              = 0x23,
    OBJ_WOOD_BOARD                = 0x24,
    OBJ_CLAW_SHOT_TG              = 0x25,
    OBJ_BULB_SWITCH               = 0x26,
    OBJ_SIDE_SHUTTER              = 0x27,
    OBJ_HIT_LEVER_SW              = 0x28,
    OBJ_FENCE_IRON                = 0x29,
    OBJ_UPDOWN_LAVA               = 0x2A,
    OBJ_BB_OBJECTS                = 0x2B,
    OBJ_BRIDGE_BUILDING           = 0x2C,
    OBJ_CANNON                    = 0x2D,
    OBJ_ROULETTE_ISLAND_C         = 0x2E,
    OBJ_ROULETTE_ISLAND_R         = 0x2F,
    OBJ_BRIDGE_STRETCH            = 0x30,
    OBJ_IRON_STAGE                = 0x31,
    OBJ_UTAJIMA_STOPPER           = 0x32,
    OBJ_UTAJIMA_MAIN_MECHA        = 0x33,
    OBJ_UTAJIMA_PEDESTAL          = 0x34,
    OBJ_UTAJIMA_ISLAND            = 0x35,
    OBJ_CANNON_COVER              = 0x36,
    OBJ_UTAJIMA                   = 0x37,
    OBJ_UTAJIMA_LV2               = 0x38,
    OBJ_PUZZLE_ISLAND             = 0x39,
    OBJ_FENCE_BOKO                = 0x3A,
    OBJ_FENCE_BOKO2               = 0x3B,
    OBJ_WINDMILL                  = 0x3C,
    OBJ_PINWHEEL                  = 0x3D,
    OBJ_LIGHTHOUSE_HARP           = 0x3E,
    OBJ_FENCE_KONSAI              = 0x3F,
    OBJ_STAGE_SINK                = 0x40,
    OBJ_STAGE_WATER               = 0x41,
    OBJ_STAGE_COVER               = 0x42,
    OBJ_STAGE_CRACK               = 0x43,
    OBJ_TERRY_ISLAND              = 0x44,
    OBJ_INSECT_ISLAND             = 0x45,
    OBJ_SHRINE_AFTER              = 0x46,
    OBJ_SHRINE_BEFORE             = 0x47,
    OBJ_SHIP_WINDOW               = 0x48,
    OBJ_WATER_SURFACE             = 0x49,
    OBJ_PUMPKIN_BAR               = 0x4A,
    OBJ_TREASURE_ISLAND           = 0x4B,
    OBJ_SEALED_DOOR               = 0x4C,
    OBJ_EVIL_FIELD                = 0x4D,
    OBJ_MEGAMI_ISLAND             = 0x4E,
    OBJ_CITY                      = 0x4F,
    OBJ_BAMBOO_ISLAND             = 0x50,
    OBJ_STREAM_LAVA               = 0x51,
    OBJ_DOWN_LAVA                 = 0x52,
    OBJ_APPEAR_BRIDGE             = 0x53,
    OBJ_TRUCK_STOPPER             = 0x54,
    OBJ_ISLAND_NUSI               = 0x55,
    OBJ_ROCK_SKY                  = 0x56,
    OBJ_TREASURE_ISLAND_B         = 0x57,
    OBJ_WATER_F100                = 0x58,
    OBJ_BELL                      = 0x59,
    OBJ_SHRINE_BEF_INSIDE         = 0x5A,
    OBJ_WINDMILL_DESERT           = 0x5B,
    OBJ_CITY_WATER                = 0x5C,
    OBJ_MOLE_COVER                = 0x5D,
    OBJ_DESERT_DEBRIS             = 0x5E,
    OBJ_BB_BROKEN_PARTS           = 0x5F,
    OBJ_KUMITE_WALL               = 0x60,
    OBJ_WATER_SHIELD              = 0x61,
    OBJ_BSTONE                    = 0x62,
    OBJ_WIND02                    = 0x63,
    OBJ_LEAF_SWING                = 0x64,
    RIDE_ROCK_SET_TAG             = 0x65,
    OBJ_RIDE_ROCK                 = 0x66,
    OBJ_MOVE_LIFT_VOL             = 0x67,
    OBJ_TRUCK                     = 0x68,
    OBJ_TERRY_SHOP                = 0x69,
    OBJ_TRAP_ROCK_1               = 0x6A,
    OBJ_STOPPER_ROCK              = 0x6B,
    OBJ_SHUTTER_FENCE             = 0x6C,
    OBJ_SINK_FLOOR_F              = 0x6D,
    E_GUMARM                      = 0x6E,
    OBJ_STEP_GUMARM               = 0x6F,
    OBJ_BRIDGE_FALL               = 0x70,
    OBJ_BRIDGE_STEP               = 0x71,
    OBJ_BRIDGE_BONE               = 0x72,
    OBJ_BB_BRIDGE                 = 0x73,
    OBJ_BRIDGE_TIME               = 0x74,
    OBJ_BOAT                      = 0x75,
    OBJ_BALLISTA                  = 0x76,
    OBJ_BALLISTA_F3               = 0x77,
    OBJ_TIME_BOAT                 = 0x78,
    OBJ_GODDESS_STATUE            = 0x79,
    OBJ_STONE_STAND               = 0x7A,
    OBJ_TIME_STAGE_BG             = 0x7B,
    OBJ_WARP_HOLE                 = 0x7C,
    OBJ_GEAR                      = 0x7D,
    OBJ_DESERT                    = 0x7E,
    OBJ_D300                      = 0x7F,
    OBJ_SEA_F301                  = 0x80,
    OBJ_DESERT_AGO                = 0x81,
    OBJ_DESERT_METER              = 0x82,
    OBJ_NEEDLE_DESERT             = 0x83,
    OBJ_LOTUS                     = 0x84,
    OBJ_TARZAN_POLE               = 0x85,
    OBJ_STEP_TIME_SLIP            = 0x86,
    OBJ_TIME_BASE                 = 0x87,
    OBJ_SWITCH_SHUTTER            = 0x88,
    OBJ_WATERFALL_D101            = 0x89,
    OBJ_ROLL_PILLAR               = 0x8A,
    OBJ_CHEST                     = 0x8B,
    OBJ_ROCK_BOAT                 = 0x8C,
    OBJ_BLOCK_UNDERGROUND         = 0x8D,
    OBJ_UNDERGROUND               = 0x8E,
    OBJ_TROLLEY                   = 0x8F,
    OBJ_LAVA_PLATE                = 0x90,
    OBJ_SAND_FLOOR                = 0x91,
    OBJ_SW_SYAKO                  = 0x92,
    OBJ_SYAKO_SHUTTER             = 0x93,
    OBJ_DUNGEON_SHIP              = 0x94,
    OBJ_NEEDLE_UNDERGROUND        = 0x95,
    OBJ_STEP_STATUE               = 0x96,
    OBJ_GRAVE                     = 0x97,
    OBJ_SHED                      = 0x98,
    OBJ_GIRAHIMU_FLOOR            = 0x99,
    OBJ_TENIJIMA                  = 0x9A,
    OBJ_SAND_D301                 = 0x9B,
    OBJ_DOOR_BOSSD101             = 0x9C,
    OBJ_BOXCAGE_F300              = 0x9D,
    OBJ_TOWER_HAND_D101           = 0x9E,
    OBJ_DORMITORY_GATE            = 0x9F,
    OBJ_PISTON                    = 0xA0,
    OBJ_FRUIT_TREE                = 0xA1,
    OBJ_FARMLAND                  = 0xA2,
    OBJ_PROPELLER_LIFT            = 0xA3,
    OBJ_D3_DUMMY                  = 0xA4,
    B_BIGBOSS_BASE                = 0xA5,
    B_BIGBOSS                     = 0xA6,
    B_BIGBOSS2                    = 0xA7,
    B_BIGBOSS3                    = 0xA8,
    B_VD                          = 0xA9,
    OBJ_VDB                       = 0xAA,
    E_CAPTAIN                     = 0xAB,
    OBJ_TRUCK_RAIL_COL            = 0xAC,
    BIRD                          = 0xAD,
    BIRD_TARGET                   = 0xAE,
    BIRD_NPC                      = 0xAF,
    BIRD_KOBUNA                   = 0xB0,
    BIRD_KOBUNB                   = 0xB1,
    BIRD_RIVAL                    = 0xB2,
    BIRD_ZELDA_TRAINING           = 0xB3,
    AVATER_RACE_MNG               = 0xB4,
    AVATER_BULLET                 = 0xB5,
    NUSI_BASE                     = 0xB6,
    NUSI_NPC                      = 0xB7,
    B_NUSI                        = 0xB8,
    B_NUSI_TENTAKLE               = 0xB9,
    B_NUSI_BULLET                 = 0xBA,
    OBJ_LIGHT_LINE                = 0xBB,
    OBJ_LIGHT_SHAFT_SMALL         = 0xBC,
    TAG_LIGHT_SHAFT_EFF           = 0xBD,
    MEGAMI_DIVING_TAG             = 0xBE,
    COMMON_BULLET                 = 0xBF,
    E_SYAKOMAITO                  = 0xC0,
    E_MR                          = 0xC1,
    E_PH                          = 0xC2,
    B_KR                          = 0xC3,
    B_KRH                         = 0xC4,
    B_KRA                         = 0xC5,
    OBJ_FLYING_CLAWSHOT_TARGET    = 0xC6,
    OBJ_DIS_SHIP                  = 0xC7,
    PLAYER                        = 0xC8,
    TAG_SHUTTER_FENCE_PERMISSION  = 0xC9,
    SHUTTER                       = 0xCA,
    OBJ_SHUTTER_CHANGE_SCENE      = 0xCB,
    OBJ_DOOR_BOSS                 = 0xCC,
    OBJ_DOOR                      = 0xCD,
    OBJ_FENCE                     = 0xCE,
    TAG_SHUTTER_FENCE_FORBIDDANCE = 0xCF,
    OBJ_TROLLEY_SHUTTER           = 0xD0,
    OBJ_TR_SHUTTER_CS             = 0xD1,
    OBJ_BG                        = 0xD2,
    BOOMERANG                     = 0xD3,
    GENKI_MGR_TAG                 = 0xD4,
    TAG_MIECHAN                   = 0xD5,
    DEMO_NPC_BIRD                 = 0xD6,
    NPC_RVL                       = 0xD7,
    NPC_RIVAL_LOD                 = 0xD8,
    NPC_KBN                       = 0xD9,
    NPC_KBN2                      = 0xDA,
    NPC_KOBUN_B_NIGHT             = 0xDB,
    NPC_SKN                       = 0xDC,
    NPC_SKN2                      = 0xDD,
    NPC_GZL                       = 0xDE,
    NPC_ZLD                       = 0xDF,
    NPC_DSK                       = 0xE0,
    NPC_DRB                       = 0xE1,
    NPC_DRBC                      = 0xE2,
    NPC_CE_FRIEND                 = 0xE3,
    NPC_CE_LADY                   = 0xE4,
    NPC_TOILET_GHOST              = 0xE5,
    NPC_SORAJIMA_FATHER           = 0xE6,
    NPC_SORAJIMA_MOTHER           = 0xE7,
    NPC_SORAJIMA_GIRL             = 0xE8,
    NPC_KYUI_WIZARD               = 0xE9,
    NPC_KYUI_FIRST                = 0xEA,
    NPC_ORD_KYUI                  = 0xEB,
    NPC_KYUI_ELDER                = 0xEC,
    NPC_KYUI_THIRD                = 0xED,
    NPC_KYUI4                     = 0xEE,
    NPC_TMN                       = 0xEF,
    NPC_SALESMAN_S                = 0xF0,
    NPC_DOUGUYA_NIGHT             = 0xF1,
    NPC_MED_WIFE_NIGHT            = 0xF2,
    NPC_MED_HUS_NIGHT             = 0xF3,
    NPC_JUNK_NIGHT                = 0xF4,
    NPC_AZUKARIYA_NIGHT           = 0xF5,
    NPC_DOUGUYA_MOTHER            = 0xF6,
    NPC_DOUGUYA_MOTHER_LOD        = 0xF7,
    NPC_JUNK_MOTHER               = 0xF8,
    NPC_JUNK_MOTHER_LOD           = 0xF9,
    NPC_SENPAIA_MOTHER            = 0xFA,
    NPC_SENPAIA_MOTHER_LOD        = 0xFB,
    NPC_SORAJIMA_MAN_E            = 0xFC,
    NPC_SORAJIMA_MAN_D            = 0xFD,
    NPC_AZUKARIYA_FATHER          = 0xFE,
    NPC_DAISHINKAN_N              = 0xFF,
    NPC_SORAJIMA_MALE             = 0x100,
    NPC_BDSW                      = 0x101,
    NPC_SORAJIMA_FEMALE           = 0x102,
    NPC_KENSEI                    = 0x103,
    NPC_TALK_KENSEI               = 0x104,
    NPC_BDZ                       = 0x105,
    NPC_OIM                       = 0x106,
    NPC_YIM                       = 0x107,
    NPC_BGR                       = 0x108,
    NPC_SLTK                      = 0x109,
    NPC_SLB2                      = 0x10A,
    NPC_SMA3                      = 0x10B,
    NPC_SMA2                      = 0x10C,
    NPC_PMA                       = 0x10D,
    NPC_PDU                       = 0x10E,
    NPC_ICGK                      = 0x10F,
    NPC_PCS                       = 0x110,
    NPC_FDR                       = 0x111,
    NPC_TDR                       = 0x112,
    NPC_TDS                       = 0x113,
    NPC_TDRB                      = 0x114,
    TAG_SWORD_BATTLE_GAME         = 0x115,
    TAG_SIREN_TIME_ATTACK         = 0x116,
    NPC_ADR                       = 0x117,
    NPC_GHM                       = 0x118,
    NPC_SHA                       = 0x119,
    NPC_GRA                       = 0x11A,
    NPC_GRC                       = 0x11B,
    NPC_GRD                       = 0x11C,
    NPC_SORAJIMA_BOY              = 0x11D,
    NPC_AKUMAKUN                  = 0x11E,
    NPC_AKU_HUMAN                 = 0x11F,
    NPC_SUISEI                    = 0x120,
    NPC_SUISEI_SUB                = 0x121,
    NPC_SUISEI_NORMAL             = 0x122,
    MOLE_MGR_TAG                  = 0x123,
    NPC_MOLE_MG                   = 0x124,
    NPC_MOLE                      = 0x125,
    NPC_MOLE_NORMAL               = 0x126,
    NPC_MOLE_NORMAL2              = 0x127,
    NPC_MOLE_ES_NML               = 0x128,
    NPC_MOLE_TACKLE               = 0x129,
    NPC_MOLE_TACKLE2              = 0x12A,
    NPC_CHEF                      = 0x12B,
    NPC_SLFB                      = 0x12C,
    NPC_SLRP                      = 0x12D,
    NPC_SLFL                      = 0x12E,
    NPC_TERRY                     = 0x12F,
    NPC_DIVE_GAME_JUDGE           = 0x130,
    KNIGHT_LEADER_BIRD            = 0x131,
    NPC_KNIGHT_LEADER             = 0x132,
    NPC_SENPAI                    = 0x133,
    NPC_SENPAI_B                  = 0x134,
    NPC_REGRET_RIVAL              = 0x135,
    NPC_RESCUE                    = 0x136,
    NPC_SLB                       = 0x137,
    FLY_SLB                       = 0x138,
    OBJ_PROPERA                   = 0x139,
    OBJ_ROULETTE                  = 0x13A,
    NPC_MOLE_ELDER                = 0x13B,
    NPC_SALBAGE_MORRY             = 0x13C,
    NPC_MOLE_SAL                  = 0x13D,
    OBJ_POT_SAL                   = 0x13E,
    OBJ_MOLE_SOIL                 = 0x13F,
    LITTLE_BIRD_MGR               = 0x140,
    LITTLE_BIRD                   = 0x141,
    FISH_MGR                      = 0x142,
    FISH                          = 0x143,
    EEL                           = 0x144,
    JSTUDIO_SYSOBJ                = 0x145,
    JSTUDIO_ACTOR                 = 0x146,
    B_BBSHWV                      = 0x147,
    NPC_BBRVL                     = 0x148,
    OBJ_BIGBOMB_FLOWER            = 0x149,
    OBJ_BBLARGEBOMB               = 0x14A,
    OBJ_BSTN                      = 0x14B,
    B_MG                          = 0x14C,
    B_LASTBOSS                    = 0x14D,
    J_TEST                        = 0x14E,
    E_AM                          = 0x14F,
    T_QUAKE                       = 0x150,
    T_KUMITE                      = 0x151,
    GROUP_TEST                    = 0x152,
    GROUP_SUMMON                  = 0x153,
    T_BCAL                        = 0x154,
    E_SM                          = 0x155,
    E_BEAMOS                      = 0x156,
    GEKO_TAG                      = 0x157,
    E_GEKO                        = 0x158,
    E_SIREN                       = 0x159,
    E_PO                          = 0x15A,
    OBJ_RING                      = 0x15B,
    E_OR                          = 0x15C,
    E_OR_CANNON                   = 0x15D,
    OR_CANN_BULLET                = 0x15E,
    E_EYE                         = 0x15F,
    OBJ_HOLE                      = 0x160,
    OBJ_INTO_HOLE                 = 0x161,
    E_SPARK                       = 0x162,
    E_MAGMA                       = 0x163,
    E_MAGUPPO                     = 0x164,
    MAGUPPO_BULLET                = 0x165,
    E_BS                          = 0x166,
    E_SF                          = 0x167,
    E_SF4                         = 0x168,
    E_ST                          = 0x169,
    E_ST_WIRE                     = 0x16A,
    ENEMY_CONTROL                 = 0x16B,
    KIESU_TAG                     = 0x16C,
    E_KS                          = 0x16D,
    E_HB                          = 0x16E,
    E_HB_LEAF                     = 0x16F,
    E_REMLY                       = 0x170,
    E_LIZARUFOS                   = 0x171,
    E_LIZA_TAIL                   = 0x172,
    E_HIDOKARI                    = 0x173,
    E_HIDOKARIS                   = 0x174,
    E_HYDRA                       = 0x175,
    E_GUNHO                       = 0x176,
    E_GUNHOB                      = 0x177,
    E_BFISH                       = 0x178,
    E_CACTUS                      = 0x179,
    E_HOC                         = 0x17A,
    E_OC                          = 0x17B,
    E_KGIRA                       = 0x17C,
    OBJ_PIPE                      = 0x17D,
    E_BC                          = 0x17E,
    E_BCE                         = 0x17F,
    E_BCAL                        = 0x180,
    E_BCARROW                     = 0x181,
    E_BCALARROW                   = 0x182,
    BCZ_TAG                       = 0x183,
    E_BCZ                         = 0x184,
    E_SKYTAIL                     = 0x185,
    E_HP                          = 0x186,
    E_CHB                         = 0x187,
    E_GUE                         = 0x188,
    GUE_BULLET                    = 0x189,
    E_GE                          = 0x18A,
    E_RUPEE_GUE                   = 0x18B,
    E_GEROCK                      = 0x18C,
    E_TN2                         = 0x18D,
    E_HIDORY                      = 0x18E,
    HIDORY_FIRE                   = 0x18F,
    E_WS                          = 0x190,
    NPC_BIRD                      = 0x191,
    B_GIRAHIMU_BASE               = 0x192,
    B_GIRAHIMU                    = 0x193,
    B_GIRAHIMU2                   = 0x194,
    B_GIRAHIMU3_BASE              = 0x195,
    B_GIRAHIMU3_FIRST             = 0x196,
    B_GIRAHIMU3_SECOND            = 0x197,
    B_GIRAHIMU3_THIRD             = 0x198,
    OBJ_GH_SW_L                   = 0x199,
    OBJ_GH_KNIFE                  = 0x19A,
    OBJ_BIRD_SP_UP                = 0x19B,
    GH_SWORD_BEAM                 = 0x19C,
    B_ASURA                       = 0x19D,
    ASURA_ARM                     = 0x19E,
    ASURA_FOOT                    = 0x19F,
    ASURA_BULLET                  = 0x1A0,
    ASURA_SWORD                   = 0x1A1,
    ASURA_PILLAR                  = 0x1A2,
    INVISIBLE                     = 0x1A3,
    E_MR_SHIELD                   = 0x1A4,
    E_KG                          = 0x1A5,
    NPC_HONEYCOMB                 = 0x1A6,
    NPC_BEE                       = 0x1A7,
    HEART_FLOWER                  = 0x1A8,
    BOMBF                         = 0x1A9,
    BOMB                          = 0x1AA,
    OBJ_CARRY_STONE               = 0x1AB,
    OBJ_ROLL_ROCK                 = 0x1AC,
    COL_STP                       = 0x1AD,
    KANBAN                        = 0x1AE,
    OBJ_BAMBOO                    = 0x1AF,
    OBJ_SWHIT                     = 0x1B0,
    OBJ_SW_SWORD_BEAM             = 0x1B1,
    OBJ_SW_HARP                   = 0x1B2,
    OBJ_SIREN_BARRIER             = 0x1B3,
    OBJ_TOGE_TRAP                 = 0x1B4,
    PUMPKIN                       = 0x1B5,
    OBJ_PUMPKIN_LEAF              = 0x1B6,
    OBJ_WATER_NUT_LEAF            = 0x1B7,
    OBJ_WATER_NUT                 = 0x1B8,
    OBJ_TABLEWARE                 = 0x1B9,
    OBJ_SW_WHIPLEVER              = 0x1BA,
    OBJ_MUSHROOM                  = 0x1BB,
    WOODAREA_TAG                  = 0x1BC,
    OBJ_FRUIT                     = 0x1BD,
    OBJ_SKULL                     = 0x1BE,
    SOUND_TAG                     = 0x1BF,
    OBJ_ROCK_DRAGON               = 0x1C0,
    TAG_INSECT                    = 0x1C1,
    INSECT_LADYBUG                = 0x1C2,
    INSECT_DRAGONFLY              = 0x1C3,
    INSECT_BEETLE                 = 0x1C4,
    INSECT_GRASSHOPPER            = 0x1C5,
    INSECT_CICADA                 = 0x1C6,
    INSECT_ANT                    = 0x1C7,
    INSECT_BUTTERFLY              = 0x1C8,
    INSECT_SCARAB                 = 0x1C9,
    INSECT_FIREFLY                = 0x1CA,
    OBJ_SAIL                      = 0x1CB,
    OBJ_LOTUS_FLOWER              = 0x1CC,
    OBJ_LOTUS_SEED                = 0x1CD,
    OBJ_SHUTTER_LOCK              = 0x1CE,
    OBJ_LAMP                      = 0x1CF,
    TAG_ROCK_BOAT                 = 0x1D0,
    OBJ_TOWER_GEAR_D101           = 0x1D1,
    OBJ_SHUTTER_WATER_D101        = 0x1D2,
    OBJ_ANCIENT_JEWELS            = 0x1D3,
    OBJ_MG_PUMPKIN                = 0x1D4,
    OBJ_FLAG                      = 0x1D5,
    OBJ_CHANDELIER                = 0x1D6,
    TAG_PUMPKIN_CLAY              = 0x1D7,
    TAG_REACTION                  = 0x1D8,
    OBJ_SPORE                     = 0x1D9,
    OBJ_FRUIT_B                   = 0x1DA,
    OBJ_DIVINER_CRYSTAL           = 0x1DB,
    TAG_NOEFFECT_AREA             = 0x1DC,
    TAG_D3_SCENE_CHANGE           = 0x1DD,
    OBJ_DECOA                     = 0x1DE,
    OBJ_DECOB                     = 0x1DF,
    OBJ_SANDBAG                   = 0x1E0,
    OBJ_PAINT                     = 0x1E1,
    OBJ_CONTROL_PANEL             = 0x1E2,
    OBJ_UG_SWITCH                 = 0x1E3,
    OBJ_CLEARNESS_WALL            = 0x1E4,
    OBJ_RUINED_SAVE               = 0x1E5,
    OBJ_TRIFORCE                  = 0x1E6,
    OBJ_KANBAN_STONE              = 0x1E7,
    TBOX                          = 0x1E8,
    OBJ_BUBBLE                    = 0x1E9,
    OBJ_VSD                       = 0x1EA,
    OBJ_SOIL                      = 0x1EB,
    OBJ_IVY_ROPE                  = 0x1EC,
    OBJ_GRASS_COIL                = 0x1ED,
    OBJ_ROPE_IGAIGA               = 0x1EE,
    OBJ_FIRE                      = 0x1EF,
    OBJ_TUBO                      = 0x1F0,
    OBJ_TUBO_BIG                  = 0x1F1,
    OBJ_CHAIR                     = 0x1F2,
    TIME_AREA                     = 0x1F3,
    OBJ_BLAST_ROCK                = 0x1F4,
    OBJ_SW_DIR                    = 0x1F5,
    OBJ_SW_DIR_DOOR               = 0x1F6,
    OBJ_SW_BANK                   = 0x1F7,
    OBJ_SW_BANK_SMALL             = 0x1F8,
    T_FAIRY                       = 0x1F9,
    OBJ_FAIRY                     = 0x1FA,
    BIRD_MOB                      = 0x1FB,
    OBJ_BALLISTA_HANDLE           = 0x1FC,
    OBJ_TIME_BOAT_BULLET          = 0x1FD,
    OBJ_TIME_DOOR                 = 0x1FE,
    OBJ_TIME_DOOR_BEFORE          = 0x1FF,
    TAG_TIME_DOOR_BEAM            = 0x200,
    OBJ_COL                       = 0x201,
    OBJ_DAYNIGHT                  = 0x202,
    OBJ_BUILDING                  = 0x203,
    OBJ_OCT_GRASS                 = 0x204,
    OBJ_OCT_GRASS_LEAF            = 0x205,
    OBJ_TUMBLE_WEED               = 0x206,
    TUMBLE_WEED_TAG               = 0x207,
    OBJ_FLOWER_ANCIENT            = 0x208,
    OBJ_BARREL                    = 0x209,
    OBJ_WARP                      = 0x20A,
    OBJ_WATER_MARK                = 0x20B,
    OBJ_WATER_JAR                 = 0x20C,
    OBJ_STOPPING_ROPE             = 0x20D,
    OBJ_TRAP_BIRD_WOOD            = 0x20E,
    OBJ_TACKLE                    = 0x20F,
    TACKLE_TAG                    = 0x210,
    OBJ_VORTEX                    = 0x211,
    OBJ_TOWER_BOMB                = 0x212,
    OBJ_SEAT_SWORD                = 0x213,
    OBJ_POLE_STONY                = 0x214,
    OBJ_SWORD_CANDLE              = 0x215,
    OBJ_SAVE                      = 0x216,
    OBJ_POOL_COCK                 = 0x217,
    OBJ_FIREWALL                  = 0x218,
    HARP_TAG                      = 0x219,
    OBJ_SWORD_STAB                = 0x21A,
    OBJ_GODDESS_CUBE              = 0x21B,
    OBJ_TIME_BLOCK                = 0x21C,
    OBJ_MOVE_ELEC                 = 0x21D,
    OBJ_LAVA_D201                 = 0x21E,
    OBJ_HARP_HINT                 = 0x21F,
    OBJ_F302_LIGHT                = 0x220,
    OBJ_TOD3_STONE                = 0x221,
    OBJ_B300_SAND                 = 0x222,
    T_DOWSING                     = 0x223,
    T_MAP_MARK                    = 0x224,
    BEETLE_TAG                    = 0x225,
    EFFECT_GEN_TAG                = 0x226,
    TAG_TIME_AREA_CHECK           = 0x227,
    TAG_RESTART_TIME_STONE        = 0x228,
    SHOP_SAMPLE                   = 0x229,
    OBJ_TERRY_GIMMICK             = 0x22A,
    OBJ_TERRY_SWITCH              = 0x22B,
    OBJ_TERRY_HOLE                = 0x22C,
    OBJ_TERRY_BIKE                = 0x22D,
    OBJ_JUNK_REPAIR               = 0x22E,
    CO_TEST                       = 0x22F,
    OBJ_ARROW_SWITCH              = 0x230,
    OBJ_VENT_FAN                  = 0x231,
    OBJ_ELECTRIC_LIGHT            = 0x232,
    OBJ_WATER_SWITCH              = 0x233,
    OBJ_ROTATION_LIGHT            = 0x234,
    OBJ_HOLE_MINIGAME             = 0x235,
    OBJ_CLOUD_DIVE                = 0x236,
    OBJ_MUSASABI                  = 0x237,
    OBJ_FORTUNE_RING              = 0x238,
    OBJ_BLOW_COAL                 = 0x239,
    OBJ_SPIKE                     = 0x23A,
    OBJ_WATER_SPOUT               = 0x23B,
    OBJ_SMOKE                     = 0x23C,
    OBJ_LIGHTHOUSE_LIGHT          = 0x23D,
    OBJ_WATER_IGAIGA              = 0x23E,
    OBJ_BLADE                     = 0x23F,
    OBJ_FIRE_OBSTACLE             = 0x240,
    OBJ_FIRE_PILLAR               = 0x241,
    OBJ_GUARD_LOG                 = 0x242,
    OBJ_SLICE_LOG                 = 0x243,
    OBJ_SLICE_LOG_PARTS           = 0x244,
    OBJ_STAGE_DEBRIS              = 0x245,
    OBJ_GROUND_COVER              = 0x246,
    OBJ_CUMUL_CLOUD               = 0x247,
    OBJ_UNDER_CLOUD               = 0x248,
    OBJ_WATERFALL_F102            = 0x249,
    OBJ_GOD_MARK                  = 0x24A,
    OBJ_IMPA_DOOR                 = 0x24B,
    OBJ_WATERFALL_D100            = 0x24C,
    OBJ_GIRAHIM_FOOT              = 0x24D,
    OBJ_ISLAND_LOD                = 0x24E,
    OBJ_UTA_DEMO_PEDEST           = 0x24F,
    OBJ_LAVA_F200                 = 0x250,
    OBJ_ROPE_BASE                 = 0x251,
    OBJ_SUN_LIGHT                 = 0x252,
    OBJ_SIREN_2DMAP               = 0x253,
    OBJ_DISPLAY_ONLY_NBS          = 0x254,
    OBJ_AMBER                     = 0x255,
    OBJ_BIRD_STATUE               = 0x256,
    OBJ_F400_GATE_LEAF            = 0x257,
    OBJ_F400_GATE_SEAL            = 0x258,
    OBJ_MAPPARTS                  = 0x259,
    OBJ_RO_AT_TARGET              = 0x25A,
    RO_AT_TAR_MANAGER_TAG         = 0x25B,
    TAG_MUSASABI                  = 0x25C,
    TAG_MAP_INST                  = 0x25D,
    TAG_AUTO_MESSAGE              = 0x25E,
    TAG_SHIP_SLOPE                = 0x25F,
    TAG_SHIP_FLOOD                = 0x260,
    TAG_BARREL                    = 0x261,
    TAG_BARREL_POS                = 0x262,
    TAG_HEAT_RESIST               = 0x263,
    TAG_HOLY_WATER                = 0x264,
    TAG_BELT_OBSTACLE             = 0x265,
    TAG_DRUM                      = 0x266,
    TAG_ROLL_ATTACK_LOG           = 0x267,
    TAG_SHIP_WINDOW               = 0x268,
    ARROW                         = 0x269,
    MASS_OBJ_TAG                  = 0x26A,
    SOUND_AREA_MGR                = 0x26B,
    TAG_SOUND_AREA                = 0x26C,
    ATT_TAG                       = 0x26D,
    TLP_TAG                       = 0x26E,
    SKYENEMY_T                    = 0x26F,
    TOUCH_TAG                     = 0x270,
    CAMERA_TAG                    = 0x271,
    CAMERA2_TAG                   = 0x272,
    ACTION_TAG                    = 0x273,
    SC_CHANGE_TAG                 = 0x274,
    GATE2GND_TAG                  = 0x275,
    ALLDIE_TAG                    = 0x276,
    SW_TAG                        = 0x277,
    PL_RESTART                    = 0x278,
    SW_AREA_TAG                   = 0x279,
    SIREN_TAG                     = 0x27A,
    TAG_TKEVNT                    = 0x27B,
    MOLE_PROHIBIT_TAG             = 0x27C,
    TAG_DEFEAT_BOSS               = 0x27D,
    TAG_TIMER                     = 0x27E,
    TAG_FENCE_SYNCHRONIZER        = 0x27F,
    TAG_GENKI_DOWSING_TARGET      = 0x280,
    ITEM                          = 0x281,
    OBJ_ITEM_HEART_CONTAINER      = 0x282,
    OBJ_CLEF                      = 0x283,
    OBJ_FRUIT_GUTS_LEAF           = 0x284,
    OBJ_SWRD_PRJ                  = 0x285,
    OBJ_VACU_DUST_PARTS           = 0x286,
    OBJ_VACU_DUST                 = 0x287,
    OBJ_RAIL_POST                 = 0x288,
    OBJ_RAIL_END                  = 0x289,
    OBJ_TENI_RAIL                 = 0x28A,
    OBJ_TENI_RAIL_POST            = 0x28B,
    OBJ_FORCE_SIGN                = 0x28C,
    TAG_FORCE_GET_FLAG            = 0x28D,
    TAG_CLEF_MANAGER              = 0x28E,
    TAG_CLEF_GAME                 = 0x28F,
    TAG_MINIGAME_INSECT_CAPTURE   = 0x290,
    CAMERA                        = 0x291,
    WEATHER_TAG                   = 0x292,
    SPORE_TAG                     = 0x293,
    MIST_TAG                      = 0x294,
    SPARKS_TAG                    = 0x295,
    SPARKS2_TAG                   = 0x296,
    KYTAG_TAG                     = 0x297,
    LBTHUNDER_TAG                 = 0x298,
    PLTCHG_TAG                    = 0x299,
    PLIGHT_TAG                    = 0x29A,
    VRBOX_TAG                     = 0x29B,
    NPC_INV                       = 0x29C,
    NPC_TKE                       = 0x29D,
    NPC_STR                       = 0x29E,
    MESSAGE_ACTOR                 = 0x29F,
    LIGHT_OBJECT                  = 0x2A0,
    MESSAGE                       = 0x2A1,
    LYT_CONTROL_GAME              = 0x2A2,
    LYT_DEMO_DOWSING              = 0x2A3,
    LYT_CONTROL_TITLE             = 0x2A4,
    LYT_DROP_LINE                 = 0x2A5,
    LYT_FORCE_LINE                = 0x2A6,
    LYT_ENEMY_ICON                = 0x2A7,
    LYT_MINI_GAME                 = 0x2A8,
    LYT_SUIRYU_SCORE              = 0x2A9,
    LYT_SUIRYU_SCORE_COMP         = 0x2AA,
    LYT_BOSS_CAPTION              = 0x2AB,
    LYT_PAUSE                     = 0x2AC,
    LYT_GAMEOVER_MGR              = 0x2AD,
    LYT_SAVE_MGR                  = 0x2AE,
    TITLE_MANAGER                 = 0x2AF,
    LYT_TITLE_BG                  = 0x2B0,
    LYT_SHOP                      = 0x2B1,
    LYT_DEPOSIT                   = 0x2B2,
    LYT_DEMO_TITLE                = 0x2B3,
    LYT_END_ROLL                  = 0x2B4,
    LYT_SEEKER_STONE              = 0x2B5,
    LYT_FILESELECT                = 0x2B6,
    SKB                           = 0x2B7,
    EVENT_TAG                     = 0x2B8,
    EVENTF_TAG                    = 0x2B9,
    C_GAME                        = 0x2BA,
    C_BASE                        = 0x2BB,
    BOOT                          = 0x2BC,
    ROOM                          = 0x2BD,
    LAST                          = 0x2BE,
}

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut savefile::FileMgr;
    static ROOM_MGR: *mut RoomMgr;
    static DUNGEONFLAG_MGR: *mut flag::DungeonflagMgr;
    static CONNECT_MGR: ActorTreeProcess;
    static mut STATIC_DUNGEONFLAGS: [u16; 8];

    static mut ACTOR_PARAM_POS: *mut math::Vec3f;
    static mut ACTOR_PARAM_ROT: *mut math::Vec3s;
    static mut ACTOR_PARAM_SCALE: *mut math::Vec3f;
    static mut ACTOR_STAGE_OBJECT_FLAG: u16;
    static mut ACTOR_VIEW_CLIP_INDEX: u8;
    static mut ACTOR_OBJECT_INFO_PTR: *mut c_void;
    static mut ACTOR_SPAWN_WITH_REF: *mut dAcBase;
    static mut ACTORBASE_PARAM2: u32;
    static mut ACTORBASE_ROOMID: u32;
    static mut ACTORBASE_SUBTYPE: u8;

    static mut CURRENT_STAGE_NAME: [u8; 8];

    static mut INITIAL_INSERT_ANGLES: [math::Vec3s; 6];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn allocateNewActor(
        actorid: ACTORID,
        connect_parent: *const ActorTreeNode,
        actor_param1: u32,
        actor_group_type: u8,
    ) -> *mut dBase;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm
#[no_mangle]
pub fn spawn_actor(
    actorid: ACTORID,
    roomid: u32,
    actor_param1: u32,
    pos: *mut math::Vec3f,
    rot: *mut math::Vec3s,
    scale: *mut math::Vec3f,
    actor_param2: u32,
) -> *mut dBase {
    unsafe {
        ACTOR_PARAM_POS = pos;
        ACTOR_PARAM_ROT = rot;
        ACTOR_PARAM_SCALE = scale;
        ACTOR_STAGE_OBJECT_FLAG = 0xFFFF;
        ACTOR_VIEW_CLIP_INDEX = 0xFF;
        ACTOR_OBJECT_INFO_PTR = core::ptr::null_mut();
        ACTOR_SPAWN_WITH_REF = core::ptr::null_mut();
        ACTORBASE_PARAM2 = actor_param2;
        ACTORBASE_ROOMID = roomid;
        ACTORBASE_SUBTYPE = 0;

        let connect_parent: *const ActorTreeNode =
            from_ref(&(*ROOM_MGR).base.members.members.actor_mgr.connect_node);
        let group_type: u8 = 2; // 0 = other, 1 = scene, 2 = actor, 3 = unk

        let actor = allocateNewActor(actorid, connect_parent, actor_param1, group_type);

        // Reset globals
        ACTORBASE_PARAM2 = 0xFFFFFFFF;
        ACTOR_PARAM_POS = core::ptr::null_mut();
        ACTOR_PARAM_ROT = core::ptr::null_mut();
        ACTOR_PARAM_SCALE = core::ptr::null_mut();
        return actor;
    }
}

// This function was inlined so we have to create our own
#[no_mangle]
pub fn find_actor_by_type(actorid: ACTORID, start_node: *mut ActorTreeNode) -> *mut dBase {
    unsafe {
        let mut cur_node: *mut ActorTreeNode = start_node;

        if cur_node == core::ptr::null_mut() {
            cur_node = CONNECT_MGR.root;
        }

        while cur_node != core::ptr::null_mut()
            && (*(*cur_node).owner).members.members.actorid != actorid as u16
        {
            // Search the tree depth-first starting with the child node
            if (*cur_node).tree_node.child != core::ptr::null_mut() {
                cur_node = (*cur_node).tree_node.child as *mut ActorTreeNode;
            // If there's no child node go to the next sibling node
            } else if (*cur_node).tree_node.next != core::ptr::null_mut() {
                cur_node = (*cur_node).tree_node.next as *mut ActorTreeNode;
            // If there's no more sibling nodes, go up the tree until we hit
            // a node which has an unexplored sibling
            } else {
                while (*cur_node).tree_node.next == core::ptr::null_mut() {
                    cur_node = (*cur_node).tree_node.parent as *mut ActorTreeNode;
                    if cur_node == core::ptr::null_mut() {
                        return core::ptr::null_mut();
                    }
                }
                cur_node = (*cur_node).tree_node.next as *mut ActorTreeNode;
            }
        }

        if (cur_node == core::ptr::null_mut()) {
            return core::ptr::null_mut();
        }

        return (*cur_node).owner;
    }
}

#[no_mangle]
pub fn should_spawn_eldin_platforms(platform_actor_maybe: *mut dAcORockBoatMaybe) -> u32 {
    unsafe {
        // If we haven't visited the fire dragon and aren't in boko base,
        // then don't spawn the platforms
        if flag::check_storyflag(19) == 0
            && (&CURRENT_STAGE_NAME[..5] == b"F200\0" || &CURRENT_STAGE_NAME[..7] == b"F201_1\0")
        {
            return 0;
        }

        // Replaced code
        if (*platform_actor_maybe).spawnCooldown > 0 {
            (*platform_actor_maybe).spawnCooldown -= 1;
            if (*platform_actor_maybe).spawnCooldown == 0 {
                return 1;
            }
        }
        return 0;
    }
}

#[no_mangle]
pub fn set_correct_boss_key_positions() {
    unsafe {
        for bk_angle in &mut INITIAL_INSERT_ANGLES[0..6] {
            bk_angle.x = 0xC000;
            bk_angle.y = 0x4700;
            bk_angle.z = 0xB8E4;
        }
    }
}

#[no_mangle]
pub fn set_random_boss_key_positions() {
    unsafe {
        for bk_angle in &mut INITIAL_INSERT_ANGLES[0..6] {
            bk_angle.x = rng::simple_rng() as u16;
            bk_angle.y = rng::simple_rng() as u16;
            bk_angle.z = rng::simple_rng() as u16;
        }
    }
}
