from board import Board
from board import IndustryType
from game import Game
from player import Player

board = Board(2)
game = Game(2)

#print(board.cities)
#for city in board.cities:
#    city.printLinks()

#print(board.trading_hubs)
board.coal_market.removeResource()
board.iron_market.removeResource()
board.iron_market.removeResource()
print(board.coal_market.getPrice())
print(board.iron_market.getPrice())

print(game.cards)
for player in game.players:
    print(player.coins)
    print(player.iron_works)
    player.develop([IndustryType.IRONWORKS, IndustryType.COALMINE], once=False)
    print(player.coal_mines)
    print(player.iron_works)
    print(player.coins)
    print()
