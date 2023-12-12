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

// FileMgr/SaveFile stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FileMgr {
    pub allSaveFiles:  u64,
    pub saveTails:     u64,
    pub FA:            SaveFile,
    pub FB:            SaveFile,
    pub unkfiller:     [u8; 36],
    pub amiiboPos:     Vec3f,
    pub amiiboStage:   u64,
    pub unkfiller1:    [u8; 9534],
    pub preventCommit: bool,
    pub unk:           u8,
}

assert_eq_size!([u8; 52488], FileMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SaveFile {
    pub saveTime:               u64, // size is a guess
    pub unk:                    u64,
    pub unkfiller:              [u8; 2244],
    pub playerName:             [u16; 8],
    pub storyflags:             [u16; 128],
    pub itemflags:              [u16; 64],
    pub dungeonflags:           [[u16; 8]; 26],
    pub unkfiller1:             [u8; 3680],
    pub sceneflags:             [[u16; 8]; 26],
    pub unkfiller2:             [u8; 4960],
    pub enemyKillCounters:      [u16; 100],
    pub hitByEnemyCounters:     [u16; 100],
    pub tempflags:              [u16; 4],
    pub zoneflags:              [[u16; 4]; 63],
    pub enemyDefeatedFlags:     [u16; 4096],
    pub unkfiller3:             [u8; 14],
    pub healthCapacity:         u16,
    pub someHealthRelatedThing: u16,
    pub currentHealth:          u16,
    pub unkfiller4:             [u8; 148],
    pub skykeepRoomLayout:      [u8; 9],
    pub unk21413:               u8,
    pub unk21414:               u8,
    pub currentLayer:           u8,
    pub unk21416:               u8,
    pub unk21417:               u8,
    pub unk21418:               u8,
    pub currentEntrance:        u8,
    pub unk21420:               u8,
    pub isNewFile:              bool,
    pub selectedBWheelSlot:     u8,
    pub unk21423:               u8,
    pub selectedPouchSlot:      u8,
    pub selectedDowsingSlot:    u8,
    pub unk21426:               u8,
    pub unk21427:               u8,
    pub currentNight:           u8,
    pub isAutoSave:             u8,
    pub unkfiller5:             [u8; 10],
}

assert_eq_size!([u8; 21440], SaveFile);

// Harp stuff
// Not sure what this stuff is all about
// Used to keep vanilla checks for isPlayingHarp (see SD for more details)
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct HarpRelated {
    pub unk:                             [u8; 0x30],
    pub someCheckForContinuousStrumming: u64,
    pub unk1:                            [u8; 0x22],
    pub someOtherHarpThing:              u8,
}

// FlagMgr stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagMgr {
    pub funcs:            *mut FlagMgrFuncs,
    pub flagSizeMaybe:    u32,
    pub anotherSizeMaybe: u32,
    pub flagsPtr:         *mut FlagSpace,
    // + a bunch of other stuff that's not used
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct SceneflagMgr {
    pub sceneflags:   FlagSpace,
    pub tempflags:    FlagSpace,
    pub zoneflags:    FlagSpace,
    pub unk:          u16,
    pub sceneindex:   u16,
    pub shouldCommit: u8,
    pub unk1:         [u8; 3],
}

assert_eq_size!([u8; 0x50], SceneflagMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct DungeonflagMgr {
    pub shouldCommit: u8,
    pub unk:          u8,
    pub sceneindex:   u8,
    pub unkfiller:    [u8; 5],
    pub flagdefs:     u64,
    pub unkFlagStuff: u64,
    pub dungeonflags: FlagSpace,
}

assert_eq_size!([u8; 0x30], DungeonflagMgr);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagSpace {
    pub flagPtr:       u64,
    pub staticFlagPtr: *mut [u16; 8],
    pub flagSpaceSize: u16,
    pub unk:           [u8; 6],
}

assert_eq_size!([u8; 0x18], FlagSpace);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct FlagMgrFuncs {
    pub unk:                     u64,
    pub unk1:                    u64,
    pub setFlagsPtr:             u64,
    pub unk3:                    u64,
    pub copyFlagsFromSave:       extern "C" fn(*mut FlagMgr),
    pub setupUnkFlagStuff:       extern "C" fn(*mut FlagMgr),
    pub doCommit:                extern "C" fn(*mut FlagMgr),
    pub setFlag:                 extern "C" fn(*mut FlagMgr, u16),
    pub unsetFlag:               extern "C" fn(*mut FlagMgr, u16),
    pub setFlagOrCounterToValue: extern "C" fn(*mut FlagMgr, u16, u16),
    pub getFlagOrCounter:        extern "C" fn(*mut FlagMgr, u16) -> u32,
    pub getUncommitedValue:      extern "C" fn(*mut FlagMgr, u16) -> u32,
    pub unk12:                   extern "C" fn(),
    pub getSaveFlagSpace:        extern "C" fn(*mut FlagMgr),
}

assert_eq_size!([u8; 112], FlagMgrFuncs);

// Flags
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
    DEKU_HORNET_EMPTY                = 0x16,
    UNK23                            = 0x17,
    UNK24                            = 0x18,
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
    DUSK_RELIC__                     = 0x3D,
    DUSK_RELIC_                      = 0x3E,
    SEMI_RARE_TREASURE               = 0x3F,
    RARE_TREASURE                    = 0x40,
    GUARDIAN_POTION                  = 0x41,
    GUARDIAN_POTION_PLUS             = 0x42,
    UNK67                            = 0x43,
    WATER_DRAGON_SCALE               = 0x44,
    UNK69                            = 0x45,
    FAIRY                            = 0x46,
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
    POUCH_EXPANSION_COUNTER          = 0x199,
    HEART_PIECE_COUNTER              = 0x1E9,
    DEKU_SEED_COUNTER                = 0x1ED,
    ARROW_COUNTER                    = 0x1F2,
    BOMB_COUNTER                     = 0x1F3,
    RUPEE_COUNTER                    = 0x1F5,
    CRYSTAL_PACK_COUNTER             = 0x1F6,
    KEY_PIECE_COUNTER                = 0x1F9,
    EXTRA_WALLET_COUNTER             = 0x1FC,
    MAX511                           = 0x1FF,
}

// Actors
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcItem {
    pub base:                  ActorObjectBase,
    pub unkfiller:             [u8; 124],
    pub itemid:                u16,
    pub unkfiller1:            [u8; 6],
    pub itemModelPtr:          u64,
    pub unkfiller2:            [u8; 2784],
    pub actorListElement:      u32,
    pub unkfiller3:            [u8; 816],
    pub freestandingYOffset:   f32,
    pub unkfiller4:            [u8; 44],
    pub finalDeterminedItemID: u16,
    pub unkfiller5:            [u8; 10],
    pub preventDrop:           u8,
    pub unkfiller6:            [u8; 3],
    pub noLongerWaiting:       u8,
    pub unkfiller7:            [u8; 19],
}

assert_eq_size!([u8; 4744], dAcItem);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct dAcOlightLine {
    pub base:                ActorObjectBase,
    pub unkfiller0:          [u8; 124],
    pub unkfiller:           [u8; 0x989],
    pub lightShaftActivated: bool,
    pub unkfiller1:          [u8; 6],
    pub lightShaftIndex:     u32,
    pub unkfiller2:          [u8; 4],
}

assert_eq_size!([u8; 0xDA8], dAcOlightLine);

// ActorObjectBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBase {
    pub baseBase: ActorBaseBasemembers,
    pub vtable:   *mut ActorObjectBasevtable,
    pub members:  ActorObjectBasemembers,
    pub unk:      [u8; 200],
}

assert_eq_size!([u8; 916], ActorObjectBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBasevtable {
    pub base:                 ActorBasevtable,
    pub getActorListElement:  extern "C" fn() -> u64,
    pub canBeLinkedToWoodTag: extern "C" fn() -> bool,
    pub doDrop:               extern "C" fn() -> bool,
}

assert_eq_size!([u8; 248], ActorObjectBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorObjectBasemembers {
    pub base:             ActorBasemembers,
    pub unkfiller:        [u8; 24],
    pub targetFiTextId1:  u8,
    pub unkfiller1:       [u8; 3],
    pub targetFiTextId2:  u8,
    pub unkfiller2:       [u8; 47],
    pub forwardSpeed:     f32,
    pub gravityAccel:     f32,
    pub gravity:          f32,
    pub velocity:         Vec3f,
    pub unkfiller3:       [u8; 6],
    pub currentAngle:     Vec3s,
    pub unk:              u32,
    pub currentPos:       Vec3f,
    pub unkfiller4:       [u8; 44],
    pub cullingDistance:  f32,
    pub aabbAddon:        f32,
    pub objectActorFlags: u32,
    pub unkfiller5:       [u8; 40],
    pub posCopy:          Vec3f,
    pub unkfiller6:       [u8; 36],
    pub startingPos:      Vec3f,
    pub startingAngle:    Vec3s,
    pub unkfiller7:       [u8; 26],
}

assert_eq_size!([u8; 516], ActorObjectBasemembers);

// ActorBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBase {
    pub base:    ActorBaseBasemembers,
    pub vtable:  *mut ActorBasevtable,
    pub members: ActorBasemembers,
}

assert_eq_size!([u8; 400], ActorBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBasevtable {
    pub base:                 ActorBaseBasevtable,
    pub actorInit1:           extern "C" fn(*mut ActorObjectBase),
    pub actorInit2:           extern "C" fn(*mut ActorObjectBase),
    pub actorUpdate:          extern "C" fn(*mut ActorObjectBase),
    pub actorUpdateInEvent:   extern "C" fn(*mut ActorObjectBase),
    pub unk:                  extern "C" fn(*mut ActorObjectBase),
    pub unk1:                 extern "C" fn(*mut ActorObjectBase),
    pub copyPosRot:           extern "C" fn(*mut ActorObjectBase),
    pub getCurrentActorEvent: extern "C" fn(*mut ActorObjectBase) -> u32,
    pub unk2:                 extern "C" fn(*mut ActorObjectBase),
    pub performInteraction:   extern "C" fn(*mut ActorObjectBase),
}

assert_eq_size!([u8; 224], ActorBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBasemembers {
    pub baseProperties:  u64,
    pub unkfiller:       [u8; 22],
    pub objNamePtr:      u64,
    pub unkfiller1:      [u8; 42],
    pub posPtr:          *mut Vec3f,
    pub posCopy:         Vec3f,
    pub param2:          u32,
    pub rotCopy:         Vec3s,
    pub unk:             u32,
    pub subtype:         u8,
    pub unk1:            u8,
    pub rot:             Vec3s,
    pub unk2:            u16,
    pub pos:             Vec3f,
    pub scale:           Vec3f,
    pub actorProperties: u32,
    pub unkfiller2:      [u8; 28],
    pub roomid:          u8,
    pub actorSubType:    u8,
    pub unkfiller3:      [u8; 18],
}

assert_eq_size!([u8; 200], ActorBasemembers);

// ActorBaseBase
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBase {
    pub members:        ActorBaseBasemembers,
    pub vtable:         *mut ActorBaseBasevtable,
    pub baseProperties: u64,
}

assert_eq_size!([u8; 208], ActorBaseBase);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBasevtable {
    pub init:               extern "C" fn(*mut ActorBaseBase),
    pub preInit:            extern "C" fn(*mut ActorBaseBase),
    pub postInit:           extern "C" fn(*mut ActorBaseBase),
    pub destroy:            extern "C" fn(*mut ActorBaseBase),
    pub preDestroy:         extern "C" fn(*mut ActorBaseBase),
    pub postDestroy:        extern "C" fn(*mut ActorBaseBase),
    pub baseUpdate:         extern "C" fn(*mut ActorBaseBase),
    pub preUpdate:          extern "C" fn(*mut ActorBaseBase),
    pub postUpdate:         extern "C" fn(*mut ActorBaseBase),
    pub draw:               extern "C" fn(*mut ActorBaseBase),
    pub preDraw:            extern "C" fn(*mut ActorBaseBase),
    pub postDraw:           extern "C" fn(*mut ActorBaseBase),
    pub unk:                extern "C" fn(*mut ActorBaseBase),
    pub createHeap:         extern "C" fn(*mut ActorBaseBase),
    pub createHeap2:        extern "C" fn(*mut ActorBaseBase),
    pub initModels:         extern "C" fn(*mut ActorBaseBase),
    pub dtor:               extern "C" fn(*mut ActorBaseBase),
    pub dtorWithActorHeaps: extern "C" fn(*mut ActorBaseBase),
}

assert_eq_size!([u8; 144], ActorBaseBasevtable);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorBaseBasemembers {
    pub vtable:           *mut ActorObjectBasevtable,
    pub uniqueActorIndex: u32,
    pub param1:           u32,
    pub actorID:          u16,
    pub unk:              u32,
    pub groupType:        u8,
    pub unkfiller:        [u8; 169],
}

assert_eq_size!([u8; 192], ActorBaseBasemembers);

// Misc
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

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct Player {
    pub _0:                [u8; 0x460],
    pub action_flags:      u32,
    pub more_action_flags: u32,
    pub current_action:    u32,
    // TODO: more stuff
}

assert_eq_size!([u8; 0x46C], Player);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct StartCount {
    pub counter: u16,
    pub value:   u16,
}

assert_eq_size!(u32, StartCount);

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct WarpToStartInfo {
    pub stage_name: [u8; 8],
    pub room:       u8,
    pub layer:      u8,
    pub entrance:   u8,
    pub night:      u8,
}

assert_eq_size!([u8; 12], WarpToStartInfo);

// Event Flow stuff
#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct ActorEventFlowMgr {
    vtable:                     u64,
    msbf_info:                  u64,
    current_flow_index:         u32,
    unk1:                       u32,
    unk2:                       u32,
    unk3:                       u32,
    result_from_previous_check: u32,
    current_text_label_name:    [u8; 32],
    unk4:                       u32,
    unk5:                       u32,
    unk6:                       u32,
    next_flow_delay_timer:      u32,
    another_flow_element:       EventFlowElement,
    unk7:                       u32,
    unk8:                       u32,
    unk9:                       u32,
}

#[repr(C, packed(1))]
#[derive(Copy, Clone)]
pub struct EventFlowElement {
    pub typ:      u8,
    pub sub_type: u8,
    pub pad:      u16,
    pub param1:   u16,
    pub param2:   u16,
    pub next:     u16,
    pub param3:   u16,
    pub param4:   u16,
    pub param5:   u16,
}

assert_eq_size!([u8; 16], EventFlowElement);

#[repr(C, packed(1))]
pub struct LytMsgWindow {
    pub unkfiller1:  [u8; 0xA90],
    pub textManager: *mut TextManagerMaybe,
}

assert_eq_size!([u8; 0xA98], LytMsgWindow);

#[repr(C, packed(1))]
pub struct TextManagerMaybe {
    pub unkfiller1:   [u8; 0x8AC],
    pub numeric_args: [u32; 5],
}

assert_eq_size!([u8; 0x8C0], TextManagerMaybe);
