from pathlib import Path
import yaml
from constants.configconstants import (
    CONFIG_FIELDS,
    ENTRANCE_TYPES,
    PREFERENCE_FIELDS,
    SETTING_ALIASES,
    get_default_setting,
)
from constants.itemconstants import STARTABLE_ITEMS
from filepathconstants import PREFERENCES_PATH, WORDS_PATH, PLANDO_PATH

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
        self.use_plandomizer: bool = False
        self.plandomizer_file: str | None = None
        self.theme_mode: str = None  # type: ignore
        self.theme_presets: str = None  # type: ignore
        self.use_custom_theme: bool = False
        self.font_family: str = None  # type: ignore
        self.font_size: int = 0
        self.verified_extract: bool = False
        self.tutorial_random_settings: bool = False
        self.first_time_seed_gen_text: bool = False
        self.hash: str = ""

    def get_hash(self) -> str:
        if self.hash:
            return self.hash

        # Create hash if we haven't made it yet
        with open(WORDS_PATH, encoding="utf-8") as words_file:
            words = yaml.safe_load(words_file)
            hash_words = []
            for _ in range(3):
                hash_words.append(random.choice(words))
                words.remove(hash_words[-1])

            self.hash = " ".join(hash_words)

        return self.hash


def seed_rng(
    config: Config,
    resolve_non_standard_random: bool = False,
    ignore_invalid_plandomizer: bool = True,
) -> None:
    # Seed with system time in-case we're choosing random cosmetics
    random.seed()

    # Seed RNG with combination of seed, standard settings, and plando file (if being used)
    hash_str = config.seed
    for setting_map in config.settings:
        for name, setting in setting_map.settings.items():
            if setting.info.type == SettingType.STANDARD:
                hash_str += name + setting.value
            elif resolve_non_standard_random:
                # If any non-standard settings are random, resolve them now before seeding
                setting.resolve_if_random()

        # Special handling for other settings
        for item in sorted(setting_map.starting_inventory):
            hash_str += item * setting_map.starting_inventory[item]

        for loc in sorted(setting_map.excluded_locations):
            hash_str += loc

        for loc in sorted(setting_map.excluded_hint_locations):
            hash_str += loc

        for pool in setting_map.mixed_entrance_pools:
            for entrance_type in sorted(pool):
                hash_str += entrance_type

    if config.use_plandomizer:
        if config.plandomizer_file is None or config.plandomizer_file == "None":
            if not ignore_invalid_plandomizer:
                raise ConfigError(
                    f"Cannot use plandomizer file as the current plandomizer filename is invalid: {config.plandomizer_file}"
                )
        else:
            with open(
                PLANDO_PATH / config.plandomizer_file, encoding="utf-8"
            ) as plando_file:
                hash_str += plando_file.read()

    if config.generate_spoiler_log:
        hash_str += "spoilerlog"

    random.seed(hash_str)


def create_default_config(filename: Path):
    config = load_preferences()

    for field in CONFIG_FIELDS:
        config.__setattr__(field, get_default_setting(field))

    config.settings.append(SettingMap())
    setting_map = config.settings[0]
    setting_map.starting_inventory = get_default_setting("starting_inventory")
    setting_map.excluded_locations = get_default_setting("excluded_locations")
    setting_map.excluded_hint_locations = get_default_setting("excluded_hint_locations")
    setting_map.mixed_entrance_pools = get_default_setting("mixed_entrance_pools")
    setting_map.other_mods = get_default_setting("other_mods")

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


def write_config_to_file(
    filename: Path, config: Config, write_preferences: bool = True
):
    with open(filename, "w", encoding="utf-8") as config_file:
        config_out = {}

        for field in CONFIG_FIELDS:
            config_out[field] = config.__getattribute__(field)

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
            config_out[world_num]["mixed_entrance_pools"] = [
                list() for _ in range(len(ENTRANCE_TYPES) - 1)
            ]

            for pool_index, pool in enumerate(setting_map.mixed_entrance_pools):
                config_out[world_num]["mixed_entrance_pools"][pool_index] = pool

            # Map other mods
            config_out[world_num]["other_mods"] = []

            for other_mod in setting_map.other_mods:
                config_out[world_num]["other_mods"].append(other_mod)

        yaml.safe_dump(config_out, config_file, sort_keys=False)

    if not write_preferences:
        return

    with open(PREFERENCES_PATH, "w", encoding="utf-8") as preferences_file:
        preferences_out = {}

        for field in PREFERENCE_FIELDS:
            preferences_out[field] = config.__getattribute__(field)

        # Make sure output_dir is always a string
        preferences_out["output_dir"] = preferences_out["output_dir"].as_posix()

        yaml.safe_dump(preferences_out, preferences_file, sort_keys=False)


def load_or_get_default_from_config(config: dict, setting_name: str):
    is_from_default = False

    if (setting_value := config.get(setting_name)) is None:
        setting_value = get_default_setting(setting_name)
        is_from_default = True

    return (setting_value, is_from_default)


def load_config_from_file(
    filepath: Path,
    allow_rewrite: bool = True,
    create_if_blank: bool = False,
    default_on_invalid_value: bool = False,
) -> Config:
    if create_if_blank and not filepath.is_file():
        print("No config file found. Creating default config file.")
        create_default_config(filepath)

    config = load_preferences()
    # If the config is missing any options, set defaults and resave it afterwards
    rewrite_config: bool = False
    with open(filepath, encoding="utf-8") as config_file:
        config_in = yaml.safe_load(config_file)

        if config_in is None:
            config_in = dict()

        for field in CONFIG_FIELDS:
            field_value, is_from_default = load_or_get_default_from_config(
                config_in, field
            )
            config.__setattr__(field, field_value)

            if is_from_default:
                config_in[field] = field_value
                rewrite_config = True

        world_num = 1
        world_num_str = f"World {world_num}"

        # Create default World 1 if it doesn't exist already
        if world_num_str not in config_in:
            config_in[world_num_str] = {}

        settings_info = get_all_settings_info()
        while world_num_str in config_in:
            config.settings.append(SettingMap())
            cur_world_settings = config.settings[world_num - 1]

            # Loop through and parse all settings from the config
            # in the order of the settings info
            for setting_name, info in settings_info.items():

                # If a setting does not exist, check old aliases
                # or create a new entry for the setting
                if setting_name not in config_in[world_num_str]:
                    rewrite_config = True
                    if old_setting_alias := SETTING_ALIASES.get(setting_name, False):
                        if old_alias_value := config_in[world_num_str].get(
                            old_setting_alias, False
                        ):
                            cur_world_settings.settings[setting_name] = Setting(
                                setting_name, old_alias_value, info
                            )
                            continue
                    default_value = info.options[info.default_option_index]
                    cur_world_settings.settings[setting_name] = Setting(
                        setting_name, default_value, info
                    )
                # Otherwise read in the setting normally
                else:
                    setting_value = config_in[world_num_str][setting_name]

                    if setting_value not in settings_info[setting_name].options:
                        if default_on_invalid_value:
                            rewrite_config = True
                            default_value = info.options[info.default_option_index]
                            print(
                                f'"{setting_value}" is not a valid value for setting "{setting_name}". Defaulting to "{default_value}"'
                            )
                            setting_value = default_value
                        else:
                            raise ConfigError(
                                f'"{setting_value}" is not a valid value for setting "{setting_name}"'
                            )

                    cur_world_settings.settings[setting_name] = Setting(
                        setting_name, setting_value, settings_info[setting_name]
                    )
                # TODO: Hex codes

            # Special handling for other settings
            for setting_name in (
                "starting_inventory",
                "excluded_locations",
                "excluded_hint_locations",
                "mixed_entrance_pools",
                "other_mods",
            ):
                if config_in[world_num_str].get(setting_name) is None:
                    cur_world_settings.__setattr__(
                        setting_name, get_default_setting(setting_name)
                    )
                    rewrite_config = True

                # Special handling for starting inventory
                elif setting_name == "starting_inventory":
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
                elif setting_name == "excluded_locations":
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
                elif setting_name == "excluded_hint_locations":
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
                elif setting_name == "mixed_entrance_pools":
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

                elif setting_name == "other_mods":
                    other_mods = config_in[world_num_str][setting_name]

                    if not isinstance(other_mods, list):
                        raise ConfigError(
                            f"Could not read value for setting '{setting_name}'. Are you sure that {setting_name} is defined as a list? Current value: {other_mods}."
                        )

                    cur_world_settings.other_mods = other_mods

            world_num += 1
            world_num_str = f"World {world_num}"

    if rewrite_config and allow_rewrite:
        write_config_to_file(filepath, config)

    return config


def load_preferences() -> Config:
    config = Config()
    filepath = Path(PREFERENCES_PATH)

    if not filepath.is_file():
        with open(filepath, "w", encoding="utf-8") as _:
            pass

    # If missing any options, set defaults and resave it afterwards
    rewrite_preferences: bool = False
    with open(filepath, "r", encoding="utf-8") as preferences_file:
        preferences_in = yaml.safe_load(preferences_file)

        if preferences_in is None:
            preferences_in = dict()

        for field in PREFERENCE_FIELDS:
            field_value, is_from_default = load_or_get_default_from_config(
                preferences_in, field
            )
            config.__setattr__(field, field_value)

            if is_from_default:
                preferences_in[field] = field_value
                rewrite_preferences = True

        # Make sure output_dir is always a Path object in config...
        config.output_dir = Path(config.output_dir)
        # ...and a string if being dumped
        preferences_in["output_dir"] = Path(preferences_in["output_dir"]).as_posix()

    if rewrite_preferences:
        with open(filepath, "w", encoding="utf-8") as preferences_file:
            yaml.safe_dump(preferences_in, preferences_file, sort_keys=False)

    return config
