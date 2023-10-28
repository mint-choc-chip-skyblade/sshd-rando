extends Node

var ARGS := {
	"seed": ""
}

func _ready() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.find("=") > -1:
			var key_value = argument.split("=")
			ARGS[key_value[0].lstrip("--")] = key_value[1]
		else:
			# Options without an argument will be present in the dictionary,
			# with the value set to an empty string.
			ARGS[argument.lstrip("--")] = ""
	
	print_debug("cmdline args: \n", ARGS)
