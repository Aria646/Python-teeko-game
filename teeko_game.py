# DO NOT modify or add any import statements
from support import *

# Name: Chenzhao Zhu
# Favorite Tree: cherry blossom tree
# -----------------------------------------------------------------------------

# Define your classes and functions here


# def main() -> None:    pass

# if __name__ == "__main__": main()

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# GAME CONSTANTS
# -----------------------------------------------------------------------------

EMPTY = "\U000025CB"
PLAYER_1_PIECE = '\U000025CD'
PLAYER_2_PIECE = '\U000025CF'

BOARD_SIZE = 5
NUM_PLAYER_PIECES = 4
WIN_LENGTH = NUM_PLAYER_PIECES

HELP_COMMAND = "h"
QUIT_COMMAND = "q"
PLACE_COMMAND = "p"
MOVE_COMMAND = "m"

PLAYER_1_DISPLAY = "Player 1"
PLAYER_2_DISPLAY = "Player 2"
WELCOME_MESSAGE = "Welcome to Teeko!"
INVALID_FORMAT_MESSAGE = "Invalid command. Enter 'h' for valid command format or 'q' to quit"
ENTER_COMMAND_PROMPT = "Please enter your command (h to see valid command): "
MOVE_MESSAGE = "'s turn to move"
PLACE_MESSAGE = "'s pieces to place: "
MUST_PLACE_MESSAGE = "First, you have to place all your pieces on the board!"
ALREADY_PLACED_MESSAGE = "You have already placed all your pieces on the board!"
INVALID_PLACEMENT_MESSAGE = "That position is not valid!"
INVALID_MOVEMENT_MESSAGE = "That movement is not valid!"
HELP_MESSAGE = """Valid Commands: 
    pXY   - Place a piece at row X, column Y (e.g., p34 places a piece at row 3, column 4)
    mXYUV - Move a piece from position (X,Y) to (U,V) (e.g., m3425 moves from 3,4 to 2,5)
    h     - Show this help message
    q     - Quit the game"""
VICTORY_MESSAGE = " wins!"
AGAIN_PROMPT = "Would you like to play again? (y/n): "


def turn_message(num_pieces: int) -> str:
    """
    Returns the appropriate prompting message based on remaining pieces.

    Args:
        num_pieces (int): The number of pieces the current player has left to 
                          place.

    Returns:
        str: A message prompting the player to place or move a piece.
    """
    if num_pieces:
        message = PLACE_MESSAGE + str(num_pieces)
    else:
        message = MOVE_MESSAGE
    return message


"""
A text-based implementation of the board game Teeko.

This script allows two players to play Teeko via the command line. The game
involves a placement phase and a movement phase, with the goal of getting four
of one's own pieces in a line or a 2x2 square.
"""


def num_hours():
    """Returns the estimated number of hours spent on the project."""
    return 18.0


def create_empty_board(board_size: int) -> list[list[str]]:
    """Generates a square, empty board of a given size."""
    board = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            row.append(EMPTY)
        board.append(row)
    return board


def display_board(board: list[list[str]]) -> None:
    """Prints the given game state with blank lines after every row."""
    space = " "
    board_size = len(board)
    for row_seq in range(board_size):
        print(space * 2 + str(row_seq + 1), end="")
    print()

    col_seq = 1
    for row in board:
        print(str(col_seq) + space + (space * 2).join(row))
        print()
        col_seq += 1


def add_piece(board: list[list[str]], piece: str, pos: tuple[int, int]) -> bool:
    """Adds a piece to the board at a given 1-indexed position."""
    if board[pos[0] - 1][pos[1] - 1] == EMPTY:
        board[pos[0] - 1][pos[1] - 1] = piece
        return True
    else:
        print(INVALID_PLACEMENT_MESSAGE)
        return False


def move_piece(
        board: list[list[str]],
        piece: str,
        current_pos: tuple[int, int],
        target_pos: tuple[int, int]) -> bool:
    """Moves a piece from a current position to a target position."""
    current_piece = board[current_pos[0] - 1][current_pos[1] - 1]
    target_piece = board[target_pos[0] - 1][target_pos[1] - 1]

    row_delta = abs(current_pos[0] - target_pos[0])
    col_delta = abs(current_pos[1] - target_pos[1])
    if_adjacent = (
            row_delta <= 1 and col_delta <= 1 and (
            row_delta + col_delta > 0))

    if current_piece != piece or target_piece != EMPTY or if_adjacent is False:
        print(INVALID_MOVEMENT_MESSAGE)
        return False
    else:
        board[target_pos[0] - 1][target_pos[1] - 1] = piece
        board[current_pos[0] - 1][current_pos[1] - 1] = EMPTY
        return True


def _is_single_digit_int(s: str) -> bool:
    """Helper function to check if a character is a valid board coordinate."""
    if (len(s) == 1 and
            s.isdigit() and
            int(s) - 1 in range(BOARD_SIZE)
            ):
        return True
    else:
        return False


def check_input(command: str) -> bool:
    """Validates the format of a user's command string."""
    command = command.lower()

    if len(command) == 0:
        return False
    elif command in (HELP_COMMAND, QUIT_COMMAND):
        return True
    elif command[0] in (PLACE_COMMAND):
        if (len(command) == 3 and
                _is_single_digit_int(command[1]) and
                _is_single_digit_int(command[2])):
            return True
        else:
            return False
    elif command[0] in (MOVE_COMMAND):
        if (len(command) == 5 and
                _is_single_digit_int(command[1]) and
                _is_single_digit_int(command[2]) and
                _is_single_digit_int(command[3]) and
                _is_single_digit_int(command[4])):
            return True
        else:
            return False
    else:
        return False


def get_command() -> str:
    """Repeatedly prompts the user until a validly formatted command is entered."""
    got_valid_prompt = False
    while not got_valid_prompt:
        prompt = input(ENTER_COMMAND_PROMPT)
        if check_input(prompt):
            return prompt.lower()
        else:
            print(INVALID_FORMAT_MESSAGE)


def has_unbroken_line(board: list[list[str]], piece: str) -> bool:
    """Checks for a winning line of four pieces."""
    num_rows = len(board)
    num_cols = len(board[0])

    for i in range(num_rows):
        for j in range(num_cols - WIN_LENGTH + 1):
            if (board[i][j] == piece and
                    board[i][j + 1] == piece and
                    board[i][j + 2] == piece and
                    board[i][j + 3] == piece):
                return True
    for i in range(num_rows - WIN_LENGTH + 1):
        for j in range(num_cols):
            if (board[i][j] == piece and
                    board[i + 1][j] == piece and
                    board[i + 2][j] == piece and
                    board[i + 3][j] == piece):
                return True

    for i in range(num_rows - WIN_LENGTH + 1):
        for j in range(num_cols - WIN_LENGTH + 1):
            if (board[i][j] == piece and
                    board[i + 1][j + 1] == piece and
                    board[i + 2][j + 2] == piece and
                    board[i + 3][j + 3] == piece):
                return True
    for i in range(num_rows - WIN_LENGTH + 1):
        for j in range(num_cols - WIN_LENGTH + 1):
            j1 = j + WIN_LENGTH - 1
            if (board[i][j1] == piece and
                    board[i + 1][j1 - 1] == piece and
                    board[i + 2][j1 - 2] == piece and
                    board[i + 3][j1 - 3] == piece):
                return True
    return False


def has_square(board: list[list[str]], piece: str) -> bool:
    """Checks for a winning 2x2 square of four pieces."""
    num_rows = len(board)
    num_cols = len(board[0])
    for i in range(num_rows - 1):
        for j in range(num_cols - 1):
            if (board[i][j] == piece and
                    board[i][j + 1] == piece and
                    board[i + 1][j] == piece and
                    board[i + 1][j + 1] == piece):
                return True
    return False


def check_win(board: list[list[str]]) -> str:
    """Checks if either player has won the game. Player 1 has precedence."""
    P1 = PLAYER_1_PIECE
    P2 = PLAYER_2_PIECE
    if has_unbroken_line(board, P1) or has_square(board, P1):
        return P1
    elif has_unbroken_line(board, P2) or has_square(board, P2):
        return P2
    else:
        return EMPTY


def play_game() -> None:
    """Coordinates a single game of Teeko from start to finish."""
    board = create_empty_board(BOARD_SIZE)
    pieces_to_place = [NUM_PLAYER_PIECES, NUM_PLAYER_PIECES]
    play_seq = 0
    players = [
        (PLAYER_1_PIECE, PLAYER_1_DISPLAY),
        (PLAYER_2_PIECE, PLAYER_2_DISPLAY)
    ]
    
    print(WELCOME_MESSAGE)

    while True:
        print()
        display_board(board)
        current_piece, current_display = players[play_seq]

        while True:
            remaining_pieces = pieces_to_place[play_seq]
            print(current_display + turn_message(remaining_pieces))
            command = get_command()

            if command == HELP_COMMAND:
                print(HELP_MESSAGE)
                print()
                continue

            if command == QUIT_COMMAND:
                return

            turn_successful = False
            if command[0] == PLACE_COMMAND:
                if remaining_pieces == 0:
                    print(ALREADY_PLACED_MESSAGE)
                    print()
                else:
                    pos = (int(command[1]), int(command[2]))
                    if add_piece(board, current_piece, pos):
                        pieces_to_place[play_seq] -= 1
                        turn_successful = True
                    else:
                        print()

            elif command[0] == MOVE_COMMAND:
                if remaining_pieces > 0:
                    print(MUST_PLACE_MESSAGE)
                    print()
                else:
                    current_pos = (int(command[1]), int(command[2]))
                    target_pos = (int(command[3]), int(command[4]))
                    if move_piece(board, current_piece, current_pos,
                                  target_pos):
                        turn_successful = True
                    else:
                        print()

            if turn_successful:
                break

        winner_piece = check_win(board)
        if winner_piece != EMPTY:
            print()
            display_board(board)
            if winner_piece == PLAYER_1_PIECE:
                winner_display = PLAYER_1_DISPLAY
            elif winner_piece == PLAYER_2_PIECE:
                winner_display = PLAYER_2_DISPLAY

            print(winner_display + VICTORY_MESSAGE)
            break

        play_seq = 1 - play_seq


def main() -> None:
    """Handles the main application loop."""
    while True:
        play_game()
        prompt = input(AGAIN_PROMPT)
        if prompt.lower() == 'y':
            continue
        else:
            return


if __name__ == "__main__": main()
