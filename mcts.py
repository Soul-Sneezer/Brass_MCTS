from graphviz import Digraph
from profiler import record_performance
import math 
import random
import time

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state 
        self.parent = parent 
        self.explored_moves = []
        self.unexplored_moves = state.getLegalMoves()
        self.children = [] 
        self.visits = 0
        self.total_reward = 0

    def isFullyExpanded(self):
        return len(self.children) == len(self.state.getLegalMoves())

    def bestChild(self, exploration_weight=0):
        return max(self.children, key=lambda child: (child.total_reward / (child.visits + 1e-6)) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def addChild(self, child_state):
        new_node = MCTSNode(state=child_state, parent=self)
        self.children.append(new_node)
        return new_node

duration = [ 0, 0, 0, 0, 0]

class MCTS:
    def __init__(self, environment, exploration_weight=math.sqrt(2), iterations=1000):
        self.environment = environment 
        self.exploration_weight = exploration_weight
        self.iterations = iterations
  
    def visualize_tree(self, root, max_nodes=300):
        dot = Digraph(comment="MCTS Tree")
        def make_label(node):
            label = f"Visits: {node.visits}\nValue: {node.total_reward:.2f}"
            if node.state.last_action is not None:
                label += f"\nPlayer: {node.state.last_action[0]} Move: {node.state.last_action[1]['type']}"
            return label

        node_id_map = {}
        node_id_map[root] = 0
        dot.node("0", label=make_label(root))

        current_layer = [root]
        layer = 0

        while current_layer and len(node_id_map) < max_nodes:
            next_layer_candidates = []
            for node in current_layer:
                for child in node.children:
                    if len(node_id_map) >= max_nodes:
                        break
                    if child not in node_id_map:
                        if child.visits > 0:
                            metric = child.total_reward / child.visits
                        else:
                            metric = 0.0  

                        parent_id = node_id_map[node]
                        next_layer_candidates.append((child, parent_id, metric))
            
            if not next_layer_candidates:
                break

            next_layer_candidates.sort(key=lambda x: x[2], reverse=True)
            next_layer_candidates = next_layer_candidates[:30]

            next_layer = []
            for child, parent_id, metric in next_layer_candidates:
                if child not in node_id_map:
                    new_id = len(node_id_map)
                    node_id_map[child] = new_id
                    dot.node(str(new_id), label=make_label(child))
                    dot.edge(str(parent_id), str(new_id))
                    next_layer.append(child)
                else:
                    child_id = node_id_map[child]
                    dot.edge(str(parent_id), str(child_id))
            
            current_layer = next_layer
            layer += 1

        dot.render('brass_tree', format="png", cleanup=True)

    @record_performance
    def search(self):
        root_node = MCTSNode(state=self.environment.getInitialState())

        for i in range(self.iterations):
            # Selection
            node = self._select(root_node)

            # Expansion
            if not node.state.isTerminal():
                child = self._expand(node)

            # Simulation 
            reward = self._simulate(child.state)

            # Backpropagation
            self._backpropagate(child, reward)

        self.visualize_tree(root_node)

        best_child = root_node.bestChild(exploration_weight=0)
        return best_child.state.getLastAction()

    @record_performance
    def _select(self, node):
        while not node.state.isTerminal() and node.isFullyExpanded():
            node = node.bestChild(self.exploration_weight)

        return node

    @record_performance
    def _expand(self, node):
        unexplored_moves = node.unexplored_moves
        if len(unexplored_moves) == 0:
            return node
        move = random.choice(unexplored_moves)
        node.unexplored_moves.remove(move)
        node.explored_moves.append(move)
        new_state = node.state.applyMove(move)
        return node.addChild(new_state)

    @record_performance
    def _simulate(self, state):
        current_state = state.clone()
        while not current_state.isTerminal():
            if current_state.legal_moves is None:
                legal_moves = current_state.getLegalMoves()
            else:
                legal_moves = current_state.legal_moves
            random_move = random.choice(legal_moves)
            current_state = current_state.applyMove(random_move)

        return current_state.getReward(current_state.getPlayer())

    @record_performance
    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1 
            node.total_reward += reward 
            node = node.parent
