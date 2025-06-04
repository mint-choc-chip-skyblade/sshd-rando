# Changelog

## Version 2.1

### Additions and Changes
* Updated other mods support to allow mod makers to globally replace arcs by placing them in the `[mod-name]/oarc` folder
  * Mods still need to have a `[mod-name]/romfs` folder in order to work with the randomizer
* Updated other mods support to allow mod makers to put arcs in the `[mod-name]/romfs/Object/NX` folder instead of having to share a modified `ObjectPack.arc.LZ` as part of their mod
* Updated the `Damage Multiplier` setting to accept a value of zero
  * When set to zero, the player will be invincible and take no damage
* Added some German translations for randomizer text added in version 2.0
* Moves the `Unlock all Groosenator Destinations` to the "Advanced" tab of the randomizer GUI

### Fixes
* Fixed softlock when trying to open the Faron trial gate after collecting the `Faron Woods - Kikwi Elder's Reward` and the "Scrapper" item
* Fixed tracker error when the `Trial Treasure Shuffle` setting was set to `Random`
* Fixed freestanding model scale for the "Dusk Relic" item so that it no longer appears very small
* Fixed logic for flying at night when the `Natural Night Connections` setting is turned off
* Fixed incorrect logic for traversing the tight rope before the Skyview Temple boss door
* Fixed incorrect logic of obtaining stamina fruit locations near the Eldin Volcano hot cave area (`Eldin Volcano - Stamina Fruit after Last Boko Camp Tower`, `Eldin Volcano - Stamina Fruit on Ledge near Hot Cave`, `Eldin Volcano - Stamina Fruit on Vines near Hot Cave`)
* Fixed issue where the tracker would show any "Song of the Hero" requirement twice
* Fixed issue where freestanding items would spawn inside Silent Realms when they were accessed via the Boss Rush minigame
* Fixed issue where players could use Fi's "Warp to Start" feature while in the Boss Rush minigame and lose access to key items
* Fixed issue where the help menu would incorrectly show the "Scrapper" item as unobtained at all times
* Fixed issue where applying presets would duplicate the settings and create inconsistencies between the settings shown in the randomizer program and the settings used to generate seeds
* Fixed issue where the sold out sign in Beedle's Airshop would sometimes clip into the table or float above it
* Fixed issue causing seeds to fail to generate when the `Decouple Entrances` setting is enabled



## Version 2.0

### Additions and Changes
* Overhauled the randomizer patching system
  * Shrinks the output size of randomizer patches by approximately 95%
  * Fixes a memory leak in the original game code previously preventing such an optimization
  * The first time a seed is generated, the randomizer program will need to extract a lot of data and will take longer to randomize than normal
* Added `Beedle's Airshop Shuffle`
  * The 10 shop items which Beedle sells are now randomized locations
  * Also added a `Randomize Shop Prices` setting
    * Shop prices will be randomized in such a way that the logic doesn't change
    * E.g. the `Beedle's Airshop - 300 Rupee Item` location will have a random price between 0 and 300 Rupees (as any more would require a bigger wallet)
  * Shop items will rotate like freestanding items
* Added `Trial Treasure Shuffle`
  * The 10 Dusk Relics within each Silent Realm have been turned into randomized locations
  * The `Trial Treasure Shuffle` setting controls how many relic locations are shuffled in each Silent Realm
  * Colleting a Light Fruit will highlight the trial's Tears in the trials main color and any non-relic items in a secondary color
* Added `Tadtone Shuffle`
  * Randomizes the 17 tadtone groups swimming around in Flooded Faron Woods
  * Adds 17 "Group of Tadtones" items to the item pool
    * The "Group of Tadtones" items will randomly use one of the two vanilla tadtones models
    * When all 17 have been collected, the `Flooded Faron Woods - Water Dragon's Reward` location can be obtained by talking to the Water Dragon
* Added experimental support for other mods to work with the randomizer
  * Create mod packs inside the `other_mods` folder
    * Any folders within the `other_mods` folder will show up as mod packs on the "Advanced" tab of the randomizer program
    * For a mod to be valid, it must contain a `romfs` folder directly inside the main mod pack's folder
    * The contents of the `romfs` folder must mirror the contents of the `sshd_extract/romfs` folder
* Added a `Minigame Difficulty` setting
  * Controls if minigames are `Hard`, `Vanilla`, `Easy`, or a `Guaranteed Win`
  * Scales the Pumpkin Archery, Harp Minigame, High Dive, Rickety Coaster, Bug Heaven, and Clean Cut minigames
    * Pumpkin Archery requires 800, 600, 400, or 0 points to obtain the randomized item
    * Harp Minigame requires better or worse playing depending on what the `Minigame Difficulty` setting is set to (both `Easy` and `Guaranteed Win` will allow the randomized item to be obtained without actually playing the harp)
    * High Dive will double the speed of the island, not change anything, half the speed of the island (virtually still after collecting all 5 rings), or guarantee the maximum reward is given
    * Rickety Coaster requires a time less than 1min 2secs, 1min 5secs, 1min 10secs, or just to make it around the track to obtain the randomized item
    * Bug Heaven requires a time less than 2 minutes, 3 minutes, 5 minutes, 10 minutes to obtain the randomized item
      * When set to `Easy` or `Guaranteed Win`, the Big Bug Net is logically required instead of just the Bug Net
    * Clean Cut requires 43 points, 28 points, 20 points, or 1 point to obtain a Rare Treasure
  * Minigames with multiple modes (Rickety Coaster and Bug Heaven) have their other modes scaled as well (potentially to become logical rupee farming methods in the future)
  * When set to `Guaranteed Win`, minigames with different rewards based on performance can be chosen to suit the player's needs
* Changed the in-game help menu to show information about items which don't appear on the inventory screen
  * Shows information about whether each dungeon has been complete or not
  * Shows information about the number of Small Keys, Boss Keys, and Maps found for each dungeon
  * Shows information about the Lanayru Caves Small Keys, Life Tree Fruit, Life Tree Seedling, Spiral Charge, Scrapper, and Group of Tadtones
* Added settings for choosing where different hint types should be placed
  * Each hint type can be placed on Gossip Stones, Fi, both, or neither
  * Currently, all hint types are placed on Gossip Stones except barren hints which are placed on Fi
* Added the `Hint Importance` setting
  * When enabled, location and item hints will say whether the hinted location/item is "required", "possibly required", or "not required" to beat the game
* Added the `Sealed Temple - Collect Fruit from the Tree of Life` location
  * Adds the Life Tree Seedling item to the item pool
  * Planting it in Hylia's Temple in the past will make a tree grow in the Sealed Temple in the present which can be bonked to obtain a randomized item
* Added the `Knight Academy - Deliver Barrel to Henya the Lunch Lady` location
  * Carry the barrel in the Knight Academy and place it in front of Henya the lunch lady to receive a randomized item
* Added the `Knight Academy - Horwell's Closet` location and unlocked Professor Horwell's bedroom door
* Changed Rupin's night market and Strich's bug collection to cycle between the treasures and bugs they sell without having to sleep
* Changed the `Bokoblin Base - Raised Chest in Volcano Summit` from a chest to raising the True Master Sword (like in vanilla)
  * To account for this, this location has been renamed `Bokoblin Base - Raise Sword`
  * Due to event limitations (potentially solvable in the future), the sword will appear as a chest once Bokoblin Base has been beaten
    * When the `Chest Type Matches Contents` setting isn't turned off, this workaround chest will always be a big blue chest (or a fancy chest if it contains a key) to encourage players to pull the sword rather than waiting to see the chest type
* Added support for Boss Rush
  * Adds the `Lanayru Gorge - Boss Rush 4 Bosses` and `Lanayru Gorge - Boss Rush 8 Bosses` locations
  * The Thunderdragon will say what the rewards for each location and ask to confirm if you would like to start Boss Rush
* Updated how the item pool is created so that the quantity of various rupees and treasures changed depending on which shuffles are enabled
  * If the `Goddess Chest Shuffle` setting is turned off, there will be fewer Gold Rupees in the item pool
  * If the `Hidden Item Shuffle` or `Rupee Shuffle` settings are enabled, more Green Rupees and Blue Rupees will be in the item pool
* Unlocked the ability to purchase Stamina Potions and Air Potions from the beginning of the game
  * Raising (or beating) the Lanayru Mining Facility is no longer required to purchase Stamina Potions
  * Obtaining the Water Dragon's Scale is no longer required to purchase Air Potions
  * The `Knight Academy - Help Fledge Workout` location no longer requires raising (or beating) the Lanayru Mining Facility to be logically obtained
* Changed the in-game inventory screen to show the correct Ancient Tablets
  * Previously, players would need to look at which light pillars were opened in The Sky to determine which Ancient Tablets they had in their inventory
  * Now the in-game inventory screen accurately displays this information
  * The warning after the first seed has been generated has been updated (it now only warns about the heart container models for the `Defeat Boss` locations)
* Added the `Allow Flying at Night` setting
  * Allows the loftwing to be called when diving at night
  * This setting doesn't change anything logically and just allows players to experiment (yes, this can be used to obtain locations out of logic)
  * If the `Require Natural Night Connections` setting is turned off, loftwing will be able to be flown at night as this may be logically required
* Added the `Require Natural Night Connections` setting to the randomizer program
  * Adds a GUI toggle for this setting (it previously needed to be enabled by editing the `config.yaml` file manually)
  * When enabled, logic will require that the player can reach night time only locations only by traversing through areas of the game which are normally reachable at night time
  * When disabled, the night time state will persist everywhere in the game
    * The only way to change the time of day is by sleeping
    * Most surface regions will appear a lot darker at night (most of the Lanayru Sand Sea isn't changed due to a quirk of how the night time filter works)
    * You may be logically expected to fly the loftwing at night
* Added the `Randomize Music` setting
  * Background and cutscene music can be shuffled
  * When set to `Shuffle`, music will be shuffled but some music may be shuffled to its vanilla location
  * When set to `Shuffle (Limit Vanilla)`, music will be shuffled in a way to prevent unchanged/vanilla music
  * The `Cutoff Game Over Music` controls if the game over music will continue playing after the player respawns until the track is finished or if it gets cut off when the player respawns instead
* Added unique sound effects to play when collecting Heart Containers and Ancient Tablets
* Removed the forced text trigger in the second trapped mogma room in Fire Sanctuary (where the `Fire Sanctuary - Chest from Second Trapped Mogma` location is)
* Changed the gates to the Goddess's Realm in Sky Keep to require a sword (mirrors the change to make trial gates require a sword)
* Updated the default presets with the new settings
* Changed default option for the `Open Lake Floria` setting from `Vanilla` to `Open`
* Changed the default option for the `Chest Type Matches Contents` setting from `Off` to `All Contents`
* Changed the default option for the `Deep Woods Log before Temple` setting from `Off` to `On`
* Added logic for the `Faron Woods - Stamina Fruit on Vines below First Log` location to be collectable from the vanilla entrance to Faron Woods with the Beetle
* Changed logic for the `Faron Woods - Stamina Fruit on Vines on Great Tree` location to require Clawshots or Quick Beetle instead of just Beetle
* Changed the "Randomize" button in the bottom right of the randomizer program will now read "Verify Extract" until the first time verification has been completed
  * Clicking the "Verify Extract" button will allow the first time verification to be performed without having to close and re-open the randomizer program
* Added clearer error messages in some places
* Added the `Sky Keep Lower Bars in Fire Sanctuary Room` and `Sky Keep Upper Bars in Fire Sanctuary Room` shortcut settings
* Unlocked Heart Dowsing from the start of the game
* Renamed various locations
* Reordered various locations so that they appear on the tracker in a more intuitive order
* Renamed `Wryna's House` to `Kukiel's House` to match the vanilla game
* Renamed `Mallara's House` to `Pipit's House` to match the vanilla game
* Changed all uses of the "SV" abbreviation for "Skyview Temple" to "SVT"

### Fixes
* Fixed issue where collecting the Sacred Water item in the Sealed Grounds Spiral would start a Groosenator event
* Reduced the failure rate of various entrance shuffles
* Fixed crash when entering Inside the Thunderhead after activating but not finishing the Levias fight
* Fixed Linux build name so it can be executed instead of opened as a man page
* Fixed issue with the location calculations for the `Chest Type Matches Contents` setting
* Fixed issue where the `Include Sky Keep as a Dungeon` and `Required Dungeons` settings could conflict when either is set to the "Random" option
* Fixed incorrect time of day logic for the Bazaar entrances
* Fixed logic for exiting Inside the Thunderhead
* Fixed logic for the `Lanayru Mining Facility - Chest after Armos Fight` location
* Fixed logic for `Sky Keep - Chest after Dreadfuse Fight` location
* Fixed logic error where starting at the `Pirate Stronghold Top Door from Pirate Stronghold Inside the Shark Head` entrance would incorrectly not require raising the Pirate Stronghold shark head (and therefore the Gust Bellows) to obtain the Pirate Stronghold Goddess Cube
* Fixed issue where regions could be hinted as barren multiple times
* Fixed issue where the hints would be inconsistent when generating the same seed multiple times
* Fixed issue where the main deck of the Sandship would play the incorrect music causing the music to stop when the timeshift stone was active
* Fixed minor text formatting issues and spelling mistakes



## Version 1.4

### Additions and Changes
* Added community German language translations for the text added and changed by the randomizer

### Fixes
* Fixed dungeon end locations not appearing on the tracker
* Fixed the tracker errors when playing on Linux (actually for real this time)
  * Fixed the map assets being missing
  * Fixed the errors when trying to mark various items
* Fixed incorrect logic for the `Lake Floria - Chest near Bird Statue`
* Fixed hint region assignment
  * Shipyard locations should now be correctly hinted to account for not being able to ride the minecart backwards
* Fixed incorrect labelling of double doors when the `Decouple Double Doors` setting is disabled
* Fixed error when re-assigning entrances when the `Decouple Entrances` setting is disabled



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
