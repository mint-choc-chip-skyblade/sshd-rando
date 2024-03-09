extends Node


@onready var current_scene: Node = $CurrentScene


var zoom_stack: Array[Node] = []


func _ready() -> void:
	Messenger.zoom.connect(_on_zoom)


func _on_zoom(direction: Messenger.Zoom, scene: Node) -> void:
	match direction:
		Messenger.Zoom.IN:
			var current = current_scene.get_child(0)
			current_scene.remove_child(current)
			zoom_stack.push_back(current)
			
			current_scene.add_child(scene)
		Messenger.Zoom.OUT:
			if zoom_stack.size() == 0:
				return
			
			current_scene.get_child(0).queue_free()
			var prev_scene = zoom_stack.pop_back()
			current_scene.add_child(prev_scene)


func _input(event: InputEvent) -> void:
	if event.is_action_released("zoom_out"):
		_on_zoom(Messenger.Zoom.OUT, null)
