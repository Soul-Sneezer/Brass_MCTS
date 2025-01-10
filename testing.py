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

dudley = state.board.cities[CityEnum.DUDLEY.value]
kidderminster = state.board.cities[CityEnum.KIDDERMINSTER.value]
worcester = state.board.cities[CityEnum.WORCESTER.value]
city1 = state.board.cities[CityEnum.CITY1.value]

costs = player.canBuild(dudley, player.getCoalmine())
print(f"building costs 1: {costs}")
player.build(dudley, player.getCoalmine(), costs)
print(dudley.squares[0].building_instance.building.resources)
print(dudley.isAvailable(0, IndustryType.IRONWORKS))
#print(environment.state.board.cities[name_to_index.get("Dudley")].squares[0].building_instance.building.industry_type)
costs = player.canBuild(dudley, player.getIronworks())
print(f"building costs 2: {costs}")
player.build(dudley, player.getIronworks(), costs)
print(dudley.squares[0].getStats())
print(dudley.squares[1].getStats())
print(player.coins)

print(player.iron_works)

costs = player.canDevelop([IndustryType.IRONWORKS])
print(f"develop costs {costs}")
player.develop([IndustryType.IRONWORKS], costs)
print(player.iron_works)

costs = player.canDevelop([IndustryType.IRONWORKS])
print(f"develop costs {costs}")
player.develop([IndustryType.IRONWORKS], costs)
print(player.iron_works)

costs = player.canDevelop([IndustryType.COALMINE])
player.develop([IndustryType.COALMINE], costs)

costs = player.canDevelop([IndustryType.COALMINE])
player.develop([IndustryType.COALMINE], costs)

costs = player.canSell(dudley.squares[1].building_instance)
player.sell(dudley.squares[1].building_instance, costs)
print(player.coins)
print(dudley.squares[1].getStats())
player.printStats()
