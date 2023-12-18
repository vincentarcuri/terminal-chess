#include <map>
#include <algorithm>

#include "Game.h"


Game::Game()
{
    this->turn = 1;
    this->piece_selection = nullptr;
    this->square_selection = "";
}


bool Game::determineColor()
{
    return static_cast<bool>(turn % 2);
}

bool Game::isCheckmate()
{
    bool color = determineColor();
    bool any_moves = false;
    bool king_in_check = board.kingInCheck(color);
    
    std::map<std::string, std::unordered_set<std::string>> all_moves = board.pieces.getIdentityMoves(color, board);

    // Determine if player has any moves.
    for (auto itr = all_moves.begin(); itr != all_moves.end(); itr++)
    {
        if (!itr->second.empty())
        {
            any_moves = true;
            break;
        }
    }
    if (!any_moves && king_in_check)
    {
        return true;
    }
    else
    {
        return false;
    }
}


bool Game::isStalemate()
{
    bool color = determineColor();
    bool any_moves = false;
    bool king_in_check = board.kingInCheck(color);
    
    std::map<std::string, std::unordered_set<std::string>> all_moves = board.pieces.getIdentityMoves(color, board);

    // Determine if player has any moves.
    for (auto itr = all_moves.begin(); itr != all_moves.end(); itr++)
    {
        if (!itr->second.empty())
        {
            any_moves = true;
            break;
        }
    }
    if (!any_moves && !king_in_check)
    {
        return true;
    }
    else
    {
        return false;
    }   
}

void Game::selectPiece(std::string square)
{
    piece_selection = board.pieces.getPieceAt(square);

}

void Game::selectMove(std::string square)
{
    square_selection = square;
}

GameState Game::moveAndNextTurn()
{
    if (piece_selection && !square_selection.empty())
    {
        board.move(piece_selection, square_selection);
    }
    turn++;
    piece_selection = nullptr;
    square_selection = "";
    if (isStalemate()) 
        {return STALEMATE;}
    else if (isCheckmate()) 
        {return CHECKMATE;}
    else 
        {return PLAY;}
}

int Game::eval(bool color)
{
    int white_points{0};
    int black_points{0};
    // int white_control = board.pieces.getControl(true).size();
    // int black_control = board.pieces.getControl(true).size();


    std::vector<Piece*> white_pieces = board.pieces.getPieces(true);
    std::vector<Piece*> black_pieces = board.pieces.getPieces(false);

    for (auto& piece : white_pieces)
    {
        white_points += piece->points;
    }
    for (auto& piece : black_pieces)
    {
        black_points += piece->points;
    }
    // Iterate over pieces in players control and count the points
    int points_in_white_control{0};
    int points_in_black_control{0};
    std::unordered_set<std::string> white_control_set = board.pieces.getControl(true);
    std::unordered_set<std::string> black_control_set = board.pieces.getControl(false); 
    for (auto sq : white_control_set)
    {
        Piece* piece = board.pieces.getPieceAt(sq);
        if (piece != nullptr)
        {
            points_in_white_control += piece->points;
        }
    }
        for (auto sq : black_control_set)
    {
        Piece* piece = board.pieces.getPieceAt(sq);
        if (piece != nullptr)
        {
            points_in_black_control += piece->points;
        }
    } 
 

    if (color)
    {
        return 3*(white_points - black_points) + (points_in_white_control - points_in_black_control); //+ (white_control - black_control);
    }
    else
    {
        return 3*(black_points - white_points) + (points_in_black_control - points_in_white_control); //+ (black_control - white_control);
    }
}