import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants.itemnames import *
from logic.generate import generate
from logic.config import *
from logic.search import all_logic_satisfied
from logic.world import World
from filepathconstants import SPOILER_LOGS_PATH


def config_test(
    config_file_name: str | Path,
    assert_all_locations_reachable: bool = True,
    remove_spoiler: bool = True,
    is_test_config: bool = True,
) -> list[World]:
    config_file_name = Path(config_file_name)

    if is_test_config:
        config_test_path = Path("tests") / "test_configs" / config_file_name
        assert config_test_path.exists()
    else:
        config_test_path = config_file_name

    config = load_config_from_file(config_test_path, allow_rewrite=False)
    write_config_to_file(config_file_name, config)
    worlds = generate(config_file_name)

    if assert_all_locations_reachable:
        assert all_logic_satisfied(worlds)

    config_file_name.unlink()

    if remove_spoiler:
        os.remove(f"{SPOILER_LOGS_PATH}/{worlds[0].config.get_hash()} Spoiler Log.txt")
        os.remove(
            f"{SPOILER_LOGS_PATH}/{worlds[0].config.get_hash()} Anti Spoiler Log.txt"
        )

    return worlds


def test_spoiler_as_config() -> None:
    # Gen first seed
    worlds = config_test("spoiler_as_config.yaml", remove_spoiler=False)
    assert all_logic_satisfied(worlds)
    spoiler_path = f"{SPOILER_LOGS_PATH}/{worlds[0].config.get_hash()} Spoiler Log.txt"
    anti_spoiler_path = (
        f"{SPOILER_LOGS_PATH}/{worlds[0].config.get_hash()} Anti Spoiler Log.txt"
    )
    with open(spoiler_path, "r", encoding="utf-8") as first_log:
        log1 = first_log.read()

    os.remove(spoiler_path)

    # Write log as config for second seed
    with open("spoiler_log_config_test.yaml", "w", encoding="utf-8") as config:
        config.write(log1)

    # Gen second seed
    worlds = config_test(
        "spoiler_log_config_test.yaml", remove_spoiler=False, is_test_config=False
    )
    assert all_logic_satisfied(worlds)

    with open(spoiler_path, encoding="utf-8") as second_log:
        log2 = second_log.read()

    # Output both logs for debugging
    # with open("log1.yaml", "w", encoding="utf-8") as f:
    #     f.write(log1)
    # with open("log2.yaml", "w", encoding="utf-8") as f:
    #     f.write(log2)

    assert log1 == log2

    # Cleanup
    os.remove(spoiler_path)
    os.remove(anti_spoiler_path)


def test_default_empty_config() -> None:
    config_test("default_empty_config.yaml")


def test_default_undefined_config() -> None:
    # This file does not exist intentionally to test that it behaves without it.
    config_file_name = Path("default_undefined_config.yaml")

    config = load_config_from_file(
        config_file_name, create_if_blank=True, allow_rewrite=False
    )
    write_config_to_file(config_file_name, config)
    worlds = generate(config_file_name)
    assert all_logic_satisfied(worlds)
    os.remove(config_file_name)
    return


def test_max_entrance_rando() -> None:
    config_test("max_entrance_rando.yaml")


def test_mixed_pools() -> None:
    config_test("mixed_pools.yaml")


def test_decouple_entrances() -> None:
    config_test("decouple_entrances.yaml")


def test_randomize_dungeon_entrances() -> None:
    config_test("randomize_dungeon_entrances.yaml")


def test_randomize_door_entrances() -> None:
    config_test("randomize_door_entrances.yaml")


def test_randomize_door_entrances_decoupled() -> None:
    config_test("randomize_door_entrances_decoupled.yaml")


def test_randomize_trial_gate_entrances() -> None:
    config_test("randomize_trial_gate_entrances.yaml")


def test_randomize_interior_entrances() -> None:
    config_test("randomize_interior_entrances.yaml")


def test_randomize_overworld_entrances() -> None:
    config_test("randomize_overworld_entrances.yaml")


def test_random_crystals() -> None:
    config_test("random_crystals.yaml")


def test_random_stamina_fruit() -> None:
    config_test("random_stamina_fruit.yaml")


def test_random_shops() -> None:
    config_test("random_shops.yaml")


def test_dungeon_items_vanilla() -> None:
    config_test("dungeon_items_vanilla.yaml")


def test_dungeon_items_own_dungeon() -> None:
    config_test("dungeon_items_own_dungeon.yaml")


def test_dungeon_items_any_dungeon() -> None:
    config_test("dungeon_items_any_dungeon.yaml")


def test_dungeon_items_own_region() -> None:
    config_test("dungeon_items_own_region.yaml")


def test_dungeon_items_overworld() -> None:
    config_test("dungeon_items_overworld.yaml")


def test_dungeon_items_anywhere() -> None:
    config_test("dungeon_items_anywhere.yaml")


def test_dungeon_items_removed() -> None:
    config_test("dungeon_items_removed.yaml")


def test_random_starting_statues() -> None:
    config_test("random_starting_statues.yaml")


def test_random_starting_spawn_bird_statues() -> None:
    config_test("random_starting_spawn_bird_statues.yaml")


def test_random_starting_spawn_any_surface_region() -> None:
    config_test("random_starting_spawn_any_surface_region.yaml")


def test_random_starting_spawn_anywhere() -> None:
    config_test("random_starting_spawn_anywhere.yaml")


def test_open_et_key_pieces_in_eldin() -> None:
    worlds = config_test("open_et_key_pieces_in_eldin.yaml")

    for world in worlds:
        key_piece_count = 0

        for location in world.get_all_item_locations():
            if location.current_item.name == KEY_PIECE:
                assert any(
                    la
                    for la in location.loc_access_list
                    if "Eldin Volcano" in la.area.hint_regions
                    or "Mogma Turf" in la.area.hint_regions
                )
                key_piece_count += 1

        # With default settings, there should always be 5 key pieces.
        # Ensures that all 5 are found and correct.
        assert key_piece_count == 5


def test_fi_hints() -> None:
    config_test("fi_hints.yaml")


def test_gossip_stone_hints() -> None:
    config_test("gossip_stone_hints.yaml")


def test_song_hints_basic() -> None:
    config_test("song_hints_basic.yaml")


def test_song_hints_advanced() -> None:
    config_test("song_hints_advanced.yaml")


def test_impa_sot_hint() -> None:
    config_test("impa_sot_hint.yaml")


def test_all_hints() -> None:
    config_test("all_hints.yaml")


def test_default_multiworld_config() -> None:
    config_test("default_multiworld_config.yaml")


def test_traps_all() -> None:
    worlds = config_test("traps_all.yaml")
    _check_inventory_items_were_placed(worlds)


def test_traps_off() -> None:
    worlds = config_test("traps_off.yaml")
    _check_inventory_items_were_placed(worlds)


def test_beatable_only_config() -> None:
    config_test("beatable_only.yaml")


def test_no_logic_config() -> None:
    config_test("no_logic.yaml")


def test_item_pool_minimal() -> None:
    # The minimal item pool can make the 2 Ancient Harbour Crown and the 2 Pirate Stronghold
    # Pillar rupee checks impossible to reach. And now the Bug Heaven minigame too.
    config_test("item_pool_minimal.yaml", assert_all_locations_reachable=False)


def test_item_pool_extra() -> None:
    config_test("item_pool_extra.yaml")


def test_item_pool_plentiful() -> None:
    config_test("item_pool_plentiful.yaml")


def test_minigame_difficulty_guaranteed_win() -> None:
    # The minigame_difficulty being set to guaranteed_win or easy can make the 2 Bug Heaven
    # minigame check impossible to reach.
    config_test("minigames_guaranteed_win.yaml", assert_all_locations_reachable=False)


def test_minigame_difficulty_easy() -> None:
    # The minigame_difficulty being set to guaranteed_win or easy can make the 2 Bug Heaven
    # minigame check impossible to reach.
    config_test("minigames_easy.yaml", assert_all_locations_reachable=False)


def test_minigame_difficulty_vanilla() -> None:
    config_test("minigames_vanilla.yaml")


def test_minigame_difficulty_hard() -> None:
    config_test("minigames_hard.yaml")


def test_rupee_shuffle_off() -> None:
    config_test("rupee_shuffle_off.yaml")


def test_rupee_shuffle_beginner() -> None:
    config_test("rupee_shuffle_beginner.yaml")


def test_rupee_shuffle_intermediate() -> None:
    config_test("rupee_shuffle_intermediate.yaml")


def test_rupee_shuffle_advanced() -> None:
    config_test("rupee_shuffle_advanced.yaml")


def test_tadtone_shuffle() -> None:
    config_test("random_tadtones.yaml")


def test_bad_starting_inventory() -> None:
    worlds = config_test("starting_inventory_bad.yaml")
    assert (
        len(
            [
                item
                for item in worlds[0].starting_item_pool.elements()
                if item.name == "Progressive Sword"
            ]
        )
        == 0
    )


def test_good_starting_inventory() -> None:
    worlds = config_test("starting_inventory_good.yaml")
    assert (
        len(
            [
                item
                for item in worlds[0].starting_item_pool.elements()
                if item.name == "Progressive Sword"
            ]
        )
        == 2
    )


def _check_inventory_items_were_placed(worlds: list[World]):
    for world in worlds:
        logicless_inventory_items: list[str] = (
            [
                HYLIAN_SHIELD,
                CURSED_MEDAL,
                TREASURE_MEDAL,
                POTION_MEDAL,
                BUG_MEDAL,
                SVT_MAP,
                ET_MAP,
                LMF_MAP,
                AC_MAP,
                SSH_MAP,
                FS_MAP,
                SK_MAP,
            ]
            + [HEART_MEDAL] * 2
            + [RUPEE_MEDAL] * 2
            + [HEART_PIECE] * 24
            + [HEART_CONTAINER] * 6
            + [LIFE_MEDAL] * 2
        )

        for location in world.location_table.values():
            if (
                location.current_item is not None
                and location.current_item.name in logicless_inventory_items
            ):
                logicless_inventory_items.remove(location.current_item.name)

        print(logicless_inventory_items)
        assert len(logicless_inventory_items) == 0
