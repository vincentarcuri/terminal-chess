#pragma once


#include <tuple>

#include "Game.h"



class Action
{
    public:
        std::string position;
        std::string move;

        Action(){};
        Action(std::string position, std::string move);

};




bool getPlayer(Game game);
std::vector<Action> getActions(Game& game);
std::tuple<GameState, Game, Action> getResult(Game& game, Action action);
int evaluateResult(bool player, std::tuple<GameState, Game, Action> result);
bool isCutoff(Game& original, Game& result_game, GameState state, int depth);

Action alphaBetaSearch(Game game);
std::tuple<int, Action> maxValue(bool player, Game& original, Game& result_game, GameState state, Action action, int alpha, int beta);
std::tuple<int, Action> minValue(bool player, Game& original, Game& result_game, GameState state, Action action, int alpha, int beta);

