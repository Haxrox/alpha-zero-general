import logging

import coloredlogs

from Coach import Coach
from xiangqi.XiangqiGame import XiangqiGame as Game
from xiangqi.XiangqiGame import main as GameMain
from xiangqi.XiangqiLogic import XiangqiBoard as Logic
from xiangqi.XiangqiLogic import main as LogicMain
from xiangqi.XiangqiLogic import test as LogicTest
from xiangqi.pytorch.NNet import NNetWrapper as nn
from utils import *

import subprocess

log = logging.getLogger(__name__)
logging.basicConfig(
  filename="xiangqi_test.log",
  filemode = 'w',
  level = logging.DEBUG,
  format='[%(asctime)s][%(levelname)s] %(name)s | %(message)s'
)
coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

def main():
#   log.info('Loading %s...', Game.__name__)
#   GameMain()
  log.info('Loading %s...', Logic.__name__)
  LogicTest()
#   LogicMain()

if __name__ == "__main__":
  main()