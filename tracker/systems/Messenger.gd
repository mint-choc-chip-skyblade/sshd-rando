extends Node

# Map Transition Zooms
enum Zoom {
	IN = 1,
	OUT = -1
}
signal zoom(direction: Zoom, scene: PackedScene)

# Checks
signal check_toggled(key: String, is_checked: bool)


func _ready():
	check_toggled.connect(_on_check_toggled)


func _on_check_toggled(key: String, is_checked: bool) -> void:
	print_debug(key, is_checked)
