import os
import sys
from util.arguments import get_program_args

args = get_program_args()

command = "sshdrando.py --nogui"

if sys.platform == "linux":
    command = "python3 " + command

if args.debug:
    command += " --debug"

os.system(command)
