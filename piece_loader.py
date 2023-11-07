from mdl import *

class PieceLoader:

    @staticmethod
    def load_sample_one_piece_each():
        pieces = [
            Bishop('a8', False),
            Knight('d7', False),
            Pawn('a2', False),
            King('f8', False),
            Queen('h8', False),
            King('f1', True),
            Rook('h1', True),
        ]
        return pieces

    @staticmethod
    def load_checkmate():
        pieces = [
            King('a8', False),
            Pawn('b6', True),
            Queen('a7', True),
            King('h1', True),
        ]
        return pieces

    @staticmethod
    def load_one_move_to_checkmate():
        """This loads a board where the white queen has one move to checkmate: 'a7'.
        https://lichess.org/editor/k7/3Q4/bP6/8/8/8/8/7K_w_-_-_0_1?color=white"""
        pieces = [
            King('a8', False),
            Bishop('a6', False),
            Pawn('b6', True),
            Queen('d7', True),
            King('h1', True),
        ]
        return pieces

    @staticmethod
    def load_two_moves_to_checkmate():
        """This is the same board as `load_one_move_to_checkmate`, except the white
        Queen has two moves it can use to checkmate 'a1' and 'c3'. Due to the Bishop not being
        able to block checkmate
        https://lichess.org/editor/k7/3Q4/bP6/8/8/8/8/R6K_w_-_-_0_1?color=white.
        """
        pieces = [
            King('a8', False),
            Bishop('a6', False),
            Pawn('b6', True),
            Queen('d7', True),
            King('h1', True),
            Rook('a1', True),
        ]
        return pieces

    @staticmethod
    def load_white_pawn_promotion():
        """The white pawn can promote by moving forward to 'e8' or by taking
        the rook at 'd8'.
        https://lichess.org/editor/1k1r4/4P3/8/8/8/8/8/1K6_w_-_-_0_1?color=white"""
        pieces = [
            King('b1', True),
            King('b8', False),
            Pawn('e7', True),
            Rook('d8', False),
        ]
        return pieces
    
    @staticmethod
    def load_en_passant_position():
        """If the black pawn moves to 'd5', then the white pawn at 'e5' 
        should be able to en passant take.
        https://lichess.org/editor/1k6/3p4/8/4P3/8/8/8/1K6_w_-_-_0_1?color=white"""

        pieces = [
            King('b1', True),
            King('b8', False),
            Pawn('e5', True),
            Pawn('d7', False),
        ]
        return pieces