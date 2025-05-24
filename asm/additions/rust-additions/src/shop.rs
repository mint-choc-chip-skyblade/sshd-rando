#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::item;

use core::arch::asm;
use core::ffi::{c_char, c_void};
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
    pub main_substruct:      dAcShopSampleSubclassHolder,
    pub _1:                  [u8; 0x6D8],
}
assert_eq_size!([u8; 0x13E0], dAcShopSample);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleModelHolder {
    pub model_list:         *mut dAcShopSampleModel,
    pub current_model:      *mut dAcShopSampleModel,
    pub sold_out_model:     *mut dAcShopSampleModel,
    pub model_count:        i16,
    pub use_sold_out_model: bool,
    pub _0:                 [u8; 5],
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
pub struct dAcShopSampleSubclassHolder {
    pub vtable:                     *mut c_void,
    pub _0:                         [u8; 0x10],
    pub shop_sample_subclass_array: *mut [*mut dAcShopSampleSubclass; 35],
    pub shop_sample_sold_out:       *mut *mut dAcShopSampleSubclass,
}
assert_eq_size!([u8; 0x28], dAcShopSampleSubclassHolder);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleSubclass {
    pub vtable:     *mut dAcShopSampleSubclassvtable,
    pub shop_index: u16,
    pub _0:         [u8; 6],
}
assert_eq_size!([u8; 0x10], dAcShopSampleSubclass);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcShopSampleSubclassvtable {
    pub unk_func1:               extern "C" fn(),
    pub unk_func2:               extern "C" fn(),
    pub check_pouch_space:       extern "C" fn() -> u32,
    pub unk_func4:               extern "C" fn(),
    pub unk_func5:               extern "C" fn(),
    pub unk_func6:               extern "C" fn(),
    pub check_can_buy:           extern "C" fn() -> u32,
    pub check_has_enough_rupees: extern "C" fn(*mut dAcShopSampleSubclass) -> u32,
    pub is_sold_out:             extern "C" fn(*mut dAcShopSampleSubclass) -> u32,
    pub is_at_end_of_item_chain: extern "C" fn(*mut dAcShopSampleSubclass) -> bool,
    pub unk_func11:              extern "C" fn(),
    pub unk_func12:              extern "C" fn(),
    pub unk_func13:              extern "C" fn(),
    pub give_item:               extern "C" fn(*mut dAcShopSampleSubclass),
    pub get_x_offset:            extern "C" fn(*mut dAcShopSampleSubclass) -> f32,
    pub get_scale:               extern "C" fn(*mut dAcShopSampleSubclass) -> f32,
}
assert_eq_size!([u8; 0x80], dAcShopSampleSubclassvtable);

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
    static mut SHOP_ITEMS: [dAcShopSampleShopItem; 35];
    static mut ACTORBASE_PARAM2: u32;

    static mut ITEM_GET_BOTTLE_POUCH_SLOT: u32;
    static mut NUMBER_OF_ITEMS: u32;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn getRotFromDegrees(deg: f32) -> u16;
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub extern "C" fn rotate_shop_items() {
    unsafe {
        let shop_sample: *mut dAcShopSample;
        asm!("mov {0:x}, x19", out(reg) shop_sample);

        // idk why this is backwards from the normal item actor rotation ¯\_(ツ)_/¯
        let mut degrees = -0.3f32;
        let item_index = (*(*shop_sample).model_holder.current_model).item_index as usize;

        if item_index >= 30 {
            degrees = 0.0f32;
        } else if (*shop_sample).model_holder.use_sold_out_model {
            degrees = 0.0f32;
            (*shop_sample).base.members.base.rot.y = 0;
        } else if SHOP_ITEMS[item_index].trapbits == 0xF {
            degrees = 0.3f32;
        }

        (*shop_sample).base.members.base.rot.y += getRotFromDegrees(degrees);

        // Replaced instructions
        asm!("add x21, {0:x}, #0xC58", "mov x0, x21", in(reg) shop_sample);
    }
}

#[no_mangle]
pub extern "C" fn set_shop_display_height() -> f32 {
    unsafe {
        let shop_sample: *mut dAcShopSample;
        asm!("mov {0:x}, x20", out(reg) shop_sample);

        let item_index = (*(*shop_sample).model_holder.current_model).item_index as usize;
        let mut display_height_offset = -25.0f32;

        // Prevents last item in shop list from freezing after purchase
        // Also prevents Rupin's Shop items from rotating or being badly in the table.
        if item_index == 0x7F || item_index <= 8 {
            (*shop_sample).base.members.base.rot.y = 0;
            return display_height_offset;
        }

        display_height_offset = SHOP_ITEMS[item_index].display_height_offset;

        // Override display_height_offset for progressive models
        match SHOP_ITEMS[item_index].itemid {
            flag::ITEMFLAGS::BOW => {
                if flag::check_itemflag(flag::ITEMFLAGS::IRON_BOW) != 0 {
                    display_height_offset = -35.0f32;
                } else if flag::check_itemflag(flag::ITEMFLAGS::BOW) != 0 {
                    display_height_offset = -29.0f32;
                }
            },
            flag::ITEMFLAGS::SLINGSHOT => {
                if flag::check_itemflag(flag::ITEMFLAGS::SLINGSHOT) != 0 {
                    display_height_offset = -32.0f32;
                }
            },
            flag::ITEMFLAGS::BEETLE => {
                if flag::check_itemflag(flag::ITEMFLAGS::QUICK_BEETLE) != 0 {
                    display_height_offset = -17.0f32;
                // Hook Beetle and Quick Beetle use the same offset
                } else if flag::check_itemflag(flag::ITEMFLAGS::BEETLE) != 0 {
                    display_height_offset = -16.0f32;
                }
            },
            flag::ITEMFLAGS::DIGGING_MITTS => {
                if flag::check_itemflag(flag::ITEMFLAGS::DIGGING_MITTS) != 0 {
                    display_height_offset = -38.0f32;
                }
            },
            flag::ITEMFLAGS::BUG_NET => {
                if flag::check_itemflag(flag::ITEMFLAGS::BUG_NET) != 0 {
                    display_height_offset = -32.0f32;
                }
            },
            flag::ITEMFLAGS::MEDIUM_WALLET => {
                #[allow(clippy::if_same_then_else)]
                if flag::check_itemflag(flag::ITEMFLAGS::GIANT_WALLET) != 0 {
                    display_height_offset = -32.0f32;
                } else if flag::check_itemflag(flag::ITEMFLAGS::BIG_WALLET) != 0 {
                    display_height_offset = -30.0f32; // this model sucks ;-;
                } else if flag::check_itemflag(flag::ITEMFLAGS::MEDIUM_WALLET) != 0 {
                    display_height_offset = -30.0f32;
                }
            },
            flag::ITEMFLAGS::ADVENTURE_POUCH => {
                if flag::check_itemflag(flag::ITEMFLAGS::ADVENTURE_POUCH) != 0 {
                    display_height_offset = -23.0f32;
                }
            },
            _ => {},
        }

        return display_height_offset;
    }
}

#[no_mangle]
pub extern "C" fn set_shop_sold_out_storyflag() {
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
pub extern "C" fn check_shop_sold_out_storyflag(item_index: usize) -> bool {
    unsafe {
        if item_index != 0x7F {
            let sold_out_storyflag = SHOP_ITEMS[item_index].sold_out_storyflag;

            if sold_out_storyflag != 0 && sold_out_storyflag != 0xFFFF {
                return flag::check_storyflag(sold_out_storyflag) != 0;
            }
        }

        return false;
    }
}

#[no_mangle]
pub extern "C" fn handle_shop_traps() {
    unsafe {
        let shop_item: *mut dAcShopSampleShopItem;
        asm!("mov {0:x}, x20", out(reg) shop_item);

        ACTORBASE_PARAM2 = 0xFFFFFF0F | (((*shop_item).trapbits << 4) as u32);
        ITEM_GET_BOTTLE_POUCH_SLOT = 0xFFFFFFFF;
        NUMBER_OF_ITEMS = 0;
    }
}

#[no_mangle]
pub extern "C" fn shop_use_progressive_models() {
    unsafe {
        let shop_sample: *mut dAcShopSampleShopItem;
        asm!("mov {0:x}, x26", out(reg) shop_sample);

        let item_id = (*shop_sample).itemid;

        // Fix archive name
        let mut archive_name = (*shop_sample).arc_name.as_ptr() as *const c_char;

        // Handle shop rupee colors
        //
        // Completely different from how SDR handles this
        // The solution used in SDR would require HDR to recreate several complex
        // functions which have been inlined. However, HDR has way more memory
        // than SDR so this can be bypassed by having each rupee have its own
        // model.
        archive_name = match item_id {
            flag::ITEMFLAGS::BLUE_RUPEE => c"GetBlueRupee".as_ptr(),
            flag::ITEMFLAGS::RED_RUPEE => c"GetRedRupee".as_ptr(),
            flag::ITEMFLAGS::SILVER_RUPEE => c"GetSilverRupee".as_ptr(),
            flag::ITEMFLAGS::GOLD_RUPEE => c"GetGoldRupee".as_ptr(),
            flag::ITEMFLAGS::RUPOOR => c"GetRupoor".as_ptr(),
            _ => archive_name,
        };

        (*shop_sample).arc_name =
            *(item::resolve_progressive_item_models(archive_name, item_id as u16, 1)
                as *mut [u8; 30]);

        // Fix model name
        let mut model_name = (*shop_sample).model_name.as_ptr() as *const c_char;
        (*shop_sample).model_name =
            *(item::resolve_progressive_item_models(model_name, item_id as u16, 2)
                as *mut [u8; 24]);

        // Replaced instructions
        asm!("mov w8, #0xFFFF", "mov w1, {0:w}", in(reg) (*shop_sample).spawn_storyflag);
    }
}
