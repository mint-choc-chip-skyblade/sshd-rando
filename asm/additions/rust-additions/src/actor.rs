#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use static_assertions::assert_eq_size;

// repr(C) prevents rust from reordering struct fields.
// packed(1) prevents rust from aligning structs to the size of the largest
// field.

// Using u64 or 64bit pointers forces structs to be 8-byte aligned.
// The vanilla code seems to be 4-byte aligned. To make extra sure, used
// packed(1) to force the alignment to match what you define.

// Always add an assert_eq_size!() macro after defining a struct to ensure it's
// the size you expect it to be.

#[repr(C)]
#[derive(Copy, Clone, Default)]
pub struct Vec3f {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}
assert_eq_size!([u8; 12], Vec3f);

#[repr(C)]
#[derive(Copy, Clone, Default)]
pub struct Vec3s {
    pub x: u16,
    pub y: u16,
    pub z: u16,
}
assert_eq_size!([u8; 6], Vec3s);

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
    pub pos_copy1:          Vec3f,
    pub pos_copy2:          Vec3f,
    pub pos_copy3:          Vec3f,
    pub rot_copy:           Vec3s,
    pub _1:                 u16,
    pub forward_speed:      f32,
    pub gravity_accel:      f32,
    pub gravity:            f32,
    pub velocity:           Vec3f,
    pub world_matrix:       [u8; 0x30],
    pub bounding_box:       [u8; 0x18],
    pub culling_distance:   f32,
    pub aabb_addon:         f32,
    pub object_actor_flags: u32,
    pub _2:                 f32,
    pub _3:                 [u8; 4],
    pub _4:                 f32,
    pub _5:                 [u8; 28],
    pub some_pos_copy:      Vec3f,
    pub _6:                 [u8; 12],
    pub _7:                 Vec3f,
    pub _8:                 [u8; 12],
    pub starting_pos:       Vec3f,
    pub starting_angle:     Vec3s,
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
    pub sound_pos_ptr:    *mut Vec3f,
    pub pos_copy:         Vec3f,
    pub param2:           u32,
    pub rot_copy:         Vec3s,
    pub _2:               u16,
    pub room_id_copy:     u8,
    pub _3:               u8,
    pub subtype:          u8,
    pub _4:               u8,
    pub rot:              Vec3s,
    pub _5:               u16,
    pub pos:              Vec3f,
    pub scale:            Vec3f,
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

// Player stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dPlayer {
    pub vtable:                         u64,
    pub base:                           ActorBaseBasemembers,
    pub obj_base_members:               ActorObjectBasemembers,
    pub _0:                             [u8; 8],
    pub changes_when_stabbing:          f32,
    pub sword_swing_direction:          u8,
    pub riding_type:                    u8,
    pub sword_swing_type:               u8,
    pub unk:                            u8,
    pub _1:                             [u8; 36],
    pub sword_and_more_states:          u32,
    pub flags_to_update_models:         u32,
    pub _2:                             u32,
    pub some_more_action_flags_mayhaps: u32,
    pub _3:                             u32,
    pub some_action_flags_maybe:        u32,
    pub player_anim_flags:              u32,
    pub action_flags:                   u32,
    pub action_flags_cont:              u32,
    pub current_action:                 u32,
    pub _4:                             [u8; 0x5F14],
    pub low_health_beeping_timer:       u8,
    pub _5:                             u16,
    pub some_stage_indicator:           u8,
    pub _6:                             [u8; 0x90],
    pub stamina_recovery_timer:         u16,
    pub _7:                             [u8; 8],
    pub skyward_strike_timer:           u16,
    pub some_movement_flags:            u16,
    pub _8:                             u16,
    pub _9:                             [u8; 2],
    pub idle_anim_timer:                u16,
    pub shit_smell_timer:               u16,
    pub burn_timer:                     u16,
    pub sheild_burn_timer:              u16,
    pub cursed_timer:                   u16,
    pub shock_effect_timer:             u16,
    pub _10:                            [u8; 0xA6],
    pub stamina_amount:                 u32,
    // + more stuff
}
assert_eq_size!([u8; 0x64DC], dPlayer);
