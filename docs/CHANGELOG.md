# Changelog

## Version 1.1

### Additions and Changes
* Added logic tooltips to the tracker
  * Hovering over a location on the tracker will now show the items needed to logically obtain that check
* Improved right-click functionality for tracker areas
  * Right-clicking an area on the tracker now cycles between:
    * Marking all locations currently in logic as completed
    * Marking all locations as completed
    * Marking all locations as incompleted
* Changed the tracker so all dungeons are activated by default
  * Users will now disable unrequired dungeons instead of enabling required ones
* Changed Gratitude Crystal tracking so players can track individual crystals rather than just packs of five
* Added a notes section to the tracker
* Renamed several locations to have clearer names
* Added Gust Bellows as a logical way to obtain the `Upper Skyloft - Ring Knight Academy Bell` check
* Prevented Pyrups breathing fire while the player is using the Mogma Mitts
* Increased the size of the bonk targets for the `Bonk Fire/Lightning Node Power Supply` checks to make them easier to obtain
* Changed Professor Horwell so the player can talk to him from any angle
* Changed traps to only replace junk items
  * Traps will no longer replace Heart Containers, Heart Pieces, Medals, and other inventory items
* Changed freestanding traps to rotate the opposite way to regular items
  * Traps will rotate clockwise; regular items will rotate anti-clockwise
* Stopped Groose spawning in Silent Realms that would cause the game to freeze for 2-3 seconds
* Stopped trap music playing when using a loadzone
  * Fixed softlock when trying to obtain the `Sealed Temple - Song from The Old One` check while the Groose Trap music was playing
* Updated the Goddess's Harp item get text to include instructions for how to use the harp
* Added a trick setting for "Long Ranged Skyward Strikes"
* Removed vanilla Fi text on top of the Great Tree near Yerbal
* Updated the spoiler log to also show all the excluded locations for players wanting to 100% their inventory/seed
* Updated language parsing for plurality and gender
* Removed the profanity filter checks when selecting a filename

### Fixes
* Fixed tracker autosave issue
  * The tracker now correctly saves your progress
* Fixed issue where the topmost pouch item could get overwritten by collecting Closet or Trial Reward checks
* Fixed burn traps damaging non-wooden shields
* Fixed issue preventing The Thunderhead from opening after placing the Stone of Trials
* Fixed issues with the `Barren Unrequired Dungeons` setting
* Fixed logic issue that connected the end of the Lanayru Mining Facility to the Temple of Time
  * The randomizer no longer assumes beating the Lanayru Mining Facility will give access to the Temple of Time
* Fixed tracker not showing the `Earth Temple - Rupee above First Drawbridge` check when the `Barren Unrequired Dungeons` setting was enabled
* Fixed tracker showing Sand Sea locations in the Sealed Grounds
* Fixed issue preventing Closets from sometimes giving their item
* Fixed tracker freezing the randomizer program when clicking on the sword icon while the `Starting Sword` setting is set to "Random"
* Fixed tracker error when trying to set an entrance for an unrandomized entrance type
* Fixed plandomizer making weird choices with required dungeons
* Fixed the topmost dowsing icon
  * The game will now show the correct dowsing icon when you have the Sea Chart
* Fixed the `Talk to Yerbal` option not working correctly for the `Open Lake Floria` setting
* Fixed Goddess Walls from being activated with only the Goddess's Harp (Ballad of the Goddess is also required)
* Fixed Groose Traps allowing players to obtain the `Lanayru Desert - Rescue Caged Robot` check without defeating the Technoblins
* Fixed incorrect logic for the `Eldin Volcano - Rupee on Ledge before First Room` check
* Fixed some incorrect Goddess Cube logic in Eldin Volcano
* Fixed the Lanayru Gorge region not being highlighted on the bird statue landing map when entering the Lanayru pillar to the surface
* Fixed hint text formatting
* Fixed several typos

## Version 1.0

* Initial release

The differences between HDR and SDR can be found at:
https://github.com/mint-choc-chip-skyblade/sshd-rando/blob/main/docs/differences_between_hdr_and_sdr.md
