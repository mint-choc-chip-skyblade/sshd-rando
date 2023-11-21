from logic.generate import generate
from patches.allpatchhandler import AllPatchHandler


def randomize():
    worlds = generate("config.yaml")

    patch_handler = AllPatchHandler(worlds[0])
    patch_handler.do_all_patches()
