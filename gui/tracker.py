from logic.world import *
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
    QLineEdit,
)
from PySide6 import QtCore
from PySide6.QtGui import QMouseEvent, QCursor

from gui.components.tracker_inventory_button import TrackerInventoryButton
from gui.components.tracker_dungeon_label import TrackerDungeonLabel
from gui.components.tracker_area import TrackerArea
from gui.components.tracker_back_button import TrackerBackButton
from gui.components.tracker_location_label import TrackerLocationLabel
from gui.components.tracker_entrance_label import TrackerEntranceLabel
from gui.components.tracker_target_label import TrackerTargetLabel
from gui.components.tracker_show_entrances_button import TrackerShowEntrancesButton
from gui.components.tracker_show_locations_button import TrackerShowLocationsButton
from gui.components.tracker_tablet_widget import TrackerTabletWidget
from gui.components.tracker_hint_label import TrackerHintLabel

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
        self.world: World = None  # type: ignore
        self.inventory: Counter[Item] = Counter()
        self.started: bool = False
        self.areas: dict[str, TrackerArea] = {}
        self.active_area: TrackerArea = None  # type: ignore
        self.last_opened_region: TrackerArea = None  # type: ignore
        self.last_checked_location: Location = None  # type: ignore
        self.random_settings: list = []
        self.items_on_mark: dict[Location, Item] = {}
        self.own_dungeon_key_locations: list[tuple[Item, list[Location]]] = []
        self.sphere_tracked_items: dict[Location, str]
        self.allow_sphere_tracking: bool = False

        # Holds which entrance is connected to which target
        self.connected_entrances: dict[Entrance, Entrance] = {}
        # Holds available targets for disconnected entrances
        self.target_entrance_pools: EntrancePools = OrderedDict()

        # Hide the check/uncheck all buttons until an area is selected
        self.ui.check_all_button.setVisible(False)
        self.ui.check_all_in_logic_button.setVisible(False)
        self.ui.uncheck_all_button.setVisible(False)
        self.ui.set_hints_button.setVisible(False)

        # Hide the sphere tracking info/buttons until a location is marked
        self.ui.tracker_sphere_tracking_label.setVisible(False)
        self.ui.cancel_sphere_tracking_button.setVisible(False)

        self.ui.tracker_sphere_tracking_label.setWordWrap(True)

        # Display the Sky if there's no active tracker
        self.ui.map_widget.setStyleSheet(
            Tracker.map_widget_stylesheet.replace("IMAGE_FILENAME", "Sky.png")
        )

        self.ui.map_widget.mouseReleaseEvent = self.handle_right_click

        # Hide the set random settings button until a tracker is loaded with random settings
        self.ui.set_random_settings_button.setVisible(False)
        # Same for setting starting entrance
        self.ui.set_starting_entrance_button.setVisible(False)

        # Set all sidebar buttons to use the click mouse cursor
        self.ui.start_new_tracker_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.check_all_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.check_all_in_logic_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.uncheck_all_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.set_random_settings_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.set_starting_entrance_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.cancel_sphere_tracking_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.set_hints_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )

        self.init_buttons()
        self.assign_buttons_to_layout()
        try:
            self.load_tracker_autosave()
        except Exception as e:
            self.main.fi_info_dialog.show_dialog(
                "Error loading tracker autosave",
                "There was an error loading the autosave from the tracker.<br>"
                + f"{e}.<br>"
                + "The tracker must be loaded from scratch.",
            )
            self.initialize_tracker_world()

        self.ui.start_new_tracker_button.clicked.connect(
            self.on_start_new_tracker_button_clicked
        )
        self.ui.set_random_settings_button.clicked.connect(
            self.on_set_random_settings_button_clicked
        )
        self.ui.set_starting_entrance_button.clicked.connect(
            self.on_set_starting_entrance_button_clicked
        )
        self.ui.check_all_button.clicked.connect(self.on_check_all_clicked)
        self.ui.check_all_in_logic_button.clicked.connect(
            self.on_check_all_in_logic_clicked
        )
        self.ui.uncheck_all_button.clicked.connect(self.on_uncheck_all_clicked)
        self.ui.cancel_sphere_tracking_button.clicked.connect(
            self.cancel_sphere_tracking
        )
        self.ui.set_hints_button.clicked.connect(self.show_hint_options)
        self.ui.toggle_sphere_tracking_button.left_clicked.connect(
            self.toggle_sphere_tracking
        )
        self.ui.toggle_sphere_tracking_button.right_clicked.connect(
            self.display_sphere_tracking_popup
        )

        self.update_statistics()

    def init_buttons(self):

        self.sv_small_key_button = TrackerInventoryButton(
            ["Nothing", SV_SMALL_KEY, SV_SMALL_KEY],
            [
                "dungeons/small_key_0.png",
                "dungeons/small_key_1.png",
                "dungeons/small_key_2_complete.png",
            ],
            None,
            [f"Skyview Temple Small Key ({i}/2)" for i in range(3)],
        )
        self.et_key_piece_button = TrackerInventoryButton(
            ["Nothing"] + [KEY_PIECE] * 5,
            [
                "dungeons/et_key_0.png",
                "dungeons/et_key_1.png",
                "dungeons/et_key_2.png",
                "dungeons/et_key_3.png",
                "dungeons/et_key_4.png",
                "dungeons/et_key_5.png",
            ],
            None,
            [f"Key Piece ({i}/5)" for i in range(6)],
        )
        self.lmf_small_key_button = TrackerInventoryButton(
            ["Nothing", LMF_SMALL_KEY],
            ["dungeons/small_key_0.png", "dungeons/small_key_1_complete.png"],
            None,
            [f"Lanayru Mining Facility Small Key ({i}/1)" for i in range(2)],
        )
        self.ac_small_key_button = TrackerInventoryButton(
            ["Nothing", AC_SMALL_KEY, AC_SMALL_KEY],
            [
                "dungeons/small_key_0.png",
                "dungeons/small_key_1.png",
                "dungeons/small_key_2_complete.png",
            ],
            None,
            [f"Ancient Cistern Small Key ({i}/2)" for i in range(3)],
        )
        self.ssh_small_key_button = TrackerInventoryButton(
            ["Nothing"] + [SSH_SMALL_KEY] * 2,
            [
                "dungeons/small_key_0.png",
                "dungeons/small_key_1.png",
                "dungeons/small_key_2_complete.png",
            ],
            None,
            [f"Sandship Small Key ({i}/2)" for i in range(3)],
        )
        self.fs_small_key_button = TrackerInventoryButton(
            ["Nothing"] + [FS_SMALL_KEY] * 3,
            [
                "dungeons/small_key_0.png",
                "dungeons/small_key_1.png",
                "dungeons/small_key_2.png",
                "dungeons/small_key_3_complete.png",
            ],
            None,
            [f"Fire Sanctuary Small Key ({i}/3)" for i in range(4)],
        )
        self.sk_small_key_button = TrackerInventoryButton(
            ["Nothing", SK_SMALL_KEY],
            ["dungeons/small_key_0.png", "dungeons/small_key_1_complete.png"],
            None,
            [f"Sky Keep Small Key ({i}/1)" for i in range(2)],
        )

        self.sv_boss_key_button = TrackerInventoryButton(
            ["Nothing", SV_BOSS_KEY],
            ["dungeons/golden_carving_gray.png", "dungeons/golden_carving.png"],
        )
        self.et_boss_key_button = TrackerInventoryButton(
            ["Nothing", ET_BOSS_KEY],
            ["dungeons/dragon_sculpture_gray.png", "dungeons/dragon_sculpture.png"],
        )
        self.lmf_boss_key_button = TrackerInventoryButton(
            ["Nothing", LMF_BOSS_KEY],
            ["dungeons/ancient_circuit_gray.png", "dungeons/ancient_circuit.png"],
        )
        self.ac_boss_key_button = TrackerInventoryButton(
            ["Nothing", AC_BOSS_KEY],
            ["dungeons/blessed_idol_gray.png", "dungeons/blessed_idol.png"],
        )
        self.ssh_boss_key_button = TrackerInventoryButton(
            ["Nothing", SSH_BOSS_KEY],
            ["dungeons/squid_carving_gray.png", "dungeons/squid_carving.png"],
        )
        self.fs_boss_key_button = TrackerInventoryButton(
            ["Nothing", FS_BOSS_KEY],
            [
                "dungeons/mysterious_crystals_gray.png",
                "dungeons/mysterious_crystals.png",
            ],
        )
        self.sk_sot_button = TrackerInventoryButton(
            ["Nothing", STONE_OF_TRIALS],
            ["dungeons/stone_of_trials_gray.png", "dungeons/stone_of_trials.png"],
        )

        self.bombs_button = TrackerInventoryButton(
            ["Nothing", BOMB_BAG], ["bombs_gray.png", "bombs.png"]
        )
        self.slingshot_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_SLINGSHOT] * 2,
            ["slingshot_gray.png", "slingshot.png", "scattershot.png"],
            None,
            ["No Slingshot", "Slingshot", "Scattershot"],
        )
        self.beetle_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_BEETLE] * 4,
            [
                "beetle_gray.png",
                "beetle.png",
                "hook_beetle.png",
                "quick_beetle.png",
                "tough_beetle.png",
            ],
            None,
            ["No Beetle", "Beetle", "Hook Beetle", "Quick Beetle", "Tough Beetle"],
        )
        self.bug_net_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_BUG_NET] * 2,
            ["bug_net_gray.png", "bug_net.png", "big_bug_net.png"],
            None,
            ["No Bug Net", "Bug Net", "Big Bug Net"],
        )
        self.bow_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_BOW] * 3,
            [
                "bow_gray.png",
                "bow.png",
                "iron_bow.png",
                "sacred_bow.png",
            ],
            None,
            ["No Bow", "Bow", "Iron Bow", "Sacred Bow"],
        )
        self.clawshots_button = TrackerInventoryButton(
            ["Nothing", CLAWSHOTS], ["clawshots_gray.png", "clawshots.png"]
        )
        self.whip_button = TrackerInventoryButton(
            ["Nothing", WHIP], ["whip_gray.png", "whip.png"]
        )
        self.gust_bellows_button = TrackerInventoryButton(
            ["Nothing", GUST_BELLOWS],
            ["gust_bellows_gray.png", "gust_bellows.png"],
        )

        self.sword_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_SWORD] * 6,
            [
                "swords/practice_sword_gray.png",
                "swords/practice_sword.png",
                "swords/goddess_sword.png",
                "swords/longsword.png",
                "swords/white_sword.png",
                "swords/master_sword.png",
                "swords/true_master_sword.png",
            ],
            None,
            [
                "No Sword",
                "Practice Sword",
                "Goddess Sword",
                "Goddess Longsword",
                "Goddess White Sword",
                "Master Sword",
                "True Master Sword",
            ],
        )
        self.sword_button.setMinimumWidth(65)
        self.sword_button.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )

        self.lanayru_caves_key_button = TrackerInventoryButton(
            ["Nothing"] + [LC_SMALL_KEY] * 2,
            [
                "dungeons/small_key_0.png",
                "dungeons/small_key_1.png",
                "dungeons/small_key_2_complete.png",
            ],
            None,
            [f"Lanayru Caves Small Key ({i}/2)" for i in range(3)],
        )
        self.sea_chart_button = TrackerInventoryButton(
            ["Nothing", SEA_CHART], ["sea_chart_gray.png", "sea_chart.png"]
        )
        self.spiral_charge_button = TrackerInventoryButton(
            ["Nothing", SPIRAL_CHARGE],
            ["bird_statuette_gray.png", "bird_statuette.png"],
        )
        self.adventure_pouch_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_POUCH] * 5,
            ["pouch_gray.png"] + [f"pouch{i}.png" for i in range(1, 6)],
            None,
            ["Adventure Pouch (0 Slots)"]
            + [f"Adventure Pouch ({i + 4} Slots)" for i in range(5)],
        )
        self.bottle_button = TrackerInventoryButton(
            ["Nothing"] + [EMPTY_BOTTLE] * 5,
            ["bottle_gray.png"] + [f"bottle{i}.png" for i in range(1, 6)],
            None,
            [f"Empty Bottle ({i}/5)" for i in range(6)],
        )
        self.wallet_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_WALLET] * 4,
            [
                "wallets/small_wallet.png",
                "wallets/medium_wallet.png",
                "wallets/large_wallet.png",
                "wallets/giant_wallet.png",
                "wallets/tycoon_wallet.png",
            ],
            None,
            [
                "Wallet (300 Rupees)",
                "Medium Wallet (500 Rupees)",
                "Large Wallet (1000 Rupees)",
                "Giant Wallet (5000 Rupees)",
                "Tycoon Wallet (9000 Rupees)",
            ],
        )
        self.extra_wallet_button = TrackerInventoryButton(
            ["Nothing"] + [EXTRA_WALLET] * 3,
            ["wallets/extra_wallet_gray.png"]
            + [f"wallets/extra_wallet_{i}.png" for i in range(1, 4)],
            None,
            [f"Extra Wallet (+{i*300} Rupees)" for i in range(4)],
        )
        self.mitts_button = TrackerInventoryButton(
            ["Nothing"] + [PROGRESSIVE_MITTS] * 2,
            [
                "main quest/digging_mitts_gray.png",
                "main quest/digging_mitts.png",
                "main quest/mogma_mitts.png",
            ],
            None,
            ["No Mitts", "Digging Mitts", "Mogma Mitts"],
        )

        self.harp_button = TrackerInventoryButton(
            ["Nothing", GODDESS_HARP],
            ["main quest/goddess_harp_gray.png", "main quest/goddess_harp.png"],
        )
        self.ballad_of_the_goddess_button = TrackerInventoryButton(
            ["Nothing", BALLAD_OF_THE_GODDESS],
            ["songs/ballad_of_the_goddess_gray.png", "songs/ballad_of_the_goddess.png"],
        )
        self.farores_courage_button = TrackerInventoryButton(
            ["Nothing", FARORES_COURAGE],
            ["songs/farores_courage_gray.png", "songs/farores_courage.png"],
        )
        self.nayrus_wisdom_button = TrackerInventoryButton(
            ["Nothing", NAYRUS_WISDOM],
            ["songs/nayrus_wisdom_gray.png", "songs/nayrus_wisdom.png"],
        )
        self.dins_power_button = TrackerInventoryButton(
            ["Nothing", DINS_POWER],
            ["songs/dins_power_gray.png", "songs/dins_power.png"],
        )
        self.song_of_the_hero_button = TrackerInventoryButton(
            ["Nothing"] + [SOTH_PART] * 4,
            [
                "songs/song_of_the_hero_gray.png",
                "songs/song_of_the_hero_1.png",
                "songs/song_of_the_hero_2.png",
                "songs/song_of_the_hero_3.png",
                "songs/song_of_the_hero_4.png",
            ],
            None,
            [f"Song of the Hero ({i}/4)" for i in range(5)],
        )
        self.triforce_button = TrackerInventoryButton(
            ["Nothing", TRIFORCE_OF_COURAGE, TRIFORCE_OF_WISDOM, TRIFORCE_OF_POWER],
            [f"main quest/triforce_{i}.png" for i in range(4)],
            None,
            [f"Triforce ({i}/3)" for i in range(4)],
        )

        self.water_dragon_scale_button = TrackerInventoryButton(
            ["Nothing", WATER_DRAGON_SCALE],
            [
                "main quest/water_dragon_scale_gray.png",
                "main quest/water_dragon_scale.png",
            ],
        )
        self.fireshield_earrings_button = TrackerInventoryButton(
            ["Nothing", FIRESHIELD_EARRINGS],
            [
                "main quest/fireshield_earrings_gray.png",
                "main quest/fireshield_earrings.png",
            ],
        )
        self.cawlins_latter_button = TrackerInventoryButton(
            ["Nothing", CAWLINS_LETTER],
            ["sidequests/cawlin_letter_gray.png", "sidequests/cawlin_letter.png"],
        )
        self.insect_cage_button = TrackerInventoryButton(
            ["Nothing", BEEDLES_INSECT_CAGE],
            [
                "sidequests/beedle_insect_cage_gray.png",
                "sidequests/beedle_insect_cage.png",
            ],
        )
        self.rattle_button = TrackerInventoryButton(
            ["Nothing", RATTLE],
            ["sidequests/rattle_gray.png", "sidequests/rattle.png"],
        )
        self.gratitude_crystals_button = TrackerInventoryButton(
            ["Nothing"] + [GRATITUDE_CRYSTAL_PACK] * 16,
            ["sidequests/crystal_gray.png"]
            + [f"sidequests/crystal_{i * 5}.png" for i in range(1, 17)],
            None,
            [f"Gratitude Crystals ({i*5}/80)" for i in range(18)],
        )
        self.life_tree_fruit_button = TrackerInventoryButton(
            ["Nothing", LIFE_TREE_FRUIT],
            ["main quest/life_tree_fruit_gray.png", "main quest/life_tree_fruit.png"],
        )

        # self.tadtones_button = TrackerInventoryButton(
        #    ["Nothing", GROUP_OF_TADTONES],
        #    ["main quest/tadtones_gray.png", "main quest/tadtones.png"],
        # )
        self.scrapper_button = TrackerInventoryButton(
            ["Nothing", SCRAPPER],
            ["main quest/scrapper_gray.png", "main quest/Scrapper.png"],
        )

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
            area_button.check_all.connect(self.check_all_locations_in_list)
            area_button.mouse_hover.connect(self.update_hover_text)
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

        self.ui.dungeon_sv_layout.addWidget(TrackerDungeonLabel("SV", "Skyview Temple"))
        self.ui.dungeon_et_layout.addWidget(TrackerDungeonLabel("ET", "Earth Temple"))
        self.ui.dungeon_lmf_layout.addWidget(
            TrackerDungeonLabel("LMF", "Lanayru Mining Facility")
        )
        self.ui.dungeon_ac_layout.addWidget(
            TrackerDungeonLabel("AC", "Ancient Cistern")
        )
        self.ui.dungeon_ssh_layout.addWidget(TrackerDungeonLabel("SSH", "Sandship"))
        self.ui.dungeon_fs_layout.addWidget(TrackerDungeonLabel("FS", "Fire Sanctuary"))
        self.ui.dungeon_sk_layout.addWidget(TrackerDungeonLabel("SK", "Sky Keep"))

        self.ui.inventory_sword_layout.addWidget(self.sword_button)

        self.ui.inventory_b_wheel_layout.addWidget(self.beetle_button, 0, 0)
        self.ui.inventory_b_wheel_layout.addWidget(self.slingshot_button, 0, 1)
        self.ui.inventory_b_wheel_layout.addWidget(self.bombs_button, 0, 2)
        self.ui.inventory_b_wheel_layout.addWidget(self.bug_net_button, 0, 3)
        self.ui.inventory_b_wheel_layout.addWidget(self.bow_button, 1, 0)
        self.ui.inventory_b_wheel_layout.addWidget(self.clawshots_button, 1, 1)
        self.ui.inventory_b_wheel_layout.addWidget(self.whip_button, 1, 2)
        self.ui.inventory_b_wheel_layout.addWidget(self.gust_bellows_button, 1, 3)

        self.ui.inventory_tablet_layout.addWidget(TrackerTabletWidget())
        self.ui.inventory_tablet_layout.addWidget(self.triforce_button)

        self.ui.lower_inventory_layout.addWidget(self.lanayru_caves_key_button, 0, 0)
        self.ui.lower_inventory_layout.addWidget(self.sea_chart_button, 0, 1)
        self.ui.lower_inventory_layout.addWidget(self.spiral_charge_button, 0, 2)
        self.ui.lower_inventory_layout.addWidget(self.adventure_pouch_button, 0, 3)
        self.ui.lower_inventory_layout.addWidget(self.bottle_button, 0, 4)
        self.ui.lower_inventory_layout.addWidget(self.wallet_button, 0, 5)
        self.ui.lower_inventory_layout.addWidget(self.extra_wallet_button, 0, 6)

        self.ui.lower_inventory_layout.addWidget(self.harp_button, 1, 0)
        self.ui.lower_inventory_layout.addWidget(
            self.ballad_of_the_goddess_button, 1, 1
        )
        self.ui.lower_inventory_layout.addWidget(self.farores_courage_button, 1, 2)
        self.ui.lower_inventory_layout.addWidget(self.nayrus_wisdom_button, 1, 3)
        self.ui.lower_inventory_layout.addWidget(self.dins_power_button, 1, 4)
        self.ui.lower_inventory_layout.addWidget(self.song_of_the_hero_button, 1, 5)
        self.ui.lower_inventory_layout.addWidget(self.scrapper_button, 1, 6)

        self.ui.lower_inventory_layout.addWidget(self.mitts_button, 2, 0)
        self.ui.lower_inventory_layout.addWidget(self.water_dragon_scale_button, 2, 1)
        self.ui.lower_inventory_layout.addWidget(self.fireshield_earrings_button, 2, 2)
        self.ui.lower_inventory_layout.addWidget(self.cawlins_latter_button, 2, 3)
        self.ui.lower_inventory_layout.addWidget(self.insect_cage_button, 2, 4)
        self.ui.lower_inventory_layout.addWidget(self.rattle_button, 2, 5)
        self.ui.lower_inventory_layout.addWidget(self.gratitude_crystals_button, 2, 6)

        self.ui.lower_inventory_layout.addWidget(self.life_tree_fruit_button, 3, 0)
        # self.ui.lower_inventory_layout.addWidget(self.tadtones_button, 3, 1)

        # Connect clicking a tracker inventory button to updating the tracker
        for inventory_button in self.ui.tracker_tab.findChildren(
            TrackerInventoryButton
        ):
            inventory_button.clicked.connect(self.on_click_inventory_button)
            inventory_button.mouse_hover.connect(self.update_hover_text)

        # Connect dungeon labels to adding and removing dungeon locations
        # and display the dungeon name and status on the bottom section when hovered over
        for dungeon_label in self.ui.tracker_tab.findChildren(TrackerDungeonLabel):
            dungeon_label.clicked.connect(self.update_dungeon_progress_locations)
            dungeon_label.mouse_hover.connect(self.update_hover_text)

    def initialize_tracker_world(
        self, tracker_config: Config | None = None, autosave: dict = {}
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

        # Reset some internal variables
        self.last_opened_region = None
        self.last_checked_location = None
        self.sphere_tracked_items = {}
        for area in self.areas.values():
            area.hints.clear()

        # Re-hide the check/uncheck all buttons
        self.ui.check_all_button.setVisible(False)
        self.ui.check_all_in_logic_button.setVisible(False)
        self.ui.uncheck_all_button.setVisible(False)
        self.ui.set_hints_button.setVisible(False)

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

        # Temporarily set starting hearts to not random if it is.
        # Otherwise the item pool will fail to build.
        starting_hearts = self.world.setting("starting_hearts")
        starting_hearts_value = starting_hearts.value()
        if starting_hearts == "random":
            starting_hearts.set_value("6")

        # Build the world (only as necessary)
        self.world.build()
        self.world.perform_pre_entrance_shuffle_tasks()

        # Restore starting hearts value
        starting_hearts.set_value(starting_hearts_value)

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
        # four parts for the inventory button
        if self.inventory[self.world.get_item(SONG_OF_THE_HERO)]:
            self.inventory[self.world.get_item(SONG_OF_THE_HERO)] = 0
            self.inventory[self.world.get_item(SOTH_PART)] = 4

        # Some item groups can be obtained in any order, so we normalize the orders here
        # to match what their corresponding button has
        triforce_order = [TRIFORCE_OF_COURAGE, TRIFORCE_OF_WISDOM, TRIFORCE_OF_POWER]
        for group in (triforce_order,):
            num_group_parts = sum(
                [1 for item in self.inventory.elements() if item.name in group]
            )
            for i, item_name in enumerate(group):
                item = self.world.get_item(item_name)
                self.inventory[item] = 0
                if i < num_group_parts:
                    self.inventory[item] += 1

        # Replace individual starting crystals with crystal packs
        packs_to_add = self.inventory[self.world.get_item(GRATITUDE_CRYSTAL)] // 5
        self.inventory[self.world.get_item(GRATITUDE_CRYSTAL_PACK)] += packs_to_add
        self.inventory[self.world.get_item(GRATITUDE_CRYSTAL)] = 0

        # Remember if the user was tracking spheres
        self.allow_sphere_tracking |= autosave.get("allow_sphere_tracking", False)

        if self.allow_sphere_tracking:
            self.ui.toggle_sphere_tracking_button.setText("Disable Sphere Tracking")

        # Apply starting inventory to inventory buttons and assign world
        for inventory_button in self.ui.tracker_tab.findChildren(
            TrackerInventoryButton
        ):
            inventory_button.world = self.world
            inventory_button.inventory = self.inventory
            inventory_button.state = 0
            inventory_button.forbidden_states.clear()
            inventory_button.sphere_tracked_items = self.sphere_tracked_items
            inventory_button.allow_sphere_tracking = self.allow_sphere_tracking
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

        self.items_on_mark.clear()

        # Mark any locations marked from an autosave
        for loc_name in autosave.get("marked_locations", []):
            loc = self.world.get_location(loc_name)
            loc.marked = True

        # Bind any sphere-tracked items from an autosave
        for loc_name, (item_name, image) in autosave.get(
            "sphere_tracked_items", {}
        ).items():
            item = self.world.get_item(item_name)
            loc = self.world.get_location(loc_name)
            loc.tracked_item = item
            loc.tracked_item_image = image
            self.sphere_tracked_items[loc] = item.name

        # Restore any hints from an autosave
        for area_name, hints in autosave.get("hints", {}).items():
            self.areas[area_name].hints = set(hints)

        # Change progression status of some locations
        for location in self.world.get_all_item_locations():
            # Always display single crystal locations when
            # shuffle single crystals is off
            if location.has_vanilla_gratitude_crystal():
                location.progression = True
                self.items_on_mark[location] = location.current_item
                location.remove_current_item()

            # Only display goddess cubes when goddess chest shuffle is on
            if location.has_vanilla_goddess_cube():
                # Only list goddess cubes whose associated goddess chests aren't excluded
                if (
                    self.world.setting("goddess_chest_shuffle") == "on"
                    and self.world.get_location(
                        location.original_item.chain_locations[0]
                    ).progression
                ):
                    location.progression = True
                    self.items_on_mark[location] = location.current_item
                    location.remove_current_item()
                else:
                    location.progression = False

        # Assign the initial locations for all regions
        self.update_areas_locations()
        self.update_areas_entrances()

        self.calculate_own_dungeon_key_locations()

        # If barren unrequired dungeons is on then set all dungeon locations as non-progression
        if self.world.setting("empty_unrequired_dungeons") == "on":
            for dungeon in self.world.dungeons.values():
                for loc in dungeon.locations:
                    loc.eud_progression = False

        # Set the active area to that of the autosave or the Root if there is no autosave
        self.set_map_area(autosave.get("active_area", "Root"))

        # Reset dungeon selectors
        for label in self.ui.tracker_tab.findChildren(TrackerDungeonLabel):
            label.world = self.world
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
        area = self.areas.get(area_name, None)
        if area is None:
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
        self.back_button.setVisible(area_name != "Root")

        # Save current area in the autosave
        self.autosave_tracker()

    def show_area_locations(self, area_name: str) -> None:
        area_button = self.areas.get(area_name, None)
        if area_button is not None:
            self.last_opened_region = area_button
            self.show_area_location_info(area_name)
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
            locations = area_button.get_included_locations(remove_special_types=False)

            left_layout = QVBoxLayout()
            right_layout = QVBoxLayout()

            for i, loc in enumerate(locations):

                location_label = TrackerLocationLabel(
                    loc,
                    area_button.recent_search,
                    area_button,
                    self.allow_sphere_tracking,
                )
                # Split locations evenly among the left and right layouts
                if i < len(locations) / 2:
                    left_layout.addWidget(location_label)
                else:
                    right_layout.addWidget(location_label)

            # Add vertical spacers to push labels up
            left_layout.addSpacerItem(
                QSpacerItem(
                    40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )
            right_layout.addSpacerItem(
                QSpacerItem(
                    40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )

            self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
            self.ui.tracker_locations_scroll_layout.addLayout(right_layout)

            # Set clicking labels to update tracker
            for location_label in self.ui.tracker_tab.findChildren(
                TrackerLocationLabel
            ):
                location_label.clicked.connect(self.on_click_location_label)

            self.ui.check_all_button.setVisible(area_name != "Root")
            self.ui.check_all_in_logic_button.setVisible(area_name != "Root")
            self.ui.uncheck_all_button.setVisible(area_name != "Root")
            self.ui.set_hints_button.setVisible(area_name != "Root")

    def show_area_location_info(self, area_name: str) -> None:
        area_button = self.areas.get(area_name, None)
        if area_button is not None:
            # Show the area name and how many non-marked locations are available.
            # Get the labels if they were previously created to reuse them.
            # This prevents us from having to clear the layout and making
            # the scroll bar on the list of locations sometimes jump up
            self.create_info_widgets_if_none()

            area_name_label = self.ui.tracker_tab.findChild(QLabel, "area_name_label")
            locations_remaining_label = self.ui.tracker_tab.findChild(
                QLabel, "area_things_remaining_label"
            )
            show_entrances_button = self.ui.tracker_tab.findChild(
                TrackerShowEntrancesButton
            )
            show_locations_button = self.ui.tracker_tab.findChild(
                TrackerShowLocationsButton
            )

            area_name_label.setText(area_button.area)
            locations_remaining_label.setText(
                f"({len(area_button.get_available_locations())}/{len(area_button.get_unmarked_locations())})"
            )
            show_entrances_button.area_name = area_button.area
            show_entrances_button.setVisible(bool(area_button.entrances))
            show_locations_button.setVisible(False)

    def create_info_widgets_if_none(self) -> None:
        if not self.ui.tracker_tab.findChild(QLabel, "area_name_label"):
            self.clear_layout(self.ui.tracker_locations_info_layout)
            pt_size = 20

            area_name_label = QLabel()
            area_name_label.setObjectName("area_name_label")
            area_name_label.setStyleSheet(f"font-size: {pt_size}pt")
            area_name_label.setMargin(10)
            self.ui.tracker_locations_info_layout.addWidget(area_name_label)

            locations_remaining_label = QLabel()
            locations_remaining_label.setObjectName("area_things_remaining_label")
            locations_remaining_label.setStyleSheet(
                f"font-size: {pt_size}pt; qproperty-alignment: {int(QtCore.Qt.AlignmentFlag.AlignRight)};"
            )
            locations_remaining_label.setMargin(10)
            self.ui.tracker_locations_info_layout.addWidget(locations_remaining_label)

            show_entrances_button = TrackerShowEntrancesButton("")
            show_entrances_button.show_area_entrances.connect(self.show_area_entrances)
            self.ui.tracker_locations_info_layout.addWidget(show_entrances_button)

            show_locations_button = TrackerShowLocationsButton("")
            show_locations_button.show_area_locations.connect(self.show_area_locations)
            self.ui.tracker_locations_info_layout.addWidget(show_locations_button)

    def show_area_entrances(self, area_name: str) -> None:
        if area_button := self.areas.get(area_name, None):
            self.show_area_entrance_info(area_name)
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
            entrances = area_button.entrances

            left_layout = QVBoxLayout()
            right_layout = QVBoxLayout()

            entrances.sort()

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
                QSpacerItem(
                    40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )
            right_layout.addSpacerItem(
                QSpacerItem(
                    40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )

            self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
            self.ui.tracker_locations_scroll_layout.addLayout(right_layout)
        else:
            self.clear_layout(self.ui.tracker_locations_scroll_layout)
            self.clear_layout(self.ui.tracker_locations_info_layout)

    def show_area_entrance_info(self, area_name: str):
        if area_button := self.areas.get(area_name, None):
            self.create_info_widgets_if_none()
            # Show the area name and how many entrances have been connected.
            # Get the labels if they were previously created to reuse them.
            # This prevents us from having to clear the layout and making
            # the scroll bar on the list of locations sometimes jump up
            area_name_label = self.ui.tracker_tab.findChild(QLabel, "area_name_label")
            disconnected_entrances_label = self.ui.tracker_tab.findChild(
                QLabel, "area_things_remaining_label"
            )
            # For some reason, the previous back button still exists at this point?
            # Get the last in the list of show entrances button children
            show_entrances_button = self.ui.tracker_tab.findChildren(
                TrackerShowEntrancesButton
            )[-1]
            show_locations_button = self.ui.tracker_tab.findChild(
                TrackerShowLocationsButton
            )

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

        # Layouts used for the info area
        info_outer_layout = QVBoxLayout()
        info_inner_top_layout = QHBoxLayout()
        info_inner_bottom_layout = QHBoxLayout()

        lead_to_label = QLabel(f"Where did {entrance.original_name} lead to?")
        lead_to_label.setMargin(10)
        back_button = TrackerShowEntrancesButton(parent_area_name, "Back")
        back_button.show_area_entrances.connect(self.show_area_entrances)

        # Add a way to filter entrance targets
        filter_label = QLabel("Filter:")
        filter_label.setMargin(10)
        filter_line_edit = QLineEdit("")
        filter_line_edit.textChanged.connect(self.on_filter_text_changed)

        # Add everything to the layouts
        info_inner_top_layout.addWidget(lead_to_label)
        info_inner_top_layout.addWidget(back_button)
        info_inner_bottom_layout.addWidget(filter_label)
        info_inner_bottom_layout.addWidget(filter_line_edit)

        info_outer_layout.addLayout(info_inner_top_layout)
        info_outer_layout.addLayout(info_inner_bottom_layout)
        self.ui.tracker_locations_info_layout.addLayout(info_outer_layout)

        self.clear_layout(self.ui.tracker_locations_scroll_layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        targets = self.target_entrance_pools[entrance.type]

        targets.sort(key=lambda e: e.replaces.sort_priority)

        areas_shown = set()
        for i, target in enumerate(targets):
            # Only show targets which haven't been connected yet
            # and don't show multiple targets that lead to the same
            # area

            if (
                target.connected_area is not None
                and target.connected_area not in areas_shown
            ):
                areas_shown.add(target.connected_area)
                target_label = TrackerTargetLabel(entrance, target, parent_area_name)
                target_label.clicked.connect(self.on_click_target_label)

                if i < len(targets) / 2:
                    left_layout.addWidget(target_label)
                else:
                    right_layout.addWidget(target_label)

        # Add vertical spacers to push labels up
        left_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        right_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
        self.ui.tracker_locations_scroll_layout.addLayout(right_layout)

    def on_filter_text_changed(self, filter: str) -> None:
        for label in self.ui.tracker_tab.findChildren(TrackerTargetLabel):
            label.setVisible(filter.lower() in label.text().lower())

    def on_click_location_label(self, location_area: str, location: Location) -> None:
        if not location.marked:
            # stop sphere tracking if unmarking a location
            self.last_checked_location = None
            if location.tracked_item is not None and self.allow_sphere_tracking:
                location.tracked_item = None
                location.tracked_item_image = None
                del self.sphere_tracked_items[location]
                # update the location list to remove the item
                self.show_area_locations(location_area)
        # only start sphere-tracking "normal" locations
        elif (
            not (
                location.has_vanilla_goddess_cube()
                or location.has_vanilla_gratitude_crystal()
                or location.is_gossip_stone()
            )
            and self.allow_sphere_tracking
        ):
            self.last_checked_location = location
        self.update_tracker()
        self.show_area_location_info(location_area)
        self.last_opened_region.update_hover_text()

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
        self.calculate_own_dungeon_key_locations()
        self.update_tracker()

    def tracker_disconnect_entrance(self, entrance: Entrance) -> None:
        if target := self.connected_entrances.get(entrance, None):
            restore_connections(entrance, target)
            del self.connected_entrances[entrance]
            self.update_areas_locations()
            self.update_areas_entrances()
            self.update_tracker()
            self.calculate_own_dungeon_key_locations()

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
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
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

        # Make a copy of the inventory to modify
        inventory = self.inventory.copy()

        # Add in items from certain marked locations (except gratitude crystals,
        # the user will be responsible for updating their crystal count)
        already_added = set()
        for location, item in self.items_on_mark.items():
            if location.marked and not location.has_vanilla_gratitude_crystal():
                inventory[item] += 1
                already_added.add(location)

        # Use modified inventory for main search
        # TODO: Fix weird typing
        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, [self.world], inventory)
        search.search_worlds()

        for area_button in self.areas.values():
            area_button.update(search)

        main_available_locations = search.visited_locations.copy()

        # Add items to inventory for semi-logic search
        for location, item in self.items_on_mark.items():
            if location not in already_added and location in main_available_locations:
                search.owned_items[item] += 1

        # Add own dungeon keys if all their associated locations are in logic
        search.search_worlds()
        for key, locations in self.own_dungeon_key_locations:
            if all(
                [loc in search.visited_locations or loc.marked for loc in locations]
            ):
                search.owned_items[key] += 1
                search.search_worlds()

        # Any new found locations are in semi-logic
        semi_logic_locations = search.visited_locations - main_available_locations
        search.visited_locations -= semi_logic_locations
        for location in self.world.get_all_item_locations():
            location.in_semi_logic = location in semi_logic_locations

        # Update any labels that are currently shown
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
            entrance_label.update_text(search)

        for dungeon_label in self.ui.tracker_tab.findChildren(TrackerDungeonLabel):
            dungeon_label.update_style()

        self.show_area_location_info(location_label_area_name)
        self.autosave_tracker()
        self.update_statistics()
        if self.allow_sphere_tracking:
            self.update_spheres()
            self.show_sphere_tracking_info()

    def update_areas_locations(self) -> None:
        # Clear all locations before reassigning
        for area_button in self.ui.tracker_tab.findChildren(TrackerArea):
            area_button.locations.clear()

        self.world.assign_all_areas_hint_regions()
        all_locations = self.world.get_all_item_locations()
        if self.world.setting("gossip_stone_hints") == "on":
            all_locations.extend(self.world.get_gossip_stones())
        for location in all_locations:
            for area_name in set(
                [
                    area
                    for la in location.loc_access_list
                    for area in la.area.hint_regions
                ]
            ):
                area_button = self.areas.get(area_name, None)
                if area_button is not None:
                    area_button.locations.append(location)

    def update_dungeon_progress_locations(self, dungeon_name: str) -> None:
        if not self.started:
            return

        # Don't change anything if dungeons aren't guaranteed empty
        if self.world.setting("empty_unrequired_dungeons") == "off":
            return

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
        autosave: dict = yaml_load(filename)
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
        autosave["allow_sphere_tracking"] = self.allow_sphere_tracking
        autosave["sphere_tracked_items"] = {
            loc.name: (item_name, loc.tracked_item_image)
            for loc, item_name in self.sphere_tracked_items.items()
        }
        autosave["hints"] = {
            area_name: area.hints
            for area_name, area in self.areas.items()
            if area_name != "Root"
        }

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

        autosave: dict = yaml_load(filename)

        self.initialize_tracker_world(tracker_config, autosave)
        self.update_tracker()

    def calculate_own_dungeon_key_locations(self) -> None:
        self.own_dungeon_key_locations.clear()

        small_keys: bool = self.world.setting("small_keys") == "own_dungeon"
        boss_keys: bool = self.world.setting("boss_keys") == "own_dungeon"

        item_pool = get_complete_item_pool([self.world])
        # Filter out keys from the item pool
        # Small Keys must be first
        own_dungeon_keys = [
            item for item in item_pool if (item.is_dungeon_small_key and small_keys)
        ]
        own_dungeon_keys += [
            item for item in item_pool if (item.is_boss_key and boss_keys)
        ]
        for key in own_dungeon_keys:
            item_pool.remove(key)

        # Remove boss keys if they're still in
        item_pool = [item for item in item_pool if not item.is_boss_key]

        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, [self.world], item_pool)
        # Now go through and make the list of possible locations for each key
        for key in own_dungeon_keys:
            current_dungeon = None
            for dungeon in self.world.dungeons.values():
                if key in [dungeon.small_key, dungeon.boss_key]:
                    current_dungeon = dungeon
                    break

            if current_dungeon is None:
                continue

            # Find all possible locations for this key in the dungeon
            search.search_worlds()
            possible_dungeon_locations = [
                loc
                for loc in current_dungeon.locations
                if loc in search.visited_locations and loc.progression
            ]
            self.own_dungeon_key_locations.append((key, possible_dungeon_locations))

            # Add the key in for the next search
            search.owned_items[key] += 1

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
            event.button() == QtCore.Qt.MouseButton.RightButton
            and not self.active_area.area == "Root"
        ):
            self.on_back_button_clicked()
            self.update_hover_text("")

    def update_statistics(self) -> None:
        num_accessible_locations = len(self.areas["Root"].get_available_locations())
        num_remaining_locations = len(self.areas["Root"].get_unmarked_locations())
        num_checked_locations = (
            len(self.areas["Root"].get_included_locations()) - num_remaining_locations
        )
        self.ui.tracker_stats_checked.setText(f"{num_checked_locations: {3}}")
        self.ui.tracker_stats_accessible.setText(f"{num_accessible_locations: {3}}")
        self.ui.tracker_stats_remaining.setText(f"{num_remaining_locations: {3}}")

    def on_check_all_clicked(self):
        self.handle_check_all()

    def on_check_all_in_logic_clicked(self):
        self.handle_check_all(True, True)

    def on_uncheck_all_clicked(self):
        self.handle_check_all(False, False)

    def handle_check_all(self, in_logic_only=False, check=True):
        assert self.last_opened_region != None
        if in_logic_only:
            location_list = self.last_opened_region.get_available_locations()
        else:
            location_list = self.last_opened_region.get_included_locations()
        if check == False and self.allow_sphere_tracking:
            # untrack all sphere-tracked items in this area
            self.last_checked_location = None
            for location in location_list:
                if location.tracked_item is not None:
                    del self.sphere_tracked_items[location]
                    location.tracked_item = None
                    location.tracked_item_image = None

            # update the location list to remove the item images
            self.show_area_locations(self.last_opened_region.area)

        self.check_all_locations_in_list(location_list, check)
        self.last_opened_region.update_hover_text()

    def check_all_locations_in_list(self, location_list: list[Location], check=True):
        for location in location_list:
            location.marked = check
        self.update_tracker()

    def update_hover_text(self, text: str):
        self.ui.settings_default_option_description_label.setText(text)
        # print([item.name for item in self.world.item_table.values() if item.is_game_winning_item])

    def on_click_inventory_button(self, item: Item, item_image: str):
        if self.last_checked_location is not None and item is not None:
            self.last_checked_location.tracked_item = item
            self.last_checked_location.tracked_item_image = item_image
            self.sphere_tracked_items[self.last_checked_location] = item.name
        self.update_tracker()
        if self.last_opened_region is not None:
            self.show_area_locations(self.last_opened_region.area)

    def update_spheres(self):
        # Copy the current inventory to pass into the search
        # This gives logical support for items that are tracked
        # but not assigned to a location (such as random starting items)
        inventory = self.inventory.copy()
        for loc in self.world.location_table.values():
            loc.sphere = None
            if (item := loc.tracked_item) is not None:
                # Remove any sphere-tracked items
                if inventory[item] > 0:
                    inventory[item] -= 1

        # TODO: Fix weird typing
        sphere_search = Search(SearchMode.TRACKER_SPHERES, [self.world], inventory)
        sphere_search.search_worlds()
        for num, sphere in enumerate(sphere_search.playthrough_spheres):
            for loc in sphere:
                loc.sphere = num

    def show_sphere_tracking_info(self):
        if self.last_checked_location is not None:
            self.ui.tracker_sphere_tracking_label.setVisible(True)
            self.ui.cancel_sphere_tracking_button.setVisible(True)
            self.ui.toggle_sphere_tracking_button.setVisible(False)
            item = self.last_checked_location.tracked_item
            self.ui.tracker_sphere_tracking_label.setText(
                self.last_checked_location.name
                + "\n"
                + (item.name if item is not None else "Select an item.")
            )
        else:
            self.ui.tracker_sphere_tracking_label.setVisible(False)
            self.ui.cancel_sphere_tracking_button.setVisible(False)
            self.ui.toggle_sphere_tracking_button.setVisible(True)

    def cancel_sphere_tracking(self):
        self.last_checked_location = None
        self.show_sphere_tracking_info()

    def show_hint_options(self):
        self.clear_layout(self.ui.tracker_locations_info_layout)

        # Layout used for the info area
        info_layout = QHBoxLayout()

        hint_info_label = QLabel(f"Select a hint for {self.last_opened_region.area}.")
        hint_info_label.setMargin(10)
        back_button = TrackerShowLocationsButton(self.last_opened_region.area)
        back_button.setText("Back")
        back_button.show_area_locations.connect(self.show_area_locations)

        # Add everything to the layouts
        info_layout.addWidget(hint_info_label)
        info_layout.addWidget(back_button)

        self.ui.tracker_locations_info_layout.addLayout(info_layout)

        self.clear_layout(self.ui.tracker_locations_scroll_layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        ALL_HINTS = [
            "Clear Hints",
            "Path to Ghirahim 1",
            "Path to Scaldera",
            "Path to Moldarach",
            "Path to Koloktos",
            "Path to Tentalus",
            "Path to Ghirahim 2",
            "Path to Demise",
            "Barren",
        ]

        # skip hints that are already in the area's hint list
        hints = [
            hint for hint in ALL_HINTS if hint not in self.last_opened_region.hints
        ]

        for i, hint in enumerate(hints):

            hint_label = TrackerHintLabel(hint, self.last_opened_region)
            hint_label.clicked.connect(self.on_click_hint_label)

            if i < len(hints) / 2:
                left_layout.addWidget(hint_label)
            else:
                right_layout.addWidget(hint_label)

        # Add vertical spacers to push labels up
        left_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        right_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        self.ui.tracker_locations_scroll_layout.addLayout(left_layout)
        self.ui.tracker_locations_scroll_layout.addLayout(right_layout)

    def on_click_hint_label(self, hint: str, area: TrackerArea):
        if hint == "Clear Hints":
            area.hints.clear()
        else:
            area.hints.add(hint)

        self.show_area_locations(area.area)

    def toggle_sphere_tracking(self):
        self.allow_sphere_tracking = not self.allow_sphere_tracking
        for inventory_button in self.ui.tracker_tab.findChildren(
            TrackerInventoryButton
        ):
            inventory_button.allow_sphere_tracking = self.allow_sphere_tracking
        if self.allow_sphere_tracking:
            self.ui.toggle_sphere_tracking_button.setText("Disable Sphere Tracking")
            self.update_spheres()
        else:
            self.ui.toggle_sphere_tracking_button.setText("Enable Sphere Tracking")
            self.cancel_sphere_tracking()
        if self.last_opened_region is not None:
            self.show_area_locations(self.last_opened_region.area)

        self.update_tracker()

    def display_sphere_tracking_popup(self):
        self.main.fi_info_dialog.show_dialog(
            "How to use Sphere Tracking",
            """
            <b>What is sphere tracking?</b><br><br>
            Sphere tracking is a feature of the tracker
            that allows you to keep track of where you found
            certain items, and the 'sphere' of logic that each
            check is in. A sphere describes the rough number of
            'steps' to take or items to find to access a specific
            check. For example, locations available from the start
            are listed as 'Sphere 0' locations, and any locations
            unlocked by items found in sphere 0 are sphere 1
            locations, and so on.<br><br>

            (It's important to note that SSHD Randomizer's logic
            does not inherently account for spheres; they are
            merely a helpful way to visualize progression and
            requirements throughout a seed.)<br><br>

            <b>Instructions</b><br><br>

            To start sphere tracking, mark off a location, then select an item.
            The item will now be bound to that location, and the tracker will
            take that item placement into account for sphere
            calculations. The item's icon (at the time that you marked it off)
            will now appear next to the check in the location list.
            Unmarking the location will also unbind the item that was tracked there.
            When you mouse over an item in the inventory section, a tooltip will
            appear with all the locations you tracked that item to appear in.
            """,
        )
