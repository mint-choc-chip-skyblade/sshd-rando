#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::debug;
use crate::flag;
use crate::input;
use crate::savefile;
use crate::settings;

use core::arch::asm;
use core::ffi::{c_char, c_int, c_void};
use static_assertions::assert_eq_size;
use wchar::wch;

// repr(C) prevents rust from reordering struct fields.
// packed(1) prevents rust from aligning structs to the size of the largest
// field.

// Using u64 or 64bit pointers forces structs to be 8-byte aligned.
// The vanilla code seems to be 4-byte aligned. To make extra sure, used
// packed(1) to force the alignment to match what you define.

// Always add an assert_eq_size!() macro after defining a struct to ensure it's
// the size you expect it to be.

// Lyt stuff
#[repr(C, packed(1))]
pub struct dLytMsgWindow {
    pub _0:       [u8; 0xA90],
    pub text_mgr: *mut TextMgr,
}
assert_eq_size!([u8; 0xA98], dLytMsgWindow);

#[repr(C, packed(1))]
pub struct dLytPauseDisp {
    pub _0:        [u8; 0xC5E],
    pub is_paused: bool,
    pub _1:        [u8; 0x11],
}
assert_eq_size!([u8; 0xC70], dLytPauseDisp);

// Text stuff
#[repr(C, packed(1))]
pub struct TextMgr {
    pub _0:                 [u8; 0x8AC],
    pub numeric_args:       [u32; 10],
    pub num_args_copy:      [u32; 10],
    pub _1:                 [u8; 0x20],
    pub vertical_scale:     f32,
    pub cursor_pos_y:       f32,
    pub msg_window_subtype: u8,
    pub _2:                 [u8; 0xCF],
    pub command_insert:     i32,
    pub string_args:        [[u16; 64]; 4],
}
assert_eq_size!([u8; 0xBF8], TextMgr);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static mut CURRENT_STAGE_NAME: [u8; 8];
    static dManager__sInstance: *mut c_void;
    static GLOBAL_TEXT_MGR: *mut TextMgr;
    static FILE_MGR: *mut savefile::FileMgr;
    static RANDOMIZER_SETTINGS: settings::RandomizerSettings;

    // Functions
    fn debugPrint_32(string: *const c_char, fstr: *const c_char, ...);
    fn set_string_arg(text_mgr: *mut TextMgr, arg: *const c_void, arg_num: u32);
    fn getTextMessageByLabel(
        param1: *mut c_void,
        param2: *mut c_void,
        param3: u32,
        param4: u32,
        param5: u32,
    ) -> *mut c_void;
    fn eventFlowTextProcessingRelated(
        param1: *mut c_void,
        param2: *mut c_void,
        text_string: *mut c_void,
        buffer: *mut c_void,
        buffer_size: i32,
        param6: u64,
    );
    fn get_msb_text_maybe(msbt_info: *mut c_void, tutorial_text_name: *mut c_void) -> *mut c_void;
    fn dLytHelp__stateNoneUpdate(dLytHelp: *mut c_void);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub extern "C" fn set_top_dowsing_icon() -> u32 {
    unsafe {
        if &CURRENT_STAGE_NAME[..5] == b"F103\0" {
            return 0x11; // Tadtones
        }
        if flag::check_storyflag(271) != 0 {
            return 0x12; // Sandship
        }
        return 0x13; // Zelda
    }
}

const COMPLETE_TEXT: *const c_void = wch!(u16, "Completed\0").as_ptr() as *const c_void;
const INCOMPLETE_TEXT: *const c_void = wch!(u16, "Incomplete\0").as_ptr() as *const c_void;
const OBTAINED_TEXT: *const c_void = wch!(u16, "Obtained\0").as_ptr() as *const c_void;
const NOT_OBTAINED_TEXT: *const c_void = wch!(u16, "Not Obtained\0").as_ptr() as *const c_void;

#[no_mangle]
pub extern "C" fn __set_dungeon_string_and_numeric_args(complete_storyflag: u16, sceneindex: u16) {
    unsafe {
        // Check if dungeon is complete
        if flag::check_storyflag(complete_storyflag) == 0 {
            set_string_arg(GLOBAL_TEXT_MGR, INCOMPLETE_TEXT, 0)
        } else {
            set_string_arg(GLOBAL_TEXT_MGR, COMPLETE_TEXT, 0)
        }

        // If don't have boss key and haven't placed boss key
        if flag::check_global_dungeonflag(sceneindex, 7) == 0
            && flag::check_global_dungeonflag(sceneindex, 8) == 0
        {
            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 1)
        } else {
            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 1)
        }

        // Small Keys
        (*GLOBAL_TEXT_MGR).numeric_args[0] =
            ((*FILE_MGR).FA.dungeonflags[sceneindex as usize][1] & 0xF) as u32;
        (*GLOBAL_TEXT_MGR).numeric_args[1] =
            (((*FILE_MGR).FA.dungeonflags[sceneindex as usize][1] >> 4) & 0xF) as u32;

        // Map
        if flag::check_global_dungeonflag(sceneindex, 1) == 0 {
            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 2)
        } else {
            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 2)
        }
    }
}

#[no_mangle]
pub extern "C" fn check_help_index_bounds(dLytHelp: *mut c_void, mut help_index: u32) {
    if help_index <= 0x3A {
        help_index = 0x3B;
    }

    unsafe {
        asm!("mov x0, {0:x}", in(reg) dLytHelp);
        asm!("mov w1, {0:w}", in(reg) help_index);
    }
}

#[no_mangle]
pub extern "C" fn set_help_menu_strings(param1: *mut c_void, help_index: u32) {
    unsafe {
        let help_number: u32;
        asm!("mov {0:w}, w28", out(reg) help_number);

        match help_index {
            0x3B => {
                match help_number {
                    1 => {
                        // Skyview Temple
                        __set_dungeon_string_and_numeric_args(5, 11)
                    },
                    2 => {
                        // Earth Temple
                        __set_dungeon_string_and_numeric_args(7, 14);
                        (*GLOBAL_TEXT_MGR).numeric_args[0] =
                            flag::check_itemflag(flag::ITEMFLAGS::KEY_PIECE_COUNTER);
                    },
                    3 => {
                        // Lanayru Mining Facility
                        __set_dungeon_string_and_numeric_args(935, 17);
                    },
                    _ => {},
                }
            },
            0x3C => {
                match help_number {
                    1 => {
                        // Ancient Cistern
                        __set_dungeon_string_and_numeric_args(900, 12);
                    },
                    2 => {
                        // Sandship
                        __set_dungeon_string_and_numeric_args(15, 18);
                    },
                    3 => {
                        // Check if Fire Sanctuary is complete
                        __set_dungeon_string_and_numeric_args(901, 15);
                    },
                    _ => {},
                }
            },
            0x3D => {
                match help_number {
                    1 => {
                        // Sky Keep (placeholder storyflag)
                        __set_dungeon_string_and_numeric_args(4, 17);
                        let sk_scenflag = RANDOMIZER_SETTINGS.sky_keep_beaten_sceneflag;

                        if sk_scenflag != -1
                            && flag::check_global_sceneflag(20, sk_scenflag as u16) == 0
                        {
                            set_string_arg(GLOBAL_TEXT_MGR, INCOMPLETE_TEXT, 0)
                        } else {
                            set_string_arg(GLOBAL_TEXT_MGR, COMPLETE_TEXT, 0)
                        }
                    },
                    2 => {
                        // Spiral Charge
                        if flag::check_itemflag(flag::ITEMFLAGS::BIRD_STATUETTE) == 0 {
                            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 0);
                        } else {
                            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 0);
                        }

                        if flag::check_itemflag(flag::ITEMFLAGS::SCRAPPER) == 0 {
                            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 1);
                        } else {
                            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 1);
                        }

                        // Group of Tadtone count
                        (*GLOBAL_TEXT_MGR).numeric_args[0] = flag::check_storyflag(953);
                    },
                    3 => {
                        // Check thunder dragon reward given storyflag too
                        if flag::check_itemflag(flag::ITEMFLAGS::LIFE_TREE_FRUIT) == 0
                            && flag::check_storyflag(462) == 0
                        {
                            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 0);
                        } else {
                            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 0);
                        }

                        // Check storyflag for after planting the seedling
                        if flag::check_itemflag(flag::ITEMFLAGS::LIFE_TREE_SEEDLING) == 0
                            && flag::check_storyflag(750) == 0
                        {
                            set_string_arg(GLOBAL_TEXT_MGR, NOT_OBTAINED_TEXT, 1);
                        } else {
                            set_string_arg(GLOBAL_TEXT_MGR, OBTAINED_TEXT, 1);
                        }

                        // Check Lanayru Caves Small Keys
                        (*GLOBAL_TEXT_MGR).numeric_args[0] =
                            ((*FILE_MGR).FA.dungeonflags[9][1] & 0xF) as u32;
                        (*GLOBAL_TEXT_MGR).numeric_args[1] =
                            (((*FILE_MGR).FA.dungeonflags[9][1] >> 4) & 0xF) as u32;
                    },
                    _ => {},
                }
            },
            _ => {},
        }

        asm!("mov x0, {0:x}", in(reg) param1);
        asm!("mov w1, {0:w}", in(reg) help_index - 0x3b);
    }
}

#[no_mangle]
pub extern "C" fn left_justify_help_text() {
    unsafe {
        asm!(
            "add x20, x19, x20, LSL #0x3",
            "ldr x0, [x20, #0x548]",
            "strb wzr, [x0, #0x13c]",
            "ldr x0, [x20, #0x560]",
            "strb wzr, [x0, #0x13c]",
            "ldr x0, [x20, #0x518]"
        );
    }
}

#[no_mangle]
pub extern "C" fn custom_help_menu_state_change(dLytHelp: *mut c_void) -> u32 {
    if input::check_button_pressed_down(input::BUTTON_INPUTS::DPAD_LEFT_BUTTON) {
        return 2; // Close help menu
    }

    if !input::check_button_pressed_down(input::BUTTON_INPUTS::DPAD_RIGHT_BUTTON) {
        return 0; // Continue as normal
    }

    // Trigger stateIn again
    unsafe {
        asm!("mov x0, {0:x}", in(reg) dLytHelp);
        asm!("mov w8, #1");
        asm!("str w8, [x0, #0x5a0]");

        // Increment help_index
        let mut help_index: u32;
        asm!("ldr {0:w}, [x0, #0x5a4]", out(reg) help_index);
        if help_index == 0x3D {
            help_index = 0;
        } else if help_index <= 0x3A {
            help_index = 0x3C;
        } else {
            help_index += 1;
        }
        asm!("str {0:w}, [x0, #0x5a4]", in(reg) help_index);

        if help_index == 0 {
            return 2; // Close help menu
        }

        dLytHelp__stateNoneUpdate(dLytHelp)
    }

    return 1; // Ret, don't close help menu
}

// Adapted from SDR:
// https://github.com/ssrando/ssrando/blob/029545b5e1d73ef515a1d61fc69b572946d45399/asm/custom-functions/src/rando/mod.rs#L614
#[no_mangle]
extern "C" fn get_tablet_keyframe_count() -> c_int {
    // The tablet frames effectively start with a Gray Code, the continuation of
    // which looks like this:
    //
    // Count     Emerald   Ruby      Amber     As Index
    // 0         0         0         0         0
    // 1         1         0         0         1
    // 2         1         1         0         3
    // 3         1         1         1         7
    // 4         1         0         1         5
    // 5         0         0         1         4
    // 6         0         1         1         6
    // 7         0         1         0         2

    const TABLET_BITMAP_TO_KEYFRAME: [u8; 8] = [0, 1, 7, 2, 5, 4, 6, 3];

    let item_bitmap = flag::check_itemflag(flag::ITEMFLAGS::EMERALD_TABLET) as usize
        | ((flag::check_itemflag(flag::ITEMFLAGS::RUBY_TABLET) as usize) << 1)
        | ((flag::check_itemflag(flag::ITEMFLAGS::AMBER_TABLET) as usize) << 2);

    return TABLET_BITMAP_TO_KEYFRAME[item_bitmap & 0x7] as i32;
}

#[no_mangle]
extern "C" fn override_inventory_caption_item_text(
    string: *const c_char,
    fstr: *const c_char,
    mut itemid: u32,
) {
    unsafe {
        // Is tablet
        if itemid == 177 || itemid == 178 || itemid == 179 {
            // Use a the same system as in get_tablet_keyframe_count
            // Item ids 181 -> 185 are unused in vanilla. Rando replaces them
            const TABLET_BITMAP_TO_TEXTID: [u32; 8] = [999, 177, 184, 178, 182, 181, 183, 179];

            let item_bitmap = flag::check_itemflag(flag::ITEMFLAGS::EMERALD_TABLET) as usize
                | ((flag::check_itemflag(flag::ITEMFLAGS::RUBY_TABLET) as usize) << 1)
                | ((flag::check_itemflag(flag::ITEMFLAGS::AMBER_TABLET) as usize) << 2);

            itemid = TABLET_BITMAP_TO_TEXTID[item_bitmap & 0x7];
        }
        debugPrint_32(string, fstr, itemid);
        asm!("mov x8, {0:x}", in(reg) dManager__sInstance);
    }
}
