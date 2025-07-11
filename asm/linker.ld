/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
/* | Linker structure from https://github.com/shadowninja108/exlaunch/blob/main/misc/link.ld | */
/* |          License: https://github.com/shadowninja108/exlaunch/blob/main/LICENSE          | */
/* |                                                                                         | */
/* |             This file is licensed under the GNU General Public License v2.0             | */
/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

PHDRS
{
  text PT_LOAD FLAGS(5);
  rodata PT_LOAD FLAGS(4);
  data PT_LOAD FLAGS(6);
}

SECTIONS
{
  /* App code */
  .text : {
    HIDDEN(__text_start__ = .);
    KEEP (*(.text.crt0))
    *(.text .text.*)
    HIDDEN(__text_end__ = .);
  } :text

  /* Read-only sections */
  . = ALIGN(0x1000);

  /* Make sure everything is aligned */
  . = ALIGN(8);

  /* App rodata */
  .rodata : {
    *(.rodata .rodata.*)
  } :rodata

  /* Read-write sections */
  . = ALIGN(0x1000);

  /* App data */
  .data : {
    *(.data .data.*)
  } :data
}
