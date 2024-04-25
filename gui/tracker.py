from logic.world import World
from logic.entrance_shuffle import (
    set_all_entrances_data,
    create_entrance_pools,
    create_target_pools,
    EntrancePools,
    change_connections,
    restore_connections,
)
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
    QComboBox,
    QPushButton,
    QLayout,
    QSpacerItem,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6 import QtCore
from PySide6.QtGui import QMouseEvent

from gui.components.tracker_inventory_button import TrackerInventoryButton
from gui.components.tracker_dungeon_label import TrackerDungeonLabel
from gui.components.tracker_area import TrackerArea
from gui.components.tracker_back_button import TrackerBackButton
from gui.components.tracker_location_label import TrackerLocationLabel
from gui.components.tracker_entrance_label import TrackerEntranceLabel
from gui.components.tracker_target_label import TrackerTargetLabel
from gui.components.tracker_show_entrances_button import TrackerShowEntrancesButton
from gui.components.tracker_show_locations_button import TrackerShowLocationsButton
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
        self.random_settings: list = []

        # Holds which entrance is connected to which target
        self.connected_entrances: dict[Entrance, Entrance] = {}
        # Holds available targets for disconnected entrances
        self.target_entrance_pools: EntrancePools = {}

        # Display the Sky if there's no active tracker
        self.ui.map_widget.setStyleSheet(
            Tracker.map_widget_stylesheet.replace("IMAGE_FILENAME", "Sky.png")
        )

        self.ui.map_widget.mouseReleaseEvent = self.handle_right_click

        # Hide the set random settings button until a tracker is loaded with random settings
        self.ui.set_random_settings_button.setVisible(False)
        # Same for setting starting entrance
        self.ui.set_starting_entrance_button.setVisible(False)

        self.init_buttons()
        self.assign_buttons_to_layout()
        self.load_tracker_autosave()

        self.ui.start_new_tracker_button.clicked.connect(
            self.on_start_new_tracker_button_clicked
        )
        self.ui.set_random_settings_button.clicked.connect(
            self.on_set_random_settings_button_clicked
        )
        self.ui.set_starting_entrance_button.clicked.connect(
            self.on_set_starting_entrance_button_clicked
        )

        self.update_statistics()

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
            area_entrance_name = area_button_node.get("entrance", "")
            area_button = TrackerArea(
                area_name,
                area_image,
                area_children,
                area_x,
                area_y,
                self.ui.map_widget,
                border_radius,
                alias,
                area_entrance_name,
            )
            area_button.change_map_area.connect(self.set_map_area)
            area_button.show_locations.connect(self.show_area_locations)
            area_button.set_main_entrance_target.connect(
                self.show_target_selection_info
            )
            self.areas[area_name] = area_button

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
        self, tracker_config: Config = None, autosave: dict = {}
    ) -> None:
        self.started = True

        # Generate a new config from the current settings, but if we
        # passed in one from an autosave, use that instead
        config = copy.deepcopy(self.main.config)
        if tracker_config is not None:
            config = tracker_config

        # Initialize the world
        self.world = World(0)
        self.world.setting_map = config.settings[0]
        self.world.num_worlds = 1
        self.world.config = config

        # Modify settings for various purposes

        # Don't include random starting items in the tracker world
        self.world.setting("random_starting_tablet_count").set_value("0")
        self.world.setting("random_starting_item_count").set_value("0")

        # Set random starting spawn and random starting statues to on if they're
        # random since we're going to ask the user for the entrances either way
        if self.world.setting("random_starting_spawn") == "random":
            self.world.setting("random_starting_spawn").set_value("anywhere")
        if self.world.setting("random_starting_statues") == "random":
            self.world.setting("random_starting_statues").set_value("on")
        # Set limit starting statues off since we want to ask the user about
        # the most possible entrances
        self.world.setting("limit_starting_spawn").set_value("off")

        # Build the world (only as necessary)
        self.world.build()
        self.world.perform_pre_entrance_shuffle_tasks()

        # Get any random settings. If any are passed in from the autosave
        # load those instead of loading them from the world
        if autosave_random_settings := autosave.get("random_settings", False):
            self.random_settings = [
                s
                for s in self.world.setting_map.settings.values()
                if s.name in autosave_random_settings
            ]
        else:
            self.random_settings = [
                s
                for s in self.world.setting_map.settings.values()
                if s.value == s.info.random_option and s.info.tracker_important
            ]
        # If no settings are random, then hide the set random settings button
        self.ui.set_random_settings_button.setVisible(any(self.random_settings))
        # If the starting entrance isn't being shuffled, then hide that button also
        self.ui.set_starting_entrance_button.setVisible(
            self.world.setting("random_starting_spawn") != "vanilla"
        )

        # Hide specific inventory buttons depending on settings
        # ET Key Pieces
        visible = self.world.setting("open_earth_temple") != "on"
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

        # Setup Entrances
        self.setup_tracker_entrances()

        # Connect autosaved entrances
        if autosaved_entrances := autosave.get("connected_entrances", None):
            for entrance in self.world.get_shuffled_entrances(
                only_primary=self.world.setting("decouple_entrances") == "off"
            ):
                if saved_target := autosaved_entrances.get(
                    entrance.original_name, None
                ):
                    for target in self.target_entrance_pools[entrance.type]:
                        if target.replaces.original_name == saved_target:
                            change_connections(entrance, target)
                            self.connected_entrances[entrance] = target

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
            for item_name in autosave.get("marked_items", []):
                item = self.world.get_item(item_name)
                if item_name in inventory_button.items:
                    inventory_button.state += 1
                    self.inventory[item] += 1

            inventory_button.update_icon()

        # Mark any locations marked from an autosave
        for loc_name in autosave.get("marked_locations", []):
            loc = self.world.get_location(loc_name)
            loc.marked = True

        # Assign the initial locations for all regions
        self.update_areas_locations()
        self.update_areas_entrances()

        # If barren unrequired dungeons is on then set all dungeon locations as non-progression
        if self.world.setting("empty_unrequired_dungeons") == "on":
            for dungeon in self.world.dungeons.values():
                for loc in dungeon.locations:
                    loc.eud_progression = False

        # Set the active area to that of the autosave or the Root if there is no autosave
        self.set_map_area(autosave.get("active_area", "Root"))

        # Reset dungeon selectors
        for label in self.ui.tracker_tab.findChildren(TrackerDungeonLabel):
            label.reset()
            if label.abbreviation in autosave.get("active_dungeons", []):
                label.on_clicked()

        self.update_tracker()
        self.clear_layout(self.ui.tracker_locations_info_layout)
        self.clear_layout(self.ui.tracker_locations_scroll_layout)
        # If the starting entrance is random, prompt the user to enter it
        starting_spawn = self.world.get_entrance("Link's Spawn -> Knight Academy")
        if (
            self.world.setting("random_starting_spawn") != "vanilla"
            and starting_spawn.connected_area is None
        ):
            self.on_set_starting_entrance_button_clicked()

    def setup_tracker_entrances(self) -> None:
        self.connected_entrances.clear()

        set_all_entrances_data(self.world)
        entrance_pools = create_entrance_pools(self.world)
        self.target_entrance_pools = create_target_pools(entrance_pools)

        # Prevent implicit access to any target entrances
        for target_pool in self.target_entrance_pools.values():
            for target in target_pool:
                target.requirement.set_as_impossible()
                if target.reverse:
                    target.reverse.requirement.set_as_impossible()

    def update_areas_entrances(self) -> None:
        # Clear previous entrance associations and set any areas' "main" entrance
        for area_button in self.ui.tracker_tab.findChildren(TrackerArea):
            area_button.entrances.clear()
            if area_button.main_entrance_name:
                area_button.main_entrance = self.world.get_entrance(
                    area_button.main_entrance_name
                )

        # Then redistribute entrances to each button
        for entrance in self.world.get_shuffled_entrances(
            only_primary=self.world.setting("decouple_entrances") == "off"
        ):
            if entrance.requirement.type != RequirementType.IMPOSSIBLE:
                for region in entrance.parent_area.hint_regions:
                    if area_button := self.areas.get(region, None):
                        area_button.entrances.append(entrance)

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

        # Save current area in the autosave
        self.autosave_tracker()

    def show_area_locations(self, area_name: str) -> None:
        if area_button := self.areas.get(area_name, False):
            self.show_area_location_info(area_name)
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
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
                location_label.clicked.connect(self.on_click_location_label)

    def show_area_location_info(self, area_name: str) -> None:
        if area_button := self.areas.get(area_name, False):
            # Show the area name and how many non-marked locations are available.
            # Get the labels if they were previously created to reuse them.
            # This prevents us from having to clear the layout and making
            # the scroll bar on the list of locations sometimes jump up
            area_name_label = self.ui.tracker_tab.findChild(QLabel, "area_name_label")
            locations_remaining_label = self.ui.tracker_tab.findChild(QLabel, "area_things_remaining_label")
            show_entrances_button = self.ui.tracker_tab.findChild(TrackerShowEntrancesButton)
            show_locations_button = self.ui.tracker_tab.findChild(TrackerShowLocationsButton)
            
            pt_size = 20

            if area_name_label is None:
                area_name_label = QLabel()
                area_name_label.setObjectName("area_name_label")
                area_name_label.setStyleSheet(f"font-size: {pt_size}pt")
                area_name_label.setMargin(10)
                self.ui.tracker_locations_info_layout.addWidget(area_name_label)
            
            if locations_remaining_label is None:
                locations_remaining_label = QLabel()
                locations_remaining_label.setObjectName("area_things_remaining_label")
                locations_remaining_label.setStyleSheet(
                    f"font-size: {pt_size}pt; qproperty-alignment: {int(QtCore.Qt.AlignRight)};"
                )
                locations_remaining_label.setMargin(10)
                self.ui.tracker_locations_info_layout.addWidget(locations_remaining_label)

            if show_entrances_button is None:
                show_entrances_button = TrackerShowEntrancesButton(area_button.area)
                show_entrances_button.show_area_entrances.connect(
                    self.show_area_entrances
                )
                self.ui.tracker_locations_info_layout.addWidget(show_entrances_button)

            if show_locations_button is None:
                show_locations_button = TrackerShowLocationsButton(area_name)
                show_locations_button.show_area_locations.connect(
                    self.show_area_locations
                )
                self.ui.tracker_locations_info_layout.addWidget(show_locations_button)

            area_name_label.setText(area_button.area)
            locations_remaining_label.setText(
                f"({len(area_button.get_available_locations())}/{len(area_button.get_unmarked_locations())})"
            )
            show_entrances_button.area_name = area_button.area
            show_entrances_button.setVisible(bool(area_button.entrances))
            show_locations_button.setVisible(False)


    def show_area_entrances(self, area_name: str) -> None:
        if area_button := self.areas.get(area_name, None):
            self.show_area_entrance_info(area_name)
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
            entrances = area_button.entrances

            left_layout = QVBoxLayout()
            right_layout = QVBoxLayout()

            for i, entrance in enumerate(entrances):
                entrance_label = TrackerEntranceLabel(
                    entrance, area_name, area_button.recent_search
                )
                entrance_label.choose_target.connect(self.show_target_selection_info)
                entrance_label.disconnect_entrance.connect(
                    self.on_right_click_entrance_label
                )

                if i < len(entrances) / 2:
                    left_layout.addWidget(entrance_label)
                else:
                    right_layout.addWidget(entrance_label)

            # Add vertical spacers to push labels up
            left_layout.addSpacerItem(
                QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )
            right_layout.addSpacerItem(
                QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

            self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
            self.ui.tracker_locations_scroll_layout.addLayout(right_layout)
        else:
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
            self.clear_layout(self.ui.tracker_locations_info_layout)

    def show_area_entrance_info(self, area_name: str):
        if area_button := self.areas.get(area_name, None):
            # Show the area name and how many entrances have been connected.
            # Get the labels if they were previously created to reuse them.
            # This prevents us from having to clear the layout and making
            # the scroll bar on the list of locations sometimes jump up
            area_name_label = self.ui.tracker_tab.findChild(QLabel, "area_name_label")
            disconnected_entrances_label = self.ui.tracker_tab.findChild(QLabel, "area_things_remaining_label")
            show_entrances_button = self.ui.tracker_tab.findChild(TrackerShowEntrancesButton)
            show_locations_button = self.ui.tracker_tab.findChild(TrackerShowLocationsButton)

            area_name_label.setText(area_name)
            disconnected_entrances_label.setText(
                f"({sum([1 for e in area_button.entrances if e.connected_area])}/{len(area_button.entrances)})"
            )
            show_entrances_button.setVisible(False)
            show_locations_button.area_name = area_name
            show_locations_button.setVisible(True)

    def show_target_selection_info(
        self, entrance: Entrance, parent_area_name: str = ""
    ) -> None:
        self.clear_layout(self.ui.tracker_locations_info_layout)
        lead_to_label = QLabel(f"Where did {entrance.original_name} lead to?")
        lead_to_label.setStyleSheet(
            f"qproperty-alignment: {int(QtCore.Qt.AlignCenter)};"
        )
        lead_to_label.setMargin(10)
        back_button = TrackerShowEntrancesButton(parent_area_name, "Back")
        back_button.show_area_entrances.connect(self.show_area_entrances)

        self.ui.tracker_locations_info_layout.addWidget(lead_to_label)
        self.ui.tracker_locations_info_layout.addWidget(back_button)

        self.clear_layout(self.ui.tracker_locations_scroll_layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        targets = self.target_entrance_pools[entrance.type]

        for i, target in enumerate(targets):
            # Only show targets which haven't been connected yet
            if target.connected_area is not None:
                target_label = TrackerTargetLabel(entrance, target, parent_area_name)
                target_label.clicked.connect(self.on_click_target_label)

                if i < len(targets) / 2:
                    left_layout.addWidget(target_label)
                else:
                    right_layout.addWidget(target_label)

        # Add vertical spacers to push labels up
        left_layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        right_layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
        self.ui.tracker_locations_scroll_layout.addLayout(right_layout)

    def on_click_location_label(self, location_area: str) -> None:
        self.update_tracker()
        self.show_area_location_info(location_area)

    def on_click_target_label(
        self, entrance: Entrance, target: Entrance, parent_area_name: str
    ) -> None:
        self.tracker_change_entrance_connections(entrance, target)

        # Re-list the parent areas entrances if there are any
        parent_area = self.areas.get(parent_area_name, None)
        if parent_area and parent_area.entrances:
            self.show_area_entrances(parent_area_name)
        # Otherwise clear the scroll area
        else:
            self.clear_layout(self.ui.tracker_locations_info_layout)
            self.clear_layout(self.ui.tracker_locations_scroll_layout)

    def on_right_click_entrance_label(self, entrance: Entrance, area_name: str) -> None:
        self.tracker_disconnect_entrance(entrance)
        self.show_area_entrance_info(area_name)

    def tracker_change_entrance_connections(
        self, entrance: Entrance, target: Entrance
    ) -> None:
        # Disconnect the entrance incase it was previously connected to something
        self.tracker_disconnect_entrance(entrance)

        change_connections(entrance, target)
        self.connected_entrances[entrance] = target

        # Update everything after making a connection
        self.update_areas_locations()
        self.update_areas_entrances()
        self.update_tracker()

    def tracker_disconnect_entrance(self, entrance: Entrance) -> None:
        if target := self.connected_entrances.get(entrance, None):
            restore_connections(entrance, target)
            del self.connected_entrances[entrance]
            self.update_areas_locations()
            self.update_areas_entrances()
            self.update_tracker()

    def on_start_new_tracker_button_clicked(self) -> None:
        confirm_choice = self.main.fi_question_dialog.show_dialog(
            "Start New Tracker",
            "Reset the tracker with current settings?",
        )

        if confirm_choice != QMessageBox.StandardButton.Yes:
            return

        self.initialize_tracker_world()

    def on_set_random_settings_button_clicked(self) -> None:
        # Don't do anything if the tracker isn't started
        if not self.started:
            return

        self.show_random_setting_choices()

    def on_set_starting_entrance_button_clicked(self) -> None:
        self.show_target_selection_info(
            self.world.get_entrance("Link's Spawn -> Knight Academy")
        )

    def show_random_setting_choices(self) -> None:

        # Put Update and Cancel buttons in the area info layout
        self.clear_layout(self.ui.tracker_locations_info_layout)

        update_button = QPushButton(text="Update Settings")
        update_button.clicked.connect(self.on_random_settings_update_button_clicked)

        cancel_button = QPushButton(text="Close")
        cancel_button.clicked.connect(self.on_random_settings_cancel_button_clicked)

        self.ui.tracker_locations_info_layout.addWidget(cancel_button)
        self.ui.tracker_locations_info_layout.addWidget(update_button)

        self.clear_layout(self.ui.tracker_locations_scroll_layout)

        # Put a vertical layout inside the scroll area
        outer_layout = QVBoxLayout()

        # Add a label and combobox for each random setting
        for setting in self.random_settings:
            layout = QHBoxLayout()
            layout.addWidget(QLabel(setting.info.pretty_name))

            combo_box = QComboBox()
            combo_box.addItems(setting.info.pretty_options)
            combo_box.setCurrentIndex(setting.info.options.index(setting.value))
            combo_box.setObjectName(f"tracker_setting_{setting.name}")
            layout.addWidget(combo_box)
            outer_layout.addLayout(layout)

        # Add a vertical spacer to push the labels and comboboxes up
        outer_layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.ui.tracker_locations_scroll_layout.addLayout(outer_layout)

    def on_random_settings_update_button_clicked(self) -> None:
        # Change settings
        for setting_combobox in self.ui.tracker_tab.findChildren(QComboBox):
            object_name: str = setting_combobox.objectName()
            if object_name.startswith("tracker_setting_"):
                setting_name = object_name.replace("tracker_setting_", "")
                setting_value = setting_combobox.currentIndex()
                self.world.setting(setting_name).set_value(setting_value)

        # Then trigger and immediately reload an autosave
        self.autosave_tracker()
        self.load_tracker_autosave()
        self.show_random_setting_choices()

    def on_random_settings_cancel_button_clicked(self) -> None:
        self.clear_layout(self.ui.tracker_locations_info_layout)
        self.clear_layout(self.ui.tracker_locations_scroll_layout)

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

        location_label_area_name = ""
        for location_label in self.ui.tracker_locations_scroll_area.findChildren(
            TrackerLocationLabel
        ):
            location_label.update_color(search)
            if not location_label_area_name:
                location_label_area_name = location_label.parent_area_button.area

        for entrance_label in self.ui.tracker_locations_scroll_area.findChildren(
            TrackerEntranceLabel
        ):
            entrance_label.update(search)

        self.show_area_location_info(location_label_area_name)
        self.autosave_tracker()
        self.update_statistics()

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
        if not self.started:
            return

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

        # update and autosave to save active dungeons
        self.update_tracker()

    def autosave_tracker(self) -> None:
        # write config to file
        version = VERSION.replace("+", "_")
        filename = Path(
            TRACKER_AUTOSAVE_PATH.as_posix().replace("RANDOMIZER_VERSION", version)
        )
        write_config_to_file(filename, self.world.config)

        # Then read it again to input extra data
        autosave = yaml_load(filename)
        autosave["marked_locations"] = [
            loc.name for loc in self.world.get_all_item_locations() if loc.marked
        ]
        autosave["marked_items"] = [item.name for item in self.inventory.elements()]
        autosave["connected_entrances"] = {
            f"{e}": f"{t.replaces}" for e, t in self.connected_entrances.items()
        }
        autosave["random_settings"] = [s.name for s in self.random_settings]
        autosave["active_area"] = self.active_area.area
        autosave["active_dungeons"] = [
            dungeon.abbreviation
            for dungeon in self.ui.tracker_tab.findChildren(TrackerDungeonLabel)
            if dungeon.active
        ]

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

        self.initialize_tracker_world(tracker_config, autosave)
        self.update_tracker()

    def clear_layout(self, layout: QLayout, remove_nested_layouts=True) -> None:
        # Recursively clear nested layouts
        for nested_layout in layout.findChildren(QLayout):
            self.clear_layout(nested_layout, remove_nested_layouts)

        while item := layout.takeAt(0):
            if widget := item.widget():
                widget.deleteLater()
            del item

        if remove_nested_layouts:
            for nested_layout in layout.findChildren(QLayout):
                layout.removeItem(nested_layout)

    def handle_right_click(self, event: QMouseEvent) -> None:
        if (
            event.button() == QtCore.Qt.RightButton
            and not self.active_area.area == "Root"
        ):
            self.on_back_button_clicked()

    def update_statistics(self) -> None:
        num_accessible_locations = len(self.areas["Root"].get_available_locations())
        num_remaining_locations = len(self.areas["Root"].get_unmarked_locations())
        num_checked_locations = (
            len(self.areas["Root"].get_included_locations()) - num_remaining_locations
        )
        self.ui.tracker_stats_checked.setText(f"{num_checked_locations: {3}}")
        self.ui.tracker_stats_accessible.setText(f"{num_accessible_locations: {3}}")
        self.ui.tracker_stats_remaining.setText(f"{num_remaining_locations: {3}}")
