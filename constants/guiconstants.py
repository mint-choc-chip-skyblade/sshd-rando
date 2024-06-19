from PySide6 import QtCore

OPTION_PREFIX = "&nbsp;&nbsp;➜ "

DEFAULT_PRESET = "~~ New Preset ~~"

ITEM_FILTER_TYPES = (
    "Major Items",
    "Item Wheel Items",
    "Main Quest Items",
    "Side Quest Items",
    "Dungeon Items",
    "Boss Keys",
    "Small Keys",
    "Maps",
    "Songs",
)

LOCATION_FILTER_TYPES = (
    "Minigames",
    "Goddess Chests",
    "Gratitude Crystals",
    "Batreaux's Rewards",
    "Scrapper Deliveries",
    "Silent Realms",
    "Stamina Fruits",
    "Closets",
    "Digging Spots",
    "Hidden Items",
    "Underground Rupees",
    "Freestanding Rupees",
    "Beginner Rupees",
    "Intermediate Rupees",
    "Advanced Rupees",
    "Beedle's Airshop",
    "Shop (Cheap)",
    "Shop (Medium)",
    "Shop (Expensive)",
    "Freestanding Items",
    "Chests",
    "NPC",
    "Defeat Boss",
)

TRACKER_TOOLTIP_STYLESHEET = (
    "QToolTip { color: black; background-color: white; border-image: none; border-color: white; "
    + f"qproperty-alignment: {int(QtCore.Qt.AlignmentFlag.AlignCenter)};"
    + " }"
)

TRACKER_LOCATION_TOOLTIP_STYLESHEET = (
    "QToolTip { color: white; background-color: black; border-image: none; border-color: gray; "
    + " border: 2px solid gray; max-width: MAXWIDTHpx; min-width: MINWIDTHpx;"
    + f"qproperty-alignment: {int(QtCore.Qt.AlignmentFlag.AlignLeft)};"
    + " }"
)
