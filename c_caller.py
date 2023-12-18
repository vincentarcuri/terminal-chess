import ctypes
from mdl import *
import os

current_directory = os.getcwd()


PATH = os.path.join(current_directory, "cpp_chess", "shared.so")


clibrary = ctypes.CDLL(PATH)

def board_to_binary_string(board: Board) -> str:
    """Converts the Pieces on the Board to a binary string that can be read by
    C-function."""
    string_list = []
    for piece in board.pieces.get_pieces():
        letter = piece.letter
        moved = "f"
        position = piece.position
        color = ('b', 'w')[piece.white]
        if letter == "":
            letter = "p"
        elif letter == "K" or letter == "R":
            moved = ("f", "t")[piece.has_moved]
        string_list.append(letter + position + color + moved)
    string =  " ".join(string_list)
    return string.encode('ascii')

get_move_from_state = clibrary.getMoveFromState
get_move_from_state.argtypes = [ctypes.c_char_p, ctypes.c_int]
get_move_from_state.restype = ctypes.c_char_p

def from_game_get_move(game: Game) -> tuple[str, str]:
    """Take a Game object, and call the C-library to use alpha beta minimax search
    and returns a move."""

    binary_string = board_to_binary_string(game.board)
    return_binary = get_move_from_state(binary_string, game.turn)
    string: str = return_binary.decode("ascii")
    return tuple(string.split(" "))
    

