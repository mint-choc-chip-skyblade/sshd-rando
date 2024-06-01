# Differences between HDR and SDR

## New Settings
* Entrance Randomizer with individual settings to control randomized entrance types, entrance
coupling, and mixing pools
* Traps!
* Full Plandomizer Support
* Hints are now controlled by their own settings
* Ammo Availability to control how careful you need to be with deku seeds, bombs, and arrows
* Lots of shortcuts
* In-Game Language
* Item Pool options for minimal, standard, extra, or plentiful amounts of progress items
* Chest Type Matches Contents (CTMC)
* Full Rupee Shuffle
* Single Gratitude Crystal Shuffle
* Stamina Fruit Shuffle
* Hidden Item Shuffle
* NPC Closet Shuffle
* Unlock all Groosenator Destinations
* Sky and Cloud color cosmetic settings
* Low Health Beeping Speed
* Skip Harp Playing when opening trial gates, The Thunderhead, and the Gate of Time
* Random Bottle Contents

## New Setting Options
* Every setting has a `random` option which will pick one of the other options randomly when
generating a seed
* Beatable Only logic option
* Any Dungeon, Own Region, and Overworld options for Small Key and Boss Key shuffles
* Removed option for all Key shuffles which unlocks their doors from the start
* Goddess Chest Shuffle to turn on/off randomization of the items inside Goddess Chests easily
* Correct Orientation option for Randomized Boss Key Puzzles
* The `Random Starting Item` setting is now a count where you can select how many random items you
would like to start with

## New Checks
* All the checks from Full Rupee, Single Gratitude Crystal, Stamina Fruit, Hidden Item, and NPC
Closet shuffles
* `Upper Skyloft - Rescue Remlit above Knight Academy`
* `The Sky - Form a Swirrell Ring above Volcanic Island` / `Lumpy Pumpkin` / `Bamboo Island`

## General Changes
* Tracker built into the randomizer program
* You can hold L to automatically quick charge the bow (even when using button controls)
* You can hold the R, A, and Left Stick buttons all together to soft-reset the game to quickly
return to the titlescreen and go back to your last save point
  * The Back in Time (BiT) glitch does not work by soft-resetting. There is a separate setting
    and button combination which can allow you to experiment with BiT.
* Fi will keep track of any Gossip Stone hints you find. Call her and select "Information" and
then "Notes". She will only tell you hints that you have already found
* All freestanding items spin like Heart Pieces and Triforces so that they are easier to peak
* There are no Spirit of the Sword (SotS) hints. Path hints can be "Path to Demise" which function
similarly to SotS
* Song hints will hint items in the entire Silent Realm beyond the trial gate instead of just the
trial's reward check
* Several small event cutscenes have been removed (e.g. pushing logs, freeing ropes)
* You must climb onto Bucha's back to get the `Faron Woods - Kikwi Elder Reward` check
* The Groosenator is always available in the Sealed Grounds Spiral
* You can call Fi while on fire
* Freestanding item models should all rest on the ground correctly without clipping into the floor
* Speech bubbles will always and only appear above an NPC's head when they have some important
information related to the randomizer (usually checks)
* The `Remove Enemy Music` setting also removes the music which plays when Scaldera and Tentalus
are vulnerable
* All locations and items have cryptic hint text
* Instead of 5 Empty Bottles, HDR has 3 Empty Bottles, a Revitalizing Potion, and a bottle of
Mushroom Spores
* The Imprissoned 2 fight after trying to open the Gate of Time has been removed
* Obtaining Scrapper will automatically activate all the quests associated with him

## Logic Changes
* Required dungeons aren't based on striking the Goddess Crest at the end (or running out the end
entrance of LMF). Required dungeons are only required due to the items placed on their final check
* Required dungeons will place Triforces, then Swords, then other progress items on their final
checks in descending order of priority
* Triforces are *always* required to unlock the doors to the end-game bosses
* You need the Goddess's Harp *and* Ballad of the Goddess to raise the Gate of Time
* You need the Ballad of the Goddess *and* the Goddess's Harp to open The Thunderhead
* You no longer need to beat Moldarach 2 in Shipyard to play the rickety coaster minigame
* `Knight Academy - Item from Cawlin` does not require talking to the Toilet Hand or the Goddess's
Harp
* There are now 4 Song of the Hero parts needed to open the trial gate on Skyloft
* At least Practice Sword is required for entering Trial Gates with the "Thrust Sword" action
* At least Goddess Sword is (only logically) required to defeat Ghirahim 2 (G2). You can still
physically defeat G2 with Practice Sword but the randomizer does not expect you to do so
* You logically need to defeat the Sentrobe in the Lanayru Mining Facility to use the minecart to
get to the northeast room (the vanilla boss key room)
* You logically need to be able to have and use a Shield to defeat Demise, Scervo/Dreadfuse, and
Sentrobes
* You logically need some way to defeat or stun the Deku Baba Inside the Great Tree which guards
the chest
* You logically need the Digging Mitts to collect the crystal ball near the Earth Temple entrance

## Not yet implemented / SDR-only
* Shop randomization
* Flooded Faron Woods randomization
* Chest Dowsing Matches Contents (CDMC) (HDR has CTMC instead)
* Custom Models and Music (you can use the files from SDR to achieve this)
* Random Music (you can use the files from SDR to achieve this)
* Tadtones as items
* Trial Object Shuffle
* Trial Treasure Shuffle
* Starting with a Treasures or Bugs
* Save File text isn't updated for the randomizer
