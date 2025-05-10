import logging
import sys
import coloredlogs
import torch
import time
import os

from Coach import Coach
from xiangqi.XiangqiGame import XiangqiGame as Game
from xiangqi.pytorch.NNet import NNetWrapper as nn
from utils import *

import subprocess

args = dotdict({
    'numIters': 5,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 5,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
    'logfile': time.strftime(f"logs/{os.path.basename(__file__).replace('.py', '')}-%Y-%m-%d-%H-%M-%S.log", time.localtime()),
})

log = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.DEBUG,
    filename = args.logfile,
    filemode = 'w',
    format='[%(asctime)s][%(levelname)s] %(name)s | %(message)s'
)
coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

command = "lscpu"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
log.info("CPU Info:")
log.info(result.stdout)

command = "nvidia-smi"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
log.info("Nvidia Info:")
log.info(result.stdout)

log.info("Recursion Limit: %s", sys.getrecursionlimit())
sys.setrecursionlimit(10**6)
log.info("New Recursion Limit: %s", sys.getrecursionlimit())
log.info("Python version: %s", sys.version)
log.info("Torch version: %s", torch.__version__)

torch.cuda.set_device(1)
log.info("Cuda available: %s", torch.cuda.is_available())
log.info("Cuda device count: %s", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    log.info("Cuda device %d: %s", i, torch.cuda.get_device_name(i))
    log.info("Cuda device %d properties: %s", i, torch.cuda.get_device_properties(i))

log.info("Cuda device: %s", torch.cuda.current_device())
log.info("Cuda name: %s", torch.cuda.get_device_name(torch.cuda.current_device()))
log.info("Cuda version: %s", torch.version.cuda)
log.info("Cudnn version: %s", torch.backends.cudnn.version())
log.info("Cudnn enabled: %s", torch.backends.cudnn.enabled)

def main():
    log.info('Loading %s...', Game.__name__)
    g = Game(9, 10)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
