extends Node


@onready var current_scene: Node = $CurrentScene


func _ready() -> void:
	Messenger.transition_scene.connect(_on_transition_root_scene)


func _on_transition_root_scene(scene: PackedScene) -> void:
	var next_scene := scene.instantiate()
	var prev_scene := current_scene.get_child(0)
	if prev_scene:
		prev_scene.queue_free()
	
	current_scene.add_child(next_scene)
	Messenger.transitioned_scene.emit()
