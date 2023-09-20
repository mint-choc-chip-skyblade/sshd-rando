; Replace setting the Goddess Sword item flag with
; setting a custom story flag to trigger the items
; from pulling the Goddess Sword

.offset 0x08a1759c
bl set_goddess_sword_pulled_scene_flag
