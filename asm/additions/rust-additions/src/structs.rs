#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use core::ffi::c_ushort;
use static_assertions::assert_eq_size;

// FileMgr/SaveFile stuff
#[repr(C)]
#[derive(Copy, Clone)]
pub struct FileMgr {
    pub allSaveFiles: u64,
    pub saveTails: u64,
    pub FA: SaveFile,
    pub FB: SaveFile,
    pub unkfiller: [u8; 36usize],
    pub amiiboPos: Vec3f,
    pub amiiboStage: u64,
    pub unkfiller1: [u8; 9534usize],
    pub preventCommit: bool,
}

#[repr(C)]
#[derive(Copy, Clone)]
pub struct SaveFile {
    pub saveTime: u64, // size is a guess
    pub unk: u64,
    pub unkfiller: [u8; 2244usize],
    pub playerName: [c_ushort; 8usize],
    pub storyflags: [c_ushort; 128usize],
    pub itemflags: [c_ushort; 64usize],
    pub dungeonflags: [[c_ushort; 8usize]; 26usize],
    pub unkfiller1: [u8; 3680usize],
    pub sceneflags: [[c_ushort; 8usize]; 26usize],
    pub unkfiller2: [u8; 4960usize],
    pub enemyKillCounters: [c_ushort; 100usize],
    pub hitByEnemyCounters: [c_ushort; 100usize],
    pub tempflags: [c_ushort; 4usize],
    pub zoneflags: [[c_ushort; 4usize]; 63usize],
    pub enemyDefeatedFlags: [c_ushort; 4096usize],
    pub unkfiller3: [u8; 14usize],
    pub healthCapacity: u16,
    pub someHealthRelatedThing: u16,
    pub currentHealth: u16,
    pub unkfiller4: [u8; 148usize],
    pub skykeepRoomLayout: [u8; 9usize],
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
    pub unkfiller5: [u8; 10usize],
}

// FlagMgr stuff
#[repr(C)]
#[derive(Copy, Clone)]
pub struct DungeonflagMgr {
    pub unk: u16,
    pub sceneindex: u8,
    pub unkfiller: [u8; 5usize],
    pub shouldCommit: u8,
    pub unkfiller1: [u8; 7usize],
    pub unkFlagStuff: u64,
    pub dungeonflags: FlagSpace,
}

#[repr(C)]
#[derive(Copy, Clone)]
pub struct FlagSpace {
    pub flagPtr: u64,
    pub flagcount: u16,
    pub unk: [u8; 6usize],
}

// Actors
#[repr(C)]
#[derive(Copy, Clone)]
pub struct dAcItem {
    pub base: [u8; 916usize], // ActorObjectBase,
    pub unkfiller: [u8; 124usize],
    pub itemid: u16,
    pub unkfiller1: [u8; 3666usize],
    // pub itemModelPtr: u64,
    // pub unkfiller2: [u8; 2784usize],
    // pub actorListElement: u32,
    // pub unkfiller3: [u8; 864usize],
    pub finalDeterminedItemID: u16,
    pub unkfiller4: [u8; 10usize],
    pub preventDrop: u8,
    pub unkfiller5: [u8; 3usize],
    pub noLongerWaiting: u8,
    pub unkfiller6: [u8; 19usize],
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
//     pub unk: [u8; 200usize],
// }

// const TestChecker: [u8; 916] = [0; core::mem::size_of::<ActorObjectBase>()];

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorObjectBasevtable {
//     pub base: ActorBasevtable,
//     pub getActorListElement: *mut fn() -> u64,
//     pub canBeLinkedToWoodTag: *mut fn() -> bool,
//     pub doDrop: *mut fn() -> bool,
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorObjectBasemembers {
//     pub base: ActorBasemembers,
//     pub unkfiller: [u8; 24usize],
//     pub targetFiTextId1: u8,
//     pub unkfiller1: [u8; 3usize],
//     pub targetFiTextId2: u8,
//     pub unkfiller2: [u8; 47usize],
//     pub forwardSpeed: f32,
//     pub gravityAccel: f32,
//     pub gravity: f32,
//     pub velocity: Vec3f,
//     pub unkfiller3: [u8; 6usize],
//     pub currentAngle: Vec3s,
//     pub unk: u32,
//     pub currentPos: Vec3f,
//     pub unkfiller4: [u8; 44usize],
//     pub cullingDistance: f32,
//     pub aabbAddon: f32,
//     pub objectActorFlags: u32,
//     pub unkfiller5: [u8; 40usize],
//     pub posCopy: Vec3f,
//     pub unkfiller6: [u8; 36usize],
//     pub startingPos: Vec3f,
//     pub startingAngle: Vec3s,
//     pub unkfiller7: [u8; 26usize],
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
//     pub actorInit1: *mut fn(*mut ActorObjectBase),
//     pub actorInit2: *mut fn(*mut ActorObjectBase),
//     pub actorUpdate: *mut fn(*mut ActorObjectBase),
//     pub actorUpdateInEvent: *mut fn(*mut ActorObjectBase),
//     pub unk: *mut fn(*mut ActorObjectBase),
//     pub unk1: *mut fn(*mut ActorObjectBase),
//     pub copyPosRot: *mut fn(*mut ActorObjectBase),
//     pub getCurrentActorEvent: *mut fn(*mut ActorObjectBase) -> u32,
//     pub unk2: *mut fn(*mut ActorObjectBase),
//     pub performInteraction: *mut fn(*mut ActorObjectBase),
// }

// #[repr(C)]
// #[derive(Copy, Clone)]
// pub struct ActorBasemembers {
//     pub baseProperties: u64,
//     pub unkfiller: [u8; 22usize],
//     pub objNamePtr: u64,
//     pub unkfiller1: [u8; 42usize],
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
//     pub unkfiller2: [u8; 28usize],
//     pub roomid: u8,
//     pub actorSubType: u8,
//     pub unkfiller3: [u8; 18usize],
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
//     pub init: *mut fn(*mut ActorBaseBase),
//     pub preInit: *mut fn(*mut ActorBaseBase),
//     pub postInit: *mut fn(*mut ActorBaseBase),
//     pub destroy: *mut fn(*mut ActorBaseBase),
//     pub preDestroy: *mut fn(*mut ActorBaseBase),
//     pub postDestroy: *mut fn(*mut ActorBaseBase),
//     pub baseUpdate: *mut fn(*mut ActorBaseBase),
//     pub preUpdate: *mut fn(*mut ActorBaseBase),
//     pub postUpdate: *mut fn(*mut ActorBaseBase),
//     pub draw: *mut fn(*mut ActorBaseBase),
//     pub preDraw: *mut fn(*mut ActorBaseBase),
//     pub postDraw: *mut fn(*mut ActorBaseBase),
//     pub unk: *mut fn(*mut ActorBaseBase),
//     pub createHeap: *mut fn(*mut ActorBaseBase),
//     pub createHeap2: *mut fn(*mut ActorBaseBase),
//     pub initModels: *mut fn(*mut ActorBaseBase),
//     pub dtor: *mut fn(*mut ActorBaseBase),
//     pub dtorWithActorHeaps: *mut fn(*mut ActorBaseBase),
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
//     pub unkfiller: [u8; 169usize],
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
