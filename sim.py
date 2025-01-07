from board import Board
from board import IndustryType
from game import Game
from player import Player


mcts = MCTS(environment=brass_env, exporation_weight=math.sqrt(2))

root_state = brass_env.getInitialState()
best_action = mcts.search(root_state, iterations=1000)

