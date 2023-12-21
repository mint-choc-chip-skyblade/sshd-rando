#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;

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

// Player stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dPlayer {
    pub vtable:                         u64,
    pub base:                           actor::ActorBaseBasemembers,
    pub obj_base_members:               actor::ActorObjectBasemembers,
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
    pub _6:                             [u8; 0x6F],
    pub burn_rate:                      u8,
    pub cursed_related_timer:           u16,
    pub some_timer:                     u16,
    pub triggered_buttons:              u16,
    pub _7:                             [u8; 2],
    pub held_buttons:                   u16,
    pub current_pressed_button_flags:   u16,
    pub _8:                             [u8; 4],
    pub item_being_used:                u16,
    pub item_trying_to_be_used:         u16,
    pub equipped_b_item:                u16,
    pub damage_cooldown:                u16,
    pub _9:                             [u8; 8],
    pub stamina_recovery_timer:         u16,
    pub something_we_use_for_stamina:   u8,
    pub _10:                            [u8; 7],
    pub skyward_strike_timer:           u16,
    pub some_movement_flags:            u16,
    pub _11:                            u16,
    pub _12:                            [u8; 2],
    pub idle_anim_timer:                u16,
    pub shit_smell_timer:               u16,
    pub burn_timer:                     u16,
    pub sheild_burn_timer:              u16,
    pub cursed_timer:                   u16,
    pub shock_effect_timer:             u16,
    pub _13:                            [u8; 0xA6],
    pub stamina_amount:                 u32,
    // + more stuff
}
assert_eq_size!([u8; 0x64DC], dPlayer);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

////////////////////////
// ADD FUNCTIONS HERE //
////////////////////////
