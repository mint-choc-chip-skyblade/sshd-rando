# Changelog

## Version 1.4

### Fixes
* Fixes dungeon end locations not appearing on the tracker
* Fixes the tracker errors when playing on Linux (actually for real this time)
  * Fixes the map assets being missing
  * Fixes the errors when trying to mark various items
* Fixes hint region assignment
  * Shipyard locations should now be correctly hinted to account for not being able to ride the minecart backwards



## Version 1.3

### Fixes
* Fixed issue beatable-only logic could cause errors due to dungeons being inaccessible



## Version 1.2

### Additions and Changes
* Added a setting to allow Sky Keep to be selected as a required dungeon
  * If Sky Keep is chosen as a required dungeon, one of the "Sacred Power" checks (where the Triforces are found in vanilla) is selected as the "goal"
  * Which location is selected as the Sky Keep goal can be found by talking to the stone tablet opposite the bird statue in the first room of Sky Keep
  * Increases the maximum required dungeons to 7
* Unlocked all of Rupins Gear Shop items from the start of the game
  * Allows access to buying the Iron Shield without beating the Skyview Temple
  * Allows access to buying the Sacred Shield (previously not possible)
* Improved which entrances are able to be selected on the tracker
* Added an "Everything Discovered" area to the bottom-left of tracker's map
  * Shows all locations and entrances in areas that can be accessed
* Renamed some misleading location names in the Sealed Grounds spiral
* Improved the tracker logic tooltip for locations that require access to the Bazaar
  * Instead of showing "Impossible (please discover an entrance first)", the tracker now shows "Access Item Check" and "Purchase Shield" where relevant
* Added requirement tooltips to show the logic needed to access an entrance
* Improved how sphere tracking works with Gratitude Crystals
* Removed the obscure logic for accessing Faron Woods by using the Groosenator to unlock bird statues from Flooded Faron Woods
  * There is now a new trick setting which enables this logic
* Updated logic to use the Bomb Throws trick to knock down the Bokoblin tower near the Thrill Digger entrance from behind
* Updated some error messages to give help on how to resolve them
* Decreased the size of the randomizer program by removing several unused assets

### Fixes
* Fixed the tracker issue that caused excessive CPU usage
* Fixed logic for accessing nighttime
  * Logic no longer assumes the player can access surface regions at night
* Fixed incorrect tracker logic when starting with a random sword
* Fixed issue that caused locations to appear in incorrect areas in the tracker
* Fixed softlock when trying to start the Harp minigame during the daytime
* Fixed logic using access to the LMF entrance to access the Chest on top of LMF when LMF isn't raised
* Fixed logic for inside the Pirate Stronghold shark head
* Fixed confusing setup instructions when the `sshd_extract` folder is missing
* Fixed tracker errors when marking items on Linux
* Fixed marked Gossip Stones not being saved on the tracker
* Fixed Thrill Digger Cave always appearing in Eldin Volcano on the tracker with ER enabled
* Fixed Volcano Summit Waterfall area always appearing in Volcano Summit on the tracker with ER enabled
* Fixed mixed pools data not being saved correctly
* Fixed logic for Stamina Fruit checks near the Thrill Digger entrance
* Fixed logic for entering the lower Construction Bay door from Shipyard
* Fixed issue where the player would respawn after death in different locations from the vanilla game
* Fixed several typos



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
