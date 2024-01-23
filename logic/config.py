from pathlib import Path
import yaml
from constants.configdefaults import get_default_setting
from constants.itemconstants import STARTABLE_ITEMS

from .settings import *


class ConfigError(RuntimeError):
    pass


class Config:
    def __init__(self) -> None:
        self.seed: str = None  # type: ignore
        self.settings: list[SettingMap] = []
        self.num_worlds: int = 0
        self.generate_spoiler_log = True
        self.output_dir: Path = None  # type: ignore
        self.input_dir: Path = None  # type: ignore
        self.plandomizer: bool = False
        self.plandomizer_file: Path = None  # type: ignore
        self.theme_mode: str = None  # type: ignore
        self.theme_presets: str = None  # type: ignore
        self.use_custom_theme: bool = False
        self.font_family: str = None  # type: ignore
        self.font_size: int = 0


def create_default_config(filename: Path):
    config = Config()
    config.output_dir = get_default_setting("output_dir")
    config.input_dir = get_default_setting("input_dir")
    config.seed = get_default_setting("seed")
    config.plandomizer = get_default_setting("plandomizer")
    config.plandomizer_file = get_default_setting("plandomizer_file")
    config.generate_spoiler_log = get_default_setting("generate_spoiler_log")

    config.theme_mode = get_default_setting("theme_mode")
    config.theme_presets = get_default_setting("theme_presets")
    config.use_custom_theme = get_default_setting("use_custom_theme")
    config.font_family = get_default_setting("font_family")
    config.font_size = get_default_setting("font_size")

    config.settings.append(SettingMap())
    setting_map = config.settings[0]
    setting_map.starting_inventory = get_default_setting("starting_inventory")
    setting_map.excluded_locations = get_default_setting("excluded_locations")
    setting_map.excluded_hint_locations = get_default_setting("excluded_hint_locations")
    setting_map.mixed_entrance_pools = get_default_setting("mixed_entrance_pools")

    for setting_name in get_all_settings_info():
        setting_map.settings[setting_name] = create_default_setting(setting_name)

    write_config_to_file(filename, config)


def create_default_setting(setting_name: str) -> Setting:
    all_settings_info = get_all_settings_info()

    if (setting_info := all_settings_info.get(setting_name)) is None:
        raise ConfigError(f"Could not find setting info for setting: {setting_name}.")

    new_setting = Setting(
        setting_name,
        setting_info.options[setting_info.default_option_index],
        setting_info,
    )

    return new_setting


def write_config_to_file(filename: Path, config: Config):
    with open(filename, "w") as config_file:
        config_out = {}

        config_out["seed"] = config.seed
        config_out["input_dir"] = config.input_dir.as_posix()
        config_out["output_dir"] = config.output_dir.as_posix()
        config_out["plandomizer"] = config.plandomizer
        config_out["plandomizer_file"] = config.plandomizer_file

        config_out["theme_mode"] = config.theme_mode
        config_out["theme_presets"] = config.theme_presets
        config_out["use_custom_theme"] = config.use_custom_theme
        config_out["font_family"] = config.font_family
        config_out["font_size"] = config.font_size

        for i, setting_map in enumerate(config.settings):
            world_num = f"World {i + 1}"
            config_out[world_num] = {}

            for setting_name, setting in setting_map.settings.items():
                config_out[world_num][setting_name] = setting.value

            # Map starting inventory
            config_out[world_num]["starting_inventory"] = []

            for item in setting_map.starting_inventory.elements():
                config_out[world_num]["starting_inventory"].append(item)

            # Map excluded locations
            config_out[world_num]["excluded_locations"] = []

            for loc in setting_map.excluded_locations:
                config_out[world_num]["excluded_locations"].append(loc)

            # Map excluded hint locations
            config_out[world_num]["excluded_hint_locations"] = []

            for loc in setting_map.excluded_hint_locations:
                config_out[world_num]["excluded_hint_locations"].append(loc)

            # Map mixed pools
            config_out[world_num]["mixed_entrance_pools"] = []

            for pool in setting_map.mixed_entrance_pools:
                config_out[world_num]["mixed_entrance_pools"].append(pool)

        yaml.safe_dump(config_out, config_file, sort_keys=False)


def load_or_get_default_from_config(config: dict, setting_name: str):
    if (setting_value := config.get(setting_name)) is None:
        setting_value = get_default_setting(setting_name)

    return setting_value


def load_config_from_file(
    filepath: Path, allow_rewrite: bool = True, create_if_blank: bool = False
) -> Config:
    if create_if_blank and not filepath.is_file():
        print("No config file found. Creating default config file.")
        create_default_config(filepath)

    config = Config()
    # If the config is missing any options, set defaults and resave it afterwards
    rewrite_config: bool = False
    with open(filepath) as config_file:
        config_in = yaml.safe_load(config_file)

        if config_in is None:
            config_in = dict()

        config.seed = load_or_get_default_from_config(config_in, "seed")
        config.input_dir = Path(load_or_get_default_from_config(config_in, "input_dir"))
        config.output_dir = Path(
            load_or_get_default_from_config(config_in, "output_dir")
        )
        config.plandomizer = load_or_get_default_from_config(config_in, "plandomizer")
        config.plandomizer_file = load_or_get_default_from_config(
            config_in, "plandomizer_file"
        )

        config.theme_mode = load_or_get_default_from_config(config_in, "theme_mode")
        config.theme_presets = load_or_get_default_from_config(
            config_in, "theme_presets"
        )
        config.use_custom_theme = load_or_get_default_from_config(
            config_in, "use_custom_theme"
        )
        config.font_family = load_or_get_default_from_config(config_in, "font_family")
        config.font_size = load_or_get_default_from_config(config_in, "font_size")

        world_num = 1
        world_num_str = f"World {world_num}"

        # Create default World 1 if it doesn't exist already
        if world_num_str not in config_in:
            config_in[world_num_str] = {}

        settings_info = get_all_settings_info()
        while world_num_str in config_in:
            config.settings.append(SettingMap())
            cur_world_settings = config.settings[world_num - 1]

            for setting_name in config_in[world_num_str]:
                # Special handling for starting inventory
                if setting_name == "starting_inventory":
                    starting_inventory: list = config_in[world_num_str][setting_name]

                    if not isinstance(starting_inventory, list):
                        raise ConfigError(
                            f"Could not read value for setting '{setting_name}'. Are you sure that {setting_name} is defined as a list? Current value: {starting_inventory}."
                        )

                    # Verify starting inventory list is valid
                    invalid_starting_items = starting_inventory.copy()

                    for item in STARTABLE_ITEMS:
                        if item in invalid_starting_items:
                            invalid_starting_items.remove(item)

                    if len(invalid_starting_items) > 0:
                        for item in invalid_starting_items:
                            starting_inventory.remove(item)

                        config_in[world_num_str][setting_name] = starting_inventory
                        cur_world_settings.starting_inventory = Counter(
                            starting_inventory
                        )
                        rewrite_config = True

                        print(
                            f"WARNING: Invalid starting items found. The invalid entries have been removed. Invalid starting items: {invalid_starting_items}"
                        )

                    cur_world_settings.starting_inventory = Counter(starting_inventory)
                    continue

                # Special handling for excluded locations
                if setting_name == "excluded_locations":
                    excluded_locations: list[str] = config_in[world_num_str][
                        setting_name
                    ]

                    if not isinstance(excluded_locations, list):
                        raise ConfigError(
                            f"Could not read value for setting '{setting_name}'. Are you sure that {setting_name} is defined as a list? Current value: {excluded_locations}."
                        )

                    cur_world_settings.excluded_locations = excluded_locations
                    continue

                # Special handling for excluded hint locations
                if setting_name == "excluded_hint_locations":
                    excluded_hint_locations: list[str] = config_in[world_num_str][
                        setting_name
                    ]

                    if not isinstance(excluded_hint_locations, list):
                        raise ConfigError(
                            f"Could not read value for setting '{setting_name}'. Are you sure that {setting_name} is defined as a list? Current value: {excluded_hint_locations}."
                        )

                    cur_world_settings.excluded_hint_locations = excluded_hint_locations
                    continue

                # Special handling for mixed entrance pools
                if setting_name == "mixed_entrance_pools":
                    mixed_pools = config_in[world_num_str][setting_name]

                    if not isinstance(mixed_pools, list):
                        raise ConfigError(
                            f"Could not read value for setting '{setting_name}'. Are you sure that {setting_name} is defined as a list? Current value: {mixed_pools}."
                        )

                    for pool in mixed_pools:
                        cur_world_settings.mixed_entrance_pools.append(pool)

                    # Turn mixed pools into a list of lists
                    if mixed_pools:
                        if type(mixed_pools[0]) is str:
                            cur_world_settings.mixed_entrance_pools = [  # type: ignore
                                cur_world_settings.mixed_entrance_pools  # type: ignore
                            ]
                    continue

                if setting_name not in settings_info:
                    rewrite_config = True
                    continue

                setting_value = config_in[world_num_str][setting_name]
                # TODO: Hex codes

                if setting_value not in settings_info[setting_name].options:
                    raise ConfigError(
                        f'"{setting_value}" is not a valid value for setting "{setting_name}"'
                    )

                cur_world_settings.settings[setting_name] = Setting(
                    setting_name, setting_value, settings_info[setting_name]
                )

            # Add in defaults settings that weren't listed
            for setting_name, info in settings_info.items():
                if setting_name not in cur_world_settings.settings:
                    default_value = info.options[info.default_option_index]
                    cur_world_settings.settings[setting_name] = Setting(
                        setting_name, default_value, info
                    )
                    rewrite_config = True

            # Special handling for other settings
            for setting_name in (
                "starting_inventory",
                "excluded_locations",
                "excluded_hint_locations",
                "mixed_entrance_pools",
            ):
                if config_in[world_num_str].get(setting_name) is None:
                    cur_world_settings.__setattr__(
                        setting_name, get_default_setting(setting_name)
                    )
                    rewrite_config = True

            world_num += 1
            world_num_str = f"World {world_num}"

    if rewrite_config and allow_rewrite:
        write_config_to_file(filepath, config)

    return config
