from copy import deepcopy
from operator import methodcaller
from enum import Enum

class Square:
    
    def __init__(self):
        self.squares = [[f"{ltr}{num}" for ltr in list("abcdefgh")] for num in range(1,9)]
        self.squares.reverse()



    def __getitem__(self, sq: str) -> tuple:
        for row in range(len(self.squares)):
            for col in range(len(self.squares[row])):
                if self.squares[row][col] == sq:
                    return (row, col)
    
    def up(self, sq: str) -> str:
        if sq is None:
            return None
        row, col = self[sq]
        row -= 1
        if row >= 0:
            return self.squares[row][col]
        else:
            return None
        
    def down(self, sq: str) -> str:
        if sq is None:
            return None
        row, col = self[sq]
        row += 1
        if row <= 7:
            return self.squares[row][col]
        else:
            return None
    
    def left(self, sq: str) -> str:
        if sq is None:
            return None
        row, col = self[sq]
        col -= 1
        if col >= 0:
            return self.squares[row][col]
        else:
            return None
    
    def right(self, sq: str) -> str:
        if sq is None:
            return None
        row, col = self[sq]
        col += 1
        if col <= 7:
            return self.squares[row][col]
        else:
            return None

class Piece:

    def __init__(self, position: str, white: bool):
        self.squares = Square()
        self.position = position
        self.index = self.squares[position]
        self.white = white
        self.letter = ""
        self.points = 0
    
    def get_control(self, black_position: set, white_position: set) -> set:
        control_set = set()
        return control_set
    
    def get_moves(self, board: 'Board') -> set[str]:
        move_set = set()
        for move in self.get_control(board.pieces.get_set('position', 'black'), board.pieces.get_set('position', 'white')):
            # Create yet another copy of board.
            board_copy = board.get_board_copy()
            if board_copy.get_piece_at(move) != None:
                board_copy.remove_piece_at(move)
            self_copy = [piece for piece in board_copy.pieces.get_pieces() if repr(piece)==repr(self)][0]
            self_copy.set_position(move)
            if not board_copy.king_in_check(self.white):
                move_set.add(move)
            del board_copy
        return move_set
    
    def return_moves_without_king_in_check(self, moves_to_check: list[str], board:'Board') -> set[str]:
        move_set = set()
        for move in moves_to_check:
            # Create yet another copy of board.
            board_copy = board.get_board_copy()
            self_copy = board_copy.get_piece_at(self.position)
            board_copy.move(self_copy, move)
            if not board_copy.king_in_check(self.white):
                move_set.add(move)
            del board_copy
        return move_set
    
    
    def get_identity(self):
        return f"{self.letter}{self.position}"
    
    def get_instance(self):
        return self

    def get_position(self):
        return self.position
    
    def set_position(self, position: str):
        self.position = position
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.position}', {self.white})"


class Knight(Piece):

    def __init__(self, position: str, white: bool):
        super().__init__(position, white)
        self.letter = 'N'
        self.points = 3

    def get_control(self, black_position: set, white_position: set) -> set[str]:
        control_set = set()
        # Create combinations of 2 ups, downs, lefts, and right.
        up2 = self.squares.up(self.squares.up(self.position))
        down2 = self.squares.down(self.squares.down(self.position))
        left2 = self.squares.left(self.squares.left(self.position))
        right2 = self.squares.right(self.squares.right(self.position))

        control_set.add(self.squares.left(up2))
        control_set.add(self.squares.right(up2))
        control_set.add(self.squares.left(down2))
        control_set.add(self.squares.right(down2))
        control_set.add(self.squares.up(left2))
        control_set.add(self.squares.down(left2))
        control_set.add(self.squares.up(right2))
        control_set.add(self.squares.down(right2))

        control_set -= (black_position, white_position)[self.white]
        control_set -= {None}
        
        return control_set

        
    
class Bishop(Piece):

    def __init__(self, position: str, white: bool):
        super().__init__(position, white)
        self.letter = 'B'
        self.points = 3
    
    def get_control(self, black_position: set, white_position: set) -> set[str]:
        control_set = set()
        # Up-Left
        sq = self.squares.up(self.squares.left(self.position))
        while sq is not None and sq not in (black_position, white_position)[self.white]:
            control_set.add(sq)
            if sq in (black_position, white_position)[not self.white]:
                break
            sq = self.squares.up(sq)
            sq = self.squares.left(sq)
        # Up-Right
        sq = self.squares.up(self.squares.right(self.position))
        while sq is not None and sq not in (black_position, white_position)[self.white]:
            control_set.add(sq)
            if sq in (black_position, white_position)[not self.white]:
                break
            sq = self.squares.up(sq)
            sq = self.squares.right(sq)
        # Down-Left
        sq = self.squares.down(self.squares.left(self.position))
        while sq is not None and sq not in (black_position, white_position)[self.white]:
            control_set.add(sq)
            if sq in (black_position, white_position)[not self.white]:
                break
            sq = self.squares.down(sq)
            sq = self.squares.left(sq)
        # Down-Right
        sq = self.squares.down(self.squares.right(self.position))
        while sq is not None and sq not in (black_position, white_position)[self.white]:
            control_set.add(sq)
            if sq in (black_position, white_position)[not self.white]:
                break
            sq = self.squares.down(sq)
            sq = self.squares.right(sq)

        return control_set

class Rook(Piece):

    def __init__(self, position: set, white: bool):
        super().__init__(position, white)
        self.letter = 'R'
        self.has_moved = False
        self.points = 5

    def get_control(self, black_position: set, white_position: set) -> set[str]:
        control_set = set()
        for move_direction in [self.squares.up, self.squares.down, self.squares.right, self.squares.left]:
            sq = move_direction(self.position)
            while sq is not None and sq not in (black_position, white_position)[self.white]:
                control_set.add(sq)
                if sq in (black_position, white_position)[not self.white]:
                    break
                sq = move_direction(sq)
        return control_set

    def set_position(self, position: str):
        self.has_moved = True
        return super().set_position(position)
    
class Queen(Piece):

    def __init__(self, position, white):
        super().__init__(position, white)
        self.letter = 'Q'
        self.points = 9

    def get_control(self, black_position: set, white_position: set) -> set:
        control_set = set()
        for move_direction in [self.squares.up, self.squares.down, self.squares.right, self.squares.left]:
            sq = move_direction(self.position)
            while True:
                if sq is None or sq in (black_position, white_position)[self.white]:
                    break
                elif sq in (black_position, white_position)[not self.white]:
                    control_set.add(sq)
                    break
                else:
                    control_set.add(sq)
                sq = move_direction(sq)
        for vertical_move in [self.squares.up, self.squares.down]:
            for horizontal_move in [self.squares.left, self.squares.right]:
                sq = vertical_move(horizontal_move(self.position))
                while True:
                    if sq is None or sq in (black_position, white_position)[self.white]:
                        break
                    elif sq in (black_position, white_position)[not self.white]:
                        control_set.add(sq)
                        break
                    else:
                        control_set.add(sq)
                    sq = vertical_move(horizontal_move(sq))
        return control_set
                

class King(Piece):
    
    def __init__(self, position: set, white: bool):
        super().__init__(position, white)
        self.letter = 'K'
        self.has_moved = False

    def get_control(self, black_position: set, white_position: set) -> set:
        control_set = set()
        for move_direction in [self.squares.up, self.squares.down, self.squares.right, self.squares.left]:
            control_set.add(move_direction(self.position))
        for move_direction in [(x, y) for x in [self.squares.up, self.squares.down] 
                               for y in [self.squares.left, self.squares.right]]:
            control_set.add(move_direction[0](move_direction[1](self.position)))
        control_set -= (black_position, white_position)[self.white]
        control_set -= {None}
        return control_set
    
    def get_moves(self, board: 'Board') -> set[str]:
        move_set = set()
        black_position = board.pieces.get_set('position', 'black')
        white_position = board.pieces.get_set('position', 'white')
        black_control = board.pieces.get_set('control', 'black')
        white_control = board.pieces.get_set('control', 'white')
        if not self.has_moved:
            # Define location of Rooks for short castling.
            short_castle_loc = ('Rh8', 'Rh1')[self.white]
            long_castle_loc = ('Ra8', 'Ra1')[self.white]
            piece_locations = board.pieces.get_dict('identity', 'instance')
            # Get the rook at location.
            short_castle_rook = piece_locations.get(short_castle_loc)
            long_castle_rook = piece_locations.get(long_castle_loc)
            # Squares that cannot be under attack.
            short_safe_squares = ({'e8', 'f8', 'g8'}, {'e1', 'f1', 'g1'})[self.white]
            long_safe_squares = ({'e8', 'd8', 'c8'}, {'e1', 'd1', 'c1'})[self.white]
            long_unoccupied = ({'e8', 'd8', 'c8', 'b8'}, {'e1', 'd1', 'c1', 'b1'})[self.white]
            # Short castle
            if short_castle_rook:
                short_requirements = [
                    not short_safe_squares.issubset((black_control, white_control)[not self.white]),
                    not short_safe_squares.issubset((black_position, white_position)[self.white]),
                    not short_castle_rook.has_moved,
                    ]
                if all(short_requirements): move_set.add('O-O')
            # Long Castle
            if long_castle_rook:
                long_requirements = [
                    not long_safe_squares.issubset((black_control, white_control)[not self.white]),
                    not long_unoccupied.issubset((black_position, white_position)[self.white]),
                    not long_castle_rook.has_moved,
                ]
                if all(long_requirements): move_set.add('O-O-O')
        for move in self.get_control(black_position, white_position):
            # Create yet another copy of board.
            board_copy = board.get_board_copy()
            if board_copy.get_piece_at(move) != None:
                board_copy.remove_piece_at(move)
            self_copy = [piece for piece in board_copy.pieces.get_pieces() if piece.get_identity() == self.get_identity()][0]
            self_copy.set_position(move)
            #if not {self_copy.position}.issubset(board_copy.pieces.get_set('control', not self.white)):
            #    move_set.add(move)
            if not board_copy.king_in_check(self.white):
                move_set.add(move)
            del board_copy
        return move_set

    def set_position(self, position: str):
        self.has_moved = True
        return super().set_position(position)

class Pawn(Piece):

    def __init__(self, position: str, white: bool):
        super().__init__(position, white)
        self.points = 1

    def get_control(self, black_position: set, white_position: set) -> set:
        control_set = set()
        if self.white:
            control_set.add(self.squares.up(self.squares.left(self.position)))
            control_set.add(self.squares.up(self.squares.right(self.position)))
        else:
            control_set.add(self.squares.down(self.squares.left(self.position)))
            control_set.add(self.squares.down(self.squares.right(self.position)))
        control_set.discard(None)
        return control_set
    
    
    def get_moves(self, board: 'Board') -> set[str]:

        player_position = board.pieces.get_set('position', self.white)
        opponent_position = board.pieces.get_set('position', not self.white)
        starting_position = ('7', '2')[self.white]
        promotion_position = ('1', '8')[self.white]

        # Possible Moves
        moves_to_check = []
        forward_move = (self.squares.down(self.position), self.squares.up(self.position))[self.white]
        double_forward_move = (self.squares.down(forward_move), self.squares.up(forward_move))[self.white]
        diagonal_left = self.squares.left(forward_move)
        diagonal_right = self.squares.right(forward_move)
        
        # Add forward moves, if promotion available add all four different promotions
        if forward_move not in player_position and forward_move not in opponent_position:
            if forward_move[1] == promotion_position:
                moves_to_check += self.add_promotion_letters_to_move(forward_move)
            elif self.position[1] == starting_position and (
                    double_forward_move not in player_position and double_forward_move not in opponent_position):
                moves_to_check.append(forward_move)
                moves_to_check.append(double_forward_move)
            else:
                moves_to_check.append(forward_move)
        for diagonal in [diagonal_left, diagonal_right]:
            if diagonal in opponent_position:
                if diagonal[1] == promotion_position:
                    moves_to_check += self.add_promotion_letters_to_move(diagonal)
                else:
                    moves_to_check.append(diagonal)
        
        # Add en passant taking move if available.
        if board.en_passant:
            en_passant_squares = [self.squares.right(board.en_passant), self.squares.left(board.en_passant)]
            en_passant_take = (self.squares.down(board.en_passant), self.squares.up(board.en_passant))[self.white]
            if self.position in en_passant_squares:
                moves_to_check.append(en_passant_take)

        moves_to_check = [move for move in moves_to_check if move != None]
        return self.return_moves_without_king_in_check(moves_to_check, board)
        


    def add_promotion_letters_to_move(self, move: str) -> list[str]:
        letter_list = list("QRNB")
        return [f"{move}{letter}" for letter in letter_list]





def load_pieces() -> list[Piece]:
    pieces = [
        Rook('a1', True),
        Knight('b1', True),
        Bishop('c1', True),
        Queen('d1', True),
        King('e1', True),
        Bishop('f1', True),
        Knight('g1', True),
        Rook('h1', True),
        Rook('a8', False),
        Knight('b8', False),
        Bishop('c8', False),
        Queen('d8', False),
        King('e8', False),
        Bishop('f8', False),
        Knight('g8', False),
        Rook('h8', False),
    ]
    white_pawns = [Pawn(f"{file}2", True) for file in list("abcdefgh")]
    black_pawns = [Pawn(f"{file}7", False) for file in list("abcedfgh")]
    return pieces + white_pawns + black_pawns


class OnBoardPieces:
    """
    Class for accessing piece data and info.

    Attributes
    ----------
    pieces: list[Piece]
        A list of pieces on the board.

    Methods
    -------
    get_pieces(white=None)
        Returns a list of piece instances, color optional.
    get_dict(key, value, white=None, board=None)
        Returns a dict with specified key, value pairs.
    get_set(key, white=None)
        Returns a set: position or control.
    get_king_position(white):
        Returns the position of the King of a specified color.
    """

    def __init__(self):
        self.piece_list = load_pieces()
    
    def remove(self, square: str) -> Piece:
        square = square[:2]
        for piece in self.piece_list:
            if piece.position == square:
                idx = self.piece_list.index(piece)
                removed_piece = self.piece_list.pop(idx)
        return removed_piece 

    
    def get_pieces(self, white=None):
        """
        Get a list of piece instances.

        Parameters
        ----------
        white : None | bool | str : {'white', 'black'}, optional

        Returns
        -------
        list[Piece]
            List of all pieces on the board, or specified by color.
        """
        match white:
            case None:
                return self.piece_list
            case True | 'white':
                return [piece for piece in self.piece_list if piece.white]
            case False | 'black':
                return [piece for piece in self.piece_list if not piece.white]
    
    
    def get_dict(self, key: str, value: str, white: bool|str=None, board=None):
        """
        Creates a dictionary of piece information.

        Parameters
        ----------
        key : {'instance', 'position', 'identity', 'representation'}
            The resulting key in the dictionary.
        value: {'moves', 'control', 'position', 'instance', 'identity', 'representation'}
            The resulting value in the dictionary.
            Using the 'moves' option requires both a color (white=...),
            and passing the board as an argument.
        white: bool | str: {'white', 'black'}, default=None
        board : Board, default=None
            The Board instance of the game.
        """
        match key:
            case 'instance':
                getKey = methodcaller('get_instance')
            case 'position':
                getKey = methodcaller('get_position')
            case 'identity':
                getKey = methodcaller('get_identity')
            case 'representation':
                getKey = methodcaller('__repr__')
            case _:
                raise Exception("Invalid key. KEYS: 'instance', 'position', 'identity', 'representation'.")
        match value:
            case 'moves':
                if board == None:
                    raise Exception('Must pass Board instance to retrieve moves.')
                elif white == None:
                    raise Exception("Must pass 'white = True | False'. Only one color's moves can be accessed at a time.")
                else:
                    board_copy = board.get_board_copy()
                    getValue = methodcaller('get_moves', board_copy)
            case 'control':
                getValue = methodcaller('get_control', black_position=self.get_set('position', False), white_position=self.get_set('position', True))
            case 'position':
                getValue = methodcaller('get_position')
            case 'instance':
                getValue = methodcaller('get_instance')
            case 'identity':
                getValue = methodcaller('get_identity')
            case 'representation':
                getValue = methodcaller('__repr__')
            case _:
                raise Exception("Invalid value. VALUES: 'instance', 'position', 'identity', 'representation', 'moves', 'control'.")
        return {getKey(piece): getValue(piece) for piece in self.get_pieces(white=white)}
    
    def get_set(self, key, white=None):
        """
        Creates a set of pieces positions or control.

        Paramaters
        ----------
        key: {'position', 'control'}
            Get a set of board positions or piece controls.
        white: bool | str: {'white', 'black'}, default=None
            Not optional for returning  piece control.
        
        Returns
        -------
        position : set
            The position of the pieces on the board, optionally by color.
        control_set: set
            The set of squares controlled by a specified color.

        """
        match key:
            case 'position':
                return {piece.position for piece in self.get_pieces(white=white)}
            case 'control':
                if white == None:
                    raise Exception("Must pass 'white = True | False'.")
                else:
                    control_set = set()
                    for piece in self.get_pieces(white=white):
                        control_set.update(piece.get_control(
                            self.get_set('position', white=False), self.get_set('position', white=True)))
                    return control_set
    
    def get_king_position(self, white:bool|str) -> str:
        for piece in self.get_pieces(white=white):
            if piece.__class__.__name__ == "King":
                return piece.position
    
    def __getitem__(self, square: str) -> Piece:
        return self.get_dict('position', 'instance')[square]

class OffBoardPieces:

    def __init__(self):
        self.piece_list = []
    
    def get_pieces(self, white: bool|str = None) -> list[Piece]:
        """
        Get a list of piece instances.

        Parameters
        ----------
        white : None | bool | str : {'white', 'black'}, optional

        Returns
        -------
        list[Piece]
            List of all pieces off the board, or specified by color.
        """
        match white:
            case None:
                return self.piece_list
            case True | 'white':
                return [piece for piece in self.piece_list if piece.white]
            case False | 'black':
                return [piece for piece in self.piece_list if not piece.white]

    def add(self, piece: Piece):
        piece.position = None
        self.piece_list.append(piece)
    
    def get_points(self, white:bool|str):
        return sum(self.get_pieces(white=white))
    


class MoveType(Enum):
    STANDARD = 0
    CASTLE = 1
    PROMOTION = 2
    EN_PASSANT_SET = 3
    EN_PASSANT_TAKE = 4




class Board:

    def __init__(self):
        self.squares = Square()
        self.pieces = OnBoardPieces()
        self.off_board_pieces = OffBoardPieces()
        self.en_passant = None
    

    def king_in_check(self, white: bool) -> bool:
        king_location = self.pieces.get_king_position(white=white)
        if king_location in self.pieces.get_set('control', not white):
            return True
        else:
            return False
    
    def get_board_copy(self):
        return deepcopy(self)

    def get_piece_at(self, square: str):
        try:
            return self.pieces[square]
        except KeyError:
            return None

    def remove_piece_at(self, square: str):
        self.off_board_pieces.add(self.pieces.remove(square))

    def promote(self, square, promote_to, white):
        self.pieces.remove(square)
        match promote_to:
            case 'Q':
                promotion = Queen(square, white)
            case 'B':
                promotion = Bishop(square, white)
            case 'N':
                promotion = Knight(square, white)
            case 'R':
                promotion = Rook(square, white)
        self.pieces.piece_list.append(promotion)


    def move(self, piece: Piece, square: str):
        move_type = self.determine_move_type(piece, square)
        match move_type:
            case MoveType.STANDARD:
                if square in self.pieces.get_set('position', not piece.white):
                    self.remove_piece_at(square)
                piece.set_position(square)
                self.set_en_passant(None)
            case MoveType.CASTLE:
                self.handle_castling(piece, square)
                self.set_en_passant(None)
            case MoveType.EN_PASSANT_SET:
                piece.set_position(square)
                self.set_en_passant(square)
            case MoveType.EN_PASSANT_TAKE:
                self.handle_en_passant_take(piece, square)
                self.set_en_passant(None)
            case MoveType.PROMOTION:
                self.handle_promotion(piece, square)
                self.set_en_passant(None)


    def determine_move_type(self, piece: Piece, square: str) -> MoveType:
        en_passant_start = ('7', '2')[piece.white]
        en_passant_end = ('5', '4')[piece.white]
        if square == 'O-O' or square == 'O-O-O':
            return MoveType.CASTLE
        elif piece.__class__.__name__ == 'Pawn':
            if piece.position[1] == en_passant_start and square[1] == en_passant_end:
                return MoveType.EN_PASSANT_SET
            elif square == (self.squares.down(self.en_passant), self.squares.up(self.en_passant))[piece.white]:
                return MoveType.EN_PASSANT_TAKE
            elif square[-1] in list('QRNB'):
                return MoveType.PROMOTION
            else:
                return MoveType.STANDARD
        else:
            return MoveType.STANDARD
    
    def set_en_passant(self, square: str|None):
        self.en_passant = square

    def handle_promotion(self, piece: Piece, square: str):
        move = square[:2]
        promotion_letter = square[2]
        if move in self.pieces.get_set('position', not piece.white):
            self.remove_piece_at(move)
        piece.set_position(move)
        self.promote(move, promotion_letter, piece.white)

    def handle_castling(self, piece: Piece, square: str):
        short_castle, long_castle = 'O-O', 'O-O-O'
        if square == short_castle:
            if piece.white:
                piece.set_position('g1')
                self.pieces['h1'].set_position('f1')
            else:
                piece.set_position('g8')
                self.pieces['h8'].set_position('f8')
        else: # Long Castle
            if piece.white:
                piece.set_position('c1')
                self.pieces['a1'].set_position('d1')
            else:
                piece.set_position('c8')
                self.pieces['a8'].set_position('d8')
    
    def handle_en_passant_take(self, piece: Piece, square):
        self.remove_piece_at(self.en_passant)
        piece.set_position(square)

           




class GameState(Enum):
    PLAY = 0
    CHECKMATE = 1
    STALEMATE = 2

class SelectionType(Enum):
    SELECTED = 0
    NO_PIECE = 1
    NO_MOVE = 2
    RESELECT = 3
    PROMOTION = 4



class Game:

    def __init__(self):
        self.board = Board()
        self.turn = 1
        self.piece_selection = None
        self.square_selection = None
    
    def determine_color(self) -> bool:
        return bool(self.turn % 2)
    
    def is_checkmate(self) -> bool:
        color = self.determine_color()
        any_moves = any(self.board.pieces.get_dict('identity', 'moves', color, self.board).values())
        king_in_check = self.board.king_in_check(color)
        if not any_moves and king_in_check:
            return True
        else:
            return False

    def is_stalemate(self) -> bool:
        color = self.determine_color()
        any_moves = any(self.board.pieces.get_dict('identity', 'moves', color, self.board).values())
        king_in_check = self.board.king_in_check(color)
        if not any_moves and not king_in_check:
            return True
        else:
            return False
        
    def select_piece(self, square: str) -> SelectionType:
        color = self.determine_color()
        if square not in self.board.pieces.get_set('position', color):
            return SelectionType.NO_PIECE
        else:
            self.piece_selection = piece = self.board.get_piece_at(square)
            return SelectionType.SELECTED
        
    def select_move(self, square: str) -> SelectionType:
        color = self.determine_color()
        moves = self.board.pieces.get_dict('instance', 'moves', color, self.board)[self.piece_selection]
        # Castling
        if 'O-O' in moves:
            short_castle = (['g8', 'h8'], ['g1', 'h1'])[color]
            if square in short_castle:
                self.square_selection = 'O-O'
                return SelectionType.SELECTED
        if 'O-O-O' in moves:
            long_castle = (['a8', 'c8'], ['a1', 'c1'])[color]
            if square in long_castle:
                self.square_selection = 'O-O-O'
                return SelectionType.SELECTED
            
        # Non-Castling Moves and Promotion    
        if square in self.board.pieces.get_set('position', color):
            self.piece_selection = self.board.pieces[square]
            return SelectionType.RESELECT
        elif square + 'Q' in moves:
            self.square_selection = square
            return SelectionType.PROMOTION
        elif square not in moves:
            return SelectionType.NO_MOVE
        else:
            self.square_selection = square
            return SelectionType.SELECTED

    def move_and_next_turn(self) -> GameState:
        self.board.move(self.piece_selection, self.square_selection)
        self.turn += 1
        self.piece_selection = None
        self.square_selection = None
        if self.is_stalemate():
            return GameState.STALEMATE
        elif self.is_checkmate():
            return GameState.CHECKMATE
        else: 
            return GameState.PLAY
        


        