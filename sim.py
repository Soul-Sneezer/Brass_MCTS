from environment import environment
from mcts import MCTS
import math
from profiler import PerformanceRecorder 
from profiler import plot_performance

recorder = PerformanceRecorder()

mcts = MCTS(environment=environment, exploration_weight=math.sqrt(2), iterations=10000)
mcts.search()

plot_performance()

