#include <sstream>

#include "Pieces2.h"
#include "Board2.h"
#include "Game.h"
#include "search.h"



// Splits a binary string to a vector of strings.
std::vector<std::string> splitStr(const std::string &str, char delim)
{
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string item;

    while (getline(ss, item, delim)) {
        result.push_back(item);

    }
    return result;
}

extern "C" {
    const char* getMoveFromState(char * str, int turn)
    {
        // char -> string
        std::string input_string(str);
        // Split string to vector
        std::vector<std::string> build_data = splitStr(input_string, ' ');
        // Load board from string vector
        Game game;
        game.turn = turn;
        game.board.pieces.deleteAllPieces();
        game.board.pieces.loadPiecesFromStringVector(build_data);
        // Find optimal move, depth 2
        Action move = alphaBetaSearch(game);
        std::string return_string = move.position + " " + move.move;
        // Convert to C-style string.
        const char* c_string = return_string.c_str();
        return c_string;
    }
}