#include <sstream>

#include "Pieces2.h"
#include "Board2.h"




std::string STAND_STRING = "Ra1wf Nb1wf Bc1wf Qd1wf Ke1wf Bf1wf Ng1wf Rh1wf Ra8bf Nb8bf Bc8bf Qd8bf Ke8bf Bf8bf Ng8bf Rh8bf pa2wf pb2wf pc2wf pd2wf pe2wf pf2wf pg2wf ph2wf pa7bf pb7bf pc7bf pe7bf pd7bf pf7bf pg7bf ph7bf";

std::vector<std::string> split(const std::string &str, char delim)
{
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string item;

    while (getline(ss, item, delim)) {
        result.push_back(item);

    }
    return result;
}


// OnBoardPieces

OnBoardPieces::OnBoardPieces()
{
    loadPiecesStandard();
}

OnBoardPieces::OnBoardPieces(std::vector<std::string> build_data)
{
    loadPiecesFromStringVector(build_data);
}

OnBoardPieces::OnBoardPieces(OnBoardPieces &mold)
{
    std::vector<Piece> piece_list{};
    std::vector<std::string> build_data = mold.boardToStringVector();
    loadPiecesFromStringVector(build_data);
}



void OnBoardPieces::loadPiecesStandard()
{
    std::vector<std::string> std_pieces = split(STAND_STRING, ' ');
    loadPiecesFromStringVector(std_pieces);

}

void OnBoardPieces::loadPiecesFromStringVector(std::vector<std::string> build_data)
{
    deleteAllPieces();
    for (auto str : build_data)
    {
        piece_list.push_back(buildPieceFromString(str));
    }
}

Piece OnBoardPieces::buildPieceFromString(std::string str)
{
    
    char piece_type = str.at(0);
    std::string piece_position = str.substr(1, 2);
    char color = str.at(3);
    bool white = (color == 'w');
    char move_flag = str.at(4);
    bool has_moved = (move_flag == 't') ? true : false;

    Piece piece(piece_type, piece_position, white, has_moved);

    return piece;
}


void OnBoardPieces::deleteAllPieces()
{
    piece_list.clear();
}

std::vector<std::string> OnBoardPieces::boardToStringVector()
{
    std::vector<std::string> build_data;
    char piece_type;
    std::string pos;
    std::string color;
    std::string move_flag;

    for (auto& piece : piece_list)
    {
        piece_type = piece.letter;
        pos = piece.position;
        color = (piece.white) ? "w" : "b";
        move_flag = (piece.has_moved) ? "t" : "f"; 
        build_data.push_back(piece_type + pos + color + move_flag);
    }
    return build_data;
}

// Accessors

std::vector<Piece*> OnBoardPieces::getPieces()
{
    std::vector<Piece*> piece_pointers;
    for (auto& p : piece_list)
    {
        piece_pointers.push_back(p.getInstance());
    }
    return piece_pointers;
}

std::vector<Piece*> OnBoardPieces::getPieces(bool white)
{
    std::vector<Piece*> pieces_by_color;
    for (auto& p : piece_list)
    {
        if (p.white == white)
        {
            pieces_by_color.push_back(p.getInstance());
        }
    }
    
    return pieces_by_color;
}

std::map<Piece*, std::unordered_set<std::string>> OnBoardPieces::getInstanceMoves(bool white, Board& board)
{
    std::map<Piece*, std::unordered_set<std::string>> map;

    int i;
    for (auto& p : piece_list)
    {
        if (p.white == white)
        {
            map[p.getInstance()] = p.getMoves(board);
        }
    }
    return map;
}

std::map<std::string, std::unordered_set<std::string>> OnBoardPieces::getIdentityMoves(bool white, Board& board)
{
    std::map<std::string, std::unordered_set<std::string>> map;
    for (auto& p : piece_list)
    {
        map[p.getIdentity()] = p.getMoves(board);
    }
    return map;
}

std::map<std::string, std::string> OnBoardPieces::getIdentityPosition()
{
    std::map<std::string, std::string> map;
    for (auto& p : piece_list)
    {
        map[p.getIdentity()] = p.getPosition();
    }
    return map;
}

std::map<std::string, std::string> OnBoardPieces::getIdentityPosition(bool white)
{
    std::map<std::string, std::string> map;
    for (auto& p : piece_list)
    {
        if (p.white == white)
        {
            map[p.getIdentity()] = p.getPosition();
        }
    }
    return map;
}


std::map<std::string, Piece*> OnBoardPieces::getPositionInstance()
{
    std::map<std::string, Piece*> map;
    std::vector<Piece*> pieces = getPieces();
    int i;
    for (auto& p : piece_list)
    {
        map[p.getPosition()] = p.getInstance();
    }
    return map;
}

std::map<std::string, Piece*> OnBoardPieces::getPositionInstance(bool white)
{
    std::map<std::string, Piece*> map;

    int i;
    for (auto&p : piece_list)
    {
        {
            map[p.getPosition()] = p.getInstance();
        }
    }
    return map;
}



std::unordered_set<std::string>OnBoardPieces::getPosition()
{
    std::unordered_set<std::string> position_set;

    for (auto& p : piece_list)
    {
        position_set.insert(p.getPosition());
    }
    return position_set;
    
}

std::unordered_set<std::string>OnBoardPieces::getPosition(bool white)
{
    std::unordered_set<std::string> position_set;
    for (auto& p : piece_list)
    {
        if (p.white == white)
        {
            position_set.insert(p.getPosition());
        }
    }
    return position_set;
}

std::unordered_set<std::string>OnBoardPieces::getControl()
{
    std::unordered_set<std::string> control_set;
    std::vector<Piece*> pieces = getPieces();
    std::unordered_set<std::string> piece_control;
    std::unordered_set<std::string>::iterator sq;

    for (auto& p : piece_list)
    {
        piece_control = p.getControlSet(getPosition(false), getPosition(true));
        for (sq=piece_control.begin(); sq != piece_control.end(); sq++)
        {
            control_set.insert((*sq));
        }
        piece_control.clear();
    }
    return control_set;


}

std::unordered_set<std::string>OnBoardPieces::getControl(bool white)
{
    std::unordered_set<std::string> control_set;
    std::vector<Piece*> pieces_by_color = getPieces(white);
    std::unordered_set<std::string> piece_control;
    std::unordered_set<std::string>::iterator sq;
    int i;

    for (auto& p : piece_list)
    {
        if (p.white == white)
        {        
            piece_control = p.getControlSet(getPosition(false), getPosition(true));
            for (sq=piece_control.begin(); sq != piece_control.end(); sq++)
            {
                control_set.insert((*sq));
            }
            piece_control.clear();
        }
    }
    return control_set;
}

Piece* OnBoardPieces::getPieceAt(std::string sq)
{
    int i;

    for (auto& p : piece_list)
    {
        if (p.getPosition() == sq)
        {
            return p.getInstance();
        }
    }
    return nullptr;
}

std::string OnBoardPieces::getKingPosition(bool white)
{
    
    for (auto &p : piece_list)
    {
        if ((p.letter == 'K') && (p.white == white))
        {
            return p.getPosition();
        }
    }
    return std::string();
}

// Mutators
void OnBoardPieces::removePieceAt(std::string sq)
{
    int i;
    for (i=0; i < piece_list.size(); i++)
    {
        if (piece_list[i].getPosition() == sq)
        {
            piece_list.erase(piece_list.begin() + i);
            break;
        }
    }
    
}




// Board

// Board::Board(Board& old_board)
// {
//     std::vector<std::string> build_data = old_board.pieces.boardToStringVector();
//     pieces.deleteAllPieces();
//     pieces.loadPiecesFromStringVector(build_data);

// }

bool Board::kingInCheck(bool white)
{
    std::string king_location = pieces.getKingPosition(white);
    std::unordered_set<std::string> opponent_control = pieces.getControl(!white);
    
    if (opponent_control.find(king_location) == opponent_control.end())
    {
        return false;
    }
    else
    {
        return true;
    }

}

void Board::promote(std::string square, char promote_to, bool white)
{
    pieces.removePieceAt(square);
    Piece piece(promote_to, square, true);
    pieces.piece_list.push_back(piece);
    

}


MoveType Board::determineMoveType(Piece* piece, std::string square)
{
    char en_passant_start, en_passant_end;
    std::string en_passant_take;
    en_passant_start = (piece->white) ? '2' : '7';
    en_passant_end = (piece->white) ? '4' : '5';
    en_passant_take = (piece->white) ? squares.up(en_passant) : squares.down(en_passant);
    
    
    if (square == "O-O" || square == "O-O-O") 
        {return CASTLE;}
    else if (piece->letter == 'p')
    {
        if (piece->getPosition()[1] == en_passant_start && square[1] == en_passant_end)
        {
            return EN_PASSANT_SET;
        }
        else if (square == en_passant_take) 
            {return EN_PASSANT_TAKE;}
        else if (square.size() == 3) 
            {return PROMOTION;}
        else 
            {return STANDARD;}
    }
    else
        {return STANDARD;}
}


void Board::setEnPassant(std::string square)
{
    en_passant = square;
}


void Board::handlePromotion(Piece* piece, std::string square)
{
    std::string mv = square.substr(0, 2);
    char promotion_letter = square.at(2);
    std::unordered_set<std::string> opponent_postion = pieces.getPosition(!piece->white);
    
    if (opponent_postion.find(mv) != opponent_postion.end())
        {pieces.removePieceAt(mv);}
    piece->setPosition(mv);
    promote(mv, promotion_letter, piece->white);
}


void Board::handleCastling(Piece* piece, std::string square)
{
    std::string short_castle = "O-O";
    
    if (square == short_castle)
    {
        if (piece->white)
        {
            piece->setPosition("g1");
            pieces.getPieceAt("h1")->setPosition("f1");
        }
        else
        {
            piece->setPosition("g8");
            pieces.getPieceAt("h8")->setPosition("f8");          
        }
    }
    else
        {
        if (piece->white)
        {
            piece->setPosition("c1");
            pieces.getPieceAt("a1")->setPosition("d1");
        }
        else
        {
            piece->setPosition("c8");
            pieces.getPieceAt("a8")->setPosition("d8");          
        }
    } 
}

void Board::handleEnPassantTake(Piece* piece, std::string square)
{
    pieces.removePieceAt(en_passant);
    piece->setPosition(square);
}


void Board::move(Piece* piece, std::string square)
{
    MoveType move_type = determineMoveType(piece, square);
    std::unordered_set<std::string> opponent_postion = pieces.getPosition(!piece->white);
    std::string none = "";

    switch (move_type)
    {
        case STANDARD:
            if (opponent_postion.find(square) != opponent_postion.end())
                {pieces.removePieceAt(square);}
            piece->setPosition(square);
            setEnPassant(none);
            break;
        case CASTLE:
            handleCastling(piece, square);
            setEnPassant(none);
            break;
        case EN_PASSANT_SET:
            piece->setPosition(square);
            setEnPassant(square);
            break;
        case EN_PASSANT_TAKE:
            handleEnPassantTake(piece, square);
            setEnPassant(none);
            break;
        case PROMOTION:
            handlePromotion(piece, square);
            setEnPassant(none);
    }
}