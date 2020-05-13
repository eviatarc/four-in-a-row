import sys
import communicator as c
from game import Game
from gui import Graphic as gu
import ai
import tkinter as tki

PLAYER_ONE_NUM_OF_ARGS = 3
PLAYER_TOW_NUM_OF_ARGS = 4
MAX_PORT = 65535
ARGS_ERROR_MESSAGE = "‫‪Illegal‬‬ ‫‪program‬‬ ‫‪arguments."
IS_HUMAN_IND = 1
PORT_IND = 2
IP_IND = 3
IS_HUMAN = None
HUMAN_STR = 'human'
AI_STR = 'ai'


def check_args(args):
    if len(args) != PLAYER_ONE_NUM_OF_ARGS and len(args) != PLAYER_TOW_NUM_OF_ARGS:
        return False
    if not is_arg_one_valid(args):
        return False
    if args[PORT_IND] > MAX_PORT:
        return False
    return True

def is_arg_one_valid(args):
    if args[IS_HUMAN_IND] == HUMAN_STR or args[IS_HUMAN_IND] == AI_STR:
        return True
    return False

def main(args):
    args[PORT_IND] = int(args[PORT_IND])
    if not check_args(args):
        print(ARGS_ERROR_MESSAGE)
        return
    root = tki.Tk()
    if len(args) == PLAYER_ONE_NUM_OF_ARGS:
        single_game = gu(args[1], root, args[PORT_IND])
    elif len(args) == PLAYER_TOW_NUM_OF_ARGS:
        single_game = gu(args[1], root, args[PORT_IND], args[IP_IND])
    single_game.start_running()

if __name__ == '__main__':
    main(sys.argv)
