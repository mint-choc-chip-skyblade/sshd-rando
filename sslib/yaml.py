# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/yaml_files.py

import yaml
from pathlib import Path


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate {key!r} key found in YAML.")
            mapping.add(key)
        return super().construct_mapping(node, deep)


def yaml_load(filePath: Path):
    with filePath.open("r", encoding="utf-8") as file:
        return yaml.load(file, UniqueKeyLoader)
