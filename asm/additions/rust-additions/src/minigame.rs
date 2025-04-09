#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::flag;
use crate::item;
use crate::savefile;

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

#[repr(i32)]
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum MinigameState {
    State0,
    BambooCutting,
    FunFunIsland,
    ThrillDigger,
    PumpkinCarry,
    BugHeaven,
    PumpkinArchery,
    RicketyCoaster,
    SilentRealmTimeTrial,
    BossRush,
    HouseCleaning,
    SpiralChargeTutorial,
    HarpPlaying,
    StateNone = -1,
}

impl MinigameState {
    pub fn get() -> Self {
        unsafe { MINIGAME_STATE }
    }

    pub fn is_current(self) -> bool {
        Self::get() == self
    }
}

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut savefile::FileMgr;

    static mut MINIGAME_STATE: MinigameState;

    static mut BOSS_RUSH_CURRENT_SCENEINDEX: u16;
    static mut BOSS_RUSH_STORYFLAG_STATES: u16;

    static mut BOSS_RUSH_SCENEFLAG_BKP: [u16; 8];
    static mut BOSS_RUSH_DUNGEONFLAG_BKP: [u16; 8];

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

#[no_mangle]
pub fn prevent_minigame_death(final_health: i32) -> (u32, i32) {
    unsafe {
        let mut new_final_health = final_health;
        // Set final health to 1 if we're in the thrill digger or bug heaven minigames
        if new_final_health <= 0
            && (MinigameState::ThrillDigger.is_current() || MinigameState::BugHeaven.is_current())
        {
            new_final_health = 1;
        }

        // Replaced Code
        let mut restricted_pouch: u32 = 0;
        if flag::check_storyflag(166) == 1 {
            restricted_pouch = 1;
        }

        return (restricted_pouch, new_final_health);
    }
}

#[no_mangle]
pub fn try_end_pumpkin_archery(bell_actor: *mut actor::dAcObell) -> *mut actor::dAcObell {
    unsafe {
        if ((*bell_actor).field_0x860 & 1) == 1 {
            let npc_pcs = actor::find_actor_by_type(actor::ACTORID::NPC_PCS, core::ptr::null_mut())
                as *mut actor::dAcNpcPcs;
            if npc_pcs != core::ptr::null_mut() {
                (*npc_pcs).pumpkin_archery_timer = 0;
            }
            asm!("mov w8, #1")
        } else {
            asm!("mov w8, #0")
        }
    }

    return bell_actor;
}

#[no_mangle]
pub fn boss_rush_backup_flags(sceneindex: u16) {
    unsafe {
        BOSS_RUSH_CURRENT_SCENEINDEX = sceneindex;

        BOSS_RUSH_SCENEFLAG_BKP = (*FILE_MGR).FA.sceneflags[sceneindex as usize];
        BOSS_RUSH_DUNGEONFLAG_BKP = (*FILE_MGR).FA.dungeonflags[sceneindex as usize];

        BOSS_RUSH_STORYFLAG_STATES = 0x0000;

        // 131 = Imp 1 Defeated (shouldn't be necessary due to separate asm patch)
        BOSS_RUSH_STORYFLAG_STATES |= flag::check_storyflag(131) as u16;
        // 132 = Imp 2 Defeated
        BOSS_RUSH_STORYFLAG_STATES |= (flag::check_storyflag(132) << 1) as u16;
        // 648 = Koloktos Defeated
        BOSS_RUSH_STORYFLAG_STATES |= (flag::check_storyflag(648) << 2) as u16;
    }
}

#[no_mangle]
pub fn boss_rush_restore_flags() {
    unsafe {
        let sceneindex = BOSS_RUSH_CURRENT_SCENEINDEX;
        BOSS_RUSH_CURRENT_SCENEINDEX == 0xFFFF;

        (*FILE_MGR).FA.sceneflags[sceneindex as usize] = BOSS_RUSH_SCENEFLAG_BKP;
        (*FILE_MGR).FA.dungeonflags[sceneindex as usize] = BOSS_RUSH_DUNGEONFLAG_BKP;

        // 131 = Imp 1
        if (BOSS_RUSH_STORYFLAG_STATES & 0x1) == 1 {
            flag::set_storyflag(131);
        } else {
            flag::unset_storyflag(131);
        }

        // 131 = Imp 2
        if (BOSS_RUSH_STORYFLAG_STATES & 0x2) == 2 {
            flag::set_storyflag(132);
        } else {
            flag::unset_storyflag(132);
        }

        // 648 = Koloktos
        if (BOSS_RUSH_STORYFLAG_STATES & 0x4) == 4 {
            flag::set_storyflag(648);
        } else {
            flag::unset_storyflag(648);
        }

        BOSS_RUSH_STORYFLAG_STATES = 0x0000;
    }
}
