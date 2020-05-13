
class Coin:

    def __init__(self, row, col, player, board):
        """
        initialize one piece on the board
        :param row: horizontal coordinate
        :param col: vertical coordinate
        :param player: the player the coin belong to
        :param board: game board
        """
        self.__data = player
        self.__col = col
        self.__row = row
        self.__neighbors(board) # the coins around

    def __neighbors(self, board):

        self.__right = board[(self.__row, self.__col+1)]
        self.__up_right = board[(self.__row-1, self.__col+1)]
        self.__down_right = board[(self.__row+1, self.__col+1)]
        self.__left = board[(self.__row, self.__col-1)]
        self.__up_left = board[(self.__row-1, self.__col-1)]
        self.__down_left = board[(self.__row+1, self.__col-1)]
        self.__up = board[(self.__row-1, self.__col)]
        self.__down = board[(self.__row+1, self.__col)]

    def __update_right(self, board):
        self.__right = board[(self.__row, self.__col+1)]

    def __update_up_right(self, board):
        self.__up_right = board[(self.__row-1, self.__col+1)]

    def __update_down_right(self, board):
        self.__down_right = board[(self.__row+1, self.__col+1)]

    def __update_left(self, board):
        self.__left = board[(self.__row, self.__col-1)]

    def __update_up_left(self, board):
        self.__up_left = board[(self.__row-1, self.__col-1)]

    def __update_down_left(self, board):
        self.__down_left = board[(self.__row+1, self.__col-1)]

    def __update_up(self, board):
        self.__up = board[(self.__row-1, self.__col)]

    def __update_down(self, board):
        self.__down = board[(self.__row+1, self.__col)]

    def add_to_neighbors_of_the_neighbors(self, board):
        """let the other coins know the new neighbor"""
        if self.__check_neighbor(self.__right):
            self.__right.__update_left(board)
        if self.__check_neighbor(self.__left):
            self.__left.__update_right(board)
        if self.__check_neighbor(self.__down):
            self.__down.__update_up(board)
        if self.__check_neighbor(self.__up):
            self.__up.__update_down(board)
        if self.__check_neighbor(self.__down_left):
            self.__down_left.__update_up_right(board)
        if self.__check_neighbor(self.__up_right):
            self.__up_right.__update_down_left(board)
        if self.__check_neighbor(self.__down_right):
            self.__down_right.__update_up_left(board)
        if self.__check_neighbor(self.__up_left):
            self.__up_left.__update_down_right(board)

    def get_row(self):
        return self.__row

    def get_col(self):
        return self.__col

    def get_data(self):
        return self.__data

    def __check_neighbor(self, neighbor):
        """check if the neighbor is a friend"""
        if neighbor is None:
            return
        if neighbor.get_data() == self.__data:
            return True
        return False

    def __left_sequence(self, sequence):
        if self.__check_neighbor(self.__left):
            sequence.append((self.get_row(), self.__left.get_col()))
            self.__left.__left_sequence(sequence)

    def __right_sequence(self, sequence):
        if self.__check_neighbor(self.__right):
            sequence.append((self.__right.get_row(), self.__right.get_col()))
            self.__right.__right_sequence(sequence)

    def __horizontal_sequence(self):
        right_sequence = list()
        left_sequence = list()
        self.__right_sequence(right_sequence)
        self.__left_sequence(left_sequence)
        horizontal_sequence = right_sequence +\
                              [(self.get_row(), self.__col)] + left_sequence
        return horizontal_sequence

    def __vertical_sequence(self):
        down_sequence = list()
        self.__down_sequence(down_sequence)
        vertical_sequence = [(self.__row, self.__col)] + down_sequence
        return vertical_sequence

    def __down_sequence(self, down_sequence):

        if self.__check_neighbor(self.__down):
            down_sequence.append((self.__down.get_row(),
                                  self.__down.get_col()))

            self.__down.__down_sequence(down_sequence)

    def __up_left_to_down_right_sequence(self):
        up_left_sequence = list()
        down_right_sequence = list()
        self.__up_left_sequence(up_left_sequence)
        self.__down_right_sequence(down_right_sequence)
        up_left_to_down_right_sequence = up_left_sequence + \
                                         down_right_sequence + [(self.__row,
                                                                 self.__col)]
        return up_left_to_down_right_sequence

    def __up_left_sequence(self, up_left_sequence):
        if self.__check_neighbor(self.__up_left):
            up_left_sequence.append((self.__up_left.get_row(),
                                     self.__up_left.get_col()))
            self.__up_left.__up_left_sequence(up_left_sequence)

    def __down_right_sequence(self, down_right_sequence):
        if self.__check_neighbor(self.__down_right):
            down_right_sequence.append((self.__down_right.get_row(),
                                        self.__down_right.get_col()))
            self.__down_right.__down_right_sequence(down_right_sequence)

    def __down_left_to_up_right_sequence(self):
        down_left_sequence = list()
        up_right_sequence = list()
        self.__down_left_sequence(down_left_sequence)
        self.__up_right_sequence(up_right_sequence)
        down_left_to_up_right_sequence = up_right_sequence +\
                                         [(self.__row, self.__col)]\
                                         + down_left_sequence
        return down_left_to_up_right_sequence

    def __down_left_sequence(self, down_left_sequence):
        if self.__check_neighbor(self.__down_left):
            down_left_sequence.append((self.__down_left.get_row(),
                                       self.__down_left.get_col()))
            self.__down_left.__down_left_sequence(down_left_sequence)

    def __up_right_sequence(self, up_right_sequence):
        if self.__check_neighbor(self.__up_right):
            up_right_sequence.append((self.__up_right.get_row(),
                                      self.__up_right.get_col()))
            self.__up_right.__up_right_sequence(up_right_sequence)

    def __sequences_dict(self):
        """dictionary of all sequences that contains the coin"""
        return {'horizontal': self.__horizontal_sequence(), 'vertical':
            self.__vertical_sequence(), 'up_left_to_down_right':
                    self.__up_left_to_down_right_sequence(),
                'down_left_to_up_right':
                    self.__down_left_to_up_right_sequence()}

    def longest_sequence(self):
        """return the longest sequence tht contains the coin"""
        longest, length = None, 0
        for sequence_name, sequence in self.__sequences_dict().items():
            if len(sequence) > length:
                longest, length = sequence_name, len(sequence)
        return self.__sequences_dict()[longest]


class Game:
    WINNING_SEQUENCE = 4
    LOWEST = 5
    HIGHEST_ROW = 0
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    NUM_OF_COLUMNS = 7
    NUM_OF_ROWS = 6
    ILLEGAL_MOVE_EXEPTION = 'Illegal move.'

    def __init__(self):
        self.__winner = None
        self.__total_num_of_coins = 0
        self.__available = list(range(Game.NUM_OF_COLUMNS))  # available columns list
        self.board = self.__empty_board()
        self.__last_coin = None
        self.curr_move = None
        self.winning_seq = None

    def __empty_board(self):
        """create an empty board"""
        board = dict()
        for row in range(-1, Game.NUM_OF_ROWS+1):
            for column in range(-1, Game.NUM_OF_COLUMNS+1):
                board[(row,column)] = None
        return board

    def make_move(self, column):
        """if the given column available put coin in it on the board"""
        player = self.get_current_player()
        if column not in self.__available:
            self.curr_move = None
            raise self.ILLEGAL_MOVE_EXEPTION
        row = Game.LOWEST
        while self.board[(row, column)]:
            row -= 1
        self.__last_coin = Coin(row, column, player, self.board )
        self.board[(row, column)] = self.__last_coin
        self.__last_coin.add_to_neighbors_of_the_neighbors(self.board)
        self.__total_num_of_coins += 1
        if row == Game.HIGHEST_ROW:
            self.__available.remove(column)
        self.curr_move = (row, column)
        return True

    def get_winner(self):
        """return the winner or draw if the game ended, none otherwise"""
        if self.__last_coin:
            self.winning_seq = self.__last_coin.longest_sequence()
        if len(self.__last_coin.longest_sequence()) >= Game.WINNING_SEQUENCE:
                return self.__last_coin.get_data()
        if not self.__available:
            return self.DRAW
        return None

    def get_player_at(self, row, col):
        """return the owner of the coin in given location, none if empty"""
        if self.board[(row,col)]:
            return self.board[(row,col)].get_data()
        return self.board[(row, col)]

    def get_current_player(self):
        if self.__total_num_of_coins % 2:
            return self.PLAYER_TWO
        return self.PLAYER_ONE

    def get_available(self):
        """return thr available columns"""
        return self.__available

