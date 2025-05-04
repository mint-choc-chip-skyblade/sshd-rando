import os
from util.arguments import get_program_args

args = get_program_args()

if args.debug:
    os.system("sshdrando.py --nogui --debug")
else:
    os.system("sshdrando.py --nogui ")
