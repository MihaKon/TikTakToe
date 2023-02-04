import sqlite3


def connect_to_db():
    con = sqlite3.connect("players.db")
    cur_t = con.cursor()
    cur_t.execute("CREATE TABLE IF NOT EXISTS players(name, W, L, D)")
    return cur_t


def check_player_in_db(name, cur_t):
    result = cur_t.execute(f"SELECT name FROM players WHERE name='{name}'")
    if result.fetchone() is None:
        insert_player_into_db(name, cur_t)
    else:
        print(result.fetchone())


def insert_player_into_db(name, cur_t):
    cur_t.execute(f"INSERT INTO players VALUES ('{name}',0,0,0)")


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
    This function appears to be implementing the gameplay of a tic-tac-toe game. The game is played on a playing
    board represented by a list, which is initialized with a clear board (presumably all entries are empty) in each
    iteration of the outer while loop. The game is played by two players, and the turn of each player is tracked by
    the turn variable, which is incremented at the end of each player's turn. The players are stored in a list
    players_t, and the current player is selected using the turn % len(players_t) expression. In each turn,
    the function first retrieves the current playing board, then calls the check_user_input function to get the move
    of the current player. The selected position on the board is then marked with the current player's marker,
    either 'X' or 'O', which is stored in the marker variable. The game continues until the is_game_finished function
    returns True, which indicates that either one of the players has won or the game has ended in a draw. At the end
    of the game, the winner is determined by calling the get_winner function and is reported to the user with a
    message. If the winner is 'X', the message reports that player one, represented by the player_one_x variable,
    has won. If the winner is 'O', the message reports that player two, represented by the player_two_o variable,
    has won. If the winner is neither 'X' nor 'O', the message reports a draw.

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
    cur = connect_to_db()
    player_one_x = input("Name of the player 1(x): ")
    check_player_in_db(player_one_x, cur)
    player_two_o = input("Name of the player 2(0): ")
    check_player_in_db(player_two_o, cur)

    players = [(player_one_x, "X"), (player_two_o, "O")]
    play(players)
