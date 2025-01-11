from graphviz import Digraph
import math 
import random

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state 
        self.parent = parent 
        self.children = []
        self.valid_moves = state.getLegalMoves() 
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

class MCTS:
    def __init__(self, environment, exploration_weight=math.sqrt(2)):
        self.environment = environment 
        self.exploration_weight = exploration_weight 
    
    def visualize_tree(self, root_node):
        dot = Digraph(comment='MCTS Tree')
        self._add_node(dot, root_node)
        dot.render('brass_tree', format="png", view=True, cleanup=True)

    def _add_node(self, dot, node):
        node_id = str(id(node))
        label = f"visits={node.visits}\nreward={node.total_reward}"
        dot.node(node_id, label=label)

        for child in node.children:
            child_id = str(id(child))
            dot.edge(node_id, child_id)
            self._add_node(dot, child)

    def search(self, root_state, iterations=1000):
        root_node = MCTSNode(state=root_state)

        for _ in range(iterations):
            # Selection
            node = self._select(root_node)

            # Expansion
            if not node.state.isTerminal():
                node = self._expand(node)

            # Simulation 
            reward = self._simulate(node.state)

            # Backpropagation
            self._backpropagate(node, reward)

        self.visualize_tree(root_node)

        best_child = root_node.bestChild(exploration_weight=0)
        return best_child.state.getLastAction()

    def _select(self, node):
        while not node.state.isTerminal() and node.isFullyExpanded():
            node = node.bestChild(self.exploration_weight)

        return node

    def _expand(self, node):
        legal_moves = node.state.getLegalMoves()
        unexplored_moves = [move for move in legal_moves if move not in [child.state.getLastAction() for child in node.children]]
        move = random.choice(unexplored_moves)
        new_state = node.state.applyMove(move)
        return node.addChild(new_state)

    def _simulate(self, state):
        current_state = state.clone()
        while not current_state.isTerminal():
            legal_moves = current_state.getLegalMoves()
            random_move = random.choice(legal_moves)
            current_state = current_state.applyMove(random_move)

        return current_state.getReward(current_state.getPlayer())

    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1 
            node.total_reward += reward 
            node = node.parent
