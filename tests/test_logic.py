import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic.generate import generate
from logic.config import *
from logic.search import all_locations_reachable
from logic.world import World

def config_test(config_file_name: str) -> list[World]:
    assert os.path.exists(f"tests/test_configs/{config_file_name}")
    config = load_config_from_file(f"tests/test_configs/{config_file_name}", allow_rewrite=False)
    write_config_to_file(config_file_name, config)
    worlds = generate(config_file_name)
    assert all_locations_reachable(worlds)
    os.remove(config_file_name)
    return worlds

def test_default_config() -> None:
    config_test("default_config.yaml")

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

def test_default_multiworld_config() -> None:
    config_test("default_multiworld_config.yaml")