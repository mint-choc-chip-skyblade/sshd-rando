import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic.generate import generate
from logic.config import *
from logic.search import all_locations_reachable
from logic.world import World


def config_test(config_file_name: str | Path) -> list[World]:
    config_file_name = Path(config_file_name)

    config_test_path = Path("tests") / "test_configs" / config_file_name
    assert config_test_path.exists()

    config = load_config_from_file(config_test_path, allow_rewrite=False)
    write_config_to_file(config_file_name, config)
    worlds = generate(config_file_name)
    assert all_locations_reachable(worlds)
    config_file_name.unlink()
    return worlds


def test_default_config() -> None:
    config_test("default_config.yaml")


def test_random_crystals() -> None:
    config_test("random_crystals.yaml")


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


def test_random_starting_spawn_bird_statues() -> None:
    config_test("random_starting_spawn_bird_statues.yaml")


def test_random_starting_spawn_any_surface_region() -> None:
    config_test("random_starting_spawn_any_surface_region.yaml")


def test_random_starting_spawn_anywhere() -> None:
    config_test("random_starting_spawn_anywhere.yaml")


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


def test_decouple_entrances() -> None:
    config_test("decouple_entrances.yaml")


def test_mixed_pools() -> None:
    config_test("mixed_pools.yaml")


def test_max_entrance_rando() -> None:
    config_test("max_entrance_rando.yaml")


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


def test_spoiler_as_config() -> None:
    config_test("spoiler_as_config.yaml")
    log1 = ""
    with open("Spoiler Log.txt", "r") as first_log:
        log1 = first_log.read()

    os.remove("Spoiler Log.txt")

    with open("config.yaml", "w") as config:
        config.write(log1)
        worlds = generate(Path("config.yaml"))
        assert all_locations_reachable(worlds)

    with open("Spoiler Log.txt") as second_log:
        assert log1 == second_log.read()
