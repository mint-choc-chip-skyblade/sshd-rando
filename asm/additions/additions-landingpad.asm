; Start using subsdk8 0x500 bytes into the .text section
; Please leave 0x1000 bytes for this landingpad

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
b.eq check_local_sceneflag

cmp w8, #13
b.eq patch_freestanding_item_fields

cmp w8, #14
b.eq drop_arrows_bombs_seeds

cmp w8, #15
b.eq drop_nothing

cmp w8, #16
b.eq fix_item_get_under_water

cmp w8, #17
b.eq activation_checks_for_goddess_walls

cmp w8, #18
b.eq remove_timeshift_stone_cutscenes

ret ; this should never be reached

; ends at 0x712e0a7000
