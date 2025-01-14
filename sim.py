from environment import environment
from mcts import MCTS
import math

mcts = MCTS(environment=environment, exploration_weight=math.sqrt(2))

root_state = environment.getInitialState()
best_action = mcts.search(root_state, iterations=100)

