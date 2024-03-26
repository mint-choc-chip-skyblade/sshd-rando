import base64
from collections import Counter
from constants.configconstants import ENTRANCE_TYPES
from constants.itemconstants import STARTABLE_ITEMS
from constants.randoconstants import VERSION
from logic.config import Config
from logic.location import Location
from logic.location_table import build_location_table
from logic.settings import Setting, SettingMap, SettingType, get_all_settings_info
from randomizer.packed_bits import PackedBitsReader, PackedBitsWriter

SETTING_STRING_VERSION = f"SSHDR-{VERSION}"
DELIMITER = ":"


class SettingStringError(RuntimeError):
    pass


# The setting string is made up of 2 major parts:
# * The header
# * World specific settings
#
# Each part is separated by a delimiter: b"\0".
#
# The header contains:
# * The randomizer version that created the setting string
# * The generate_spoiler_log config setting
# * The seed
#
# Each section of the header is separated by a delimiter b"\0".
#
# The world specific settings are base64 encoded strings representing all the
# settings for each world of a config. Each world is also separated by a
# delimiter: b"\0" + "W".
def setting_string_from_config(
    config: Config, location_table: dict[str, Location] | None
) -> str:
    if location_table is None:
        location_table = build_location_table()

    setting_string = b""
    setting_string += SETTING_STRING_VERSION.encode("ascii")
    setting_string += b"\0"
    setting_string += str(int(config.generate_spoiler_log)).encode("ascii")
    setting_string += b"\0"
    setting_string += config.seed.encode("ascii")

    setting_info = get_all_settings_info()

    for world_index, world_settings in enumerate(config.settings):
        bits_writer = PackedBitsWriter()

        for setting_name in setting_info:
            setting = world_settings.settings[setting_name]

            if setting.info.type == SettingType.COSMETIC:
                continue

            bits_writer.write(
                setting.current_option_index, get_bit_length_for_setting(setting)
            )

        for location in location_table:
            bits_writer.write(
                int(
                    location
                    in world_settings.excluded_locations
                    + world_settings.excluded_hint_locations
                ),
                1,
            )

        startable_items = Counter(STARTABLE_ITEMS)

        for item in startable_items:
            item_count = 0

            if item in world_settings.starting_inventory:
                item_count = world_settings.starting_inventory[item]

            bits_writer.write(item_count, startable_items[item].bit_length())

        # Mixed entrance pools
        #
        # Data stored as a list of pool_indexes for each entrance type
        # Assumes each entrance type only appears once and that the order of
        # entrance types doesn't change
        mixed_entrance_pools = world_settings.mixed_entrance_pools

        for entrance_index, entrance_type in enumerate(ENTRANCE_TYPES):
            pool_index = 0

            while pool_index < len(ENTRANCE_TYPES):
                if (
                    pool_index < len(mixed_entrance_pools)
                    and entrance_type in mixed_entrance_pools[pool_index]
                ):
                    break

                pool_index += 1

            bits_writer.write(pool_index, len(ENTRANCE_TYPES).bit_length())

        bits_writer.flush()

        setting_string += b"\0" + f":W".encode("ascii")
        setting_string += bits_writer.get_packed_bytes()

    return base64.b64encode(setting_string).decode("ascii")


def update_config_from_setting_string(
    config: Config,
    encoded_setting_string: str,
    location_table: dict[str, Location] | None,
    allow_all_versions=False,
) -> Config:
    if location_table is None:
        location_table = build_location_table()

    encoded_setting_string = encoded_setting_string.strip()
    if not encoded_setting_string:
        raise SettingStringError(f"Could not process setting string as it is empty.")

    setting_string = base64.b64decode(encoded_setting_string)
    header, *worlds = setting_string.split(b"\0" + ":W".encode("ascii"))

    version, spoiler_log, seed = (
        value.decode("ascii") for value in header.split(b"\0", 2)
    )

    if not allow_all_versions and version != SETTING_STRING_VERSION:
        raise SettingStringError(
            f"Cannot use a setting string from a different version of the randomizer. Expected: {SETTING_STRING_VERSION}. Found: {version}."
        )

    config.generate_spoiler_log = bool(int(spoiler_log))
    config.seed = seed

    config.num_worlds = len(worlds)

    setting_info = get_all_settings_info()

    for world_index, world_packed_bytes in enumerate(worlds):
        bits_reader = PackedBitsReader(world_packed_bytes)

        if world_index >= len(config.settings):
            config.settings.append(SettingMap())

        world_settings = config.settings[world_index]

        for setting_name in setting_info:
            setting = world_settings.settings[setting_name]

            if setting.info.type == SettingType.COSMETIC:
                continue

            value_len = get_bit_length_for_setting(setting)
            value_index = bits_reader.read(value_len)

            if value_index >= len(setting.info.options):
                warning_string = f"WARNING: Invalid value index ({value_index}) for setting: {setting.name}. This value will be ignored."
                print(warning_string)

                if not allow_all_versions:
                    raise SettingStringError(warning_string)
            else:
                setting.update_current_value(value_index)

        for location in location_table:
            if "Hint Location" in location_table[location].types:
                location_list = world_settings.excluded_hint_locations
            else:
                location_list = world_settings.excluded_locations

            if bits_reader.read(1):
                if location not in location_list:
                    location_list.append(location)
            else:
                if location in location_list:
                    location_list.remove(location)

        startable_items = Counter(STARTABLE_ITEMS)

        for item in startable_items:
            item_count = bits_reader.read(startable_items[item].bit_length())
            world_settings.starting_inventory[item] = item_count

        world_settings.mixed_entrance_pools = [
            list() for _ in range(len(ENTRANCE_TYPES) - 1)
        ]

        for entrance_index, entrance_type in enumerate(ENTRANCE_TYPES):
            pool_index = bits_reader.read(len(ENTRANCE_TYPES).bit_length())

            if pool_index == len(ENTRANCE_TYPES):
                continue

            world_settings.mixed_entrance_pools[pool_index].append(entrance_type)

    return config


def get_bit_length_for_setting(setting: Setting) -> int:
    # -1 to count 0 as a possible value
    return (len(setting.info.options) - 1).bit_length()
