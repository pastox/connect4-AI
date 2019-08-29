import argparse

from player import HumanPlayer, RandomPlayer
from ai_player_Pastox import AIPlayer
import ai_player_skoolpy
import ai_player_paul_cacheux
import ai_player_your_game_Nassimator
from ui_game import UIGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='Pastox')
    parser.add_argument('--p2', default='Nassimator')
    args = parser.parse_args()

    player1 = AIPlayer()
    player1.name = args.p1
    player2 = ai_player_your_game_Nassimator.AIPlayer()
    player2.name = args.p2

    game = UIGame(player1, player2)
