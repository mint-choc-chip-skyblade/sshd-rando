; Start using subsdk8 0x500 bytes into the .text section
; 1st 0x500 bytes are left to make sure none of the subsdk setup is mangled
; The next 0x1000 bytes are reserved for the landingpad
; The next 0x500 bytes are reserved for additions not written in rust


;;;;;;;;;;;;;;;;;;;;;;;;;;
;; additions begin here ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;
.offset 0x712e0a7000
.global handle_custom_item_get
.type handle_custom_item_get, @function

.global handle_startflags
.type handle_startflags, @function

.global check_storyflag
.type check_storyflag, @function

.global set_local_sceneflag
.type set_local_sceneflag, @function

.global unset_local_sceneflag
.type unset_local_sceneflag, @function

.global check_local_sceneflag
.type check_local_sceneflag, @function

.global set_goddess_sword_pulled_story_flag
.type set_goddess_sword_pulled_story_flag, @function

.global fix_freestanding_item_y_offset
.type fix_freestanding_item_y_offset, @function

.global fix_sandship_boat
.type fix_sandship_boat, @function

.global handle_er_cases
.type handle_er_cases, @function

.global handle_er_action_states
.type handle_er_action_states, @function

.global set_stone_of_trials_placed_flag
.type set_stone_of_trials_placed_flag, @function

.global fix_sky_keep_exit
.type fix_sky_keep_exit, @function

.global update_day_night_storyflag
.type update_day_night_storyflag, @function

.global check_night_storyflag
.type check_night_storyflag, @function

.global patch_freestanding_item_fields
.type patch_freestanding_item_fields, @function

.global drop_arrows_bombs_seeds
.type drop_arrows_bombs_seeds, @function

.global drop_nothing
.type drop_nothing, @function

.global fix_item_get_under_water
.type fix_item_get_under_water, @function

.global activation_checks_for_goddess_walls
.type activation_checks_for_goddess_walls, @function

.global set_custom_collection_flag
.type set_custom_collection_flag @function