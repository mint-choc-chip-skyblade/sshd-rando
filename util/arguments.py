import argparse


def get_program_args():

    parser = argparse.ArgumentParser(
        description="A randomizer for The Legend of Zelda: Skyward Sword HD."
    )

    parser.add_argument(
        "--with-gui",
        dest="with_gui",
        action="store_true",
        help="Runs the randomizer through a gui.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Generates a debug log when running the rando.",
    )

    # parser.print_help()
    args = parser.parse_args()

    return args
