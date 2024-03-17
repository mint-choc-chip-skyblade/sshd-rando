#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::actor;
use crate::debug;
use crate::savefile;

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

// FlagMgr stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagMgr {
    pub funcs:              *mut FlagMgrFuncs,
    pub flag_size_maybe:    u32,
    pub another_size_maybe: u32,
    pub flags_ptr:          *mut FlagSpace,
    // + a bunch of other stuff that's not used
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SceneflagMgr {
    pub sceneflags:    FlagSpace,
    pub tempflags:     FlagSpace,
    pub zoneflags:     FlagSpace,
    pub _0:            u16,
    pub sceneindex:    u16,
    pub should_commit: u8,
    pub _1:            [u8; 3],
}
assert_eq_size!([u8; 0x50], SceneflagMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct DungeonflagMgr {
    pub should_commit:  u8,
    pub _0:             u8,
    pub sceneindex:     u8,
    pub _1:             [u8; 5],
    pub flagdefs:       u64,
    pub unk_flag_stuff: u64,
    pub dungeonflags:   FlagSpace,
}
assert_eq_size!([u8; 0x30], DungeonflagMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagSpace {
    pub flag_ptr:        u64,
    pub static_flag_ptr: *mut [u16; 8],
    pub flag_space_size: u16,
    pub _0:              [u8; 6],
}
assert_eq_size!([u8; 0x18], FlagSpace);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagMgrFuncs {
    pub _0:                           u64,
    pub _1:                           u64,
    pub set_flags_ptr:                u64,
    pub _2:                           u64,
    pub copy_flags_from_save:         extern "C" fn(*mut FlagMgr),
    pub setup_unk_flag_stuff:         extern "C" fn(*mut FlagMgr),
    pub do_commit:                    extern "C" fn(*mut FlagMgr),
    pub set_flag:                     extern "C" fn(*mut FlagMgr, u16),
    pub unset_flag:                   extern "C" fn(*mut FlagMgr, u16),
    pub set_flag_or_counter_to_value: extern "C" fn(*mut FlagMgr, u16, u16),
    pub get_flag_or_counter:          extern "C" fn(*mut FlagMgr, u16) -> u32,
    pub get_uncommited_value:         extern "C" fn(*mut FlagMgr, u16) -> u32,
    pub _3:                           extern "C" fn(),
    pub get_save_flag_space:          extern "C" fn(*mut FlagMgr),
}
assert_eq_size!([u8; 112], FlagMgrFuncs);

// Flag enums
#[repr(u16)]
#[derive(Copy, Clone, Hash, PartialEq, Eq)]
pub enum ITEMFLAGS {
    CUPBOARD_TEXT                    = 0x0,
    SMALL_KEY                        = 0x1,
    GREEN_RUPEE                      = 0x2,
    BLUE_RUPEE                       = 0x3,
    RED_RUPEE                        = 0x4,
    COMPLETED_TRIFORCE               = 0x5,
    HEART                            = 0x6,
    SINGLE_ARROW                     = 0x7,
    BUNDLE_OF_ARROWS                 = 0x8,
    GODDESS_WHITE_SWORD              = 0x9,
    PRACTICE_SWORD                   = 0xA,
    GODDESS_SWORD                    = 0xB,
    GODDESS_LONGSWORD                = 0xC,
    MASTER_SWORD                     = 0xD,
    TRUE_MASTER_SWORD                = 0xE,
    SAILCLOTH                        = 0xF,
    GODDESS_HARP                     = 0x10,
    SPIRIT_VESSEL                    = 0x11,
    UNK18                            = 0x12,
    BOW                              = 0x13,
    CLAWSHOTS                        = 0x14,
    BIRD_STATUETTE                   = 0x15,
    COMMON_BUG                       = 0x16,
    UNCOMMON_BUG                     = 0x17,
    RARE_BUG                         = 0x18,
    ANCIENT_CISTERN_BOSS_KEY         = 0x19,
    FIRE_SANCTUARY_BOSS_KEY          = 0x1A,
    SANDSHIP_BOSS_KEY                = 0x1B,
    KEY_PIECE                        = 0x1C,
    SKYVIEW_BOSS_KEY                 = 0x1D,
    EARTH_TEMPLE_BOSS_KEY            = 0x1E,
    LANAYRU_MINING_FACILITY_BOSS_KEY = 0x1F,
    SILVER_RUPEE                     = 0x20,
    GOLD_RUPEE                       = 0x21,
    RUPOOR                           = 0x22,
    FIVE_GRATITUDE_CRYSTALS          = 0x23,
    GLITTERING_SPORES                = 0x24,
    UNK37                            = 0x25,
    UNK38                            = 0x26,
    UNK39                            = 0x27,
    FIVE_BOMBS                       = 0x28,
    TEN_BOMBS                        = 0x29,
    STAMINA_FRUIT                    = 0x2A,
    TEAR_OF_FARORE                   = 0x2B,
    TEAR_OF_DIN                      = 0x2C,
    TEAR_OF_NAYRU                    = 0x2D,
    SACRED_TEAR                      = 0x2E,
    LIGHT_FRUIT                      = 0x2F,
    ONE_GRATITUDE_CRYSTAL            = 0x30,
    GUST_BELLOWS                     = 0x31,
    DUNGEON_MAP_FI_TEXT              = 0x32,
    DUNGEON_MAP_EMPTY                = 0x33,
    SLINGSHOT                        = 0x34,
    BEETLE                           = 0x35,
    WATER                            = 0x36,
    MUSHROOM_SPORES                  = 0x37,
    DIGGING_MITTS                    = 0x38,
    FIVE_DEKU_SEEDS                  = 0x39,
    UNK58                            = 0x3A,
    UNK59                            = 0x3B,
    TEN_DEKU_SEEDS                   = 0x3C,
    COMMON_TREASURE                  = 0x3D,
    COMMON_TREASURE2                 = 0x3E,
    UNCOMMON_TREASURE                = 0x3F,
    RARE_TREASURE                    = 0x40,
    GUARDIAN_POTION                  = 0x41,
    GUARDIAN_POTION_PLUS             = 0x42,
    UNK67                            = 0x43,
    WATER_DRAGON_SCALE               = 0x44,
    UNK69                            = 0x45,
    BUG_MEDAL                        = 0x46,
    BUG_NET                          = 0x47,
    FAIRY_WITH_BUG_NET               = 0x48,
    UNK73                            = 0x49,
    SACRED_WATER                     = 0x4A,
    HOOK_BEETLE                      = 0x4B,
    QUICK_BEETLE                     = 0x4C,
    TOUGH_BEETLE                     = 0x4D,
    HEART_POTION                     = 0x4E,
    HEART_POTION_PLUS                = 0x4F,
    UNK80                            = 0x50,
    HEART_POTION_PLUS_PLUS           = 0x51,
    UNK82                            = 0x52,
    GUARDIAN_POTION_EMPTY            = 0x53,
    STAMINA_POTION                   = 0x54,
    STAMINA_POTION_PLUS              = 0x55,
    AIR_POTION                       = 0x56,
    AIR_POTION_PLUS                  = 0x57,
    FAIRY_                           = 0x58,
    UNK89                            = 0x59,
    IRON_BOW                         = 0x5A,
    SACRED_BOW                       = 0x5B,
    BOMB_BAG                         = 0x5C,
    HEART_CONTAINER                  = 0x5D,
    HEART_PIECE                      = 0x5E,
    TRIFORCE_OF_COURAGE              = 0x5F,
    TRIFORCE_OF_POWER                = 0x60,
    TRIFORCE_OF_WISDOM               = 0x61,
    SEA_CHART                        = 0x62,
    MOGMA_MITTS                      = 0x63,
    HEART_MEDAL                      = 0x64,
    RUPEE_MEDAL                      = 0x65,
    TREASURE_MEDAL                   = 0x66,
    POTION_MEDAL                     = 0x67,
    CURSED_MEDAL                     = 0x68,
    SCATTERSHOT                      = 0x69,
    UNK106                           = 0x6A,
    UNK107                           = 0x6B,
    MEDIUM_WALLET                    = 0x6C,
    BIG_WALLET                       = 0x6D,
    GIANT_WALLET                     = 0x6E,
    TYCOON_WALLET                    = 0x6F,
    ADVENTURE_POUCH                  = 0x70,
    POUCH_EXPANSION                  = 0x71,
    LIFE_MEDAL                       = 0x72,
    UNK115                           = 0x73,
    WOODEN_SHIELD                    = 0x74,
    BANDED_SHIELD                    = 0x75,
    BRACED_SHIELD                    = 0x76,
    IRON_SHIELD                      = 0x77,
    REINFORCED_SHIELD                = 0x78,
    FORTIFIED_SHIELD                 = 0x79,
    SACRED_SHIELD                    = 0x7A,
    DIVINE_SHIELD                    = 0x7B,
    GODDESS_SHIELD                   = 0x7C,
    HYLIAN_SHIELD                    = 0x7D,
    REVITALIZING_POTION              = 0x7E,
    REVITALIZING_POTION_PLUS         = 0x7F,
    SMALL_SEED_SATCHEL               = 0x80,
    MEDIUM_SEED_SATCHEL              = 0x81,
    LAGRE_SEED_SATCHEL               = 0x82,
    SMALL_QUIVER                     = 0x83,
    MEDIUM_QUIVER                    = 0x84,
    LARGE_QUIVER                     = 0x85,
    SMALL_BOMB_BAG                   = 0x86,
    MEDIUM_BOMB_BAG                  = 0x87,
    LARGE_BOMB_BAG                   = 0x88,
    WHIP                             = 0x89,
    FIRESHIELD_EARRINGS              = 0x8A,
    UNK139                           = 0x8B,
    BIG_BUG_NET                      = 0x8C,
    FARON_GRASSHOPPER                = 0x8D,
    WOODLAND_RHINO_BEETLE            = 0x8E,
    DEKU_HORNET                      = 0x8F,
    SKYLOFT_MANTIS                   = 0x90,
    VOLCANIC_LADYBUG                 = 0x91,
    BLESSED_BUTTERFLY                = 0x92,
    LANAYRU_ANT                      = 0x93,
    SAND_CICADA                      = 0x94,
    GERUDO_DRAGONFLY                 = 0x95,
    ELDIN_ROLLER                     = 0x96,
    SKY_STAG_BEETLE                  = 0x97,
    STARRY_FIREFLY                   = 0x98,
    BOTTLE                           = 0x99,
    RUPEE_MEDAL_                     = 0x9A,
    HEART_MEDAL_                     = 0x9B,
    UNK156                           = 0x9C,
    UNK157                           = 0x9D,
    CAWLIN_LETTER                    = 0x9E,
    BEEDLES_INSECT_CAGE              = 0x9F,
    RATTLE                           = 0xA0,
    HORNET_LAVAE                     = 0xA1,
    BIRD_FEATHER                     = 0xA2,
    TUMBLEWEED                       = 0xA3,
    LIZARD_TAIL                      = 0xA4,
    ELDIN_ORE                        = 0xA5,
    ANCIENT_FLOWER                   = 0xA6,
    AMBER_RELIC                      = 0xA7,
    DUSK_RELIC                       = 0xA8,
    JELLY_BLOB                       = 0xA9,
    MONSTER_CLAW                     = 0xAA,
    MONSTER_HORN                     = 0xAB,
    ORNAMENTAL_SKULL                 = 0xAC,
    EVIL_CRYSTAL                     = 0xAD,
    BLUE_BIRD_FEATHER                = 0xAE,
    GOLDEN_SKULL                     = 0xAF,
    GODDESS_PLUME                    = 0xB0,
    EMERALD_TABLET                   = 0xB1,
    RUBY_TABLET                      = 0xB2,
    AMBER_TABLET                     = 0xB3,
    STONE_OF_TRIALS                  = 0xB4,
    UNK181                           = 0xB5,
    UNK182                           = 0xB6,
    UNK183                           = 0xB7,
    UNK184                           = 0xB8,
    UNK185                           = 0xB9,
    BALLAD_OF_THE_GODDESS            = 0xBA,
    FARORE_COURAGE                   = 0xBB,
    NAYRU_WISDOM                     = 0xBC,
    DIN_POWER                        = 0xBD,
    FARON_SONG_OF_THE_HERO_PART      = 0xBE,
    ELDIN_SONG_OF_THE_HERO_PART      = 0xBF,
    LANAYRU_SONG_OF_THE_HERO_PART    = 0xC0,
    SONG_OF_THE_HERO                 = 0xC1,
    REVITALIZING_POTION_PLUS_PLUS    = 0xC2,
    HOT_PUMPKIN_SOUP                 = 0xC3,
    COLD_PUMPKIN_SOUP                = 0xC4,
    LIFE_TREE_SEEDLING               = 0xC5,
    LIFE_TREE_FRUIT                  = 0xC6,
    EXTRA_WALLET                     = 0xC7,
    HEART_PIECE_COUNTER              = 0x1E9,
    POUCH_EXPANSION_COUNTER          = 0x1EA,
    DEKU_SEED_COUNTER                = 0x1ED,
    ARROW_COUNTER                    = 0x1F2,
    BOMB_COUNTER                     = 0x1F3,
    RUPEE_COUNTER                    = 0x1F5,
    CRYSTAL_PACK_COUNTER             = 0x1F6,
    KEY_PIECE_COUNTER                = 0x1F9,
    EXTRA_WALLET_COUNTER             = 0x1FC,
    MAX511                           = 0x1FF,
}

// Start flag stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct StartCount {
    pub counter: u16,
    pub value:   u16,
}
assert_eq_size!(u32, StartCount);

// IMPORTANT: when using vanilla code, the start point must be declared in
// symbols.yaml and then added to this extern block.
extern "C" {
    static FILE_MGR: *mut savefile::FileMgr;

    static STORYFLAG_MGR: *mut FlagMgr;
    static ITEMFLAG_MGR: *mut FlagMgr;
    static SCENEFLAG_MGR: *mut SceneflagMgr;
    static DUNGEONFLAG_MGR: *mut DungeonflagMgr;

    static mut STATIC_STORYFLAGS: [u16; 128];
    static mut STATIC_SCENEFLAGS: [u16; 8];
    static mut STATIC_TEMPFLAGS: [u16; 4];
    static mut STATIC_ZONEFLAGS: [[u16; 4]; 63];
    static mut STATIC_ITEMFLAGS: [u16; 64];
    static mut STATIC_DUNGEONFLAGS: [u16; 8];

    static mut NEXT_NIGHT: u8;
    static mut NEXT_UNK: u8;

    // Custom symbols
    static STARTFLAGS: [u16; 1000];
    static START_COUNTS: [StartCount; 50];

    static mut TRIAL_GATE_EXIT_WAIT_TIMER: u32;

    // Functions
    fn debugPrint_128(string: *const c_char, fstr: *const c_char, ...);
    fn SceneflagMgr__setFlag(sceneflag_mgr: *mut SceneflagMgr, roomid: u32, flag: u32);
    fn SceneflagMgr__unsetFlag(sceneflag_mgr: *mut SceneflagMgr, roomid: u32, flag: u32);
    fn SceneflagMgr__checkFlag(sceneflag_mgr: *mut SceneflagMgr, roomid: u32, flag: u32) -> u16;
    fn GameReloader__triggerExit(
        game_reloader: *mut actor::GameReloader,
        current_room: u32,
        exit_index: u32,
        force_night: u32,
        force_trial: u32,
    );
}

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to
// additions/rust-additions.asm

// Flags
// Storyflags
#[no_mangle]
pub fn set_storyflag(flag: u16) {
    unsafe {
        ((*(*STORYFLAG_MGR).funcs).set_flag)(STORYFLAG_MGR, flag);
    };
}

#[no_mangle]
pub fn unset_storyflag(flag: u16) {
    unsafe {
        ((*(*STORYFLAG_MGR).funcs).unset_flag)(STORYFLAG_MGR, flag);
    };
}

#[no_mangle]
pub fn check_storyflag(flag: u16) -> u32 {
    unsafe {
        return ((*(*STORYFLAG_MGR).funcs).get_flag_or_counter)(STORYFLAG_MGR, flag);
    }
}

// Sceneflags (local)
#[no_mangle]
pub fn set_local_sceneflag(flag: u32) {
    unsafe {
        return SceneflagMgr__setFlag(SCENEFLAG_MGR, 0, flag);
    }
}

#[no_mangle]
pub fn unset_local_sceneflag(flag: u32) {
    unsafe {
        return SceneflagMgr__unsetFlag(SCENEFLAG_MGR, 0, flag);
    }
}

#[no_mangle]
pub fn check_local_sceneflag(flag: u32) -> u16 {
    unsafe {
        return SceneflagMgr__checkFlag(SCENEFLAG_MGR, 0, flag);
    }
}

// Sceneflags (global)
#[no_mangle]
pub fn set_global_sceneflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

#[no_mangle]
pub fn unset_global_sceneflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] &= !(1 << lower_flag);
    }
}

#[no_mangle]
pub fn check_global_sceneflag(sceneindex: u16, flag: u16) -> u16 {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        return ((*FILE_MGR).FA.sceneflags[sceneindex as usize][upper_flag as usize] >> lower_flag)
            & 0x1;
    }
}

// Dungeonflags (global)
#[no_mangle]
pub fn set_global_dungeonflag(sceneindex: u16, flag: u16) {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        (*FILE_MGR).FA.dungeonflags[sceneindex as usize][upper_flag as usize] |= 1 << lower_flag;
    }
}

#[no_mangle]
pub fn check_global_dungeonflag(sceneindex: u16, flag: u16) -> u16 {
    let upper_flag = (flag & 0xF0) >> 4;
    let lower_flag = flag & 0x0F;

    unsafe {
        return ((*FILE_MGR).FA.dungeonflags[sceneindex as usize][upper_flag as usize]
            >> lower_flag)
            & 0x1;
    }
}

// Itemflags
#[no_mangle]
pub fn set_itemflag(flag: ITEMFLAGS) {
    unsafe {
        ((*(*ITEMFLAG_MGR).funcs).set_flag)(ITEMFLAG_MGR, flag as u16);
    }
}

#[no_mangle]
pub fn unset_itemflag(flag: ITEMFLAGS) {
    unsafe {
        ((*(*ITEMFLAG_MGR).funcs).unset_flag)(ITEMFLAG_MGR, flag as u16);
    }
}

#[no_mangle]
pub fn check_itemflag(flag: ITEMFLAGS) -> u32 {
    unsafe {
        return ((*(*ITEMFLAG_MGR).funcs).get_flag_or_counter)(ITEMFLAG_MGR, flag as u16);
    }
}

// Misc flag funcs
#[no_mangle]
pub fn set_goddess_sword_pulled_story_flag() {
    // Set story flag 951 (Raised Goddess Sword in Goddess Statue).
    set_storyflag(951);
}

#[no_mangle]
pub fn check_night_storyflag() -> bool {
    return check_storyflag(899) != 0; // 899 == day/night flag
}

#[no_mangle]
pub fn update_day_night_storyflag() {
    // debug::debug_print("Updating night flag");

    unsafe {
        // 899 == day/night storyflag
        if NEXT_NIGHT == 1 {
            // debug::debug_print("Setting night flag");
            set_storyflag(899);
        } else {
            // debug::debug_print("Unsetting night flag");
            unset_storyflag(899);
        }

        ((*(*STORYFLAG_MGR).funcs).do_commit)(STORYFLAG_MGR);

        // Replaced instruction
        NEXT_UNK = 0xFF;
    }

    return;
}

#[no_mangle]
pub fn set_stone_of_trials_placed_flag(
    game_reloader: *mut actor::GameReloader,
    current_room: u32,
    exit_index: u32,
    force_night: u32,
    force_trial: u32,
) {
    unsafe {
        GameReloader__triggerExit(
            game_reloader,
            current_room,
            exit_index,
            force_night,
            force_trial,
        )
    }

    set_storyflag(22); // 22 == Stone of Trials placed storyflag
}

#[no_mangle]
pub fn check_and_set_trial_completion_flag(trial_gate_actor: *mut actor::dAcOWarp) -> u32 {
    unsafe {
        // Array of tuples (trial index, trial completion storyflag)
        let indexes_and_flags = [(0, 919), (1, 921), (2, 920), (3, 922)];

        // Set storyflag and reset counter
        for (index, flag) in indexes_and_flags {
            if (*trial_gate_actor).trialIndex == index && check_storyflag(flag) == 0 {
                set_storyflag(flag);
                TRIAL_GATE_EXIT_WAIT_TIMER = 0;
            }
        }

        // Ensure that we wait long enough for link to receive the item being given
        // to him before exiting the trial. Wait until counter reaches 45 before
        // returning 1 to allow proceeding to exit the trial. Not sure exactly how long
        // is necessary for this, but 45 hasn't failed so far.
        TRIAL_GATE_EXIT_WAIT_TIMER += 1;
        if TRIAL_GATE_EXIT_WAIT_TIMER > 45 {
            TRIAL_GATE_EXIT_WAIT_TIMER = 45;
            return 1;
        }
        return 0;
    }
}

#[no_mangle]
pub fn handle_startflags() {
    unsafe {
        (*FILE_MGR).prevent_commit = true;

        let mut delimiter_count = 0;
        let mut pouch_item_counter = 0;

        for flag_ptr in STARTFLAGS.iter() {
            let mut flag = *flag_ptr;

            if flag == 0xFFFF {
                delimiter_count += 1;
                continue;
            }

            match delimiter_count {
                // Storyflags
                0 => {
                    ((*(*STORYFLAG_MGR).funcs).set_flag)(STORYFLAG_MGR, flag.into());
                },

                // Sceneflags
                1 => {
                    // flag = 0xFFSS where SS == sceneindex and FF == sceneflag
                    let sceneindex = flag & 0xFF;
                    let sceneflag = flag >> 8;

                    if (*SCENEFLAG_MGR).sceneindex == sceneindex {
                        set_local_sceneflag(sceneflag.into());
                    }

                    set_global_sceneflag(sceneindex, sceneflag);
                },

                // Itemflags
                2 => {
                    ((*(*ITEMFLAG_MGR).funcs).set_flag)(ITEMFLAG_MGR, flag.into());

                    // Set pouch items if applicable
                    match flag {
                        // Hylian Shield
                        125 => {
                            (*FILE_MGR).FA.pouch_items[pouch_item_counter] = 125 | 0x30 << 0x10;
                            pouch_item_counter += 1;
                        },
                        // Bottle
                        153 => {
                            (*FILE_MGR).FA.pouch_items[pouch_item_counter] = 153;
                            pouch_item_counter += 1;
                        },
                        _ => {},
                    }
                },

                // Dungeonflags
                3 => {
                    let sceneindex = flag & 0xFF;
                    flag = flag >> 8;

                    // Convert dungeonflag numbers to be like sceneflags
                    // Dungeonflags start offset by 1 due to an undefined value in the flag
                    // definitions.
                    if flag == 2 || flag == 3 || flag == 4 {
                        flag -= 1;
                    } else if flag == 12 {
                        // The rooms are defined before the boss key placed flag
                        flag = 7;
                    } else if flag == 16 {
                        flag = 8;
                    }

                    // flag = 0xFFSS where SS == sceneindex and FF == dungeonflag
                    set_global_dungeonflag(sceneindex, flag);
                },

                _ => {
                    break;
                },
            }
        }

        let mut starting_hearts: u16 = 6 * 4;

        for start_count in START_COUNTS.iter() {
            if start_count.counter == 0xFFFF {
                break;
            }

            // Total up Heart Pieces and Heart Containers for starting health
            if start_count.counter == 0x5E {
                starting_hearts += start_count.value;
            } else if start_count.counter == 0x5D {
                starting_hearts += start_count.value * 4;
            }
            // If the counter is less than 25, it's a dungeon scene
            // for small key counts. Otherwise, it's a regular item flag counter
            else if start_count.counter <= 25 {
                (*FILE_MGR).FA.dungeonflags[start_count.counter as usize][1] = start_count.value;
            } else {
                ((*(*ITEMFLAG_MGR).funcs).set_flag_or_counter_to_value)(
                    ITEMFLAG_MGR,
                    start_count.counter,
                    start_count.value,
                );
            }
        }

        // Apply starting hearts
        (*FILE_MGR).FA.health_capacity = starting_hearts;
        (*FILE_MGR).FA.current_health = starting_hearts;

        // amiibo
        (*FILE_MGR).game_options |= 1;

        ((*(*STORYFLAG_MGR).funcs).do_commit)(STORYFLAG_MGR);
        ((*(*ITEMFLAG_MGR).funcs).do_commit)(ITEMFLAG_MGR);

        (*FILE_MGR).prevent_commit = false;
    }
}
