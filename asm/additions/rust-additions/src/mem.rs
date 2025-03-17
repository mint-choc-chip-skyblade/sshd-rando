#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

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

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn debug_print_heap_info() {
    unsafe {
        debug::debug_print(c"".as_ptr());
        debug::debug_print(c"Heap Info:".as_ptr());
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"Current Heap:".as_ptr());
        if sCurrentHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*sCurrentHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*sCurrentHeap).vtable).get_total_free_size)(sCurrentHeap) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mDvd__l_ArchiveHeap:".as_ptr());
        if mDvd__l_ArchiveHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mDvd__l_ArchiveHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mDvd__l_ArchiveHeap).vtable).get_total_free_size)(mDvd__l_ArchiveHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mDvd__l_CommandHeap:".as_ptr());
        if mDvd__l_CommandHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mDvd__l_CommandHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mDvd__l_CommandHeap).vtable).get_total_free_size)(mDvd__l_CommandHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_archiveHeap:".as_ptr());
        if mHeap__g_archiveHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_archiveHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_archiveHeap).vtable).get_total_free_size)(mHeap__g_archiveHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_commandHeap:".as_ptr());
        if mHeap__g_commandHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_commandHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_commandHeap).vtable).get_total_free_size)(mHeap__g_commandHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_assertHeap:".as_ptr());
        if mHeap__g_assertHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_assertHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_assertHeap).vtable).get_total_free_size)(mHeap__g_assertHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_dylinkHeap:".as_ptr());
        if mHeap__g_dylinkHeap != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_dylinkHeap).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_dylinkHeap).vtable).get_total_free_size)(mHeap__g_dylinkHeap)
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__s_SavedCurrentHeap:".as_ptr());
        if mHeap__s_SavedCurrentHeap != core::ptr::null_mut() {
            debug::debug_print_str(
                c"Heap Name: %s".as_ptr(),
                (*mHeap__s_SavedCurrentHeap).mName,
            );
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__s_SavedCurrentHeap).vtable).get_total_free_size)(
                    mHeap__s_SavedCurrentHeap,
                ) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        // Crashes as not null but also not a standard heap
        //
        // debug::debug_print(c"SOME_HEAP:".as_ptr());
        // if SOME_HEAP != core::ptr::null_mut() {
        //     debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*SOME_HEAP).mName);
        //     debug::debug_print_num(
        //         c"Total Free Size: %d".as_ptr(),
        //         ((*(*SOME_HEAP).vtable).get_total_free_size)(SOME_HEAP) as usize,
        //     );
        // } else {
        //     debug::debug_print(c"Is nullptr:".as_ptr());
        // }
        // debug::debug_print(c"".as_ptr());

        debug::debug_print(c"WORK1_HEAP:".as_ptr());
        if WORK1_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*WORK1_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*WORK1_HEAP).vtable).get_total_free_size)(WORK1_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"WORK2_HEAP:".as_ptr());
        if WORK2_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*WORK2_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*WORK2_HEAP).vtable).get_total_free_size)(WORK2_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"WORK_EX_HEAP:".as_ptr());
        if WORK_EX_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*WORK_EX_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*WORK_EX_HEAP).vtable).get_total_free_size)(WORK_EX_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"LAYOUT_HEAP:".as_ptr());
        if LAYOUT_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*LAYOUT_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*LAYOUT_HEAP).vtable).get_total_free_size)(LAYOUT_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"LAYOUT_EX_HEAP:".as_ptr());
        if LAYOUT_EX_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*LAYOUT_EX_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*LAYOUT_EX_HEAP).vtable).get_total_free_size)(LAYOUT_EX_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"LAYOUT_EX2_HEAP:".as_ptr());
        if LAYOUT_EX2_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*LAYOUT_EX2_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*LAYOUT_EX2_HEAP).vtable).get_total_free_size)(LAYOUT_EX2_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"LAYOUT_RES_HEAP:".as_ptr());
        if LAYOUT_RES_HEAP != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*LAYOUT_RES_HEAP).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*LAYOUT_RES_HEAP).vtable).get_total_free_size)(LAYOUT_RES_HEAP) as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_gameHeaps[0]:".as_ptr());
        if mHeap__g_gameHeaps[0] != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_gameHeaps[0]).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_gameHeaps[0]).vtable).get_total_free_size)(mHeap__g_gameHeaps[0])
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        debug::debug_print(c"mHeap__g_gameHeaps[1]:".as_ptr());
        if mHeap__g_gameHeaps[1] != core::ptr::null_mut() {
            debug::debug_print_str(c"Heap Name: %s".as_ptr(), (*mHeap__g_gameHeaps[1]).mName);
            debug::debug_print_num(
                c"Total Free Size: %d".as_ptr(),
                ((*(*mHeap__g_gameHeaps[1]).vtable).get_total_free_size)(mHeap__g_gameHeaps[1])
                    as usize,
            );
        } else {
            debug::debug_print(c"Is nullptr:".as_ptr());
        }
        debug::debug_print(c"".as_ptr());

        // Crashes as not null but also not a standard heap
        //
        // debug::debug_print(c"mHeap__g_gameHeaps[2]:".as_ptr());
        // if mHeap__g_gameHeaps[2] != core::ptr::null_mut() {
        //     debug::debug_print_str(c"Heap Name: %s".as_ptr(),
        // (*mHeap__g_gameHeaps[2]).mName);     debug::debug_print_num(
        //         c"Total Free Size: %d".as_ptr(),
        //         ((*(*mHeap__g_gameHeaps[2]).vtable).
        // get_total_free_size)(mHeap__g_gameHeaps[2])             as usize,
        //     );
        // } else {
        //     debug::debug_print(c"Is nullptr:".as_ptr());
        // }
        // debug::debug_print(c"".as_ptr());

        // Crashes as not null but also not a standard heap
        //
        // debug::debug_print(c"mHeap__g_gameHeaps[3]:".as_ptr());
        // if mHeap__g_gameHeaps[3] != core::ptr::null_mut() {
        //     debug::debug_print_str(c"Heap Name: %s".as_ptr(),
        // (*mHeap__g_gameHeaps[3]).mName);     debug::debug_print_num(
        //         c"Total Free Size: %d".as_ptr(),
        //         ((*(*mHeap__g_gameHeaps[3]).vtable).
        // get_total_free_size)(mHeap__g_gameHeaps[3])             as usize,
        //     );
        // } else {
        //     debug::debug_print(c"Is nullptr:".as_ptr());
        // }
        // debug::debug_print(c"".as_ptr());

        debug::debug_print(c"".as_ptr());
    }
}
