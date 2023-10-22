@tool
extends Control
class_name Map


# child_scene specifies the target that this scene
# will transition into when entered.
@export var child_scene: PackedScene


# interactable_area is the child interaction zone for this node.
#
# When an interaction occurs within this area, the node should act.
@onready var interactable_area: Area2D = $Area2D
# parent references the parent node of a map
@onready var parent: Node = get_parent()


# is_selected allows for a quick toggle of this interactable
# being enabled or disabled.
var is_selected := false
# id of the child
var id: int
# child_id tracks the id given to the child
var child_id: int


func _ready() -> void:
	Messenger.closed_child_map.connect(_on_close_child_map)


func _input(event) -> void:
	if (child_scene != null
	&& is_selected
	&& (event.is_action_pressed("interact") || event.is_action_pressed("zoom_in"))):
		open_child_map()
	
	if id != null && event.is_action("zoom_out"):
		Messenger.closed_child_map.emit(self)


func _on_area_2d_mouse_entered() -> void:
	is_selected = true


func _on_area_2d_mouse_exited() -> void:
	is_selected = false


func _get_configuration_warnings() -> PackedStringArray:
	var warnings = []

	if child_scene && !interactable_area:
		warnings.append("Map's with a child_scene must have an Area2D")

	# Returning an empty array means "no warning".
	return warnings


func _on_close_child_map(child: Map) -> void:
	if child.id != child_id:
		return
	
	child.queue_free()
	
	visible = true


func open_child_map() -> void:
	child_id = ResourceUID.create_id()
	
	var child: Map = child_scene.instantiate()
	child.id = child_id
	parent.add_child(child)
	
	visible = false
