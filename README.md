# Brass Birmingham MCTS

## Overview
This project implements a Monte Carlo Tree Search (MCTS) for the board game Brass Birmingham.
The scope of this project is to generate a state tree that explores the most promising nodes, by the most promising I mean the ones that should result in the most amounts of points by the end of the game. By generating such a tree I expect to find interesting game strategies.


This can be further expanded by changing game parameters. For example, maybe by distributing the cards in a certain manner, we can find out how much of a factor luck is, and whether there are certain types of cards that are extremely valuable compared to the other ones.

## Project Status 🚧
This project is currently **unfinished** and is a **work in progress**. While the core functionality is implemented, it requires further development, testing, and refinement.

## Key Features
### Core Game Implementation
- Complete Brass Birmingham rules implementation
- Resource management (coal, iron, beer)
- Industry development system (Ironworks, Coal Mines, Breweries, Potteries, Cotton Mills)
- Network building (canals and rails)
- Dual-era gameplay mechanics

### AI Components
- Monte Carlo Tree Search implementation
  - UCB1 selection policy
  - Random simulation (rollout)
  - Backpropagation of results
  - Tree visualization using Graphviz
- Game state cloning for simulation
- Legal move generation and validation

### Visualization and Analysis
- Interactive game tree visualization
- Move statistics and metrics
- Resource market tracking
- Player state monitoring

```
Brass_MCTS/
├── board.py          # Game board and state representation
├── environment.py    # Game rules and mechanics
├── mcts.py           # MCTS algorithm implementation
├── player.py         # Player logic and AI
├── sim.py            # Simulation controller
├── testing.py        # Testing and visualization
├── brass_tree.pdf    # Example game tree visualization
├── brass_tree.png    # Example game tree visualization
├── brass_tree2.png   # Example game tree visualization
└── documentatie.pdf  # Project documentation
```
## Development Roadmap

### Core Improvements
- [ ] Implement state pruning techniques
- [ ] Add GPU acceleration for tree exploration
- [ ] Improve performance through more convential optimization methods (better data structures, cache friendly algorithms, removing redundant steps in the algorithms)

### AI Enhancements
- [ ] Integrate Reinforcement Learning techniques
- [ ] Develop heuristic evaluation functions
- [ ] Implement opening book strategies(maybe?)

### Visualization
- [ ] Enhanced game tree visualization
- [ ] Real-time move statistics
- [ ] Interactive game state exploration

## References
1. The Brass Birmingham game manual (I guess this was to be expected)
2. Artificial Intelligence A Modern Approach - Norvig, Russell
