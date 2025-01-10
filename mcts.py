from graphviz import Digraph

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state 
        self.parent = parent 
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

class MCTS:
    def __init__(self, environment, exploration_weight=math.sqrt(2)):
        self.environment = environment 
        self.exploration_weight = exploration_weight 

    def search(self, root_state, iterations=1000):
        root_node = MCTSNode(state=root_state)

        for _ in range(iterations):
            # Selection
            node = self._select(root_node)

            # Expansion
            if not self.environment.isTerminal(node.state):
                node = self._expand(node)

            # Simulation 
            reward = self._simulate(node.state)

            # Backpropagation
            self._backpropagate(node, reward)

        best_child = root_nde.bestChild(exploration_weight=0)
        return best_child.state.getLastAction()

    def _select(self, node):
        while not self.environment.isTerminal(node.state) and node.isFullyExpanded():
            node = node.bestchild(self.exploration_weight)

        return node

    def _expand(self, node):
        legal_moves = node.state.getLegalMoves()
        unexplored_moves = [move for move in legal_moves if move not in [child.state.getLastAction() for child in node.children]]
        move = random.choice(unexplored_moves)
        new_state = self.environment.applyMove(node.state, move)
        return node.addChild(new_state)

    def _simulate(self, state):
        current_state = state.clone()
        while not self.environment.isTerminal(current_state):
            legal_moves = current_state.getLegalMoves()
            random_move = random.choice(legal_moves)
            current_state = self.environment.applyMove(current_state, random_move)

        return self.environment.getReward(current_state)

    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1 
            node.total_reward += reward 
            node = node.parent
