import logging
import time
import os

import Arena
from MCTS import MCTS
from xiangqi.XiangqiGame import XiangqiGame
from xiangqi.XiangqiPlayer import *
from xiangqi.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

logging.basicConfig(
    level = logging.DEBUG,
    filename = time.strftime(f"logs/{os.path.basename(__file__).replace('.py', '')}-%Y-%m-%d-%H-%M-%S.log", time.localtime()),
    filemode = 'a',
    format='[%(asctime)s][%(levelname)s] %(name)s | %(message)s'
)

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

# mini_othello = False  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = True

# if mini_othello:
#     g = XiangqiGame(6)
# else:
#     g = XiangqiGame(8)

g = XiangqiGame(9, 10)

# all players
rp = RandomPlayer(g).play
# gp = GreedyOthelloPlayer(g).play
hp = HumanXiangqiPlayer(g).play
hp2 = HumanXiangqiPlayer(g).play



# nnet players
# n1 = NNet(g)
# if mini_othello:
#     n1.load_checkpoint('./pretrained_models/othello/pytorch/','6x100x25_best.pth.tar')
# else:
#     n1.load_checkpoint('./pretrained_models/othello/pytorch/','8x8_100checkpoints_best.pth.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(g, n1, args1)
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    # n2 = NNet(g)
    # n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    # args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    # mcts2 = MCTS(g, n2, args2)
    # n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    # player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.
    pass

# arena = Arena.Arena(rp, player2, g, display=XiangqiGame.display)
arena = Arena.Arena(hp2, player2, g, display=XiangqiGame.display)

print(arena.playGames(2, verbose=True))
