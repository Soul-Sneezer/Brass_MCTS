# Brass_MCTS

I came up with the idea for this project while playing the game(Brass Birmingham) with a friend. I noticed that almost every time the difference between the first and second place was less than 5 points, meaning that a wrong or wasted move could lose you the game. So rather than simply playing and finding new strategies, I preferred to use my programming skills for insights regarding the game. 

At first I wanted to use Reinforcement Learning (without knowing a lot about this technique), but I ended up using MCTS so I could present this as a project for one of my university classes. I intend to combine MCTS with RL later on. But first I would like to improve the current code and learn more about RL.

I don't believe pure MCTS will suffice for a game with such a large branching factor as Brass Birmingham.

# To Do
* rewrite the more poorly written parts of the codebase
* find ways to prune states, so the more useful parts of the search tree can be explored
* improve data visualization(for the game tree and game related metrics)
* improve performance of the code using simple optimizations
* explore the game tree more efficiently by utilizing the parallel processing capabilities of the GPU
* some parts of the game have been simplified or removed, I will add them after finishing the above tasks
