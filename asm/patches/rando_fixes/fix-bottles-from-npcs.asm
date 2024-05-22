; Give filled bottles instead of filling existing ones
.offset 0x7100516e64
mov w8, #59
bl additions_jumptable

; Don't require having an empty bottle in order to receive a filled bottle
.offset 0x7100516914
b 0x7100516db0
