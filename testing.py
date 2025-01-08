from board import Board
from board import IndustryType
from environment import State
from environment import Environment
from player import Player
from environment import CityEnum

board = Board(2)
environment = Environment(2)
state = environment.getInitialState()

#print(board.cities)
#for city in board.cities:
#    city.printLinks()

#print(board.trading_hubs)
board.coal_market.removeResource()
board.iron_market.removeResource()
board.iron_market.removeResource()
print(board.coal_market.getPrice())
print(board.iron_market.getPrice())

print(state.cards)
player = state.players[0]
#print(player.build(environment.state.board.cities[1], player.getManufactory()))
print(state.board.cities)
print(player.coins)
#print(environment.state.board.cities[1].squares[0].building_instance.building.industry_type) # bruh 
player.coins = 100

dudley = state.board.cities[CityEnum.DUDLEY]
kidderminster = state.board.cities[CityEnum.KIDDERMINSTER]
worcester = state.board.cities[CityEnum.WORCESTER]
city1 = state.board.cities[CityEnum.CITY1]

print(player.build(dudley, player.getCoalmine()))
print(dudley.squares[0].building_instance.building.resources)
print(dudley.isAvailable(0, IndustryType.IRONWORKS))
#print(environment.state.board.cities[name_to_index.get("Dudley")].squares[0].building_instance.building.industry_type)
print(player.build(dudley, player.getIronworks()))
print(dudley.squares[1].getStats())
print(player.coins)
print(player.develop([IndustryType.IRONWORKS]))
print(player.coins)
print(dudley.squares[1].building_instance.building.resources)

