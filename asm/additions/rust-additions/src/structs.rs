#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use static_assertions::assert_eq_size;

// FileMgr/SaveFile stuff
#[repr(C)]
#[derive(Copy, Clone)]
pub struct FileMgr {
    pub allSaveFiles: u64,
    pub saveTails: u64,
    pub FA: SaveFile,
    pub FB: SaveFile,
    pub unkfiller: [u8; 36],
    pub amiiboPos: Vec3f,
    pub amiiboStage: u64,
    pub unkfiller1: [u8; 9534],
    pub preventCommit: bool,
    pub unk: u8,
}

assert_eq_size!([u8; 52488], FileMgr);

#[repr(C)]
#[derive(Copy, Clone)]
pub struct SaveFile {
    pub saveTime: u64, // size is a guess
    pub unk: u64,
    pub unkfiller: [u8; 2244],
    pub playerName: [u16; 8],
    pub storyflags: [u16; 128],
    pub itemflags: [u16; 64],
    pub dungeonflags: [[u16; 8]; 26],
    pub unkfiller1: [u8; 3680],
    pub sceneflags: [[u16; 8]; 26],
    pub unkfiller2: [u8; 4960],
    pub enemyKillCounters: [u16; 100],
    pub hitByEnemyCounters: [u16; 100],
    pub tempflags: [u16; 4],
    pub zoneflags: [[u16; 4]; 63],
    pub enemyDefeatedFlags: [u16; 4096],
    pub unkfiller3: [u8; 14],
    pub healthCapacity: u16,
    pub someHealthRelatedThing: u16,
    pub currentHealth: u16,
    pub unkfiller4: [u8; 148],
    pub skykeepRoomLayout: [u8; 9],
    pub unk21413: u8,
    pub unk21414: u8,
    pub currentLayer: u8,
    pub unk21416: u8,
    pub unk21417: u8,
    pub unk21418: u8,
    pub currentEntrance: u8,
    pub unk21420: u8,
    pub isNewFile: bool,
    pub selectedBWheelSlot: u8,
    pub unk21423: u8,
    pub selectedPouchSlot: u8,
    pub selectedDowsingSlot: u8,
    pub unk21426: u8,
    pub unk21427: u8,
    pub currentNight: u8,
    pub isAutoSave: u8,
    pub unkfiller5: [u8; 10],
}

assert_eq_size!([u8; 21440], SaveFile);

// FlagMgr stuff
#[repr(C)]
#[derive(Copy, Clone)]
pub struct FlagMgr {
    pub funcs: *mut FlagMgrFuncs,
    pub flagSizeMaybe: u32,
    pub anotherSizeMaybe: u32,
    pub flagsPtr: *mut FlagSpace,
    // + a bunch of other stuff that's not used
}

#[repr(C)]
#[derive(Copy, Clone)]
pub struct DungeonflagMgr {
    pub unk: u16,
    pub sceneindex: u8,
    pub unkfiller: [u8; 5],
    pub shouldCommit: u8,
    pub unkfiller1: [u8; 7],
    pub unkFlagStuff: u64,
    pub dungeonflags: FlagSpace,
}

assert_eq_size!([u8; 40], DungeonflagMgr);

#[repr(C)]
#[derive(Copy, Clone)]
pub struct FlagSpace {
    pub flagPtr: u64,
    pub flagcount: u16,
    pub unk: [u8; 6],
}

assert_eq_size!([u8; 16], FlagSpace);

#[repr(C)]
#[derive(Copy, Clone)]
pub struct FlagMgrFuncs {
    pub unk: u64,
    pub unk1: u64,
    pub setFlagsPtr: u64,
    pub unk3: u64,
    pub copyFlagsFromSave: extern "C" fn(*mut FlagMgr),
    pub setupUnkFlagStuff: extern "C" fn(*mut FlagMgr),
    pub doCommit: extern "C" fn(*mut FlagMgr),
    pub setFlag: extern "C" fn(*mut FlagMgr, u16),
    pub unsetFlag: extern "C" fn(*mut FlagMgr, u16),
    pub setFlagOrCounterToValue: extern "C" fn(*mut FlagMgr, u16, u16),
    pub getFlagOrCounter: extern "C" fn(*mut FlagMgr, u16),
    pub getUncommitedValue: extern "C" fn(*mut FlagMgr, u16),
    pub unk12: extern "C" fn(),
    pub getSaveFlagSpace: extern "C" fn(*mut FlagMgr),
}

assert_eq_size!([u8; 112], FlagMgrFuncs);

// Actors
#[repr(C)]
#[derive(Copy, Clone)]
pub struct dAcItem {
    pub base: [u8; 916], // ActorObjectBase,
    pub unkfiller: [u8; 124],
    pub itemid: u16,
    pub unkfiller1: [u8; 3666],
    // pub itemModelPtr: u64,
    // pub unkfiller2: [u8; 2784],
    // pub actorListElement: u32,
    // pub unkfiller3: [u8; 864],
    pub finalDeterminedItemID: u16,
    pub unkfiller4: [u8; 10],
    pub preventDrop: u8,
    pub unkfiller5: [u8; 3],
    pub noLongerWaiting: u8,
    pub unkfiller6: [u8; 19],
}

assert_eq_size!([u8; 4744], dAcItem);

// Using u64 or 64bit pointers forces structs to be 8-byte aligned.
// The vanilla code seems to be 4-byte aligned and I haven't figured out how
// to force rust to do the same. So, for now, just pretend ¯\_(ツ)_/¯

// ActorObjectBase
// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorObjectBase {
//     pub baseBase: ActorBaseBasemembers,
//     pub vtable: *mut ActorObjectBasevtable,
//     pub members: ActorObjectBasemembers,
//     // _alignment_padding: u32,
//     pub unk: [u8; 200],
// }

// const TestChecker: [u8; 916] = [0; core::mem::size_of::<ActorObjectBase>()];

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorObjectBasevtable {
//     pub base: ActorBasevtable,
//     pub getActorListElement: extern fn() -> u64,
//     pub canBeLinkedToWoodTag: extern fn() -> bool,
//     pub doDrop: extern fn() -> bool,
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorObjectBasemembers {
//     pub base: ActorBasemembers,
//     pub unkfiller: [u8; 24],
//     pub targetFiTextId1: u8,
//     pub unkfiller1: [u8; 3],
//     pub targetFiTextId2: u8,
//     pub unkfiller2: [u8; 47],
//     pub forwardSpeed: f32,
//     pub gravityAccel: f32,
//     pub gravity: f32,
//     pub velocity: Vec3f,
//     pub unkfiller3: [u8; 6],
//     pub currentAngle: Vec3s,
//     pub unk: u32,
//     pub currentPos: Vec3f,
//     pub unkfiller4: [u8; 44],
//     pub cullingDistance: f32,
//     pub aabbAddon: f32,
//     pub objectActorFlags: u32,
//     pub unkfiller5: [u8; 40],
//     pub posCopy: Vec3f,
//     pub unkfiller6: [u8; 36],
//     pub startingPos: Vec3f,
//     pub startingAngle: Vec3s,
//     pub unkfiller7: [u8; 26],
// }

// // ActorBase
// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBase {
//     pub base: ActorBaseBasemembers,
//     pub vtable: *mut ActorBasevtable,
//     pub members: ActorBasemembers,
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBasevtable {
//     pub base: ActorBaseBasevtable,
//     pub actorInit1: extern fn(*mut ActorObjectBase),
//     pub actorInit2: extern fn(*mut ActorObjectBase),
//     pub actorUpdate: extern fn(*mut ActorObjectBase),
//     pub actorUpdateInEvent: extern fn(*mut ActorObjectBase),
//     pub unk: extern fn(*mut ActorObjectBase),
//     pub unk1: extern fn(*mut ActorObjectBase),
//     pub copyPosRot: extern fn(*mut ActorObjectBase),
//     pub getCurrentActorEvent: extern fn(*mut ActorObjectBase) -> u32,
//     pub unk2: extern fn(*mut ActorObjectBase),
//     pub performInteraction: extern fn(*mut ActorObjectBase),
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBasemembers {
//     pub baseProperties: u64,
//     pub unkfiller: [u8; 22],
//     pub objNamePtr: u64,
//     pub unkfiller1: [u8; 42],
//     pub posPtr: *mut Vec3f,
//     pub posCopy: Vec3f,
//     pub param2: u32,
//     pub rotCopy: Vec3s,
//     pub unk: u32,
//     pub subtype: u8,
//     pub unk1: u8,
//     pub rot: Vec3s,
//     pub unk2: u16,
//     pub pos: Vec3f,
//     pub scale: Vec3f,
//     pub actorProperties: u32,
//     pub unkfiller2: [u8; 28],
//     pub roomid: u8,
//     pub actorSubType: u8,
//     pub unkfiller3: [u8; 18],
// }

// // ActorBaseBase
// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBaseBase {
//     pub members: ActorBaseBasemembers,
//     pub vtable: *mut ActorBaseBasevtable,
//     pub baseProperties: u64,
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBaseBasevtable {
//     pub init: extern fn(*mut ActorBaseBase),
//     pub preInit: extern fn(*mut ActorBaseBase),
//     pub postInit: extern fn(*mut ActorBaseBase),
//     pub destroy: extern fn(*mut ActorBaseBase),
//     pub preDestroy: extern fn(*mut ActorBaseBase),
//     pub postDestroy: extern fn(*mut ActorBaseBase),
//     pub baseUpdate: extern fn(*mut ActorBaseBase),
//     pub preUpdate: extern fn(*mut ActorBaseBase),
//     pub postUpdate: extern fn(*mut ActorBaseBase),
//     pub draw: extern fn(*mut ActorBaseBase),
//     pub preDraw: extern fn(*mut ActorBaseBase),
//     pub postDraw: extern fn(*mut ActorBaseBase),
//     pub unk: extern fn(*mut ActorBaseBase),
//     pub createHeap: extern fn(*mut ActorBaseBase),
//     pub createHeap2: extern fn(*mut ActorBaseBase),
//     pub initModels: extern fn(*mut ActorBaseBase),
//     pub dtor: extern fn(*mut ActorBaseBase),
//     pub dtorWithActorHeaps: extern fn(*mut ActorBaseBase),
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBaseBasemembers {
//     pub vtable: *mut ActorObjectBasevtable,
//     pub uniqueActorIndex: u32,
//     pub param1: u32,
//     pub actorID: u16,
//     pub unk: u32,
//     pub groupType: u8,
//     pub unkfiller: [u8; 169],
// }

// Misc
#[repr(C)]
#[derive(Copy, Clone)]
pub struct Vec3f {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

assert_eq_size!([u8; 12], Vec3f);

#[repr(C)]
#[derive(Copy, Clone)]
pub struct Vec3s {
    pub x: u16,
    pub y: u16,
    pub z: u16,
}

assert_eq_size!([u8; 6], Vec3s);
