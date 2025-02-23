# ASM

## Requirements

The core requirement for making asm changes is having `devkitpro` installed.
Without it, you cannot assemble your changes. Specifically, you will need to
have `devkitA64` installed. This should be included if you check the "Switch
Development" option when installing the `devkitpro` components.

Instructions for how to install `devkitpro` can be found at
https://devkitpro.org/wiki/devkitPro_pacman.

If you are running on a Windows operating system, you will need to make sure
that `devkitA64` is installed at `C:\devkitPro\devkitA64`.

If you are running on a non-Windows operating system, you will need to make
sure that the `DEVKITA64` environment variable is set to the path of your
`devkitA64` installation.

## How to

### Patches

All the existing asm patches can be found in the `asm/patches` directory.
Each patch should be named in lowercase, have words separated by hyphens
(`-`), and end with the `.asm` file extension.

Each patch file should serve a specific purpose. This is to make it easier to
find specific patches as well as make it easier to understand what patches
have been made. If in doubt, create a new patch file rather than extending an
existing one.

Patches are written using the ARMv8-A instruction set. All asm instruction
blocks must be preceded by the offset where the instructions are to be
patched. This is done with `.offset address`. For example:

```
.offset 0x7100000000
mov w8, #2
```

For more information about the addresses used, see the Addresses and Offsets
section below

### Additions (custom functions)

All the existing asm additons can be found in the `asm/additions` directory.
Each addition should be named in lowercase, have words separated by hyphens
(`-`), and end with the `.asm` file extension. Where possible, please write
additions in rust rather than asm. There is currently only one example of
additions written in asm: `ac-boko-item-flag.asm` vs 100+ rust functions.

All additions rely on a patch branching to the additional code. However,
because the additions are written to a separate module, a single branch
instruction cannot make the jump. To get around this issue, there is a single
point that handles branching to the additional code by reading register `w8` to
determine which custom function should be branched to.

E.g. If you wanted to create a patch that branched to custom function 69, you
would write:

```
.offset 0x7100000000
mov w8, #69
bl additions_jumptable
```

Please note, the custom symbol `additions_jumptable` has been defined so that
the exact address doesn't need to be known and so patches are more readable.
Please make sure to use this symbol rather than the raw address.

This will create a patch that branches to the jumptable with a value of 69. The
jumptable will branch to the "additions landingpad" in the additional code
space. Here, the value in `w8` is read and compared so that a final branch can
be made to the actual additional code. The landingpad is defined in
`additions-landingpad.asm`.

#### Single Instruction Additions Branching

Sometimes, finding a place where you can overwrite 2 instructions is difficult.
For these cases, `jumptable.asm` can be used as an intermediate step. However,
this method is highly discouraged as the jumptable space is very small. 

#### subsdk8
Additions are placed in a separate nso file and are loaded as their own
module. Specifically, subsdk1 is copied, modified with any additions, and
re-packed as subsdk8. Games usually use the lowest subsdk numbers first and
subsdk9 is used by `exlaunch` so subsdk8 has been chosen to maximize
flexibility.

### Assembling

Any changes that you make will need to be assembled in order to be used by the
randomizer. If you follow have followed the guidance detailed above, any
changes you have made can be assembled by running:

```
cd asm
python assemble.py
```

from the root of the randomizer. All the asm files will then be assembled,
linked, and converted to binary. The output can be viewed in
`asm/patches/diffs`.

**Do not** directly change these files. Any changes made directly to the diff
files will be overwritten the next time the assembler is called.

## General Resources and Inforamation

### Instruction Set

The Nintendo Switch runs on an
(ARM Cortex-A57)[https://en.wikipedia.org/wiki/ARM_Cortex-A57] processor. It
implements the
(ARMv8-A)[https://en.wikipedia.org/wiki/ARM_architecture_family#64/32-bit_architecture]
64-bit instruction set.

The documentation for the ARMv8-A instruction set can be found at
https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Armv8-A%20Instruction%20Set%20Architecture.pdf?revision=818c7869-3849-4e5d-bde2-710e69defb57.

#### Registers

Unlike preivous Nintendo consoles, the Nintendo Switch has a 64-bit processor
(rather than 32-bit). As a result, the registers work differently. Like the
previous consoles, there are 32 general purpose registers to work with.
However, these registers aren't `r0` -> `r31`. Instead, there are registers
x0 -> x31. These are 64-bit registers. There are also aliases for the lower
32-bits of a register: `w0` -> `w31`. Changing the value of a register with a
`w` at the start will set the upper 32 bits of the equivalent `x` register to
zeros.

### Addresses and Offsets

The offsets used with the patches are the relative addresses for each vanilla
`.nso` file (`main`, `rtld`, `sdk`, `subsdk0`, `subsdk1`). These are similar to
the addresses used in ghidra but not exactly the same. the address 0x80001234
would be 0x7100001234 in ghidra.

These addresses come from `gdb` (instructions about how to install and use
`gdb` can be found at
https://gist.github.com/jam1garner/c9ba6c0cff150f1a2480d0c18ff05e33).

For The Legend of Zelda: Skyward Sword HD, the relative addresses for each
`.nso` file are:
* `rtld    (nnrtld)       = 0x80000000 -> 0x80003FFF`
* `main    (Shoebill.nss) = 0x80004000 -> 0xAD036FFF`
* `subsdk0 (glslc)        = 0xAD037000 -> 0xAD9FEFFF`
* `subsdk1 (multimedia)   = 0xAD9FF000 -> 0xAE0A4FFF`
* `sdk     (nnSdk)        = 0xAE0A5000 -> 0xAEDD8FFF`

#### subsdk8

The above addresses are changed slightly by the randomizer to allow for asm
additions to the code. The relative addresses for each `.nso` file with the
randomizer asm changes are:
* `rtld    (nnrtld)       = 0x80000000 -> 0x80003FFF`
* `main    (Shoebill.nss) = 0x80004000 -> 0xAD036FFF`
* `subsdk0 (glslc)        = 0xAD037000 -> 0xAD9FEFFF`
* `subsdk1 (multimedia)   = 0xAD9FF000 -> 0xAE0A4FFF`
* `subsdk8 (multimedia)   = 0xAE0A5000 -> 0xAE74AFFF`
* `sdk     (nnSdk)        = 0xAE74B000 -> 0xAF47EFFF`
