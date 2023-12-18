#pragma once

#include <vector>
#include <map>
#include <unordered_set>
#include <memory>


#include "Pieces2.h"




class OnBoardPieces
{
    public:
        std::vector<Piece> piece_list;

        OnBoardPieces();
        OnBoardPieces(std::vector<std::string> build_data);
        OnBoardPieces(OnBoardPieces &mold);
        // OnBoardPieces& operator= (OnBoardPieces&) = delete;
    

        void loadPiecesStandard();
        void loadPiecesFromStringVector(std::vector<std::string> build_data);
        Piece buildPieceFromString(std::string str);
        std::vector<std::string> boardToStringVector();
        void deleteAllPieces();

        // Accessors
        Piece* getPieceAt(std::string sq);
        std::vector<Piece*> getPieces();
        std::vector<Piece*> getPieces(bool white);
        std::map<Piece*, std::unordered_set<std::string>> getInstanceMoves(bool white, Board& board);
        std::map<std::string, std::unordered_set<std::string>> getIdentityMoves(bool white, Board& board);
        std::map<std::string, std::string> getIdentityPosition();
        std::map<std::string, std::string> getIdentityPosition(bool white);
        std::map<std::string, Piece*> getPositionInstance();
        std::map<std::string, Piece*> getPositionInstance(bool white);
        std::unordered_set<std::string>getControl();
        std::unordered_set<std::string>getControl(bool white);
        std::unordered_set<std::string>getPosition();
        std::unordered_set<std::string>getPosition(bool white);
        std::string getKingPosition(bool white);

        // Mutators
        void removePieceAt(std::string sq);

};


enum MoveType
{
    STANDARD,
    CASTLE,
    PROMOTION,
    EN_PASSANT_SET,
    EN_PASSANT_TAKE,
};


class Board
{
    public:
        Square squares;
        OnBoardPieces pieces;
        std::string en_passant;

        Board(){};
        // Board(Board& old_board);
        bool kingInCheck(bool white);
        void move(Piece* piece, std::string square);
        MoveType determineMoveType(Piece* piece, std::string square);
        void setEnPassant(std::string square);
        void handlePromotion(Piece* piece, std::string square);
        void handleCastling(Piece* piece, std::string square);
        void handleEnPassantTake(Piece* piece, std::string square);
        void promote(std::string square, char promote_to, bool white);

};