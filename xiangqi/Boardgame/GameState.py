from enum import Enum

GameState = Enum("GameState", [("PLAYER_WIN", -1), ("AI_WIN", 1), ("DRAW", 0)])