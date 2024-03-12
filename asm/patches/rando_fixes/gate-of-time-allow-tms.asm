; Need Master Sword **or higher** to open the Gate of Time.
.offset 0x7100977df8
b.lt 0x7100977bd0

; onlyif got_sword_requirement == goddess_sword
.offset 0x7100977df4
cmp w8, #1

; onlyif got_sword_requirement == goddess_longsword
.offset 0x7100977df4
cmp w8, #2

; onlyif got_sword_requirement == goddess_white_sword
.offset 0x7100977df4
cmp w8, #3

; onlyif got_sword_requirement == master_sword
.offset 0x7100977df4
cmp w8, #4

; onlyif got_sword_requirement == true_master_sword
.offset 0x7100977df4
cmp w8, #5
