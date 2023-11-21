from filepathconstants import CONFIG_PATH
from logic.generate import generate
from patches.allpatchhandler import AllPatchHandler


def randomize():
    worlds = generate(CONFIG_PATH)

    patch_handler = AllPatchHandler(worlds[0])
    patch_handler.do_all_patches()
