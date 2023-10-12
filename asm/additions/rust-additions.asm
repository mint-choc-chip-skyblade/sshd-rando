; Start using subsdk8 0x500 bytes into the .text section
; 1st 0x500 bytes are left to make sure none of the subsdk setup is mangled
; The next 0x1000 bytes are reserved for the landingpad


;;;;;;;;;;;;;;;;;;;;;;;;;;
;; additions begin here ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;
.offset 0x360A6500
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
