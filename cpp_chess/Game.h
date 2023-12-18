#pragma once


#include "Pieces2.h"
#include "Board2.h"

enum GameState
{
    PLAY,
    CHECKMATE,
    STALEMATE,
};



class Game
{

    

    public:
        Board board;
        unsigned int turn;
        Piece* piece_selection;
        std::string square_selection;

        Game();


        bool determineColor();
        bool isCheckmate();
        bool isStalemate();
        void selectPiece(std::string square);
        void selectMove(std::string square);
        GameState moveAndNextTurn();
        int eval(bool color);
};