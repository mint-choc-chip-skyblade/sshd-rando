#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;

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
pub struct Heap {
    pub vtable:       *mut HeapVtable,
    pub containHeap:  *mut Heap,
    pub mLink:        [u8; 0x10],
    pub heapHandle:   [u8; 0x8],
    pub mParentBlock: [u8; 0x8],
    pub mFlag:        u16,
    pub _0:           [u8; 0x2],
    pub mNode:        [u8; 0x10],
    pub _1:           [u8; 0x4],
    pub mChildren:    [u8; 0x14],
    pub _2:           [u8; 0x4],
    pub mName:        *const c_char,
}
assert_eq_size!([u8; 0x68], Heap);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct HeapVtable {
    pub dt1:                  extern "C" fn(heap: *mut Heap),
    pub dt2:                  extern "C" fn(heap: *mut Heap),
    pub get_heap_type:        extern "C" fn(heap: *mut Heap) -> u32,
    pub init_allocator:       extern "C" fn(heap: *mut Heap, allocator: u64, align: i32),
    pub alloc:                extern "C" fn(heap: *mut Heap, size: i32, alignment: i32) -> u64,
    pub free:                 extern "C" fn(heap: *mut Heap, to_free: *mut c_void) -> u64,
    pub destroy:              extern "C" fn(heap: *mut Heap),
    pub resize_for_m_block:   extern "C" fn(heap: *mut Heap, block: *mut c_void, size: i32) -> u32,
    pub get_total_free_size:  extern "C" fn(heap: *mut Heap) -> i32,
    pub get_allocatable_size: extern "C" fn(heap: *mut Heap, alignment: i32) -> i32,
    pub adjust:               extern "C" fn(heap: *mut Heap) -> i32,
}
assert_eq_size!([u8; 0x58], HeapVtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct RootHeapsMgr {
    pub vtable:             *mut RootHeapsMgrVtable,
    pub root_heap1_start:   u64,
    pub root_heap1_end:     u64,
    pub root_heap2_start:   u64,
    pub root_heap2_end:     u64,
    pub mem_size:           u64,
    pub root_heap1:         *mut Heap,
    pub root_heap2:         *mut Heap,
    pub debug_heap:         *mut Heap,
    pub egg_sys_heap:       *mut Heap, // ExpHeap
    pub current_thread:     *mut c_void,
    pub virt_start_maybe:   u64,
    pub system_heap_start:  u64,
    pub system_heap_size:   u64,
    pub graphics_fifo_size: u64,
    pub snd_audio_mgr:      *mut c_void,
    pub video:              *mut c_void,
    pub xfb_mgr:            *mut c_void,
    pub async_display:      *mut c_void,
    pub perf_view:          *mut c_void,
    pub scn_mgr:            *mut c_void,
}
assert_eq_size!([u8; 0xA8], RootHeapsMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct RootHeapsMgrVtable {
    pub get_video_or_render_modeobj: extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub get_system_heap:             extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> *mut Heap,
    pub get_display:                 extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub get_xfb_mgr:                 extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub get_perf_view:               extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub get_scene_mgr:               extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub get_snd_audio_mgr:           extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub on_begin_frame:              extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub on_end_frame:                extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub init_render_mode:            extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub initialize_inner:            extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub run:                         extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
    pub initialize:                  extern "C" fn(rheaps_mgr: *mut RootHeapsMgr) -> u64,
}
assert_eq_size!([u8; 0x68], RootHeapsMgrVtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ArcMgr {
    pub vtable:         u64,
    pub entries:        *mut [ArcEntry; 400],
    pub entry_count:    u16,
    pub _0:             [u8; 0x6],
    pub stage_arc_type: u64,
}
assert_eq_size!([u8; 0x20], ArcMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct StageArcMgr {
    pub vtable:                         u64,
    pub stage_name:                     [c_char; 32],
    pub current_loading_stage_arc_name: [c_char; 32],
    pub stage_extra_layer_arc_name:     [c_char; 32],
    pub entries:                        *mut [ArcEntry; 400],
    pub entry_count:                    u16,
    pub _0:                             [u8; 0x6],
    pub stage_arc_type:                 u64,
}
assert_eq_size!([u8; 0x80], StageArcMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ArcEntry {
    pub arc_name:  [c_char; 32],
    pub ref_count: i16,
    pub _0:        [u8; 0x6],
    pub dvd_req:   u64,
    pub arc:       *mut Arc,
    pub heap:      *mut Heap,
    pub _1:        [u8; 0x18],
}
assert_eq_size!([u8; 0x58], ArcEntry);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct Arc {
    pub vtable:            u64,
    pub disposer:          [u8; 0x18],
    pub mount_type:        i32,
    pub ref_count:         i32,
    pub arc_start_address: u64,
    pub fst_start:         u64,
    pub file_start:        u64,
    pub entry_num:         u32,
    pub _0:                [u8; 0x4],
    pub fst_string_start:  *const c_char,
    pub fst_len:           i32,
    pub current_dir:       i32,
    pub dvd_entry_num:     i32,
    pub _1:                [u8; 0x4],
    pub nand_file:         u64,
    pub _2:                [u8; 0x20],
}
assert_eq_size!([u8; 0x88], Arc);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct xtxThing {
    pub unk_ptr:        u64,
    pub some_index:     u32,
    pub _0:             [u8; 0x4],
    pub file_extension: *const c_char,
    pub heap:           *mut Heap,
    pub align:          i32,
    pub _1:             [u8; 0x4],
    pub arc_name:       [u8; 32],
}
assert_eq_size!([u8; 0x48], xtxThing);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static sCurrentHeap: *mut Heap;
    static mDvd__l_ArchiveHeap: *mut Heap;
    static mDvd__l_CommandHeap: *mut Heap;
    static mHeap__g_gameHeaps: [*mut Heap; 4];
    static mHeap__g_archiveHeap: *mut Heap;
    static mHeap__g_assertHeap: *mut Heap;
    static mHeap__g_commandHeap: *mut Heap;
    static mHeap__g_dylinkHeap: *mut Heap;
    static mHeap__s_SavedCurrentHeap: *mut Heap;
    static SOME_HEAP: *mut Heap;
    static WORK1_HEAP: *mut Heap;
    static WORK2_HEAP: *mut Heap;
    static WORK_EX_HEAP: *mut Heap;
    static LAYOUT_HEAP: *mut Heap;
    static LAYOUT_EX_HEAP: *mut Heap;
    static LAYOUT_EX2_HEAP: *mut Heap;
    static LAYOUT_RES_HEAP: *mut Heap;

    static ARC_MGR: *mut ArcMgr;
    static STAGE_ARC_MGR: *mut StageArcMgr;

    static mut NEXT_STAGE_NAME: [u8; 8];

    static mut BZS_STRING: [c_char; 32];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn strcmp(s1: *const c_char, s2: *const c_char) -> i32;
    fn allocateNewActor(
        actorid: actor::ACTORID,
        connect_parent: *const actor::ActorTreeNode,
        actor_param1: u32,
        actor_group_type: u8,
    ) -> *mut actor::dBase;
    fn EGG__Archive__mount(p1: *mut c_void, p2: *mut Heap, p3: i32, p4: *const c_char) -> *mut Arc;
    fn dRawArcEntry_c__destroy(arc_entry: *mut ArcEntry, stage_arc_type: u64);
    fn dRawArcTable_c__getArcOrLoadFromDisk(
        arc_table: *mut c_void,
        arc_name: *const c_char,
        parent_dir_name: *const c_char,
        heap: *mut c_void,
    );
    fn dRawArcTable_c__getDataFromOarc(
        arc_table: *mut c_void,
        arc_name: *const c_char,
        model_path: *const c_char,
    ) -> *mut c_void; // actually *mut ResFile
    fn dRawArcTable_c__addEntryFromParentArc(
        arc_table: *mut c_void,
        arc_name: *const c_char,
        some_ptr: *mut c_void,
        heap: *mut c_void,
    );
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub extern "C" fn fix_memory_leak(
    u8File: *mut c_void,
    heap: *mut Heap,
    align: i32,
    xtx_thing_file_extension: *const c_char,
    xtx_thing: *mut xtxThing,
) -> u32 {
    unsafe {
        let mut arc_name = (*xtx_thing).arc_name;
        // debug::debug_print(arc_name.as_ptr() as *const c_char);

        if &arc_name[..6] == b"/oarc/" {
            let mut arc_name_len = 0_usize;

            for c in &arc_name[6..] {
                if *c == 0 {
                    break;
                }
                arc_name_len += 1;
            }

            arc_name[6 + arc_name_len - 4] = 0;

            let arc_name_cstr = arc_name[6..].as_ptr() as *const c_char;

            // Check if arc has already been loaded
            let mut current_entry_num = 0;
            let mut next_entry = (*(*ARC_MGR).entries)[current_entry_num as usize];

            while next_entry.arc_name[0] != 0 {
                if strcmp(arc_name_cstr, next_entry.arc_name.as_ptr()) == 0
                    && next_entry.ref_count >= 1
                {
                    // debug::debug_print_str(c"DUPLICATE: %s".as_ptr(), arc_name_cstr);
                    return (*xtx_thing).some_index;
                }

                current_entry_num += 1;
                next_entry = (*(*ARC_MGR).entries)[current_entry_num as usize];
            }
        }

        let new_arc = EGG__Archive__mount(u8File, heap, align, xtx_thing_file_extension);
        (*new_arc).ref_count = 0;

        return (*xtx_thing).some_index;
    }
}

#[no_mangle]
pub extern "C" fn arc_table_print(p1: actor::ACTORID, p2: *const actor::ActorTreeNode) {
    unsafe {
        let mut current_entry_num = 0;
        let mut next_entry = (*(*ARC_MGR).entries)[current_entry_num as usize];

        while next_entry.arc_name[0] != 0 {
            debug::debug_print(next_entry.arc_name.as_ptr());
            debug::debug_print_num(c"refs: %d".as_ptr(), next_entry.ref_count as usize);
            debug::debug_print(c"".as_ptr());

            current_entry_num += 1;
            next_entry = (*(*ARC_MGR).entries)[current_entry_num as usize];
        }

        allocateNewActor(p1, p2, 0, 3);
    }
}

#[no_mangle]
pub extern "C" fn load_custom_bzs(
    arc_table: *mut c_void,
    arc_name: *const c_char,
    parent_dir_name: *const c_char,
    heap: *mut c_void,
) {
    unsafe {
        dRawArcTable_c__getArcOrLoadFromDisk(arc_table, arc_name, parent_dir_name, heap);
        dRawArcTable_c__getArcOrLoadFromDisk(arc_table, c"bzs".as_ptr(), c"Stage".as_ptr(), heap);
    }
}

#[no_mangle]
pub extern "C" fn use_custom_bzs(
    arc_table: *mut c_void,
    arc_name: *const c_char,
    model_path: *const c_char,
) -> *mut c_void {
    unsafe {
        if strcmp(model_path, (*c"dat/stage.bzs").as_ptr()) == 0 {
            let new_arc_name = (*c"bzs").as_ptr();
            let mut current_char_index = 0;

            for character in b"dat/" {
                BZS_STRING[current_char_index] = *character as i8;
                current_char_index += 1;
            }

            let mut found_string_terminator = false;
            for stage_char in &mut NEXT_STAGE_NAME[0..6] {
                if !found_string_terminator && *stage_char != 0 {
                    BZS_STRING[current_char_index] = *stage_char as i8;
                    current_char_index += 1;
                } else {
                    found_string_terminator = true;
                }
            }

            for character in b"_stage.bzs\0" {
                BZS_STRING[current_char_index] = *character as i8;
                current_char_index += 1;
            }

            asm!("mov x2, {0:x}", in(reg) &BZS_STRING);
            asm!("mov x1, {0:x}", in(reg) new_arc_name);
        } else if strcmp(model_path, (*c"dat/room.bzs").as_ptr()) == 0 {
            let new_arc_name = (*c"bzs").as_ptr();
            let mut current_char_index = 0;

            for character in b"dat/" {
                BZS_STRING[current_char_index] = *character as i8;
                current_char_index += 1;
            }

            let mut found_string_terminator = false;
            for stage_char in &mut NEXT_STAGE_NAME[0..8] {
                if !found_string_terminator && *stage_char != 0 {
                    BZS_STRING[current_char_index] = *stage_char as i8;
                    current_char_index += 1;
                } else {
                    found_string_terminator = true;
                }
            }

            for character in b"_room_" {
                BZS_STRING[current_char_index] = *character as i8;
                current_char_index += 1;
            }

            let indexable_arc_name = core::slice::from_raw_parts(arc_name, 16);
            let mut roomid_char_index = 0;

            // Get the roomid from the arc_name string
            while indexable_arc_name[roomid_char_index] != 0 {
                roomid_char_index += 1;
            }

            // b"0"
            if indexable_arc_name[roomid_char_index - 2] != 48 {
                BZS_STRING[current_char_index] = indexable_arc_name[roomid_char_index - 2];
                current_char_index += 1;
            }

            BZS_STRING[current_char_index] = indexable_arc_name[roomid_char_index - 1];
            current_char_index += 1;

            for character in b".bzs\0" {
                BZS_STRING[current_char_index] = *character as i8;
                current_char_index += 1;
            }

            asm!("mov x2, {0:x}", in(reg) &BZS_STRING);
            asm!("mov x1, {0:x}", in(reg) new_arc_name);
        } else {
            asm!("mov x2, {0:x}", in(reg) model_path);
            asm!("mov x1, {0:x}", in(reg) arc_name);
        }

        asm!("mov x0, {0:x}", in(reg) arc_table);

        // Replaced instructions
        asm!("ldrh w23, [x0, #0x8]");

        return arc_table;
    }
}

#[no_mangle]
pub extern "C" fn debug_print_heap_info(heap: *mut Heap, heap_identifier: *const c_char) {
    debug::debug_print_str(c"Heap info for: %s".as_ptr(), heap_identifier);
    if !heap.is_null() {
        debug::debug_print(c"Heap Name:".as_ptr());
        debug::debug_print(unsafe { (*heap).mName });
        debug::debug_print_num(c"Total Free Size: %d".as_ptr(), unsafe {
            ((*(*heap).vtable).get_total_free_size)(heap)
        } as usize);
    } else {
        debug::debug_print(c"Is nullptr:".as_ptr());
    }
    debug::debug_print(c"".as_ptr());
}

#[no_mangle]
pub extern "C" fn debug_print_all_heap_info() {
    let heaps = unsafe {
        [
            (sCurrentHeap, c"sCurrentHeap".as_ptr()),
            (mDvd__l_ArchiveHeap, c"mDvd__l_ArchiveHeap".as_ptr()),
            (mDvd__l_CommandHeap, c"mDvd__l_CommandHeap".as_ptr()),
            (mHeap__g_archiveHeap, c"mHeap__g_archiveHeap".as_ptr()),
            (mHeap__g_assertHeap, c"mHeap__g_assertHeap".as_ptr()),
            (mHeap__g_commandHeap, c"mHeap__g_commandHeap".as_ptr()),
            (mHeap__g_dylinkHeap, c"mHeap__g_dylinkHeap".as_ptr()),
            (
                mHeap__s_SavedCurrentHeap,
                c"mHeap__s_SavedCurrentHeap".as_ptr(),
            ),
            (WORK1_HEAP, c"WORK1_HEAP".as_ptr()),
            (WORK2_HEAP, c"WORK2_HEAP".as_ptr()),
            (WORK_EX_HEAP, c"WORK_EX_HEAP".as_ptr()),
            (LAYOUT_HEAP, c"LAYOUT_HEAP".as_ptr()),
            (LAYOUT_EX_HEAP, c"LAYOUT_EX_HEAP".as_ptr()),
            (LAYOUT_EX2_HEAP, c"LAYOUT_EX2_HEAP".as_ptr()),
            (LAYOUT_RES_HEAP, c"LAYOUT_RES_HEAP".as_ptr()),
            (mHeap__g_gameHeaps[0], c"mHeap__g_gameHeaps[0]".as_ptr()),
            (mHeap__g_gameHeaps[1], c"mHeap__g_gameHeaps[1]".as_ptr()),
        ]
    };

    debug::debug_print(c"".as_ptr());
    debug::debug_print(c"Heap Info:".as_ptr());
    debug::debug_print(c"".as_ptr());

    for (heap, heap_identifier) in heaps {
        debug_print_heap_info(heap, heap_identifier);
    }
}
