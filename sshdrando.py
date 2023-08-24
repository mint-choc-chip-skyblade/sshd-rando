from patches.allpatchhandler import AllPatchHandler
from logic.generate import generate


worlds = generate()

patchHandler = AllPatchHandler(worlds[0])
patchHandler.do_all_patches()
