; Fix SotH inventory text
.offset 0x7100d6f51c
mov w0, #192 ; Lanayru SotH part itemflag
bl 0x71004e1cc0 ; dAcItem::checkItemFlag
