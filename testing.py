from board import Board
from board import IndustryType
from environment import State
from environment import Environment
from player import Player
from environment import CityEnum
from environment import environment
from environment import MoveType

board = Board(2)
environment = Environment(2)
state = environment.get_initial_state()

#print(board.cities)
#for city in board.cities:
#    city.printLinks()

#print(board.trading_hubs)
board.coal_market.remove_resource()
board.iron_market.remove_resource()
board.iron_market.remove_resource()
print(board.coal_market.get_price())
print(board.iron_market.get_price())

print(state.cards)
player = state.players[0]
#print(player.build(environment.state.board.cities[1], player.get_manufactory()))
print(state.board.cities)
print(player.coins)
#print(environment.state.board.cities[1].squares[0].building_instance.building.industry_type) # bruh 
player.coins = 100

dudley = state.board.cities[CityEnum.DUDLEY.value]
kidderminster = state.board.cities[CityEnum.KIDDERMINSTER.value]
worcester = state.board.cities[CityEnum.WORCESTER.value]
city1 = state.board.cities[CityEnum.CITY1.value]

costs = player.can_build(dudley, player.get_coalmine())
print(f"building costs 1: {costs}")
player.build(dudley, player.get_coalmine(), costs)
print(dudley.squares[0].building_instance.building.resources)
print(dudley.is_available(0, IndustryType.IRONWORKS))
#print(environment.state.board.cities[name_to_index.get("Dudley")].squares[0].building_instance.building.industry_type)
costs = player.can_build(dudley, player.get_ironworks())
print(f"building costs 2: {costs}")
player.build(dudley, player.get_ironworks(), costs)
print(dudley.squares[0].get_stats())
print(dudley.squares[1].get_stats())
print(player.coins)

print(player.iron_works)

costs = player.can_develop([IndustryType.IRONWORKS])
print(f"develop costs {costs}")
player.develop([IndustryType.IRONWORKS], costs)
print(player.iron_works)

costs = player.can_develop([IndustryType.IRONWORKS])
print(f"develop costs {costs}")
player.develop([IndustryType.IRONWORKS], costs)
print(player.iron_works)

costs = player.can_develop([IndustryType.COALMINE])
player.develop([IndustryType.COALMINE], costs)

costs = player.can_develop([IndustryType.COALMINE])
player.develop([IndustryType.COALMINE], costs)

costs = player.can_sell(dudley.squares[1].building_instance)
player.sell(dudley.squares[1].building_instance, costs)

costs = player.can_build(worcester, player.get_manufactory())
player.build(worcester, player.get_manufactory(), costs)

costs = player.can_build(city1, player.get_brewery())
player.build(city1, player.get_brewery(), costs)

costs = player.can_network(environment.get_initial_state().board.links[0])
player.network(environment.get_initial_state().board.links[0], costs)

print(player.coins)
print(dudley.squares[1].get_stats())
player.print_stats()

environment.get_initial_state().legal_moves = environment.get_initial_state().get_legal_moves()
once = False

print(player.iron_works)
print(player.coal_mines)

for move in environment.get_initial_state().get_legal_moves():
    #if move['type'] == MoveType.DEVELOP and not(once):
    #    print(move)
    #    print()
    #    environment.get_initial_state().apply_move(move)
    #    once = True
    #if move['type'] == MoveType.SELL and move['building_instance'].building.industry_type == IndustryType.MANUFACTORY and not(once):
    #    print(move)
    #    print()
    #    environment.get_initial_state().apply_move(move)
    #    once = True
    print(move)
    print()

print(environment.get_initial_state().is_terminal())
print(environment.get_initial_state().get_reward(environment.get_initial_state().get_player()))
print(player.cards)
player.discard_random_cards()
player.discard_random_cards()
print(player.cards)
print(player.get_stats())
player.end_turn()
print(player.get_stats())
player.end_turn()
print(player.get_stats())
print(player.cards)
environment.get_initial_state().apply_move(environment.get_initial_state().legal_moves[0])
print(player.get_stats())
print(player.cards)

for building_instance in player.buildings_on_board:
    print(f"{building_instance.building} {building_instance.sold}")

print(player.iron_works)
print(player.coal_mines)
