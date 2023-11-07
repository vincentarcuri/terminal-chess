import sys
import inspect
from operator import methodcaller

from mdl import *
from piece_loader import PieceLoader


class Test:
    """Base class for designing test. All tests must start with `test`. 
    DO NOT name attributes test, only the methods `test...`!!!!!!"""

    def run_all(self, verbose=False):
        test_method_names = [method for method in dir(
            self) if method.startswith("test")]
        for test_name in test_method_names:
            try:
                test_method = methodcaller(test_name)
                test_method(self)
            except AssertionError as e:
                print(e)
            else:
                if verbose:
                    print(f"{test_name:<36}-----> {'OK':>6}")

    @staticmethod
    def assertTrue(test):
        try:
            assert test
        except AssertionError:
            class_name = inspect.stack(
                )[1][0].f_locals["self"].__class__.__name__
            test_name = inspect.stack()[1][3]
            exception_msg = f"{class_name}: {test_name}-----------------------> FAILED\n"
            exception_msg += f"\tTest Answer: False EXPECTED True\n"
            raise AssertionError(exception_msg) from None
    
    @staticmethod
    def assertFalse(test):
        try:
            assert not test
        except AssertionError:
            class_name = inspect.stack(
                )[1][0].f_locals["self"].__class__.__name__
            test_name = inspect.stack()[1][3]
            exception_msg = f"{class_name}: {test_name}-----------------------> FAILED\n"
            exception_msg += f"\tTest Answer: True EXPECTED False\n"
            raise AssertionError(exception_msg) from None
        

    @staticmethod
    def assertEquals(test, correct):

        try:
            assert test == correct
        except AssertionError:
            class_name = inspect.stack(
                )[1][0].f_locals["self"].__class__.__name__
            test_name = inspect.stack()[1][3]
            exception_msg = f"{class_name}: {test_name}-----------------------> FAILED\n"
            exception_msg += f"\tTest Answer: {test}\n\t\tDOES NOT EQUAL\n\tCorrect Answer:{correct}\n"
            raise AssertionError(exception_msg) from None

    @staticmethod
    def assertNotEquals(test, correct):
        try:
            assert test != correct
        except AssertionError:
            class_name = inspect.stack(
                )[1][0].f_locals["self"].__class__.__name__
            test_name = inspect.stack()[1][3]
            exception_msg = f"{class_name}: {test_name}---> FAILED\n"
            exception_msg += f"\tTest Answer: {test} DOES NOT EQUAL Correct Answer:{correct}"
            raise AssertionError(exception_msg) from None


class TestSquares(Test):

    def __init__(self):
        self.squares = Square()
        self.list_of_squares = ['a1', 'a8', 'h1', 'h8', 'c5']

    def test_getitem(self):
        correct_answer = [(7, 0), (0, 0), (7, 7), (0, 7), (3, 2)]
        test_answer = []
        for sq in self.list_of_squares:
            test_answer.append(self.squares[sq])
        Test.assertEquals(test_answer, correct_answer)

    def test_up(self):
        correct_answer = ['a2', None, 'h2', None, 'c6']
        test_answer = list(map(self.squares.up, self.list_of_squares))
        Test.assertEquals(test_answer, correct_answer)

    def test_down(self):
        correct_answer = [None, 'a7', None, 'h7', 'c4']
        test_answer = list(map(self.squares.down, self.list_of_squares))
        Test.assertEquals(test_answer, correct_answer)

    def test_right(self):
        correct_answer = ['b1', 'b8', None, None, 'd5']
        test_answer = list(map(self.squares.right, self.list_of_squares))
        Test.assertEquals(test_answer, correct_answer)

    def test_left(self):
        correct_answer = [None, None, 'g1', 'g8', 'b5']
        test_answer = list(map(self.squares.left, self.list_of_squares))
        Test.assertEquals(test_answer, correct_answer)


class TestPieceControl(Test):

    def __init__(self):
        self.black_position = {'f8'}
        self.white_position = {'f1'}

    def test_pawn(self):

        black_pawn = Pawn('e5', False)
        black_added = self.black_position | {'e5'}
        test_answer = black_pawn.get_control(black_added, self.white_position)
        correct_answer = {'d4', 'f4'}
        Test.assertEquals(test_answer, correct_answer)

        white_pawn = Pawn('a3', True)
        white_added = self.white_position | {'a3'}
        test_answer = white_pawn.get_control(self.black_position, white_added)
        correct_answer = {'b4'}
        Test.assertEquals(test_answer, correct_answer)

    def test_rook(self):
        black_rook = Rook('c7', False)
        black_added = self.black_position | {'c7'}
        test_answer = black_rook.get_control(black_added, self.white_position)
        correct_answer = {'c1', 'c2', 'c3', 'c4', 'c5', 'c6',
                          'c8', 'a7', 'b7', 'd7', 'e7', 'f7', 'g7', 'h7'}
        Test.assertEquals(test_answer, correct_answer)

        white_rook = Rook('b1', True)
        white_added = self.white_position | {'b1'}
        test_answer = white_rook.get_control(self.black_position, white_added)
        correct_answer = {'b2', 'b3', 'b4', 'b5',
                          'b6', 'b7', 'b8', 'a1', 'c1', 'd1', 'e1'}
        Test.assertEquals(test_answer, correct_answer)

    def test_bishop(self):
        # Includes capture of white king
        black_bishop = Bishop('a6', False)
        black_added = self.black_position | {'a6'}
        test_answer = black_bishop.get_control(
            black_added, self.white_position)
        correct_answer = {'c8', 'b7', 'b5', 'c4', 'd3', 'e2', 'f1'}
        Test.assertEquals(test_answer, correct_answer)

    def test_knight(self):
        # Includes capture of white king
        black_knight = Knight('e3', False)
        black_added = self.black_position | {'e3'}
        test_answer = black_knight.get_control(
            black_added, self.white_position)
        correct_answer = {'d1', 'f1', 'g2', 'g4', 'f5', 'd5', 'c4', 'c2'}
        Test.assertEquals(test_answer, correct_answer)

    def test_queen(self):
        # Includes capture of black king, and running into white king.
        white_queen = Queen('f4', True)
        white_added = self.white_position | {'f4'}
        test_answer = white_queen.get_control(self.black_position, white_added)
        correct_answer = {'f2', 'f3', 'f5', 'f6', 'f7', 'f8',  # UP-DOWN
                          'a4', 'b4', 'c4', 'd4', 'e4', 'g4', 'h4',  # LEFT-RIGHT
                          'b8', 'c7', 'd6', 'e5', 'g3', 'h2',  # Left diagonal
                          'c1', 'd2', 'e3', 'g5', 'h6'}  # Right Diagonal
        Test.assertEquals(test_answer, correct_answer)

    def test_king(self):
        white_king = King('f1', True)
        test_answer = white_king.get_control(
            self.black_position, self.white_position)
        correct_answer = {'e1', 'e2', 'f2', 'g2', 'g1'}
        Test.assertEquals(test_answer, correct_answer)


class TestOnBoardPieces(Test):
    """This class tests every option of OnBoardPieces EXCEPT `moves`, because that
    requires instantiating the board."""

    def test_remove_piece_removed(self):
        on_board_pieces = OnBoardPieces()
        on_board_pieces.remove('a1')
        test_answer = on_board_pieces.piece_list
        correct_answer = [piece for piece in load_pieces() if repr(
            piece) != "Rook('a1', True)"]
        test_answer = [repr(piece) for piece in test_answer]
        correct_answer = [repr(piece) for piece in correct_answer]
        test_answer.sort()
        correct_answer.sort()
        Test.assertEquals(test_answer, correct_answer)

    def test_remove_piece_returned(self):
        on_board_pieces = OnBoardPieces()
        test_answer = repr(on_board_pieces.remove('b7'))
        correct_answer = "Pawn('b7', False)"
        Test.assertEquals(test_answer, correct_answer)

    def test_get_pieces_both(self):
        on_board_pieces = OnBoardPieces()
        correct_answer = [King('a1', False), King('a4', True)]
        on_board_pieces.piece_list = correct_answer
        test_answer = on_board_pieces.get_pieces()
        Test.assertEquals(test_answer, correct_answer)

    def test_get_pieces_white(self):
        on_board_pieces = OnBoardPieces()
        correct_answer = [King('a1', False), King('a4', True)]
        on_board_pieces.piece_list = correct_answer
        test_answer = on_board_pieces.get_pieces('white')
        Test.assertEquals(test_answer, [correct_answer[1]])

    def test_get_pieces_black(self):
        on_board_pieces = OnBoardPieces()
        correct_answer = [King('a1', False), King('a4', True)]
        on_board_pieces.piece_list = correct_answer
        test_answer = on_board_pieces.get_pieces('black')
        Test.assertEquals(test_answer, [correct_answer[0]])

    def test_get_dict_identity_position(self):
        sample_pieces = [King('a1', False), King(
            'a4', True), Rook('b4', True), Pawn('g7', False)]
        on_board_pieces = OnBoardPieces()
        on_board_pieces.piece_list = sample_pieces
        test_answer = on_board_pieces.get_dict('identity', 'position')
        correct_answer = {
            'Ka1': 'a1',
            'Ka4': 'a4',
            'Rb4': 'b4',
            'g7': 'g7',
        }
        Test.assertEquals(test_answer, correct_answer)

    def test_get_dict_identity_control(self):
        on_board_pieces = OnBoardPieces()
        on_board_pieces.piece_list = PieceLoader.load_sample_one_piece_each()
        test_answer = on_board_pieces.get_dict('identity', 'control')
        correct_answer = {
            'Ba8': {'b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'},
            'a2': {'b1'},
            'Nd7': {'b8', 'b6', 'c5', 'e5', 'f6'},
            'Qh8': {'g8', 'h7', 'h6', 'h5', 'h4', 'h3', 'h2', 'h1',
                    'g7', 'f6', 'e5', 'd4', 'c3', 'b2', 'a1'},
            'Kf8': {'e8', 'e7', 'f7', 'g7', 'g8'},
            'Kf1': {'e1', 'e2', 'f2', 'g2', 'g1'},
            'Rh1': {'g1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'},
        }
        Test.assertEquals(test_answer, correct_answer)

    def test_get_set_position(self):
        on_board_pieces = OnBoardPieces()
        on_board_pieces.piece_list = PieceLoader.load_sample_one_piece_each()
        test_answer = on_board_pieces.get_set('position', 'black')
        correct_answer = {'a8', 'd7', 'f8', 'h8', 'a2'}
        Test.assertEquals(test_answer, correct_answer)

    def test_get_set_control(self):
        on_board_pieces = OnBoardPieces()
        on_board_pieces.piece_list = PieceLoader.load_sample_one_piece_each()
        test_answer = on_board_pieces.get_set('control', 'black')
        correct_answer = set()
        correct_answer |= {'e8', 'e7', 'f7', 'g7',
                           'g8'}                    # Black King
        correct_answer |= {'g8', 'h7', 'h6', 'h5', 'h4', 'h3', 'h2', 'h1',
                           'g7', 'f6', 'e5', 'd4', 'c3', 'b2', 'a1'}        # Black Queen
        correct_answer |= {'b8', 'b6', 'c5', 'e5',
                           'f6'}                    # Black Knight
        # Black Pawn
        correct_answer |= {'b1'}
        correct_answer |= {'b7', 'c6', 'd5', 'e4',
                           'f3', 'g2', 'h1'}        # Black Bishop
        Test.assertEquals(test_answer, correct_answer)


class TestPieceMovesCheckmatePosition(Test):
    """
    Checks the individual moves in the one move to checkmate position.
    If we are testing a piece of a certain color, it is a given that it is that color's move.
    The methods that end in `...one_move` are from `load_one_move_to_checkmate`.
    The methods that end in `...two_moves` are from `load_two_moves_to_checkmate`.
    """

    def test_black_king_one_move(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        test_answer = board.pieces['a8'].get_moves(board.get_board_copy())
        correct_answer = {'b8'}
        Test.assertEquals(test_answer, correct_answer)
    
    def test_black_king_checkmated(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        white_queen = board.pieces['d7']
        white_queen.set_position('a7')
        test_answer = board.pieces['a8'].get_moves(board)
        Test.assertFalse(test_answer)

    def test_black_bishop_one_move(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        test_answer = board.pieces['a6'].get_moves(board.get_board_copy())
        correct_answer = {'c8', 'b7', 'b5', 'c4', 'd3', 'e2', 'f1'}
        Test.assertEquals(test_answer, correct_answer)

    def test_white_pawn_one_move(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        test_answer = board.pieces['b6'].get_moves(board.get_board_copy())
        correct_answer = {'b7'}
        Test.assertEquals(test_answer, correct_answer)

    def test_white_queen_one_move(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        test_answer = board.pieces['d7'].get_moves(board.get_board_copy())
        correct_answer = {'d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd8',  # Up-Down
                          'a7', 'b7', 'c7', 'e7', 'f7', 'g7', 'h7',  # Left-Right
                          'e8', 'c6', 'b5', 'a4',
                          'c8', 'e6', 'f5', 'g4', 'h3'}
        Test.assertEquals(test_answer, correct_answer)

    def test_black_bishop_two_moves(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_two_moves_to_checkmate()
        test_answer = board.pieces['a6'].get_moves(board.get_board_copy())
        correct_answer = set()
        Test.assertEquals(test_answer, correct_answer)


class TestPieceMovesPawnPromotion(Test):

    def test_white_pawn_promotion(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_white_pawn_promotion()
        test_answer = board.pieces['e7'].get_moves(board.get_board_copy())
        correct_answer = {'d8Q', 'd8B', 'd8N', 'd8R', 'e8Q', 'e8B', 'e8N', 'e8R'}
        Test.assertEquals(test_answer, correct_answer)


class TestBoard(Test):
    
    def test_king_in_check_checkmate_position_black(self):
        """This should return true for black."""
        board = Board()
        board.pieces.piece_list = PieceLoader.load_checkmate()
        test_answer = board.king_in_check(False)
        Test.assertTrue(test_answer)
    
    def test_king_in_check_checkmate_position_white(self):
        """This should return false for white."""
        board = Board()
        board.pieces.piece_list = PieceLoader.load_checkmate()
        test_answer = board.king_in_check(True)
        Test.assertFalse(test_answer)
    
    def test_en_passant_square_is_set(self):
        """The black pawn moves two squares and white en passant takes."""
        board = Board()
        board.pieces.piece_list = PieceLoader.load_en_passant_position()
        turn = 2 # Black's turn
        black_pawn = board.pieces['d7']
        board.move(black_pawn, 'd5', turn)
        Test.assertEquals(test=board.en_passant, correct='d5')
    
    def test_en_passant_move_available(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_en_passant_position()
        turn = 2 # Black's turn
        black_pawn = board.pieces['d7']
        board.move(black_pawn, 'd5', turn)
        white_pawn_moves = board.pieces['e5'].get_moves(board)
        Test.assertTrue({'d6'}.issubset(white_pawn_moves))

    def test_en_passant_removes_piece(self):
        board = Board()
        board.pieces.piece_list = PieceLoader.load_en_passant_position()
        turn = 2 # Black's turn
        black_pawn = board.pieces['d7']
        white_pawn = board.pieces['e5']
        board.move(black_pawn, 'd5', turn)
        turn += 1
        board.move(white_pawn, 'd6', turn)
        Test.assertFalse('d5' in board.pieces.get_dict('identity', 'position', 'black').values())


class TestGame(Test):

    def test_select_piece_return_no_piece(self):
        game = Game()
        test_answer = game.select_piece('a5')
        correct_answer = SelectionType.NO_PIECE
        Test.assertEquals(test_answer, correct_answer)
    
    def test_select_piece_selection_set(self):
        game = Game()
        game.select_piece('a2')
        test_answer = game.piece_selection
        correct_answer = game.board.pieces['a2']
        Test.assertEquals(test_answer, correct_answer)
    
    def test_select_move_return_reselect(self):
        game = Game()
        game.select_piece('a2')
        test_answer = game.select_move('b2')
        correct_answer = SelectionType.RESELECT
        Test.assertEquals(test_answer, correct_answer)

    def test_select_move_return_no_move(self):
        game = Game()
        game.select_piece('a2')
        test_answer = game.select_move('b6')
        correct_answer = SelectionType.NO_MOVE
        Test.assertEquals(test_answer, correct_answer)

    def test_select_move_selection_set(self):
        game = Game()
        game.select_piece('a2')
        game.select_move('a3')
        Test.assertTrue(game.square_selection == 'a3')
    
    def test_move_and_next_turn_move(self):
        game = Game()
        game.select_piece('a2')
        game.select_move('a3')
        game.move_and_next_turn()
        Test.assertTrue({'a3'}.issubset(game.board.pieces.get_set('position', 'white')))       

    def test_move_and_next_turn_selection_reset(self):
        game = Game()
        game.select_piece('a2')
        game.select_move('a3')
        game.move_and_next_turn()
        Test.assertTrue(not game.piece_selection and not game.square_selection)

    def test_move_and_next_turn_turn_increment(self):
        game = Game()
        game.select_piece('a2')
        game.select_move('a3')
        game.move_and_next_turn()
        Test.assertTrue(game.turn == 2)

    def test_move_and_next_turn_returns_checkmate(self):
        game = Game()
        game.board.pieces.piece_list = PieceLoader.load_one_move_to_checkmate()
        game.select_piece('d7')
        game.select_move('a7')
        test_answer = game.move_and_next_turn()
        correct_answer = GameState.CHECKMATE
        Test.assertEquals(test_answer, correct_answer)

    def test_move_and_next_turn_returns_stalemate(self):
        game = Game()
        game.board.pieces.piece_list = PieceLoader.load_two_moves_to_checkmate()
        game.select_piece('d7')
        game.select_move('c7')
        test_answer = game.move_and_next_turn()
        correct_answer = GameState.STALEMATE
        Test.assertEquals(test_answer, correct_answer)




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        verbose_flag = True
    else:
        verbose_flag = False

    test_squares = TestSquares()
    test_squares.run_all(verbose_flag)

    test_piece_control = TestPieceControl()
    test_piece_control.run_all(verbose_flag)

    test_on_board_pieces = TestOnBoardPieces()
    test_on_board_pieces.run_all(verbose_flag)

    test_piece_moves_checkmate_position = TestPieceMovesCheckmatePosition()
    test_piece_moves_checkmate_position.run_all(verbose=verbose_flag)

    test_pawn_promotion = TestPieceMovesPawnPromotion()
    test_pawn_promotion.run_all(verbose=verbose_flag)

    test_board = TestBoard()
    test_board.run_all(verbose_flag)

    test_game = TestGame()
    test_game.run_all()
