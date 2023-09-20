# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/yaml_files.py

import yaml
from pathlib import Path


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node: yaml.MappingNode, deep=False):
        mapping = set()

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)

            if key in mapping:
                raise ValueError(f"Duplicate {key!r} key found in YAML.")

            mapping.add(key)

        return super().construct_mapping(node, deep)


def yaml_load(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return yaml.load(file, UniqueKeyLoader)


def yaml_write(file_path: Path, data: dict):
    # Change how yaml dumps lists so each element isn't on a separate line.
    yaml.CDumper.add_representer(
        list,
        lambda dumper, data: dumper.represent_sequence(
            "tag:yaml.org,2002:seq", data, flow_style=True
        ),
    )

    # Output integers as hexadecimal.
    yaml.CDumper.add_representer(
        int,
        lambda dumper, data: yaml.ScalarNode("tag:yaml.org,2002:int", f"0x{data:02X}"),
    )

    # Output strings (the offsets) as hexadecimal.
    yaml.CDumper.add_representer(
        str,
        lambda dumper, data: yaml.ScalarNode(
            "tag:yaml.org,2002:int", f"0x{int(data, 16):08X}"
        ),
    )

    with file_path.open("w", encoding="utf-8", newline="") as file:
        file.write(yaml.dump(data, Dumper=yaml.CDumper, line_break="\n"))
