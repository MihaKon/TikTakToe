import sqlite3


def connect_to_db():
    """
    This code fragment is creating a database connection and initializing a database cursor to interact with an
    SQLite database.

    :return cur_t: cursor object
    :return con_t: connection object
    """
    con_t = sqlite3.connect("players.db")
    cur_t = con_t.cursor()
    cur_t.execute("CREATE TABLE IF NOT EXISTS players(name, W, L, D)")
    return cur_t, con_t


def check_player_in_db(name, cur_t, con_t):
    """
    This code fragment is checking whether a player with a given name exists in a database.
    
    :param name: string, name of the player
    :param cur_t: cursor object to DB
    :param con_t: connection object to DB
    """
    result_t = cur_t.execute(f"SELECT name FROM players WHERE name='{name}'")
    if result_t.fetchone():
        print("Name exists")
    else:
        insert_player_into_db(name, cur_t, con_t)


def insert_player_into_db(name, cur_t, con_t):
    """
    This code fragment inserts a new player into the 'players' table in an SQLite database.
    :param name:
    :param cur_t:
    :param con_t:
    """
    cur_t.execute(f"INSERT INTO players VALUES ('{name}',0,0,0)")
    con_t.commit()


def display_db(cur_t):
    """
    Displays content of selected dB.

    :param cur_t: object cursor pointing at dB
    :return:
    """
    for row in cur_t.execute("SELECT * FROM players"):
        print(row)


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
        elif winner == 'O':
            print(player_two_o.upper(), ' WON!')
        else:
            print('DRAW!')


if __name__ == "__main__":
    cur, con = connect_to_db()

    player_one_x = input("Name of the player 1(x): ")
    check_player_in_db(player_one_x, cur, con)
    player_two_o = input("Name of the player 2(0): ")
    check_player_in_db(player_two_o, cur, con)

    players = [(player_one_x, "X"), (player_two_o, "O")]
    play(players)
