from constants.verificationconstants import *
from filepathconstants import CONFIG_PATH
from logic.generate import generate
from patches.allpatchhandler import AllPatchHandler
from randomizer.verify_extract import verify_extract


def randomize():
    verify_extract()
    worlds = generate(CONFIG_PATH)

    patch_handler = AllPatchHandler(worlds[0])
    patch_handler.do_all_patches()
