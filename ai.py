import random


class AI:
    NO_POSSIBLE_COL_EXEPTION = "‫‪No‬‬ ‫‪possible‬‬ ‫‪AI‬‬ ‫‪moves.‬"

    def __init__(self):
        pass

    def find_legal_move(self, g, func, timeout=None):
        """assuming we use this function only if the board is not full,
        if it is so we stop the game before wer got here"""
        if len(g.get_available()) == 0:
            raise self.NO_POSSIBLE_COL_EXEPTION
        else:
            random_col = random.choice(g.get_available())
            func(random_col)