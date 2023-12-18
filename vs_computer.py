import curses
from curses import wrapper
from enum import Enum

from mdl import *
from piece_loader import PieceLoader

import c_caller


class UnicodePieces(Enum):
    WHITE_KING = u"\u2654"
    WHITE_QUEEN = u"\u2655"
    WHITE_ROOK = u"\u2656"
    WHITE_BISHOP = u"\u2657"
    WHITE_KNIGHT = u"\u2658"
    WHITE_PAWN = u"\u2659"
    BLACK_KING = u"\u265A"
    BLACK_QUEEN = u"\u265B"
    BLACK_ROOK = u"\u265C"
    BLACK_BISHOP = u"\u265D"
    BLACK_KNIGHT = u"\u265E"
    BLACK_PAWN = u"\u265F"

    WHITE_SQUARE = u"\u25A1"
    BLACK_SQUARE = u"\u25A0"

class TerminalSquare:

    def __init__(self, name: str, color: UnicodePieces, cursor: tuple[int, int]):
        self.name = name
        self.color = color
        self.piece = None
        self.cursor = cursor
    
    def set_piece(self, piece: Piece):
        letter = piece.letter
        white = piece.white
        match letter:
            case "": 
                self.piece = (UnicodePieces.BLACK_PAWN, UnicodePieces.WHITE_PAWN)[white]
            case "K": 
                self.piece = (UnicodePieces.BLACK_KING, UnicodePieces.WHITE_KING)[white]
            case "Q":
                self.piece = (UnicodePieces.BLACK_QUEEN, UnicodePieces.WHITE_QUEEN)[white]
            case "R":
                self.piece = (UnicodePieces.BLACK_ROOK, UnicodePieces.WHITE_ROOK)[white]
            case "B":
                self.piece = (UnicodePieces.BLACK_BISHOP, UnicodePieces.WHITE_BISHOP)[white]
            case "N":
                self.piece = (UnicodePieces.BLACK_KNIGHT, UnicodePieces.WHITE_KNIGHT)[white]
    

    def reset(self):
        self.piece = None

    def __repr__(self):
        if self.piece:
            return self.piece.value
        else:
            return self.color.value

            

class TerminalBoard:

    def __init__(self):
        self.squares : dict[str, TerminalSquare] = self.load()

    def load(self) -> dict[str, TerminalSquare]:
        board = dict()
        for counter, file in enumerate(list("abcdefgh")):
            for rank in range(8, 0, -1):
                square = f"{file}{rank}"
                cursor_position = (abs(8 - rank), counter * 2)
                if counter % 2:
                    unicode_square = (UnicodePieces.BLACK_SQUARE, UnicodePieces.WHITE_SQUARE)[rank % 2]
                else:
                    unicode_square = (UnicodePieces.WHITE_SQUARE, UnicodePieces.BLACK_SQUARE)[rank % 2]
                board[square] = TerminalSquare(name=square, color=unicode_square, cursor=cursor_position)
        return board
    
    def reset(self):
        for square in self.squares.values():
            square.reset()
    
    def update(self, board_dict: dict[str, Piece]):
        for square, piece in board_dict.items():
            self.squares[square].set_piece(piece)
    
    def decode(self, cursor_position):
        reversed_dictionary = {square.cursor: square.name 
                               for square in self.squares.values()}
        return reversed_dictionary[cursor_position]
        

    

class Cursor:

    MIN_WIDTH = 0
    MIN_DEPTH = 0
    MAX_WIDTH = 14
    MAX_DEPTH = 8

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    
    def up(self):
        if self.y - 1 <= Cursor.MIN_DEPTH:
            self.y = Cursor.MIN_DEPTH
        else:
            self.y -= 1

    def down(self):
        if self.y + 1 >= Cursor.MAX_DEPTH:
            self.y = Cursor.MAX_DEPTH
        else:
            self.y += 1

    def left(self):
        if self.x - 2 <= Cursor.MIN_WIDTH:
            self.x = Cursor.MIN_WIDTH
        else:
            self.x -= 2

    def right(self):
        if self.x + 2 >= Cursor.MAX_WIDTH:
            self.x = Cursor.MAX_WIDTH
        else:
            self.x += 2
    
    def get_pos(self) -> tuple[int, int]:
        return (self.y, self.x)

class WindowEvent:
    IDLE = 0
    ACTION = 1

    def __init__(self, event, value: str):
        self.event = event
        self.value = value

class GameInfo:

    def __init__(self, game: Game, selection: SelectionType, game_state = GameState.PLAY):
        self.piece_selection = game.piece_selection
        self.turn = game.turn
        self.player = ("Black", "White")[game.determine_color()]
        self.selection = selection
        self.game_state = game_state
        self.board_dict = game.board.pieces.get_dict('position', 'instance')


class Window:

    def __init__(self):
        self.window = curses.initscr()
        self.toggle_flip = False
        curses.noecho()
        curses.cbreak()
        self.window.keypad(True)
        self.terminal_board = TerminalBoard()
        self.load_board()
        self.cursor = Cursor()
        self.update()
        # Hack to get flipped board to work
        self.players_turn: str = 'White'
    
    def get_input(self) -> WindowEvent:

        key = self.window.getch()
        match key:
            case curses.KEY_UP:
                self.cursor.up()
                return WindowEvent(WindowEvent.IDLE, None)
            case curses.KEY_DOWN:
                self.cursor.down()
                return WindowEvent(WindowEvent.IDLE, None)
            case curses.KEY_LEFT:
                self.cursor.left()
                return WindowEvent(WindowEvent.IDLE, None)
            case curses.KEY_RIGHT:
                self.cursor.right()
                return WindowEvent(WindowEvent.IDLE, None)
            case 102: # 'f' key
                if self.toggle_flip:
                    self.toggle_flip = False
                else:
                    self.toggle_flip = True
                return WindowEvent(WindowEvent.IDLE, None)
            case 113: # 'q' key: quit
                #return WindowEvent(WindowEvent.IDLE, None)
                self.window.erase()
                self.window.refresh()
                curses.endwin()
                exit()
            case 10 | 13: # "Enter"
                if self.toggle_flip and self.players_turn == "Black":
                    unformatted_for_flip_cursor_pos = self.cursor.get_pos()
                    y, x = unformatted_for_flip_cursor_pos
                    cursor_pos = (abs(7-y), abs(14-x))
                else:
                    cursor_pos = self.cursor.get_pos()
                square_selected = self.terminal_board.decode(cursor_pos)
                return WindowEvent(WindowEvent.ACTION, square_selected)
            case _:
                return WindowEvent(WindowEvent.IDLE, None)

    def load_board(self, game_info: GameInfo | None = None):
        if self.toggle_flip and game_info.player == "Black":
            for square in self.terminal_board.squares.values():
                y, x = square.cursor
                y = abs(7 - y)
                x = abs(14 - x)
                string = repr(square)
                self.window.addstr(y, x, string)
            for y in range(8):
                files = list("hgfedcba")
                rank = str(y + 1)
                self.window.addstr(y, Cursor.MAX_WIDTH + 2, rank)
                self.window.addstr(Cursor.MAX_DEPTH + 1, y * 2, files[y])
        else:
            for square in self.terminal_board.squares.values():
                y, x = square.cursor
                string = repr(square)
                self.window.addstr(y, x, string)
        
            # Draw Board Markers
            for y in range(8):
                files = list("abcdefgh")
                rank = str(abs(y-8))
                self.window.addstr(y, Cursor.MAX_WIDTH + 2, rank)
                self.window.addstr(Cursor.MAX_DEPTH + 1, y * 2, files[y])
    
    def choose_promotion(self) -> str:
        self.window.erase()
        self.window.refresh()
        self.window.addstr(0, 0, "Press")
        self.window.addstr(1, 4, "Q: Queen")
        self.window.addstr(2, 4, "B: Bishop")
        self.window.addstr(3, 4, "N: Knight")
        self.window.addstr(4, 4, "R: Rook")
        key = self.window.getkey()
        while key not in list("qbnrQBNR"):
            key = self.window.getkey()
        self.window.erase()
        self.window.refresh()
        return key.upper()
    
    def clear_line(self, y: int, x: int):
        """Clears to the end of a line "y" starting at position "x",
        then resets the position."""
        self.window.move(y, x)
        self.window.clrtoeol()
        self.window.move(*self.cursor.get_pos())

    
    def show_info(self, game_info: GameInfo):
        # Draw Rules
        info_section = Cursor.MAX_WIDTH + 8
        self.window.addstr(0, info_section, "Use arrow keys to navigate the board.")
        self.window.addstr(1, info_section, "Press ENTER to select a piece.")
        self.window.addstr(2, info_section, "Press Q to quit.")
        self.window.addstr(3, info_section, "Press F to Toggle Flip")
        if self.toggle_flip:
            self.clear_line(4, info_section)
            self.window.addstr(4, info_section+4, "ON", curses.A_REVERSE)
            self.window.addstr(4, info_section+7, "OFF")
        else:
            self.clear_line(4, info_section)
            self.window.addstr(4, info_section+4, "ON")
            self.window.addstr(4, info_section+7, "OFF", curses.A_REVERSE)
        
        # Draw Game Information
        self.window.addstr(5, info_section, f"{game_info.player}'s Turn")
        piece_selected = game_info.piece_selection
        if piece_selected:
            piece_name = piece_selected.__class__.__name__
            piece_square = piece_selected.position
        else:
            self.clear_line(6, info_section)
        match game_info.selection:
            case SelectionType.SELECTED:
                self.clear_line(6, info_section)
                selection_msg = f"SELECTED: {piece_name} at {piece_square}"
            case SelectionType.NO_PIECE:
                self.clear_line(6, info_section)
                selection_msg = f"{game_info.player} does not have a piece there."
            case SelectionType.NO_MOVE:
                self.clear_line(6, info_section)
                selection_msg = f"{game_info.player}'s {piece_name} can't move there."
            case SelectionType.RESELECT:
                self.clear_line(6, info_section)
                selection_msg = f"SELECTED: {piece_name} at {piece_square}"
            case _:
                selection_msg = ""
        self.window.addstr(6, info_section, selection_msg)



    
    def update_board(self, game_info: GameInfo):
        self.players_turn = game_info.player
        self.show_info(game_info)
        self.terminal_board.reset()
        self.terminal_board.update(game_info.board_dict)
        self.load_board(game_info)

    def update(self):
        
        self.window.move(*self.cursor.get_pos())
        self.window.refresh()

class CLIController:

    def __init__(self):
        self.game = Game()
        self.ready_to_select_move = False
        self.opponent_turn = False
    
    def handle_event_and_return_info(self, event_obj: WindowEvent, window: Window):
        if event_obj.event == WindowEvent.IDLE:
            return GameInfo(self.game, selection=None)
        elif event_obj.event == WindowEvent.ACTION:
            game_info = self.handle_input(event_obj.value, window)
            return game_info

    def handle_input(self, square_selection, window: Window):
        if not self.ready_to_select_move:
            selection_message = self.game.select_piece(square_selection)
            match selection_message:
                case SelectionType.NO_PIECE:
                    return GameInfo(self.game, selection_message)
                case SelectionType.SELECTED:
                    self.ready_to_select_move = True
                    return GameInfo(self.game, selection_message)
        else:
            selection_message = self.game.select_move(square_selection)
            match selection_message:
                case SelectionType.RESELECT:
                    return GameInfo(self.game, selection_message)
                case SelectionType.NO_MOVE:
                    return GameInfo(self.game, selection_message)
                case SelectionType.SELECTED:
                    game_state = self.game.move_and_next_turn()
                    self.ready_to_select_move = False
                    self.opponent_turn = True
                    return GameInfo(self.game, selection=None, game_state=game_state)
                case SelectionType.PROMOTION:
                    # Get the piece to promote.
                    piece_to_promote = self.game.piece_selection
                    position = piece_to_promote.position
                    color = piece_to_promote.white
                    # Call the window to get user input for promotion
                    promote_to = window.choose_promotion()
                    # Promote the piece
                    self.game.board.promote(position, promote_to, color)
                    # Reset the piece selection to new piece
                    self.game.piece_selection = self.game.board.get_piece_at(position)
                    game_state = self.game.move_and_next_turn()
                    self.ready_to_select_move = False
                    self.opponent_turn = True
                    return GameInfo(self.game, selection=None, game_state=game_state)
                
    def computer_move(self) -> GameInfo:
        action = c_caller.from_game_get_move(self.game)
        self.game.select_piece(action[0])
        self.game.select_move(action[1])
        game_state = self.game.move_and_next_turn()
        self.opponent_turn = False
        return GameInfo(self.game, selection=None, game_state=game_state)

                    
                
                
            


def main():
    window = Window()
    controller = CLIController()
    while True:
        window_event = window.get_input()
        game_info = controller.handle_event_and_return_info(window_event, window)
        window.update_board(game_info)
        window.update()
        if controller.opponent_turn:
            game_info = controller.computer_move()
            window.update_board(game_info)
            window.update()
        




if __name__ == '__main__':
    main()
