; Start using subsdk8 0x500 bytes into the .text section
; Please leave 0x1000 bytes for this landingpad

; Yes, this in not very optimal. However, this big comparison chain is easier
; to edit and harder to mess up than a more elegant solution. In particular,
; this method makes it very easy to remove functions without having to change
; `w8` across the codebase.

.offset 0x712e0a5500

; custom item gets
cmp w8, #0
b.eq handle_custom_item_get

; don't set AC boko flag on death
cmp w8, #1
b.eq 0x712e0a6500

; startflags
cmp w8, #2
b.eq handle_startflags

; set goddess sword pulled scene flag
cmp w8, #3
b.eq set_goddess_sword_pulled_story_flag

; freestanding item y offset
cmp w8, #4
b.eq fix_freestanding_item_y_offset

; fix sandship boat
cmp w8, #5
b.eq fix_sandship_boat

; handle er cases
cmp w8, #6
b.eq handle_er_cases

; handle er action states
cmp w8, #7
b.eq handle_er_action_states

; fix Sky Keep entrance
cmp w8, #8
b.eq set_stone_of_trials_placed_flag

; update day/night storyflag
cmp w8, #9
b.eq update_day_night_storyflag

cmp w8, #10
b.eq check_night_storyflag

cmp w8, #11
b.eq fix_sky_keep_exit

cmp w8, #12
b.eq check_bucha_local_sceneflag

cmp w8, #13
b.eq handle_crest_hit_give_item

cmp w8, #14
b.eq drop_arrows_bombs_seeds

cmp w8, #15
b.eq drop_nothing

cmp w8, #16
b.eq fix_item_get

cmp w8, #17
b.eq activation_checks_for_goddess_walls

cmp w8, #18
b.eq remove_timeshift_stone_cutscenes

cmp w8, #19
b.eq fix_light_pillars

cmp w8, #20
b.eq custom_event_commands

cmp w8, #21
b.eq warp_to_start

cmp w8, #22
b.eq update_crystal_count

cmp w8, #23
b.eq check_and_modify_item_actor

cmp w8, #24
b.eq npc_traps

cmp w8, #25
b.eq spawned_actor_traps

cmp w8, #26
b.eq fix_tbox_traps

cmp w8, #27
b.eq handle_effect_timers

cmp w8, #28
b.eq setup_traps

cmp w8, #29
b.eq give_squirrel_item

cmp w8, #30
b.eq should_spawn_eldin_platforms

cmp w8, #31
b.eq horwell_always_interactable

cmp w8, #32
b.eq rotate_freestanding_items

cmp w8, #33
b.eq fix_items_in_sand_piles

cmp w8, #34
b.eq init_appearing_chest_subtype

cmp w8, #35
b.eq spawn_appeared_chest

cmp w8, #36
b.eq hide_appearing_chest

cmp w8, #37
b.eq set_correct_boss_key_positions

cmp w8, #38
b.eq set_random_boss_key_positions

cmp w8, #39
b.eq prevent_minigame_death

cmp w8, #40
b.eq is_kikwi_found

cmp w8, #41
b.eq check_and_set_trial_completion_flag

cmp w8, #42
b.eq try_end_pumpkin_archery

cmp w8, #43
b.eq tgreact_spawn_custom_item

cmp w8, #44
b.eq academy_bell_give_custom_item

cmp w8, #45
b.eq after_item_collection_hook

cmp w8, #46
b.eq get_arc_model_from_item

cmp w8, #47
b.eq get_item_model_name_ptr

cmp w8, #48
b.eq change_model_scale

cmp w8, #49
b.eq main_loop_inject

cmp w8, #50
b.eq activate_back_in_time

cmp w8, #51
b.eq handle_closet_traps

cmp w8, #52
b.eq handle_bucha_traps

cmp w8, #53
b.eq handle_ac_boko_and_heartco_and_digspot_traps

cmp w8, #54
b.eq init_rainbow_colors

cmp w8, #55
b.eq check_stage_on_bucha_interaction

cmp w8, #56
b.eq allow_saving_respawn_info_on_new_file_start

cmp w8, #57
b.eq allow_autosave_on_new_file_start

cmp w8, #58
b.eq require_sword_to_enter_trial_gate

cmp w8, #59
b.eq fix_bottle_items_from_npcs

cmp w8, #60
b.eq check_for_botg_itemflag_for_light_tower

cmp w8, #61
b.eq force_traps_to_have_textboxes

cmp w8, #62
b.eq get_custom_freestanding_item_scale

cmp w8, #63
b.eq not_should_pyrup_breathe_fire

cmp w8, #64
b.eq prevent_pyrup_fire_when_underground2

cmp w8, #65
b.eq set_top_dowsing_icon

cmp w8, #66
b.eq load_additional_sfx

cmp w8, #67
b.eq assign_item_textbox_collection_sfx

cmp w8, #68
b.eq get_silent_realm_item_glow_color

cmp w8, #69 ; nice
b.eq give_tadtone_random_item

cmp w8, #70
b.eq check_tadtone_counter_before_song_event

cmp w8, #71
b.eq set_shop_sold_out_storyflag

cmp w8, #72
b.eq check_shop_sold_out_storyflag

cmp w8, #73
b.eq handle_shop_traps

cmp w8, #74
b.eq rotate_shop_items

cmp w8, #75
b.eq set_shop_display_height

cmp w8, #76
b.eq set_boko_base_restricted_sword_flag_before_event

cmp w8, #77
b.eq remove_vanilla_tms_sword_pull_textbox

cmp w8, #78
b.eq fix_boko_base_sword_model

cmp w8, #79
b.eq check_local_sceneflag

cmp w8, #80
b.eq spawn_tree_of_life_item

cmp w8, #81
b.eq fix_memory_leak

cmp w8, #82
b.eq load_custom_bzs

cmp w8, #83
b.eq use_custom_bzs

cmp w8, #84
b.eq check_should_spawn_horwell

cmp w8, #85
b.eq check_should_spawn_remlit

cmp w8, #86
b.eq require_sword_to_enter_sacred_realm

cmp w8, #87
b.eq set_help_menu_strings

cmp w8, #88
b.eq left_justify_help_text

cmp w8, #89
b.eq custom_help_menu_state_change

cmp w8, #90
b.eq check_help_index_bounds

cmp w8, #91
b.eq shop_use_progressive_models

cmp w8, #92
b.eq get_tablet_keyframe_count

cmp w8, #93
b.eq override_inventory_caption_item_text

cmp w8, #94
b.eq randomize_music

ret ; this should never be reached

; ends at 0x712e0a7000
