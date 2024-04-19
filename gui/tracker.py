from logic.world import World
from logic.settings import SettingMap
from logic.search import *
from util.text import load_text_data
from typing import TYPE_CHECKING
import copy

from sslib.yaml import yaml_load
import yaml

from PySide6.QtWidgets import (
    QSizePolicy,
    QMessageBox,
    QLabel,
    QLayout,
    QSpacerItem,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6 import QtCore

from gui.components.tracker_inventory_button import TrackerInventoryButton
from gui.components.tracker_dungeon_label import TrackerDungeonLabel
from gui.components.tracker_area import TrackerArea
from gui.components.tracker_back_button import TrackerBackButton
from gui.components.tracker_location_label import TrackerLocationLabel
from gui.dialogs.fi_question_dialog import FiQuestionDialog

from constants.itemconstants import *
from filepathconstants import *
from constants.randoconstants import VERSION

from logic.config import write_config_to_file, load_config_from_file

if TYPE_CHECKING:
    from gui.main import Main
    from gui.ui.ui_main import Ui_main_window


class Tracker:

    map_widget_stylesheet = f'border-image: url("{TRACKER_ASSETS_PATH.as_posix()}/maps/IMAGE_FILENAME"); background-repeat: none; background-position: center;'

    def __init__(self, main: "Main", ui: "Ui_main_window") -> None:
        load_text_data()
        self.main = main
        self.ui = ui
        self.world: World = None
        self.inventory: Counter[Item] = Counter()
        self.started: bool = False
        self.areas: dict[str, TrackerArea] = {}
        self.active_area: TrackerArea = None

        # Display the Sky if there's no active tracker
        self.ui.map_widget.setStyleSheet(
            Tracker.map_widget_stylesheet.replace("IMAGE_FILENAME", "Sky.png")
        )

        self.init_buttons()
        self.assign_buttons_to_layout()
        self.load_tracker_autosave()

        self.ui.start_new_tracker_button.clicked.connect(
            self.on_start_new_tracker_button_clicked
        )

    def init_buttons(self):

        self.sv_small_key_button = TrackerInventoryButton(
            ["Nothing", SV_SMALL_KEY, SV_SMALL_KEY],
            [
                "dungeons/0_smallKey.png",
                "dungeons/1_smallKey.png",
                "dungeons/2_smallKey.png",
            ],
        )
        self.et_key_piece_button = TrackerInventoryButton(
            ["Nothing", KEY_PIECE, KEY_PIECE, KEY_PIECE, KEY_PIECE, KEY_PIECE],
            [
                "dungeons/et_key_0.png",
                "dungeons/et_key_1.png",
                "dungeons/et_key_2.png",
                "dungeons/et_key_3.png",
                "dungeons/et_key_4.png",
                "dungeons/et_key_5.png",
            ],
        )
        self.lmf_small_key_button = TrackerInventoryButton(
            ["Nothing", LMF_SMALL_KEY],
            ["dungeons/0_smallKey.png", "dungeons/1_smallKey.png"],
        )
        self.ac_small_key_button = TrackerInventoryButton(
            ["Nothing", AC_SMALL_KEY, AC_SMALL_KEY],
            [
                "dungeons/0_smallKey.png",
                "dungeons/1_smallKey.png",
                "dungeons/2_smallKey.png",
            ],
        )
        self.ssh_small_key_button = TrackerInventoryButton(
            ["Nothing", SSH_SMALL_KEY, SSH_SMALL_KEY],
            [
                "dungeons/0_smallKey.png",
                "dungeons/1_smallKey.png",
                "dungeons/2_smallKey.png",
            ],
        )
        self.fs_small_key_button = TrackerInventoryButton(
            ["Nothing", FS_SMALL_KEY, FS_SMALL_KEY, FS_SMALL_KEY],
            [
                "dungeons/0_smallKey.png",
                "dungeons/1_smallKey.png",
                "dungeons/2_smallKey.png",
                "dungeons/3_smallKey.png",
            ],
        )
        self.sk_small_key_button = TrackerInventoryButton(
            ["Nothing", SK_SMALL_KEY],
            ["dungeons/0_smallKey.png", "dungeons/1_smallKey.png"],
        )

        self.sv_boss_key_button = TrackerInventoryButton(
            ["Nothing", SV_BOSS_KEY],
            ["dungeons/sv_noBossKey.png", "dungeons/SS_Golden_Carving_Icon.png"],
        )
        self.et_boss_key_button = TrackerInventoryButton(
            ["Nothing", ET_BOSS_KEY],
            ["dungeons/et_noBossKey.png", "dungeons/SS_Dragon_Sculpture_Icon.png"],
        )
        self.lmf_boss_key_button = TrackerInventoryButton(
            ["Nothing", LMF_BOSS_KEY],
            ["dungeons/lmf_noBossKey.png", "dungeons/SS_Ancient_Circuit_Icon.png"],
        )
        self.ac_boss_key_button = TrackerInventoryButton(
            ["Nothing", AC_BOSS_KEY],
            ["dungeons/ac_noBossKey.png", "dungeons/SS_Blessed_Idol_Icon.png"],
        )
        self.ssh_boss_key_button = TrackerInventoryButton(
            ["Nothing", SSH_BOSS_KEY],
            ["dungeons/ssh_noBossKey.png", "dungeons/SS_Squid_Carving_Icon.png"],
        )
        self.fs_boss_key_button = TrackerInventoryButton(
            ["Nothing", FS_BOSS_KEY],
            ["dungeons/fs_noBossKey.png", "dungeons/SS_Mysterious_Crystals_Icon.png"],
        )
        self.sk_sot_button = TrackerInventoryButton(
            ["Nothing", STONE_OF_TRIALS],
            ["dungeons/No_Stone_of_Trials.png", "dungeons/Stone_of_Trials.png"],
        )

        self.bombs_button = TrackerInventoryButton(
            ["Nothing", BOMB_BAG], ["Bomb_Silhouette.png", "Bomb_Icon.png"]
        )
        self.slingshot_button = TrackerInventoryButton(
            ["Nothing", PROGRESSIVE_SLINGSHOT, PROGRESSIVE_SLINGSHOT],
            ["Slingshot_Silhouette.png", "Slingshot_Icon.png", "Scattershot_Icon.png"],
        )
        self.beetle_button = TrackerInventoryButton(
            [
                "Nothing",
                PROGRESSIVE_BEETLE,
                PROGRESSIVE_BEETLE,
                PROGRESSIVE_BEETLE,
                PROGRESSIVE_BEETLE,
            ],
            [
                "Beetle_Silhouette.png",
                "Beetle_Icon.png",
                "Hook_Beetle_Icon.png",
                "Quick_Beetle_Icon.png",
                "Tough_Beetle_Icon.png",
            ],
        )
        self.bug_net_button = TrackerInventoryButton(
            ["Nothing", PROGRESSIVE_BUG_NET, PROGRESSIVE_BUG_NET],
            ["Bugnet_Silhouette.png", "Bugnet_Icon.png", "Big_Bugnet_Icon.png"],
        )
        self.bow_button = TrackerInventoryButton(
            ["Nothing", PROGRESSIVE_BOW, PROGRESSIVE_BOW, PROGRESSIVE_BOW],
            [
                "Bow_Silhouette.png",
                "Bow_Icon.png",
                "Iron_Bow_Icon.png",
                "Sacred_Bow_Icon.png",
            ],
        )
        self.clawshots_button = TrackerInventoryButton(
            ["Nothing", CLAWSHOTS], ["Clawshots_Silhouette.png", "Clawshots_Icon.png"]
        )
        self.whip_button = TrackerInventoryButton(
            ["Nothing", WHIP], ["Whip_Silhouette.png", "Whip_Icon.png"]
        )
        self.gust_bellows_button = TrackerInventoryButton(
            ["Nothing", GUST_BELLOWS],
            ["Gust_Bellows_Silhouette.png", "Gust_Bellows_Icon.png"],
        )

        self.sword_button = TrackerInventoryButton(
            [
                "Nothing",
                PROGRESSIVE_SWORD,
                PROGRESSIVE_SWORD,
                PROGRESSIVE_SWORD,
                PROGRESSIVE_SWORD,
                PROGRESSIVE_SWORD,
                PROGRESSIVE_SWORD,
            ],
            [
                "swords/No_Sword.png",
                "swords/Practice Sword.png",
                "swords/Goddess Sword.png",
                "swords/Goddess Long Sword.png",
                "swords/Goddess White Sword.png",
                "swords/Master Sword.png",
                "swords/True Master Sword.png",
            ],
        )
        self.sword_button.setMinimumSize(50, 200)
        self.sword_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.lanayru_caves_key_button = TrackerInventoryButton(
            ["Nothing", LC_SMALL_KEY, LC_SMALL_KEY],
            [
                "dungeons/0_smallKey.png",
                "dungeons/1_smallKey.png",
                "dungeons/2_smallKey.png",
            ],
        )
        self.sea_chart_button = TrackerInventoryButton(
            ["Nothing", SEA_CHART], ["no_sea_chart.png", "sea_chart.png"]
        )
        self.spiral_charge_button = TrackerInventoryButton(
            ["Nothing", SPIRAL_CHARGE], ["no_bird_statuette.png", "bird_statuette.png"]
        )
        self.adventure_pouch_button = TrackerInventoryButton(
            [
                "Nothing",
                PROGRESSIVE_POUCH,
                PROGRESSIVE_POUCH,
                PROGRESSIVE_POUCH,
                PROGRESSIVE_POUCH,
                PROGRESSIVE_POUCH,
            ],
            # TODO - separate images for each pouch
            [
                "no_pouch.png",
                "pouch.png",
                "pouch.png",
                "pouch.png",
                "pouch.png",
                "pouch.png",
            ],
        )
        self.bottle_button = TrackerInventoryButton(
            [
                "Nothing",
                EMPTY_BOTTLE,
                EMPTY_BOTTLE,
                EMPTY_BOTTLE,
                EMPTY_BOTTLE,
                EMPTY_BOTTLE,
            ],
            # TODO - separate images for each bottle
            [
                "no_bottle.png",
                "bottle.png",
                "bottle.png",
                "bottle.png",
                "bottle.png",
                "bottle.png",
            ],
        )
        self.wallet_button = TrackerInventoryButton(
            [
                "Nothing",
                PROGRESSIVE_WALLET,
                PROGRESSIVE_WALLET,
                PROGRESSIVE_WALLET,
                PROGRESSIVE_WALLET,
            ],
            [
                "wallets/smallWallet.png",
                "wallets/mediumWallet.png",
                "wallets/bigWallet.png",
                "wallets/giantWallet.png",
                "wallets/tycoonWallet.png",
            ],
        )
        self.mitts_button = TrackerInventoryButton(
            ["Nothing", PROGRESSIVE_MITTS, PROGRESSIVE_MITTS],
            [
                "main quest/no_mitts_grid.png",
                "main quest/Digging_Mitts.png",
                "main quest/Mogma_Mitts.png",
            ],
        )

        self.harp_button = TrackerInventoryButton(
            ["Nothing", GODDESS_HARP],
            ["main quest/no_harp_grid.png", "main quest/Goddess_Harp.png"],
        )
        self.ballad_of_the_goddess_button = TrackerInventoryButton(
            ["Nothing", BALLAD_OF_THE_GODDESS],
            ["songs/no_ballad_grid.png", "songs/Ballad_of_the_Goddess.png"],
        )
        self.farores_courage_button = TrackerInventoryButton(
            ["Nothing", FARORES_COURAGE],
            ["songs/no_courage_grid.png", "songs/Farores_Courage.png"],
        )
        self.nayrus_wisdom_button = TrackerInventoryButton(
            ["Nothing", NAYRUS_WISDOM],
            ["songs/no_wisdom_grid.png", "songs/Nayrus_Wisdom.png"],
        )
        self.dins_power_button = TrackerInventoryButton(
            ["Nothing", DINS_POWER], ["songs/no_power_grid.png", "songs/Dins_Power.png"]
        )
        self.song_of_the_hero_button = TrackerInventoryButton(
            ["Nothing", FARON_SOTH_PART, ELDIN_SOTH_PART, LANAYRU_SOTH_PART],
            [
                "songs/no_soth_grid.png",
                "songs/soth_grid_1.png",
                "songs/soth_grid_2.png",
                "songs/soth_grid_3.png",
            ],
        )
        self.triforce_button = TrackerInventoryButton(
            ["Nothing", TRIFORCE_OF_COURAGE, TRIFORCE_OF_WISDOM, TRIFORCE_OF_POWER],
            [
                "main quest/No_Triforce_Grid.png",
                "main quest/1_Triforce_Grid.png",
                "main quest/2_Triforce_Grid.png",
                "main quest/Full_Triforce_Grid.png",
            ],
        )

        self.water_dragon_scale_button = TrackerInventoryButton(
            ["Nothing", WATER_DRAGON_SCALE],
            ["main quest/no_scale_grid.png", "main quest/Water_Dragon_Scale.png"],
        )
        self.fireshield_earrings_button = TrackerInventoryButton(
            ["Nothing", FIRESHIELD_EARRINGS],
            ["main quest/no_earrings_grid.png", "main quest/FireShield_Earrings.png"],
        )
        self.cawlins_latter_button = TrackerInventoryButton(
            ["Nothing", CAWLINS_LETTER],
            ["sidequests/no_cawlins_letter_grid.png", "sidequests/cawlins_letter.png"],
        )
        self.insect_cage_button = TrackerInventoryButton(
            ["Nothing", BEEDLES_INSECT_CAGE],
            ["sidequests/no_cbeetle_grid.png", "sidequests/cbeetle.png"],
        )
        self.rattle_button = TrackerInventoryButton(
            ["Nothing", RATTLE],
            ["sidequests/no_rattle_grid.png", "sidequests/rattle.png"],
        )
        self.gratitude_crystals_button = TrackerInventoryButton(
            ["Nothing"] + [GRATITUDE_CRYSTAL_PACK] * 16,
            ["sidequests/no_crystal_grid.png"]
            + [f"sidequests/crystal_{i * 5}.png" for i in range(1, 17)],
        )
        self.life_tree_fruit_button = TrackerInventoryButton(
            ["Nothing", LIFE_TREE_FRUIT],
            ["main quest/no_ltf.png", "main quest/ltf.png"],
        )

        self.tadtones_button = TrackerInventoryButton(
            ["Nothing", GROUP_OF_TADTONES],
            ["main quest/no_tadtones.png", "main quest/tadtones.png"],
        )
        self.scrapper_button = TrackerInventoryButton(
            ["Nothing", SCRAPPER],
            ["main quest/No_Scrapper.png", "main quest/Scrapper.png"],
        )

        # Delcare amber tablet first so it placed below the ruby and emerald tablets.
        # Due to how the pictures are arranged, it makes more sense for the ruby and
        # emerald tablets to be above the amber tablet.
        self.amber_tablet_button = TrackerInventoryButton(
            ["Nothing", AMBER_TABLET],
            ["tablets/amber_tablet_gray.png", "tablets/amber_tablet.png"],
            self.ui.tablet_widget,
        )
        self.emerald_tablet_button = TrackerInventoryButton(
            ["Nothing", EMERALD_TABLET],
            ["tablets/emerald_tablet_gray.png", "tablets/emerald_tablet.png"],
            self.ui.tablet_widget,
        )
        self.ruby_tablet_button = TrackerInventoryButton(
            ["Nothing", RUBY_TABLET],
            ["tablets/ruby_tablet_gray.png", "tablets/ruby_tablet.png"],
            self.ui.tablet_widget,
        )

        # Manually set the positions of the tablet buttons so they can overlap
        # each other and fit together
        self.emerald_tablet_button.setFixedSize(74, 66)
        self.emerald_tablet_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.emerald_tablet_button.move(68, 90)
        self.ruby_tablet_button.setFixedSize(101, 52)
        self.ruby_tablet_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ruby_tablet_button.move(40, 49)
        self.amber_tablet_button.setFixedSize(70, 107)
        self.amber_tablet_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.amber_tablet_button.move(3, 49)

        # Load in tracker area buttons
        area_button_data = yaml_load(TRACKER_AREAS_PATH)
        for area_button_node in area_button_data:
            area_name = area_button_node["name"]
            area_image = area_button_node.get("image", "")
            area_children = area_button_node.get("children", [])
            area_x = area_button_node.get("x", -1)
            area_y = area_button_node.get("y", -1)
            border_radius = "6"
            if area_type := area_button_node.get("type", None):
                if area_type == "Dungeon Entrance":
                    border_radius = "0"
                elif area_type == "Trial Gate":
                    border_radius = "15"
            alias = area_button_node.get("alias", "")
            self.areas[area_name] = TrackerArea(
                area_name,
                area_image,
                area_children,
                area_x,
                area_y,
                self.ui.map_widget,
                border_radius,
                alias,
            )
            self.areas[area_name].change_map_area.connect(self.set_map_area)
            self.areas[area_name].show_locations.connect(self.show_area_locations)

        # Set parent areas of tracker area buttons
        for area_name, area_button in self.areas.items():
            area_button.tracker_children = list(
                map(
                    lambda area_name: self.areas[area_name],
                    area_button.tracker_children,
                )
            )
            for child in area_button.tracker_children:
                child.area_parent = area_button

        # Create the back button
        self.back_button = TrackerBackButton("Back", self.ui.map_widget)
        self.back_button.move(40, 30)
        self.back_button.setStyleSheet(
            "border-image: none; background-color: none; color: black; font-size: 14pt;"
        )
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.back_button.setVisible(False)

        # Set size policy for start new tracker button to push everything left
        self.ui.start_new_tracker_button.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Fixed
        )

        # Add vertical spacer to the inventory button layout to push all the buttons up
        self.ui.inventory_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def assign_buttons_to_layout(self) -> None:
        self.ui.dungeon_sv_keys_layout.addWidget(self.sv_small_key_button)
        self.ui.dungeon_sv_keys_layout.addWidget(self.sv_boss_key_button)
        self.ui.dungeon_et_keys_layout.addWidget(self.et_key_piece_button)
        self.ui.dungeon_et_keys_layout.addWidget(self.et_boss_key_button)
        self.ui.dungeon_lmf_keys_layout.addWidget(self.lmf_small_key_button)
        self.ui.dungeon_lmf_keys_layout.addWidget(self.lmf_boss_key_button)
        self.ui.dungeon_ac_keys_layout.addWidget(self.ac_small_key_button)
        self.ui.dungeon_ac_keys_layout.addWidget(self.ac_boss_key_button)
        self.ui.dungeon_ssh_keys_layout.addWidget(self.ssh_small_key_button)
        self.ui.dungeon_ssh_keys_layout.addWidget(self.ssh_boss_key_button)
        self.ui.dungeon_fs_keys_layout.addWidget(self.fs_small_key_button)
        self.ui.dungeon_fs_keys_layout.addWidget(self.fs_boss_key_button)
        self.ui.dungeon_sk_keys_layout.addWidget(self.sk_small_key_button)
        self.ui.dungeon_sk_keys_layout.addWidget(self.sk_sot_button)

        self.ui.dungeon_sv_layout.addWidget(TrackerDungeonLabel("SV"))
        self.ui.dungeon_et_layout.addWidget(TrackerDungeonLabel("ET"))
        self.ui.dungeon_lmf_layout.addWidget(TrackerDungeonLabel("LMF"))
        self.ui.dungeon_ac_layout.addWidget(TrackerDungeonLabel("AC"))
        self.ui.dungeon_ssh_layout.addWidget(TrackerDungeonLabel("SSH"))
        self.ui.dungeon_fs_layout.addWidget(TrackerDungeonLabel("FS"))
        self.ui.dungeon_sk_layout.addWidget(TrackerDungeonLabel("SK"))

        self.ui.inventory_b_wheel_layout.addWidget(self.beetle_button, 0, 0)
        self.ui.inventory_b_wheel_layout.addWidget(self.slingshot_button, 0, 1)
        self.ui.inventory_b_wheel_layout.addWidget(self.bombs_button, 0, 2)
        self.ui.inventory_b_wheel_layout.addWidget(self.bug_net_button, 0, 3)
        self.ui.inventory_b_wheel_layout.addWidget(self.bow_button, 1, 0)
        self.ui.inventory_b_wheel_layout.addWidget(self.clawshots_button, 1, 1)
        self.ui.inventory_b_wheel_layout.addWidget(self.whip_button, 1, 2)
        self.ui.inventory_b_wheel_layout.addWidget(self.gust_bellows_button, 1, 3)

        self.ui.inventory_sword_layout.addWidget(self.sword_button)

        self.ui.lower_inventory_layout.addWidget(self.lanayru_caves_key_button, 0, 0)
        self.ui.lower_inventory_layout.addWidget(self.sea_chart_button, 0, 1)
        self.ui.lower_inventory_layout.addWidget(self.spiral_charge_button, 0, 2)
        self.ui.lower_inventory_layout.addWidget(self.adventure_pouch_button, 0, 3)
        self.ui.lower_inventory_layout.addWidget(self.bottle_button, 0, 4)
        self.ui.lower_inventory_layout.addWidget(self.wallet_button, 0, 5)
        self.ui.lower_inventory_layout.addWidget(self.mitts_button, 0, 6)

        self.ui.lower_inventory_layout.addWidget(self.harp_button, 1, 0)
        self.ui.lower_inventory_layout.addWidget(
            self.ballad_of_the_goddess_button, 1, 1
        )
        self.ui.lower_inventory_layout.addWidget(self.farores_courage_button, 1, 2)
        self.ui.lower_inventory_layout.addWidget(self.nayrus_wisdom_button, 1, 3)
        self.ui.lower_inventory_layout.addWidget(self.dins_power_button, 1, 4)
        self.ui.lower_inventory_layout.addWidget(self.song_of_the_hero_button, 1, 5)
        self.ui.lower_inventory_layout.addWidget(self.triforce_button, 1, 6)

        self.ui.lower_inventory_layout.addWidget(self.water_dragon_scale_button, 2, 0)
        self.ui.lower_inventory_layout.addWidget(self.fireshield_earrings_button, 2, 1)
        self.ui.lower_inventory_layout.addWidget(self.cawlins_latter_button, 2, 2)
        self.ui.lower_inventory_layout.addWidget(self.insect_cage_button, 2, 3)
        self.ui.lower_inventory_layout.addWidget(self.rattle_button, 2, 4)
        self.ui.lower_inventory_layout.addWidget(self.gratitude_crystals_button, 2, 5)
        self.ui.lower_inventory_layout.addWidget(self.life_tree_fruit_button, 2, 6)

        self.ui.lower_inventory_layout.addWidget(self.tadtones_button, 3, 0)
        self.ui.lower_inventory_layout.addWidget(self.scrapper_button, 3, 1)

        # Connect clicking a tracker inventory button to updating the tracker
        for inventory_button in self.ui.tracker_tab.findChildren(
            TrackerInventoryButton
        ):
            inventory_button.clicked.connect(self.update_tracker)

        # Connect dungeon labels to adding and removing dungeon locations
        for dungeon_label in self.ui.tracker_tab.findChildren(TrackerDungeonLabel):
            dungeon_label.clicked.connect(self.update_dungeon_progress_locations)

    def initialize_tracker_world(
        self,
        tracker_config: Config = None,
        marked_items=[],
        marked_locations=[],
        connected_entrances=[],
    ) -> None:
        self.started = True

        # Generate a new config from the current settings, but if we
        # passed in one from an autosave, use that instead
        config = copy.copy(self.main.config)
        if tracker_config is not None:
            config = tracker_config

        # Modify some settings to remove adding random items to the pool
        config.settings[0].settings[
            "random_starting_tablet_count"
        ].update_current_value(0)
        config.settings[0].settings["random_starting_item_count"].update_current_value(
            0
        )

        self.world = World(0)
        self.world.setting_map = config.settings[0]
        self.world.num_worlds = 1
        self.world.config = config
        self.world.build()
        self.world.perform_pre_entrance_shuffle_tasks()

        # Hide specific inventory buttons depending on settings
        # ET Key Pieces
        visible = self.world.setting("open_earth_temple") == "off"
        self.et_key_piece_button.setVisible(visible)

        # Small Key buttons
        visible = self.world.setting("small_keys") != "removed"
        self.sv_small_key_button.setVisible(visible)
        self.lmf_small_key_button.setVisible(visible)
        self.ac_small_key_button.setVisible(visible)
        self.ssh_small_key_button.setVisible(visible)
        self.fs_small_key_button.setVisible(visible)
        self.sk_small_key_button.setVisible(visible)

        # Boss Key buttons
        visible = self.world.setting("boss_keys") != "removed"
        self.sv_boss_key_button.setVisible(visible)
        self.et_boss_key_button.setVisible(visible)
        self.lmf_boss_key_button.setVisible(visible)
        self.ac_boss_key_button.setVisible(visible)
        self.ssh_boss_key_button.setVisible(visible)
        self.fs_boss_key_button.setVisible(visible)

        # Lanayru Caves Keys
        visible = self.world.setting("lanayru_caves_keys") != "removed"
        self.lanayru_caves_key_button.setVisible(visible)

        self.inventory = self.world.starting_item_pool.copy()

        # If the inventory contains the song of the hero, split it into its
        # three parts for the inventory button
        if self.inventory[self.world.get_item(SONG_OF_THE_HERO)]:
            self.inventory[self.world.get_item(SONG_OF_THE_HERO)] = 0
            self.inventory[self.world.get_item(FARON_SOTH_PART)] = 1
            self.inventory[self.world.get_item(ELDIN_SOTH_PART)] = 1
            self.inventory[self.world.get_item(LANAYRU_SOTH_PART)] = 1

        # Some item groups can be obtained in any order, so we normalize the orders here
        # to match what their corresponding button has
        soth_order = [FARON_SOTH_PART, ELDIN_SOTH_PART, LANAYRU_SOTH_PART]
        triforce_order = [TRIFORCE_OF_COURAGE, TRIFORCE_OF_WISDOM, TRIFORCE_OF_POWER]
        for group in (soth_order, triforce_order):
            num_group_parts = sum(
                [1 for item in self.inventory.elements() if item.name in group]
            )
            for i, item_name in enumerate(group):
                item = self.world.get_item(item_name)
                self.inventory[item] = 0
                if i < num_group_parts:
                    self.inventory[item] += 1

        # Apply starting inventory to inventory buttons and assign world
        for inventory_button in self.ui.tracker_tab.findChildren(
            TrackerInventoryButton
        ):
            inventory_button.world = self.world
            inventory_button.inventory = self.inventory
            inventory_button.state = 0
            inventory_button.forbidden_states.clear()
            for item in self.inventory.elements():
                if item.name in inventory_button.items:
                    inventory_button.add_forbidden_state(inventory_button.state)
                    inventory_button.state += 1
                    self.inventory[item] -= 1

            # Then update the buttons with any marked items from an autosave
            for item_name in marked_items:
                if item_name in inventory_button.items:
                    inventory_button.state += 1
                    self.inventory[item] += 1

            inventory_button.update_icon()

        # Mark any locations marked from an autosave
        for loc_name in marked_locations:
            loc = self.world.get_location(loc_name)
            loc.marked = True

        # Assign the initial locations for all regions
        self.update_areas_locations()

        # If barren unrequired dungeons is on then set all dungeon locations as non-progression
        if self.world.setting("empty_unrequired_dungeons") == "on":
            for dungeon in self.world.dungeons.values():
                for loc in dungeon.locations:
                    loc.eud_progression = False

        self.set_map_area("Root")
        self.clear_layout(self.ui.tracker_locations_scroll_layout)

    def set_map_area(self, area_name: str) -> None:
        area = self.areas.get(area_name, "")
        if area == "":
            print(f"Unknown area {area_name}")
            return
        self.active_area = area
        # set area background
        self.ui.map_widget.setStyleSheet(
            Tracker.map_widget_stylesheet.replace("IMAGE_FILENAME", area.image_filename)
        )
        # display appropriate children
        for child in self.areas.values():
            if child in area.tracker_children:
                child.setVisible(True)
            else:
                child.setVisible(False)

        # Don't display the back button if we're at the root
        if area_name == "Root":
            self.back_button.setVisible(False)
        else:
            self.back_button.setVisible(True)

    def show_area_locations(self, area_name: str) -> None:
        if area_button := self.areas.get(area_name, False):
            self.clear_layout(
                self.ui.tracker_locations_scroll_layout, remove_nested_layouts=True
            )
            locations = area_button.get_included_locations()

            left_layout = QVBoxLayout()
            right_layout = QVBoxLayout()

            for i, loc in enumerate(locations):
                if i < len(locations) / 2:
                    left_layout.addWidget(
                        TrackerLocationLabel(
                            loc, area_button.recent_search, area_button
                        )
                    )
                else:
                    right_layout.addWidget(
                        TrackerLocationLabel(
                            loc, area_button.recent_search, area_button
                        )
                    )

            # Add vertical spacers to push labels up
            left_layout.addSpacerItem(
                QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )
            right_layout.addSpacerItem(
                QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

            self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
            self.ui.tracker_locations_scroll_layout.addLayout(right_layout)

            # Set clicking labels to update tracker
            for location_label in self.ui.tracker_tab.findChildren(
                TrackerLocationLabel
            ):
                location_label.clicked.connect(self.update_tracker)

    def on_start_new_tracker_button_clicked(self) -> None:
        confirm_choice = self.main.fi_question_dialog.show_dialog(
            "Start New Tracker",
            "Reset the tracker with current settings?",
        )

        if confirm_choice != QMessageBox.StandardButton.Yes:
            return

        self.initialize_tracker_world()
        self.update_tracker()

    def on_back_button_clicked(self) -> None:
        # need to update the tracker so that subarea markers
        # have the correct counters
        self.update_tracker()
        self.set_map_area(self.active_area.area_parent.area)

    def update_tracker(self) -> None:
        if not self.started:
            return

        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, [self.world], self.inventory)
        search.search_worlds()

        for area_button in self.areas.values():
            area_button.update(search)

        for location_label in self.ui.tracker_locations_scroll_area.findChildren(
            TrackerLocationLabel
        ):
            location_label.update_color(search)

        self.autosave_tracker()

    def update_areas_locations(self) -> None:
        # Clear all locations before reassigning
        for area_button in self.ui.tracker_tab.findChildren(TrackerArea):
            area_button.locations.clear()

        self.world.assign_all_areas_hint_regions()
        for location in self.world.get_all_item_locations():
            for area_name in set(
                [
                    area
                    for la in location.loc_access_list
                    for area in la.area.hint_regions
                ]
            ):
                if area_button := self.areas.get(area_name, False):
                    area_button.locations.append(location)

    def update_dungeon_progress_locations(self, abbreviation: str) -> None:
        # Don't change anything if dungeons aren't guaranteed empty
        if self.world.setting("empty_unrequired_dungeons") == "off":
            return

        dungeon_name = ""
        match abbreviation:
            case "SV":
                dungeon_name = "Skyview Temple"
            case "ET":
                dungeon_name = "Earth Temple"
            case "LMF":
                dungeon_name = "Lanayru Mining Facility"
            case "AC":
                dungeon_name = "Ancient Cistern"
            case "SSH":
                dungeon_name = "Sandship"
            case "FS":
                dungeon_name = "Fire Sanctuary"
            case "SK":
                dungeon_name = "Sky Keep"

        for loc in self.world.get_dungeon(dungeon_name).locations:
            loc.eud_progression = not loc.eud_progression

        if dungeon_name in self.areas:
            self.areas[dungeon_name].update()
        else:
            print(f'No marker made for dungeon "{dungeon_name}" yet')

    def autosave_tracker(self) -> None:
        # write config to file
        version = VERSION.replace("+", "_")
        filename = Path(
            TRACKER_AUTOSAVE_PATH.as_posix().replace("RANDOMIZER_VERSION", version)
        )
        write_config_to_file(filename, self.world.config)

        # Then read it again to input extra data
        autosave = yaml_load(filename)
        autosave["World 1"]["marked_locations"] = []
        autosave["World 1"]["marked_items"] = []

        for loc in self.world.get_all_item_locations():
            if loc.marked:
                autosave["World 1"]["marked_locations"].append(loc.name)

        for item in self.inventory.elements():
            autosave["World 1"]["marked_items"].append(item.name)

        with open(filename, "w") as autosave_file:
            yaml.safe_dump(autosave, autosave_file)

    def load_tracker_autosave(self) -> None:
        version = VERSION.replace("+", "_")
        filename = Path(
            TRACKER_AUTOSAVE_PATH.as_posix().replace("RANDOMIZER_VERSION", version)
        )

        # If no autosave, don't do anything
        if not filename.exists():
            return

        tracker_config = load_config_from_file(filename, allow_rewrite=False)

        autosave = yaml_load(filename)
        marked_locations = autosave["World 1"].get("marked_locations", [])
        marked_items = autosave["World 1"].get("marked_items", [])

        self.initialize_tracker_world(tracker_config, marked_items, marked_locations)
        self.update_tracker()

    def clear_layout(self, layout: QLayout, remove_nested_layouts=False) -> None:
        # Recursively clear nested layouts
        for nested_layout in layout.findChildren(QLayout):
            self.clear_layout(nested_layout)

        while item := layout.takeAt(0):
            if widget := item.widget():
                widget.deleteLater()
            del item

        if remove_nested_layouts:
            for nested_layout in layout.findChildren(QLayout):
                layout.removeItem(nested_layout)
