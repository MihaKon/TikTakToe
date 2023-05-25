import sqlite3


class Player:
    def __init__(self, name):
        self.conn, self.cur = None, None
        self.name = name
        self.connect_to_db()
        self.check_player_in_db()

    def connect_to_db(self):
        """
        This code fragment is creating a database connection and initializing a database cursor to interact with an
        SQLite database.
        """
        self.conn = sqlite3.connect("players.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS players(name, W, L, D)")

    def insert_player_into_db(self):
        """
        This code fragment inserts a new player into the 'players' table in an SQLite database.
        """
        self.cur.execute(f"INSERT INTO players VALUES ('{self.name}',0,0,0)")
        self.conn.commit()

    def check_player_in_db(self):
        """
        Checks whether a player with a given name exists in a database.
        """
        result_t = self.cur.execute(f"SELECT name FROM players WHERE name='{self.name}'")
        if result_t.fetchone():
            print("Name exists")
        else:
            Player.insert_player_into_db(self)
            print("Player created")

    def display_db(self):
        """
        Displays content of selected dB.
        """
        for row in self.cur.execute(f"SELECT * FROM players WHERE name ='{self.name}'"):
            print(row)

    def uddate_player_score_in_db(self, letter):
        """
        Increment score by one in selected table.
        :param letter: W - Wins | L - Loses | D - Draws
        """
        self.cur.execute(f"UPDATE players SET {letter} = {letter}+1 WHERE name='{self.name}'")
        self.conn.commit()


def check_board_horizontal(board):
    """
    Checks current state of playing board horizontally.

    :param board: Current state of playing board
    """
    for i in range(0, 8, 3):
        if board[i] == board[i + 1] == board[i + 2]:
            return board[i]


def check_board_vertical(board):
    """
    Checks current state of playing board vertically.

    :param board: Current state of playing board
    :return board[i]: sign X or O of the winner from wining line
    """
    for i in range(0, 2):
        if board[i] == board[i + 3] == board[i + 6]:
            return board[i]


def check_board_across(board):
    """
    Checks current state of playing board across.

    :param board: Current state of playing board
    :return board[i]: sign X or O of the winner from wining line
    """
    if board[0] == board[4] == board[8]:
        return board[0]
    if board[2] == board[4] == board[6]:
        return board[2]


def get_winner(board):
    """
    Checks which line won

    :param board: Current state of playing board
    :return h/v/a_check: Returns sign of,a wiener. If all fields are taken and no winner was found,
    returns 'DRAW!'.
    """
    if horizontal_check := check_board_horizontal(board):
        return horizontal_check

    if vertical_check := check_board_vertical(board):
        return vertical_check

    if across_check := check_board_across(board):
        return across_check

    return 'DRAW'


def is_game_finished(board):
    """
    Checks if the game has finished based on the current state of the board.

    :param board: Current state of playing board
    :return: boolean denoting whether the game is finished
    """
    winner_found = get_winner(board)
    if winner_found != 'DRAW':
        return True
    return all([number != board_entry for number, board_entry in zip(range(1, 10), board)])


def check_user_input(name, board):
    """
    Checks users input.

    :param name: players name
    :param board: current state of the playing board
    :return num-1: number to table which, sign has to be write down
    """
    while True:
        try:
            num = int(input(name + ": "))
            if 0 < num < 10 and isinstance((board[num - 1]), int):
                return num - 1
            else:
                print("Wrong number!")
        except ValueError:
            print("Wrong input!")


def get_playing_board(board):
    """
    Displays current state of the playing board.

    :param board: current state of playing board
    """
    print(board[0], '|', board[1], '|', board[2])
    print('-', '+', '-', '+', '-')
    print(board[3], '|', board[4], '|', board[5])
    print('-', '+', '-', '+', '-')
    print(board[6], '|', board[7], '|', board[8])


def get_clear_board():
    """
    :return: Array [1-9]
    """
    return [*range(1, 10)]


def play(players_t):
    """
    This function appears to be implementing the gameplay of a tic-tac-toe game. 

    :param players_t: [NAME_OF_THE_PLAYER_ONE, HIS_SIGN, NAME_OF_THE_PLAYER_TWO, HIS_SIGN,]
    """
    while True:
        playing_board = get_clear_board()
        turn = 0

        while not is_game_finished(playing_board):
            current_player, marker = players_t[turn % len(players_t)]
            get_playing_board(playing_board)
            val = check_user_input(current_player, playing_board)
            playing_board[val] = marker
            turn += 1

        winner = get_winner(playing_board)
        if winner == 'X':
            print(player_one_x.upper(), ' WON!')
            player_one.uddate_player_score_in_db('W')
            player_two.uddate_player_score_in_db('L')
        elif winner == 'O':
            print(player_two_o.upper(), ' WON!')
            player_one.uddate_player_score_in_db('L')
            player_two.uddate_player_score_in_db('W')
        else:
            print('DRAW!')
            player_one.uddate_player_score_in_db('D')
            player_two.uddate_player_score_in_db('D')

        player_one.display_db()
        player_two.display_db()


if __name__ == "__main__":
    player_one_x = input("Name of the player 1(x): ")
    player_one = Player(player_one_x)
    player_two_o = input("Name of the player 2(0): ")
    player_two = Player(player_two_o)
    players = [(player_one_x, "X"), (player_two_o, "O")]
    play(players)
