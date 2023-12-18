#include <limits.h>
#include <algorithm>
#include <iostream>

#include "search.h"




Action::Action(std::string position, std::string move)
{
    this->position = position;
    this->move = move;
}



bool getPlayer(Game game)
{
    return game.determineColor();
}

std::vector<Action> getActions(Game& game)
{
    bool player = getPlayer(game);
    std::map<Piece*, std::unordered_set<std::string>> move_map;
    std::unordered_set<std::string>::iterator mv_itr;
    move_map = game.board.pieces.getInstanceMoves(player, game.board);
    std::vector<Action> actions;
    std::string pos;
    std::unordered_set<std::string> move_set;
    std::string move;


    for (auto itr = move_map.begin(); itr != move_map.end(); itr++)
    {
        pos = itr->first->position;
        move_set = itr->second;
        if (!move_set.empty()) 
        {
            for (mv_itr = move_set.begin(); mv_itr != move_set.end(); mv_itr++)
            {
                actions.push_back(Action(pos, (*mv_itr)));
            }
        }
    }
    return actions;
}

std::tuple<GameState, Game, Action> getResult(Game& game, Action action)
{
    Game game_result{game};
    game_result.selectPiece(action.position);
    game_result.selectMove(action.move);
    GameState game_state = game_result.moveAndNextTurn();

    return std::make_tuple(game_state, game_result, action);
}

int evaluateResult(bool player, std::tuple<GameState, Game, Action> result)
{
    bool player_turn = std::get<1>(result).determineColor();

    if ((player == player_turn) && (std::get<0>(result) == CHECKMATE))
        {return -1000;}
    else if ((player != player_turn) && (std::get<0>(result) == CHECKMATE))
        {return 1000;}
    else if (std::get<0>(result) == STALEMATE)
        {return 0;}
    else
        {return std::get<1>(result).eval(player);}
}

bool isCutoff(Game& original, Game& result_game, GameState state, int depth)
{

    if ((result_game.turn - original.turn) >= depth)
        {return true;}
    else if (state != PLAY)
        {return true;}
    else
    {
        return false;
    }
}

Action alphaBetaSearch(Game game)
{
    bool player = game.determineColor();
    std::tuple<int, Action> vm_pair;
    std::string value;
    Action move;
    vm_pair = maxValue(player, game, game, PLAY, move, INT_MIN, INT_MAX);
    move = std::get<1>(vm_pair);
    return move;
}

std::tuple<int, Action> maxValue(bool player, Game& original, Game& result_game, GameState state, Action action, int alpha, int beta)
{
    std::tuple<int, Action> vm_pair;
    Action move;
    if (isCutoff(original, result_game, state, 2))
        {return std::make_tuple(evaluateResult(player, std::make_tuple(state, result_game, action)), Action{});}
    int value = INT_MIN;
    std::vector<Action> actions = getActions(result_game);
    for (auto action: actions)
    {
        std::tuple<GameState, Game, Action> new_result = getResult(result_game, action);
        vm_pair = minValue(player, original, std::get<1>(new_result), std::get<0>(new_result), std::get<2>(new_result), alpha, beta);
        int value2 = std::get<0>(vm_pair);
        if (value2 > value)
        {
            value = value2;
            move = action;
            alpha = std::max(value, alpha);
        }
        if (value >= beta)
            {return std::make_tuple(value, move);}
    }
    return std::make_tuple(value, move);
}

std::tuple<int, Action> minValue(bool player, Game& original, Game& result_game, GameState state, Action action, int alpha, int beta)
{
    std::tuple<int, Action> vm_pair;
    Action move;
    if (isCutoff(original, result_game, state, 2))
        {return std::make_tuple(evaluateResult(player, std::make_tuple(state, result_game, action)), Action{});}
    int value = INT_MAX;
    std::vector<Action> actions = getActions(result_game);
    for (auto action: actions)
    {
        std::tuple<GameState, Game, Action> new_result = getResult(result_game, action);
        vm_pair = minValue(player, original, std::get<1>(new_result), std::get<0>(new_result), std::get<2>(new_result), alpha, beta);
        int value2 = std::get<0>(vm_pair);
        if (value2 < value)
        {
            value = value2;
            move = action;
            beta = std::min(value, beta);
        }
        if (value <= alpha)
            {return std::make_tuple(value, move);}
    }
    return std::make_tuple(value, move);   
}
