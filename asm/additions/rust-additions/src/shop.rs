#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;

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
pub struct dAcShopSample {
    pub base:                actor::dAcOBase,
    pub _0:                  [u8; 0x538],
    pub unk_collider:        [u8; 0x1D0],
    pub state_mgr:           [u8; 0x70],
    pub event_flow_mgr:      [u8; 0xD0],
    pub actor_event_related: [u8; 0x68],
    pub model_holder:        dAcShopSampleModelHolder,
    pub _1:                  [u8; 0x700],
}
assert_eq_size!([u8; 0x13E0], dAcShopSample);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleModelHolder {
    pub model_list:     *mut dAcShopSampleModel,
    pub current_model:  *mut dAcShopSampleModel,
    pub sold_out_model: *mut dAcShopSampleModel,
    pub model_count:    i16,
    pub _0:             [u8; 6],
}
assert_eq_size!([u8; 0x20], dAcShopSampleModelHolder);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleModel {
    pub item_index: u16,
    pub _0:         u16,
    pub model:      [u8; 0x30],
    pub _1:         u32,
    pub next_model: *mut dAcShopSampleModel,
}
assert_eq_size!([u8; 0x40], dAcShopSampleModel);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleShopItem {
    pub buy_decide_scale:           f32,
    pub put_scale:                  f32,
    pub target_arrow_height_offset: f32,
    pub itemid:                     flag::ITEMFLAGS,
    pub price:                      u16,
    pub event_entrypoint:           u16,
    pub next_shop_item_index:       u16,
    pub spawn_storyflag:            u16,
    pub arc_name:                   [u8; 30],
    pub model_name:                 [u8; 24],
    pub display_height_offset:      f32,
    pub trapbits:                   u8,
    pub _0:                         u8,
    pub sold_out_storyflag:         u16,
}
assert_eq_size!([u8; 0x54], dAcShopSampleShopItem);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static SHOP_ITEMS: [dAcShopSampleShopItem; 35];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn getRotFromDegrees(deg: f32) -> u16;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn rotate_shop_items() {
    unsafe {
        let shop_sample: *mut dAcShopSample;
        asm!("mov {0:x}, x19", out(reg) shop_sample);

        let mut degrees = -0.3f32;
        let item_index = (*(*shop_sample).model_holder.current_model).item_index as usize;

        // TODO: fix sold out signs rotating
        if item_index == 0x7F {
            // doesn't work
            degrees = 0.0f32;
            (*shop_sample).base.members.base.rot.y = 0;
        } else if SHOP_ITEMS[item_index].trapbits != 0 {
            degrees = 0.3f32;
        }

        (*shop_sample).base.members.base.rot.y += getRotFromDegrees(degrees);

        // Replaced instructions
        asm!("add x21, x19, #0xC58", "mov x0, x21");
    }
}

#[no_mangle]
pub fn set_shop_display_height() {
    unsafe {
        let shop_sample: *mut dAcShopSample;
        asm!("mov {0:x}, x20", out(reg) shop_sample);

        let item_index = (*(*shop_sample).model_holder.current_model).item_index as usize;
        let mut display_height_offset = 0.0f32;

        if item_index != 0x7F {
            display_height_offset = SHOP_ITEMS[item_index].display_height_offset;
        }

        // Replaced instructions
        asm!("str s1, [x19]", "str {0:w}, [x19, #4]", "str s0, [x19, #8]", in(reg) display_height_offset);
    }
}

#[no_mangle]
pub fn set_shop_sold_out_storyflag() {
    unsafe {
        let item_index: usize;
        asm!("ldrh {0:w}, [x20, #8]", out(reg) item_index);

        if item_index != 0x7F {
            let storyflag = SHOP_ITEMS[item_index].sold_out_storyflag;

            if storyflag != 0 {
                flag::set_storyflag(storyflag);
            }
        }
    }
}

#[no_mangle]
pub fn check_shop_sold_out_storyflag(item_index: usize) -> bool {
    unsafe {
        if item_index != 0x7F {
            return flag::check_storyflag(SHOP_ITEMS[item_index].sold_out_storyflag) != 0;
        }

        return false;
    }
}
