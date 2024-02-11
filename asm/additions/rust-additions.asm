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

.global update_day_night_storyflag
.type update_day_night_storyflag, @function

.global check_night_storyflag
.type check_night_storyflag, @function

.global fix_sky_keep_exit
.type fix_sky_keep_exit, @function

.global setup_traps
.type setup_traps, @function

.global drop_arrows_bombs_seeds
.type drop_arrows_bombs_seeds, @function

.global drop_nothing
.type drop_nothing, @function

.global fix_item_get_under_water
.type fix_item_get_under_water, @function

.global activation_checks_for_goddess_walls
.type activation_checks_for_goddess_walls, @function

.global remove_timeshift_stone_cutscenes
.type remove_timeshift_stone_cutscenes, @function

.global fix_light_pillars
.type fix_light_pillars, @function

.global custom_event_commands
.type custom_event_commands, @function

.global warp_to_start
.type warp_to_start, @function

.global update_crystal_count
.type update_crystal_count, @function

.global check_and_modify_item_actor
.type check_and_modify_item_actor, @function

.global npc_traps
.type npc_traps, @function

.global spawned_actor_traps
.type spawned_actor_traps, @function

.global fix_tbox_traps
.type fix_tbox_traps, @function

.global handle_effect_timers
.type handle_effect_timers, @function

.global should_spawn_eldin_platforms
.type should_spawn_eldin_platforms, @function

.global give_squirrel_item
.type give_squirrel_item, @function

.global set_boss_key_positions
.type set_boss_key_positions, @function

.global set_random_key_positions
.type set_random_key_positions, @function

.global prevent_minigame_death
.type prevent_minigame_death, @function