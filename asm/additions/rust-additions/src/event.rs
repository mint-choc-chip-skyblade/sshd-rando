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

// Event
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct EventMgr {
    pub _0:             [u8; 0x10],
    pub event_owner:    [u8; 0x18],
    pub linked_actor:   [u8; 0x18],
    pub _1:             [u8; 8],
    pub actual_event:   Event,
    pub _2:             [u8; 0x160],
    pub event:          Event,
    pub probably_state: u32,
    pub state_flags:    u32,
    pub skipflag:       u16,
    pub _3:             [u8; 14],
}
assert_eq_size!([u8; 0x260], EventMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct Event {
    pub vtable:         u64,
    pub eventid:        u32,
    pub event_flags:    u32,
    pub roomid:         i32,
    pub tool_dataid:    i32,
    pub event_name:     [u8; 32],
    pub event_zev_data: u64,
    pub callbackFn1:    u64,
    pub callbackFn2:    u64,
}
assert_eq_size!([u8; 0x50], Event);

// Harp stuff
// Not sure what this stuff is all about
// Used to keep vanilla checks for isPlayingHarp (see SD for more details)
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct HarpRelated {
    pub unk:                                 [u8; 0x30],
    pub some_check_for_continuous_strumming: u64,
    pub unk1:                                [u8; 0x22],
    pub some_other_harp_thing:               u8,
}

// Event Flow stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorEventFlowMgr {
    pub vtable:                     u64,
    pub msbf_info:                  u64,
    pub current_flow_index:         u32,
    pub _0:                         [u8; 12],
    pub result_from_previous_check: u32,
    pub current_text_label_name:    [u8; 32],
    pub _1:                         [u8; 12],
    pub next_flow_delay_timer:      u32,
    pub another_flow_element:       EventFlowElement,
    pub _2:                         [u8; 12],
}
assert_eq_size!([u8; 0x70], ActorEventFlowMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct EventFlowElement {
    pub typ:     u8,
    pub subtype: u8,
    pub pad:     u16,
    pub param1:  u16,
    pub param2:  u16,
    pub next:    u16,
    pub param3:  u16,
    pub param4:  u16,
    pub param5:  u16,
}
assert_eq_size!([u8; 0x10], EventFlowElement);
