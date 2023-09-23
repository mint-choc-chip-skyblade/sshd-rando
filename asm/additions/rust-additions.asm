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

.global set_goddess_sword_pulled_story_flag
.type set_goddess_sword_pulled_story_flag, @function

.global fix_freestanding_item_y_offset
.type fix_freestanding_item_y_offset, @function
