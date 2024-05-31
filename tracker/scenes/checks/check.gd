extends Button
class_name Check

# key is the check name as it appears in the logic
@export var key: String = ""
# label is the UI friendly version of the key.
# If unset, the key will be used instead
@export var label: String = ""
# texture is the icon shown to the user
@export var texture: Texture2D

# sprite is automatically set on ready
@onready var image: TextureRect = $TextureRect

# is_checked tracks whether this has been checked or not
var is_checked = false


func _ready() -> void:
	image.texture = texture


func _on_pressed() -> void:
	is_checked = !is_checked
	Messenger.check_toggled.emit(key, is_checked)
