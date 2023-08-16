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

### Addtions (custom functions)

Currently, only asm *patching* is supported. If you need to add custom code,
you will have to find and replace some vanilla code that we don't need.

### Patches

All the existing asm patches can be found in the `asm/patches` directory.
Each patch should be named in lowercase, have words separated by hyphens
(`-`), and end with the `.asm` file extension.

Each patch file should serve a specific purpose. This is to make it easier to
find specific patches as well as make it easier to understand what patches
have been made. If in doubt, create a new patch file rather than extending an
existing one.

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
