#include <iostream>


#include "Pieces2.h"
#include "Board2.h"
#include "Game.h"
#include "search.h"


// Test Functions
void test_true(std::string name, bool test)
{
    std::cout << name;
    if (test)
    {
        std::cout << "---->\tOK\n";
    }
    else 
    {
        std::cout << "\tFAILED\n";
        std::cout << "\texpected: TRUE, answer: FALSE\n";
    }    
}




void test_string_vectors(std::string name, std::vector<std::string>test, std::vector<std::string>correct)
{
    std::cout << name;
    if (test == correct)
    {
        std::cout << "---->\tOK\n";
    }
    else 
    {
        std::cout << "\tFAILED\n";
        std::cout << "\tCorrect: "; 
        for (auto s : correct)
        {
            std::cout << s << " ";
        }
        std::cout << "\n\t!= Test: "; 
        for (auto s : correct)
        {
            std::cout << s << " ";
        }
        std::cout << "\n"; 
    }    
}

void test_string_vectors_neq(std::string name, std::vector<std::string>test, std::vector<std::string>correct)
{
    std::cout << name;
    if (test != correct)
    {
        std::cout << "---->\tOK\n";
    }
    else 
    {
        std::cout << "\tFAILED\n";
        std::cout << "\tCorrect: "; 
        for (auto s : correct)
        {
            std::cout << s << " ";
        }
        std::cout << "\n\t == Test: "; 
        for (auto s : correct)
        {
            std::cout << s << " ";
        }
        std::cout << "\n"; 
    }    
}

void test_string_sets(std::string name, std::unordered_set<std::string>test, std::unordered_set<std::string>correct)
{
    std::cout << name;
    if (test == correct)
    {
        std::cout << "---->\tOK\n";
    }
    else 
    {
        std::cout << "\tFAILED\n";
        std::cout << "\n\tCorrect: "; 
        for (auto s : correct)
        {
            std::cout << s << " ";
        }
        std::cout << "\n\tTest: "; 
        for (auto s : test)
        {
            std::cout << s << " ";
        }
        std::cout << "\n"; 
    }    
}

// Test Squares
void SquareTest()
{
    Square squares;
    std::vector<std::string> list_of_squares {
        "a1", "a8", "h1", "h8", "c5",
    };
    std::vector<std::string> test_vector;
    std::vector<std::string> correct_vector;
    // UP
    for (auto sq : list_of_squares)
    {
        test_vector.push_back(squares.up(sq));
    }
    correct_vector = {"a2", "", "h2", "", "c6"};
    test_string_vectors("Squares Up Test", test_vector, correct_vector);
    // Down
    correct_vector.clear();
    test_vector.clear();
    for (auto sq : list_of_squares)
    {
        test_vector.push_back(squares.down(sq));
    }
    correct_vector = {"", "a7", "", "h7", "c4"};
    test_string_vectors("Squares Down Test", test_vector, correct_vector);
    correct_vector.clear();
    test_vector.clear();
    // Right
    for (auto sq : list_of_squares)
    {
        test_vector.push_back(squares.right(sq));
    }
    correct_vector = {"b1", "b8", "", "", "d5"};
    test_string_vectors("Squares Right Test", test_vector, correct_vector);
    correct_vector.clear();
    test_vector.clear();
    // Left
    for (auto sq : list_of_squares)
    {
        test_vector.push_back(squares.left(sq));
    }
    correct_vector = {"", "", "g1", "g8", "b5"};
    test_string_vectors("Squares Left Test", test_vector, correct_vector);
}

// Test Piece Control

void test_pawns_control(std::string NAME)
{

    // Test Pawns
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Piece black_pawn('p', "e5", false);
    black_position = {"e5", "f8"};
    white_position = {"f1"};
    test_answer = black_pawn.getControlSet(black_position, white_position);
    correct_answer = {"d4", "f4"};
    test_string_sets(NAME + "Black Pawn", test_answer, correct_answer);
    black_position.clear();
    white_position.clear();
    test_answer.clear();
    correct_answer.clear();

    Piece white_pawn('p', "a3", true);
    black_position = {"f8"};
    white_position = {"a3", "f1"};
    test_answer = white_pawn.getControlSet(black_position, white_position);
    correct_answer = {"b4"};
    test_string_sets(NAME + "white pawn", test_answer, correct_answer);

}

void test_rook_control(std::string NAME)
{
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    // Black Rook
    Piece black_rook('R', "c7", false);
    black_position = {"f8", "c7"};
    white_position = {"f1"};
    test_answer = black_rook.getControlSet(black_position, white_position);
    correct_answer = {"c1", "c2", "c3", "c4", "c5", "c6",
                          "c8", "a7", "b7", "d7", "e7", "f7", "g7", "h7"};
    test_string_sets(NAME + "Black rook", test_answer, correct_answer);
    black_position.clear();
    white_position.clear();
    test_answer.clear();
    correct_answer.clear();
}


void test_bishop_control(std::string NAME)
{
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Piece black_bishop('B', "a6", false);
    black_position = {"f8", "a6"};
    white_position = {"f1"};
    test_answer = black_bishop.getControlSet(black_position, white_position);
    correct_answer = {"c8", "b7", "b5", "c4", "d3", "e2", "f1"};
    test_string_sets(NAME + "Black Bishop", test_answer, correct_answer);
}

void test_knight_control(std::string NAME)
{
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Piece black_knight('N', "e3", false);
    black_position = {"f8", "e3"};
    white_position = {"f1"};
    test_answer = black_knight.getControlSet(black_position, white_position);
    correct_answer = {"d1", "f1", "g2", "g4", "f5", "d5", "c4", "c2"};
    test_string_sets(NAME + "Black Knight", test_answer, correct_answer);
}

void test_queen_control(std::string NAME)
{
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Piece white_queen('Q', "f4", true);
    black_position = {"f8"};
    white_position = {"f1"};
    test_answer = white_queen.getControlSet(black_position, white_position);
    correct_answer = {"f2", "f3", "f5", "f6", "f7", "f8",  // UP-DOWN
                          "a4", "b4", "c4", "d4", "e4", "g4", "h4", // LEFT-RIGHT
                          "b8", "c7", "d6", "e5", "g3", "h2",  // Left diagonal
                          "c1", "d2", "e3", "g5", "h6"};  // Right Diagonal
    test_string_sets(NAME + "White queen", test_answer, correct_answer);
}

void test_king_control(std::string NAME)
{
    std::unordered_set<std::string> black_position;
    std::unordered_set<std::string> white_position;
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Piece white_king('K', "f1", true);
    black_position = {"f8"};
    white_position = {"f1"};
    test_answer = white_king.getControlSet(black_position, white_position);
    correct_answer = {"e1", "e2", "f2", "g2", "g1"};
    test_string_sets(NAME + "White King", test_answer, correct_answer);

}


void PieceControl()
{
    
    std::string NAME = "Piece Control() - ";
    test_pawns_control(NAME);
    test_rook_control(NAME);
    test_knight_control(NAME);
    test_bishop_control(NAME);
    test_queen_control(NAME);
    test_king_control(NAME);
}


// Test OnBoardPieces
void test_piece_removal_by_ptr(std::string NAME)
{
    OnBoardPieces on_board_pieces;
    on_board_pieces.removePieceAt("a1");
    Piece* piece = on_board_pieces.getPieceAt("a1");
    bool test = (piece == nullptr) ? true : false;
    test_true(NAME + "Test removing by pointer", test);
}

void test_piece_removal_by_board_to_string_vector(std::string NAME)
{
    std::vector<std::string> test_answer;
    std::vector<std::string> incorrect_answer;
    OnBoardPieces on_board_pieces;
    incorrect_answer = on_board_pieces.boardToStringVector();
    on_board_pieces.removePieceAt("a1");
    test_answer = on_board_pieces.boardToStringVector();
    test_string_vectors_neq(NAME + "Removal String Vectors", test_answer, incorrect_answer);
}

void test_getting_all_pieces(std::string NAME)
{
    std::vector<std::string> test_answer;
    std::vector<std::string> correct_answer;
    std::vector<Piece> to_test;
    
    OnBoardPieces on_board_pieces;
    to_test = {Piece('K', "a1", false), Piece('K', "a4", true)};
    on_board_pieces.piece_list = to_test;
    for (auto p : to_test)
    {
        correct_answer.push_back(p.getIdentity());
    }
    std::vector<Piece*> piece_ptrs = on_board_pieces.getPieces();
    for (auto p : piece_ptrs)
    {
        test_answer.push_back(p->getIdentity());
    }
    test_string_vectors(NAME + "Retrieving Pieces", test_answer, correct_answer);

}

void OnBoard()
{
    std::string NAME = "OnBoard() - ";
    test_piece_removal_by_ptr(NAME);
    test_piece_removal_by_board_to_string_vector(NAME);
    test_getting_all_pieces(NAME);
}

// Test Piece Moves, One Move to Checkmate
std::vector<std::string> LOAD_ONE_MOVE_TO_CHECKMATE {
    "Ka8bf",
    "Ba6bf",
    "pb6wf",
    "Qd7wf",
    "Kh1wf",
};

void test_black_king_one_move(std::string NAME)
{
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Board board;
    board.pieces.deleteAllPieces();
    board.pieces.loadPiecesFromStringVector(LOAD_ONE_MOVE_TO_CHECKMATE);
    test_answer = board.pieces.getPieceAt("a8")->getMoves(board);
    correct_answer = {"b8"};
    test_string_sets(NAME + "Black King One Move", test_answer, correct_answer);
}

void test_black_king_checkmated(std::string NAME)
{
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Board board;
    board.pieces.deleteAllPieces();
    board.pieces.loadPiecesFromStringVector(LOAD_ONE_MOVE_TO_CHECKMATE);
    Piece* white_queen = board.pieces.getPieceAt("d7");
    white_queen->setPosition("a7");
    test_answer = board.pieces.getPieceAt("a8")->getMoves(board);
    test_true(NAME + "Black King Checkmated", test_answer.empty());
}

void test_white_pawn_cm_pos(std::string NAME)
{
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Board board;
    board.pieces.deleteAllPieces();
    board.pieces.loadPiecesFromStringVector(LOAD_ONE_MOVE_TO_CHECKMATE);
    test_answer = board.pieces.getPieceAt("b6")->getMoves(board);
    correct_answer = {"b7"};
    test_string_sets(NAME + "White Pawn Check Mate POS", test_answer, correct_answer);
}

void test_white_queen_cm_pos(std::string NAME)
{
    std::unordered_set<std::string> test_answer;
    std::unordered_set<std::string> correct_answer;

    Board board;
    board.pieces.deleteAllPieces();
    board.pieces.loadPiecesFromStringVector(LOAD_ONE_MOVE_TO_CHECKMATE);
    test_answer = board.pieces.getPieceAt("d7")->getMoves(board);
    correct_answer = {
        "d1", "d2", "d3", "d4", "d5", "d6", "d8",
        "a7", "b7", "c7", "e7", "f7", "g7", "h7",
        "e8", "c6", "b5", "a4",
        "c8", "e6", "f5", "g4", "h3"
    };
    test_string_sets(NAME + "Queen Moves", test_answer, correct_answer);
}



void MovesCheckmate()
{
    std::string NAME = "MovesCheckmate() - ";
    test_black_king_one_move(NAME);
    test_black_king_checkmated(NAME);
    test_white_pawn_cm_pos(NAME);
    test_white_queen_cm_pos(NAME);
}


int main()
{
    SquareTest();
    PieceControl();
    OnBoard();
    MovesCheckmate();

    return 0;
}