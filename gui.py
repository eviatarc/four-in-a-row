import tkinter as tki
import game
import communicator as commu
import ai
import random

class Graphic:

    NUM_DIGITS = 10
    NOT_CONNECTED = 'not connected'
    CONNECTED = 'connected'
    COLOR_OF_BUTTONS = 'deep pink'
    WIDTH_BUTTONS = 8
    BD_BUTTONS = 10
    UPPER_FRAME_WIDTH = 200
    UPPER_FRAME_HEIGHT = 50
    CONNECTED_COLOR = 'green'
    DISCONNECTED_COLOR = 'red'
    NUM_ROWS = 6
    NUM_COLS = 7
    NUM_OF_CELLS = 42
    AI_STR = 'ai'


    def __init__(self, is_human ,root, port, ip=None):
        """constructor for object from this class"""
        self.root = root
        self.game = game.Game()
        self.Ai = None
        if is_human == self.AI_STR:
            self.Ai = ai.AI()
        self.upper_frame = tki.Frame(self.root,
                                     width=self.UPPER_FRAME_WIDTH,
                                     height=self.UPPER_FRAME_HEIGHT)
        self.upper_frame.pack()

        self.my_can = tki.Canvas(self.root)
        self.my_can.pack()
        self.get_ready_widgets()

        self.communicator = None
        self.player = None
        self.get_ready_commu(port, ip)

        self.is_connect(self.communicator.is_connected())
        if self.player != self.game.get_current_player():
            self.disable_buttons()
        if self.Ai and self.player == self.game.PLAYER_ONE:
            # in case the PLAYER_ONE (that is the first to play)
            # is ai
            self.Ai.find_legal_move(self.game, self.add_coin_image)

    def start_running(self):
        self.root.mainloop()

    def get_ready_widgets(self):
        """a function that place the widgets in the frames"""
        self.connection_frame = tki.Frame(self.upper_frame)
        self.connection_frame.pack()
        self.not_connected_lbl = tki.Label(self.connection_frame, text=
        self.NOT_CONNECTED,bg = self.DISCONNECTED_COLOR)
        self.connected_lbl =  tki.Label(self.connection_frame, text=
        self.CONNECTED,bg = self.CONNECTED_COLOR)
        self.not_connected_lbl.grid(row = 0)
        self.buttons_frame = tki.Frame(self.upper_frame)
        self.buttons_frame.pack()
        self.diff_image = tki.PhotoImage(file='tiger_backgroung.png')
        self.player1coin_image = tki.PhotoImage(file ='red_mon_devorse.png')
        self.player1win = tki.PhotoImage(file ='red_mon_win.png')
        self.player2coin_image = tki.PhotoImage(file ='blu_mon_devorse.png')
        self.player2win = tki.PhotoImage(file ='blu_mon_win.png')
        self.player1_show_win = tki.PhotoImage(file =
                                               'red_win_window_new.png')
        self.player2_show_win = tki.PhotoImage(file =
                                               'blu_win_window_new.png')
        self.draw_img = tki.PhotoImage(file='no-winners.png')

        self.button_list = []
        self.create_buttons()
        self.give_buttons_meaning()
        self.image_dict = {}
        self.start_dict()

    def create_buttons(self):
        """once called function - this function create the button widgets
        in the buttons frame"""
        for i in range(self.game.NUM_OF_COLUMNS):
            curr_button = tki.Button(self.buttons_frame,
                                     bg = self.COLOR_OF_BUTTONS,
                                     bd = self.BD_BUTTONS,
                                     width = self.WIDTH_BUTTONS)
            self.button_list.append(curr_button)
            curr_button.grid(row=0, column = i)

    def do_we_have_winner(self):
        """function that recieves from the game"""
        if self.game.get_winner() is not None:
            return True
        return False

    def able_buttons(self):
        self.give_buttons_meaning()

    def disable_buttons(self):
        for button in self.button_list:
            button.unbind("<Button-1>")

    def finish_game(self):
        """a function that disabeled the buttons when the game is finished"""
        for each in self.game.winning_seq:
            self.winning_update_each(each)
        self.disable_buttons()

    def is_connect(self,connection_status = False):
        """change color of the top of the framne when got connection"""
        if connection_status:
            self.not_connected_lbl.grid_forget()
            self.connected_lbl.grid(row=0)
        else:
            self.connected_lbl.grid_forget()
            self.not_connected_lbl.grid(row=0)

    def show_winner(self):
        """show the winner window when a winner or a draw is declared"""
        if self.game.get_winner() == self.game.PLAYER_ONE:
            winning = tki.Label(self.root, image=self.player1_show_win)
            winning.pack()
        elif self.game.get_winner() == self.game.PLAYER_TWO:
            winning = tki.Label(self.root, image=self.player2_show_win)
            winning.pack()
        else:
            winning = tki.Label(self.root, image=self.draw_img)
            winning.pack()

    def add_coin_image(self,column_clicked):
        """function that help the update board communicate with the game"""
        self.is_connect(self.communicator.is_connected())
        column_clicked = int(column_clicked)
        if self.player == self.game.get_current_player():
            if self.game.make_move(column_clicked):
                self.improved_update()
                self.send_msg(column_clicked)
                self.disable_buttons()
        else:
            self.game.make_move(column_clicked)
            self.improved_update()
            self.able_buttons()
            if self.Ai and len(self.game.get_available()) != 0 and \
                    self.game.get_winner() is None:
                self.Ai.find_legal_move(self.game, self.add_coin_image)

        if self.do_we_have_winner():
            self.show_winner()
            self.finish_game()


    def give_buttons_meaning(self):
        """a function that give the created buttons meaning by clicking"""
        button_zero = self.button_list[0]
        button_zero.bind("<Button-1>", lambda event:
        self.add_coin_image(0))
        button_one = self.button_list[1]
        button_one.bind("<Button-1>", lambda event:
        self.add_coin_image(1))
        button_two = self.button_list[2]
        button_two.bind("<Button-1>", lambda event:
        self.add_coin_image(2))
        button_three = self.button_list[3]
        button_three.bind("<Button-1>", lambda event:
        self.add_coin_image(3))
        button_four = self.button_list[4]
        button_four.bind("<Button-1>", lambda event:
        self.add_coin_image(4))
        button_five = self.button_list[5]
        button_five.bind("<Button-1>", lambda event:
        self.add_coin_image(5))
        button_six = self.button_list[6]
        button_six.bind("<Button-1>", lambda event:
        self.add_coin_image(6))

    def start_dict(self):
        """a function that start the dictionary of the cells in the board"""
        for i in range(self.NUM_OF_CELLS):
            curr = tki.Label(self.my_can, image=self.diff_image)
            curr.photo = self.diff_image
            self.image_dict[(i % self.NUM_ROWS, i % self.NUM_COLS)] = curr
            curr.grid(row=i % self.NUM_ROWS, column=i % self.NUM_COLS)

    def improved_update(self):
        """update the board when make lagel move"""
        new_tuple = self.game.curr_move
        if new_tuple is None:
            return
        curr_player_afetr_game_move_beore_gui = abs(
            self.game.get_current_player()-1)
        if curr_player_afetr_game_move_beore_gui == self.game.PLAYER_ONE:
            new_image = self.player1coin_image
        elif curr_player_afetr_game_move_beore_gui == self.game.PLAYER_TWO:
            new_image = self.player2coin_image
        curr = tki.Label(self.my_can,image=new_image)
        curr.photo = new_image
        self.image_dict[new_tuple] = [curr]
        curr.grid(row=new_tuple[0], column=new_tuple[1])

    def winning_update_each(self, where):
        """a function that update each cell of the winning player in a
        relevant image"""
        if self.game.get_winner() == self.game.PLAYER_ONE:
            new_image = self.player1win
        elif self.game.get_winner() == self.game.PLAYER_TWO:
            new_image = self.player2win
        elif self.game.get_winner() == self.game.DRAW:
            return
        curr = tki.Label(self.my_can,image=new_image)
        curr.photo = new_image
        self.image_dict[where] = [curr]
        curr.grid(row = where[0],column = where[1])

    def get_ready_commu(self,port, ip=None):
        """set the communicator and players"""
        if ip:
            self.communicator = commu.Communicator(self.root, port, ip)
            self.player = game.Game.PLAYER_TWO
        else:
            self.communicator = commu.Communicator(self.root, port)
            self.player = game.Game.PLAYER_ONE
        self.communicator.connect()
        self.communicator.bind_action_to_message(self.add_coin_image)

    def send_msg(self,rel_col):
        """a function that sends the massage to the other player after
        doing the move"""
        now_send_this_msg = int(rel_col)
        self.communicator.send_message(now_send_this_msg)