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
.offset 0x08b0d0a8
mov w8, #2
```

For more information about the addresses used, see the Addresses and Offsets
section below

### Additions (custom functions)

All the existing asm additons can be found in the `asm/additions` directory.
Each addition should be named in lowercase, have words separated by hyphens
(`-`), and end with the `.asm` file extension.

Each addition file should serve a specific purpose. This is to make it easier
to find a specific addition as well as make it easier to understand what
additions have been made. If in doubt, create a new additions file rather than
extending an existing one.

Additions that require use of the jumptable should only be created when
**absolutely** necessary. Jumptable space is **very** limited.

A janky alternative is always better than a clean use of the jumptable. When
avoiding creating a new jumptable entry, please explain any janky solutions in
detail. Additions have to be maintained. A clever solution created 6 months
ago is worthless if nobody remembers how it works.

Fortunately (at least for this specific issue), SSHD's functions have been
much more heavily in-lined than in SD. This means that there are often
duplicated bits of code that can be used instead.

Clever placement of your additions can help when you're short by an
instruction. By aligning the offset of your addition such that the last 4
digits are all zeros, you can save an instruction. For example:

```
; branches to addition at 0x360A5500
mov x16, #0x5500
movk x16, #0x360A, LSL #16
br x16
```

vs

```
; branches to addition at 0x360B0000
movz x16, #0x360B, LSL #16
br x16
```

This method is preferred to using the jumptable but, again, a solution
requiring neither should always be sought out first.

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

```python assemble.py```

in the `asm` directory. All the asm files will then be assembled, linked, and
converted to binary. The output can be viewed in `asm/patches/diffs`.
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
`.nso` file (`main`, `rtld`, `sdk`, `subsdk0`, `subsdk1`). These are the
addresses used in ghidra (if your addresses start at 0x71000000, you haven't
set up your ghidra environment correctly).

These addresses come from `gdb` (instructions about how to install and use
`gdb` can be found at
https://gist.github.com/jam1garner/c9ba6c0cff150f1a2480d0c18ff05e33).

For The Legend of Zelda: Skyward Sword HD, the relative addresses for each
`.nso` file are:
* `rtld    = 0x08000000 -> 0x08003FFF`
* `main    = 0x08004000 -> 0x09841FFF`
* `subsdk0 = 0x35037000 -> 0x359FEFFF`
* `subsdk1 = 0x359FF000 -> 0x360A4FFF`
* `sdk     = 0x360A5000 -> 0x36DA2FFF`

#### subsdk8

The above addresses are changed slightly by the randomizer to allow for asm
additions to the code. The relative addresses for each `.nso` file with the
randomizer asm changes are:
* `rtld    = 0x08000000 -> 0x08003FFF`
* `main    = 0x08004000 -> 0x09841FFF`
* `subsdk0 = 0x35037000 -> 0x359FEFFF`
* `subsdk1 = 0x359FF000 -> 0x360A4FFF`
* `subsdk8 = 0x360A5000 -> 0x3674AFFF`
* `sdk     = 0x3674B000 -> 0x3747EFFF`