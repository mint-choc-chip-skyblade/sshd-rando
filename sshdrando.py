from patches.allpatchhandler import AllPatchHandler
from logic.generate import generate

if __name__ == "__main__":
    worlds = generate("config.yaml")

    patch_handler = AllPatchHandler(worlds[0])
    patch_handler.do_all_patches()
