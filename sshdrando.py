from patches.allpatchhandler import AllPatchHandler
from logic.generate import generate

worlds = generate()

# for location in worlds[0].location_table.values():
#     item_name = f"{location.current_item}"
#     location_name = location.name
#     # Patch item into location

patchHandler = AllPatchHandler(worlds[0])
patchHandler.do_all_patches()
