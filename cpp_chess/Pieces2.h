#pragma once

#include <array>
#include <string>
#include <tuple>
#include <optional>
#include <unordered_set>

class OnBoardPieces;
class Board;


class Square
{
    public:
        std::array<std::array<std::string, 8>, 8> squares;
        std::tuple<int, int> none_tuple = std::make_tuple(-1, -1);

        Square();
        std::tuple <int, int> get_row_col(const std::string sq);
        std::string up(const std::string sq);
        std::string down(const std::string sq);
        std::string left(const std::string sq);
        std::string right(const std::string sq);
};

bool anyIsIn(std::unordered_set<std::string> any, std::unordered_set<std::string> check);

class Piece
{
    public:
        Square squares;
        std::string position;
        bool white;
        char letter;
        int points;
        bool has_moved = false;

        Piece(char letter, std::string position, bool white);
        Piece(char letter, std::string position, bool white, bool has_moved);

        void setPoints();

        std::unordered_set<std::string> getControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);
        std::unordered_set<std::string> getMoves(Board& board);
        std::unordered_set<std::string> returnMovesWithoutKingInCheck(std::unordered_set<std::string> moves_to_check, Board& board);


        // Knight
        std::unordered_set<std::string> knightControlSet(std::unordered_set<std::string>black_position, \
        std::unordered_set<std::string> white_position);

        // Bishop
        std::unordered_set<std::string> bishopControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);        

        // Rook
        std::unordered_set<std::string> rookControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);

        // Queen
        std::unordered_set<std::string> queenControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);


        // King
        std::unordered_set<std::string> kingControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);
        std::unordered_set<std::string> addCastling(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position, Board& board);
        std::unordered_set<std::string> kingMoves(Board& board);

        // Pawn
        std::unordered_set<std::string> pawnControlSet(std::unordered_set<std::string>black_position, \
            std::unordered_set<std::string> white_position);
         std::unordered_set<std::string> pawnMoves(Board& board);
        std::unordered_set<std::string> addPromotionLettersToMove(std::string move);        


        // Accessors
        const std::string getIdentity();
        Piece* getInstance();
        const std::string getPosition();
        
        //Mutators
        void setPosition(std::string sq);
};


