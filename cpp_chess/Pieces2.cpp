#include <array>
#include <string>
#include <tuple>
#include <optional>
#include <unordered_set>
#include <iostream>


#include "Pieces2.h"
#include "Board2.h"

Square::Square()
{
    squares = {{
        {"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"},
        {"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"},
        {"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"},
        {"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"},
        {"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"},
        {"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"},
        {"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"},
        {"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"},
    }};
}

std::tuple <int, int> Square::get_row_col(const std::string sq)
{
    for (int row = 0; row < squares.size(); row++)
    {
        for (int col = 0; col < squares[row].size(); col++)
        {
            if (squares[row][col] == sq) {return std::make_tuple(row, col);}
        }
        
    }
    return none_tuple;  
}

std::string Square::up(const std::string sq)
{
    if (sq.empty()) {
        return std::string();
    }
    std::tuple<int, int> row_col = get_row_col(sq);
    int row = std::get<0>(row_col); 
    int col = std::get<1>(row_col);
    --row;
    return (row >= 0) ? squares[row][col] : std::string();
}

std::string Square::down(const std::string sq)
{
    if (sq.empty()) 
    {
        return std::string();
    }
    std::tuple<int, int> row_col = get_row_col(sq);
    int row = std::get<0>(row_col); 
    int col = std::get<1>(row_col);
    ++row;
    return (row <= 7) ? squares[row][col] : std::string();
}

std::string Square::left(const std::string sq)
{
    if (sq.empty()) 
    {
        return std::string();
    }
    std::tuple<int, int> row_col = get_row_col(sq);
    int row = std::get<0>(row_col); 
    int col = std::get<1>(row_col);
    --col;
    return (col >= 0) ? squares[row][col] : std::string();
}

std::string Square::right(const std::string sq)
{
    if (sq.empty()) 
    {
        return std::string();
    }
    std::tuple<int, int> row_col = get_row_col(sq);
    int row = std::get<0>(row_col); 
    int col = std::get<1>(row_col);
    ++col;
    return (col <= 7) ? squares[row][col] : std::string();
}

bool anyIsIn(std::unordered_set<std::string> search_vars, std::unordered_set<std::string> search_space) 
{
    std::unordered_set<std::string>::iterator itr;
    for (itr = search_vars.begin(); itr != search_vars.end(); itr++)
    {
        if (search_space.find((*itr)) != search_space.end())
            {return true;}
    }
    return false;
}



// Piece


// Constructors
Piece::Piece(char letter, std::string position, bool white)
{
    this->letter = letter;
    this->position = position;
    this->white = white;
    setPoints(); 
}

Piece::Piece(char letter, std::string position, bool white, bool has_moved)
{
    this->letter = letter;
    this->position = position;
    this->white = white;
    this->has_moved = has_moved;
    setPoints(); 
}

void Piece::setPoints()
{
    switch(letter)
    {
        case 'p':
            this->points = 1;
            break;
        case 'N':
            this->points = 3;
            break;
        case 'B':
            this->points = 3;
            break;
        case 'R':
            this->points = 5;
            break;
        case 'Q':
            this->points = 9;
            break;
        case 'K':
            this->points = 0;
            break;
    }
}

std::unordered_set<std::string> Piece::getControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    switch (letter)
    {
        case 'p':
            control_set = pawnControlSet(black_position, white_position);
            break;
        case 'N':
            control_set = knightControlSet(black_position, white_position);
            break;
        case 'B':
            control_set = bishopControlSet(black_position, white_position);
            break;
        case 'R':
            control_set = rookControlSet(black_position, white_position);
            break;
        case 'Q':
            control_set = queenControlSet(black_position, white_position);
            break;
        case 'K':
            control_set = kingControlSet(black_position, white_position);
            break;
    }
    return control_set;
}


std::unordered_set<std::string> Piece::getMoves(Board& board)
{
    std::unordered_set<std::string> move_set;
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;

    black_position = board.pieces.getPosition(false);
    white_position = board.pieces.getPosition(true);
    control_set = getControlSet(black_position, white_position);

    switch (letter)
    {
        case 'p':
            move_set = pawnMoves(board);
            break;
        case 'K':
            move_set = kingMoves(board);
            break;
        default:
            move_set = returnMovesWithoutKingInCheck(control_set, board);
            break;
    }

    return move_set;
}

std::unordered_set<std::string> Piece::returnMovesWithoutKingInCheck(std::unordered_set<std::string> moves_to_check, Board& board)
{
    std::unordered_set<std::string> move_set;
    std::unordered_set<std::string>::iterator move;
    for (move=moves_to_check.begin(); move != moves_to_check.end(); move++)
    {
        //Board board_copy{board};
        Board board_copy = Board{board};
        Piece* self_copy = board_copy.pieces.getPieceAt(getPosition());
        board_copy.move(self_copy, (*move));
        if (!board_copy.kingInCheck(white))
        {
            move_set.insert((*move));
        }
    }
    
    return move_set;
}

// Knight
std::unordered_set<std::string> Piece::knightControlSet(std::unordered_set<std::string>black_position, \
std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> moves_to_remove;
    std::unordered_set<std::string>::iterator move_itr;
    std::string up2, down2, left2, right2;
    up2 = squares.up(squares.up(position));
    down2 = squares.down(squares.down(position));
    left2 = squares.left(squares.left(position));
    right2 = squares.right(squares.right(position));
    std::vector<std::string> all_combos {
        squares.left(up2),
        squares.right(up2),
        squares.left(down2),
        squares.right(down2),
        squares.up(left2),
        squares.up(right2),
        squares.down(left2),
        squares.down(right2),
    };
    // Add all_combos to control set if string not empty
    std::string sq;
    for (auto i : all_combos)
    {
        sq = i;
        if (!sq.empty())
        {
            control_set.insert(sq);
        }
    }
    // Remove all squares from control_set that are in it's own position.
    moves_to_remove = (white) ? white_position : black_position;
    for (move_itr=moves_to_remove.begin(); move_itr != moves_to_remove.end(); move_itr++)
    {
        control_set.erase((*move_itr));
    }
    return control_set;
}


// Bishop
std::unordered_set<std::string> Piece::bishopControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> opponent_position;
    std::unordered_set<std::string> player_position;
    std::string sq;

    opponent_position = (!white) ? white_position : black_position;
    player_position = (white) ? white_position : black_position;

    // Up-Left
    sq = squares.up(squares.left(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(squares.left(sq));
    }
    // Up-Right
    sq = squares.up(squares.right(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(squares.right(sq));
    }
    // Down-Left
    sq = squares.down(squares.left(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(squares.left(sq));
    }
    // Down-Right
    sq = squares.down(squares.right(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(squares.right(sq));
    }
    return control_set;
}

// Rook
std::unordered_set<std::string> Piece::rookControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> opponent_position;
    std::unordered_set<std::string> player_position;
    std::string sq;

    opponent_position = (!white) ? white_position : black_position;
    player_position = (white) ? white_position : black_position;

    // Up
    sq = squares.up(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(sq);
    }
    // Down
    sq = squares.down(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(sq);
    }
    // Left
    sq = squares.left(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.left(sq);
    }
    // Right
    sq = squares.right(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.right(sq);
    }
    return control_set;
}

// Queen
std::unordered_set<std::string> Piece::queenControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> opponent_position;
    std::unordered_set<std::string> player_position;
    std::string sq;

    opponent_position = (!white) ? white_position : black_position;
    player_position = (white) ? white_position : black_position;

        // Up
    sq = squares.up(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(sq);
    }
    // Down
    sq = squares.down(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(sq);
    }
    // Left
    sq = squares.left(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.left(sq);
    }
    // Right
    sq = squares.right(position);
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.right(sq);
    }
    // Up-Left
    sq = squares.up(squares.left(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(squares.left(sq));
    }
    // Up-Right
    sq = squares.up(squares.right(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.up(squares.right(sq));
    }
    // Down-Left
    sq = squares.down(squares.left(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(squares.left(sq));
    }
    // Down-Right
    sq = squares.down(squares.right(position));
    while (!sq.empty() && (player_position.find(sq) == player_position.end()))
    {
        control_set.insert(sq);
        if (opponent_position.find(sq) != opponent_position.end())
            {break;}
        sq = squares.down(squares.right(sq));
    }
    return control_set;
}

// King

std::unordered_set<std::string> Piece::kingControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> player_position;
    std::vector<std::string> possible_moves;
    std::string sq;

    player_position = (white) ? white_position : black_position;

    possible_moves = {
        squares.up(position),
        squares.down(position),
        squares.right(position),
        squares.left(position),
        squares.up(squares.left(position)),
        squares.up(squares.right(position)),
        squares.down(squares.left(position)),
        squares.down(squares.right(position)),
    };

    for (auto sq : possible_moves)
    {
        if (!sq.empty() && (player_position.find(sq) == player_position.end()))
            {control_set.insert(sq);}
    }
    return control_set;
}

std::unordered_set<std::string> Piece::addCastling(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position, Board& board)
{
    std::unordered_set<std::string> castle_moves;
    std::unordered_set<std::string> opponent_control;
    std::unordered_set<std::string> player_position;
    std::string short_castle_rook_loc = (white) ? "h1" : "h8";
    std::string long_castle_rook_loc = (white) ? "a1" : "a8";
    // Get the piece at the castle locations, and then cast to Rook pointer if possible.
    Piece* short_castle_rook = board.pieces.getPieceAt(short_castle_rook_loc);
    Piece* long_castle_rook = board.pieces.getPieceAt(long_castle_rook_loc);


    std::unordered_set<std::string> short_safe;
    std::unordered_set<std::string> long_safe;
    std::unordered_set<std::string> long_unoccupied;
    if (white)
    {
        short_safe = {"e1", "f1", "g1"};
        long_safe = {"e1", "d1", "c1"};
        long_unoccupied = {"e1", "d1", "c1", "b1"};
    }
    else
    {
        short_safe = {"e1", "f1", "g1"};
        long_safe = {"e1", "d1", "c1"};
        long_unoccupied = {"e1", "d1", "c1", "b1"};
    }
    // Check for castling.
    opponent_control = board.pieces.getControl(!white);
    player_position = (white) ? white_position : black_position;
    

    if (!has_moved)
    {
        if ((short_castle_rook != nullptr) && (!anyIsIn(short_safe, opponent_control)) 
            && (!anyIsIn(short_safe, player_position)))
        {
            if ((!short_castle_rook->has_moved) && (short_castle_rook->letter == 'R') && (short_castle_rook->white == white))
                {castle_moves.insert("O-O");}
        }
        if ((long_castle_rook != nullptr) && (!anyIsIn(long_safe, opponent_control)) 
            && (!anyIsIn(long_unoccupied, player_position)))
        {
            if ((!long_castle_rook->has_moved) && (long_castle_rook->letter == 'R') && (long_castle_rook->white == white))
                {castle_moves.insert("O-O-O");}
        }
    }

    return castle_moves;
}

std::unordered_set<std::string> Piece::kingMoves(Board& board)
{
    std::unordered_set<std::string> move_set;
    std::unordered_set<std::string> control_set;
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string>::iterator itr;
    
    // Get standard moves.
    black_position = board.pieces.getPosition(false);
    white_position = board.pieces.getPosition(true);
    control_set = kingControlSet(black_position, white_position);

    std::unordered_set<std::string> castle_moves = addCastling(black_position, white_position, board);
    // for (itr=castle_moves.begin(); itr != castle_moves.end(); itr++)
    // {
    //     control_set.insert((*itr));
    // }

    for (auto cm : castle_moves)
    {
        control_set.insert(cm);
    }

    move_set = returnMovesWithoutKingInCheck(control_set, board);
    return move_set;

}

// Pawn
std::unordered_set<std::string> Piece::pawnControlSet(std::unordered_set<std::string>black_position, \
    std::unordered_set<std::string> white_position)
{
    std::unordered_set<std::string> control_set;
    std::string left_diagonal;
    std::string right_diagonal;

    if (white)
    {
        left_diagonal = squares.up(squares.left(position));
        right_diagonal = squares.up(squares.right(position)); 
    }
    else
    {
        left_diagonal = squares.down(squares.left(position));
        right_diagonal = squares.down(squares.right(position)); 
    }
    if (!left_diagonal.empty())
        {control_set.insert(left_diagonal);}
    if (!right_diagonal.empty())
        {control_set.insert(right_diagonal);}
    return control_set;
}



std::unordered_set<std::string> Piece::pawnMoves(Board& board)
{
    std::unordered_set<std::string> moves_to_check;
    std::unordered_set<std::string>::iterator itr;
    std::unordered_set<std::string>::iterator p_itr;
    std::unordered_set<std::string> promote_moves;
    std::unordered_set<std::string> en_passant_squares;

    std::unordered_set<std::string> all_position = board.pieces.getPosition();
    std::unordered_set<std::string> player_position = board.pieces.getPosition(white);
    std::unordered_set<std::string> opponent_position = board.pieces.getPosition(!white);
    char starting_position = (white) ? '2' : '7';
    char promotion_position = (white) ? '8' : '1';
    std::string forward_move = (white) ? squares.up(position) : squares.down(position);
    std::string dbl_forward_move = (white) ? squares.up(forward_move) : squares.down(forward_move);
    std::unordered_set<std::string> take_moves = getControlSet(board.pieces.getPosition(false), board.pieces.getPosition(true));

    // Add Forward Moves
    if (all_position.find(forward_move) == all_position.end())
    {
        if (position.at(1) == starting_position && (all_position.find(dbl_forward_move) == all_position.end()))
        {       
                moves_to_check.insert(forward_move);
                moves_to_check.insert(dbl_forward_move);
        }
        else if (forward_move.at(1) == promotion_position)
        {
            std::unordered_set<std::string>promote_moves = addPromotionLettersToMove(forward_move);
            for (p_itr=promote_moves.begin(); p_itr != promote_moves.end(); p_itr++)
            {
                moves_to_check.insert((*p_itr));
            }
        }
        else
        {
            moves_to_check.insert(forward_move);
        }
    }
    // Add take moves if in opponent position
    for (itr=take_moves.begin(); itr != take_moves.end(); itr++)
    {
        if (opponent_position.find((*itr)) != opponent_position.end())
        {
            if ((*itr).at(1) == promotion_position)
            {
                std::unordered_set<std::string>promote_moves = addPromotionLettersToMove(forward_move);
                for (p_itr=promote_moves.begin(); p_itr != promote_moves.end(); p_itr++)
                {
                    moves_to_check.insert((*p_itr));
                }
            }
            else 
            {
                moves_to_check.insert((*itr));
            }
        }
    }
    // Add en passant
    if (!board.en_passant.empty())
    {
        en_passant_squares.insert(squares.right(board.en_passant));
        en_passant_squares.insert(squares.left(board.en_passant));

        for (itr=en_passant_squares.begin(); itr != en_passant_squares.end(); itr++)
        {
            if ((*itr) == position)
            {
                std::string en_passant_take = (white) ? squares.up(board.en_passant) : squares.down(board.en_passant);
                moves_to_check.insert((*itr));
            }
        }
    }
    return returnMovesWithoutKingInCheck(moves_to_check, board);
}

std::unordered_set<std::string> Piece::addPromotionLettersToMove(std::string move)
{
    std::unordered_set<std::string> promotion_moves;
    promotion_moves.insert(move + "Q");
    promotion_moves.insert(move + "R");
    promotion_moves.insert(move + "B");
    promotion_moves.insert(move + "N");

    return promotion_moves;
}

// Accessors
const std::string Piece::getIdentity()
{
    return letter + position;
}

Piece* Piece::getInstance()
{
    return this;
}
const std::string Piece::getPosition()
{
    return position;
}


//Mutators
void Piece::setPosition(std::string sq)
{
    has_moved = true;
    position = sq;
}
