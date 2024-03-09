extends Node

enum Zoom {
	IN = 1,
	OUT = -1
}

signal zoom(direction: Zoom, scene: PackedScene)
