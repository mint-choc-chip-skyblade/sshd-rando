from pathlib import Path
import yaml
import random

from filepathconstants import WORDS_PATH

from .settings import *

required_config_fields = [
    "input_dir",
    "seed",
    "output_dir",
    "plandomizer",
    "plandomizer_file",
]


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
    config.output_dir = Path("./output")
    config.input_dir = Path("./title")
    config.seed = get_new_seed()
    config.plandomizer = False
    config.plandomizer_file = None  # type: ignore
    config.generate_spoiler_log = True

    config.theme_mode = "Auto"
    config.theme_presets = "Default"
    config.use_custom_theme = False
    config.font_family = "Lato"
    config.font_size = 10

    config.settings.append(SettingMap())
    setting_map = config.settings[0]
    setting_map.starting_inventory = Counter()
    setting_map.excluded_locations = []
    setting_map.mixed_entrance_pools = []

    for setting_name, setting_info in get_all_settings_info().items():
        new_setting = Setting()
        new_setting.name = setting_name
        new_setting.info = setting_info
        new_setting.value = setting_info.options[setting_info.default_option_index]
        setting_map.settings[setting_name] = new_setting

    write_config_to_file(filename, config)


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

            if len(setting_map.starting_inventory) == 0:
                config_out[world_num]["starting_inventory"] = []
            else:
                config_out[world_num]["starting_inventory"] = []
                for item in setting_map.starting_inventory.elements():
                    config_out[world_num]["starting_inventory"].append(item)

            if len(setting_map.excluded_locations) == 0:
                config_out[world_num]["excluded_locations"] = []
            else:
                config_out[world_num]["excluded_locations"] = []
                for loc in setting_map.excluded_locations:
                    config_out[world_num]["excluded_locations"].append(loc)

            if len(setting_map.mixed_entrance_pools) == 0:
                config_out[world_num]["mixed_entrance_pools"] = []
            else:
                config_out[world_num]["mixed_entrance_pools"] = []
                for pool in setting_map.mixed_entrance_pools:
                    config_out[world_num]["mixed_entrance_pools"].append(pool)

        yaml.safe_dump(config_out, config_file, sort_keys=False)


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

        # Check required fields
        for field in required_config_fields:
            if field not in config_in:
                raise ConfigError(f'Missing field "{field}" in {filepath}')

        config.seed = config_in["seed"]
        config.input_dir = Path(config_in["input_dir"])
        config.output_dir = Path(config_in["output_dir"])
        config.plandomizer = config_in["plandomizer"]
        config.plandomizer_file = config_in["plandomizer_file"]

        config.theme_mode = config_in["theme_mode"]
        config.theme_presets = config_in["theme_presets"]
        config.use_custom_theme = config_in["use_custom_theme"]
        config.font_family = config_in["font_family"]
        config.font_size = config_in["font_size"]

        world_num = 1
        world_num_str = f"World {world_num}"

        settings_info = get_all_settings_info()
        while world_num_str in config_in:
            config.settings.append(SettingMap())
            cur_world_settings = config.settings[world_num - 1]

            for setting_name in config_in[world_num_str]:
                # Special handling for starting inventory
                if setting_name == "starting_inventory":
                    starting_inventory = config_in[world_num_str][setting_name]
                    cur_world_settings.starting_inventory = Counter(starting_inventory)
                    continue

                # Special handling for excluded locations
                if setting_name == "excluded_locations":
                    excluded_locations: list[str] = config_in[world_num_str][
                        setting_name
                    ]
                    cur_world_settings.excluded_locations = excluded_locations
                    continue

                # Special handling for mixed entrance pools
                if setting_name == "mixed_entrance_pools":
                    mixed_pools = config_in[world_num_str][setting_name]
                    for pool in mixed_pools:
                        cur_world_settings.mixed_entrance_pools.append(pool)
                    # Turn mixed pools into a list of lists
                    if mixed_pools:
                        if type(mixed_pools[0]) is str:
                            cur_world_settings.mixed_entrance_pools = [
                                cur_world_settings.mixed_entrance_pools
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

            world_num += 1
            world_num_str = f"World {world_num}"

    if rewrite_config and allow_rewrite:
        write_config_to_file(filepath, config)

    return config


def get_new_seed() -> str:
    with open(WORDS_PATH, "r") as words_file:
        words = yaml.safe_load(words_file)
        new_seed = ""

        for _ in range(0, 4):
            new_seed += random.choice(words)

        return new_seed
