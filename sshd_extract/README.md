# Game Extract Folder

**This document is not a comprehensive guide.**

This document explains the structure of the `sshd_extract` folder that is
necessary for the randomizer to work. For information about how to obtain an
extract of The Legend of Zelda: Skyward Sword HD, please ask on Discord or
GitHub. Alternatively, you can try to search online for instructions. However,
only follow such instructions if you fully understand the consequences.
Be careful.

## Pre-requisites

You will need:

* A modded Nintendo Switch console
* A copy of The Legend of Zelda: Skyward Sword HD (physical or digital)
* Knowledge of how to navigate a modded Nintendo Switch console - including
  how to use tools like `nxdumptool` to extract your copy of the game

OR

* An extracted copy of The Legend of Zelda: Skyward Sword HD Ver. 1.0.1
* Some way to play this copy of the game

## Required Structure

The Legend of Zelda: Skyward Sword HD game extract files are spilt into two
folders: `exefs` and `romfs`. All you *need* to know is that, if you have
correctly extracted your copy of the game, these are the 2 folders that are
needed so that the randomizer can work.

Your folder should look like this:

```
sshd_extract
├── exefs
|   └── ...
├── romfs
|   └── ...
└── README.md
```

## Required Game Version

The Legend of Zelda: Skyward Sword HD has had two different versions:

* Ver. 1.0.0
* Ver. 1.0.1

There are minimal differences between the two versions. However, you need to
make sure that your extract is of the 1.0.1 version of the game. This version
was chosen as it fixes 2 notable bugs.

### How to Check the Version of your Game

To check which version of the game you have installed on your Nintendo Switch
console, go to your installation of the game and press the + button. At the
top of the screen, beneith the title, you will see on of the following:

* Ver. 1.0.0 | Nintendo
* Ver. 1.0.1 | Nintendo

This indicates which version of the game you have installed. If you have
version 1.0.0 installed, you will need to update your game to version 1.0.1
*before* you extract the game.

### How to Update your Game

To update from 1.0.0 to 1.0.1, go to your installation of the game, press
the + button, and follow the instructions under the "Software Update" tab.
