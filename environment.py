from enum import Enum
from player import Player
from board import IndustryType
from board import LinkType
import random
import board
import copy

class MoveType(Enum):
    BUILD = "build"
    SELL = "sell"
    DEVELOP = "develop"
    SCOUT = "scout"
    LOAN = "loan"
    NETWORK = "network"
    PASS = "pass"

class CardType(Enum):
    LOCATION = 0
    INDUSTRY = 1
    WILD_LOCATION = 2
    WILD_INDUSTRY = 3

class CityEnum(Enum):
    BIRMINGHAM = 0
    REDDITCH = 1
    NUNEATON = 2
    KIDDERMINSTER = 3
    DUDLEY = 4
    WORCESTER = 5
    COALBROOKDALE = 6
    COVENTRY = 7 
    WOLVERHAMPTON = 8
    CANNOCK = 9
    STAFFORD = 10
    WALSALL = 11
    TAMWORTH = 12
    BURTON_ON_TRENT = 13
    BELPER = 14
    DERBY = 15
    LEEK = 16
    STOKE_ON_TRENT = 17
    STONE = 18
    UTTOXETER = 19
    CITY0 = 20
    CITY1 = 21

class Card:
    def __init__(self, card_type, content):
        self.card_type = card_type
        self.content = content

    def __str__(self):
        return f"({self.card_type} {self.content})\n"

    def __repr__(self):
        return f"({self.card_type}   {self.content})\n"

game_cards = [[CardType.INDUSTRY, [board.IndustryType.IRONWORKS], 4],
              [CardType.INDUSTRY, [board.IndustryType.BREWERY], 5],
              [CardType.INDUSTRY, [board.IndustryType.POTTERY], 2],
              [CardType.INDUSTRY, [board.IndustryType.COALMINE], 2],
              [CardType.LOCATION, CityEnum.BIRMINGHAM, 3],
              [CardType.LOCATION, CityEnum.REDDITCH, 1],
              [CardType.LOCATION, CityEnum.NUNEATON, 1],
              [CardType.LOCATION, CityEnum.KIDDERMINSTER, 2],
              [CardType.LOCATION, CityEnum.DUDLEY, 2],
              [CardType.LOCATION, CityEnum.WORCESTER, 2],
              [CardType.LOCATION, CityEnum.COALBROOKDALE, 3],
              [CardType.LOCATION, CityEnum.COVENTRY, 3],
              [CardType.LOCATION, CityEnum.WOLVERHAMPTON, 2],
              [CardType.LOCATION, CityEnum.CANNOCK, 2],
              [CardType.LOCATION, CityEnum.STAFFORD, 2],
              [CardType.LOCATION, CityEnum.WALSALL ,1],
              [CardType.LOCATION, CityEnum.TAMWORTH, 1],
              [CardType.LOCATION, CityEnum.BURTON_ON_TRENT, 2],
              [CardType.INDUSTRY, [board.IndustryType.MANUFACTORY, board.IndustryType.COTTONMILL], 6],
              [CardType.LOCATION, CityEnum.LEEK, 2],
              [CardType.LOCATION, CityEnum.STOKE_ON_TRENT, 3],
              [CardType.LOCATION, CityEnum.STONE, 2],
              [CardType.LOCATION, CityEnum.UTTOXETER, 2],
              [CardType.LOCATION, CityEnum.BELPER, 2],
              [CardType.LOCATION, CityEnum.DERBY, 3],
              [CardType.INDUSTRY, [board.IndustryType.COALMINE], 1],
              [CardType.INDUSTRY, [board.IndustryType.POTTERY], 1],
              [CardType.INDUSTRY, [board.IndustryType.MANUFACTORY, board.IndustryType.COTTONMILL], 2]]

class State: # the state consists of the current board, and the stats of the players, such as income, vps, cards in hand
    def __init__(self, number_of_players, current_player):
        self.cards = []
        self.players = []
        self.legal_moves = None
        self.actions_taken = 0
        self.last_action = None
        self.current_player = current_player
        self.number_of_players = number_of_players
        self.board = board.Board(number_of_players)
        self.reached_end = False
   
    def clone(self):
        return copy.deepcopy(self)

    def getPlayer(self):
        return self.players[self.current_player]
   
    def getLastAction(self):
        return self.last_action

    def calculateLinkPoints(self, player):
        player_points = {i: 0 for i in range(self.number_of_players)}
        for link in self.board.links:
            if link.owner_id is not None:
                player_points[link.owner_id] += link.points

        return player_points[player.id]

    def giveCardToPlayer(self, id):
        if len(self.cards) == 0:
            return None 

        return self.cards.pop()

    def getCoalPrice(self, count=1):
        price = 0
        count2 = count
        while count > 0:
            price += self.board.coal_market.getPrice()
            self.board.coal_market.removeResource()
            count -= 1
            
        while count2 > 0:
            self.board.coal_market.addResource()
            count2 -= 1
        
        return price

    def getIronPrice(self, count=1):
        price = 0
        count2 = count
        while count > 0:
            price += self.board.iron_market.getPrice()
            self.board.iron_market.removeResource()
            count -= 1
            
        while count2 > 0:
            self.board.iron_market.addResource()
            count2 -= 1
        
        return price
    
    def getLegalMoves(self):
        legal_moves = []
        current_player = self.getPlayer()
        if current_player.income >= 3: # add loan movet t
            new_move = {
                'type': MoveType.LOAN
            }
            legal_moves.append(new_move)

        if len(current_player.cards) >= 3: # add scout move
            new_move = {
                'type': MoveType.SCOUT
            }
            legal_moves.append(new_move)

        if len(current_player.buildings_on_board) > 0: # add sell moves
            for building_instance in current_player.buildings_on_board:
                costs = current_player.canSell(building_instance)
                if costs is not None:
                    new_move = {
                        'type': MoveType.SELL,
                        'building_instance': building_instance,
                        'costs': costs
                    }
                    legal_moves.append(new_move)

        for i in range(6):
            for j in range(7):
                if j != 6:
                    industry1 = IndustryType(i)
                    industry2 = IndustryType(j)
                    costs = current_player.canDevelop([industry1, industry2], once=False)
                    if costs is not None:
                        new_move = {
                            'type': MoveType.DEVELOP,
                            'industry1': industry1,
                            'industry2': industry2,
                            'costs': costs,
                        }
                        legal_moves.append(new_move)
                else:
                    industry1 = IndustryType(i)
                    costs = current_player.canDevelop([industry1])
                    if costs is not None:
                        new_move = {
                            'type': MoveType.DEVELOP,
                            'industry1': industry1,
                            'industry2': None,
                            'costs': costs,
                        }
                        legal_moves.append(new_move)

        for index, card in enumerate(current_player.cards): # add build moves
            if card.card_type == CardType.LOCATION:
                city = self.board.cities[card.content.value]
                                
                costs = current_player.canBuild(city, current_player.getIronworks())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getIronworks(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

                costs = current_player.canBuild(city, current_player.getCoalmine())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getCoalmine(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

                costs = current_player.canBuild(city, current_player.getBrewery())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getBrewery(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

                costs = current_player.canBuild(city, current_player.getManufactory())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getManufactory(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

                costs = current_player.canBuild(city, current_player.getCottonmill())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getCottonmill(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

                costs = current_player.canBuild(city, current_player.getPottery())
                if costs is not None:
                    new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getPottery(),
                                'costs': costs, 
                                'card_index': index
                            }
                    legal_moves.append(new_move)

            else:
                for city in current_player.available_cities:
                    if card.content == IndustryType.IRONWORKS:
                        costs = current_player.canBuild(city, current_player.getIronworks())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getIronworks(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)
 
                    if card.content == IndustryType.COALMINE:
                        costs = current_player.canBuild(city, current_player.getCoalmine())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getCoalmine(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)

                    if card.content == IndustryType.BREWERY:
                        costs = current_player.canBuild(city, current_player.getBrewery())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getBrewery(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)

                    if card.content == IndustryType.MANUFACTORY:
                        costs = current_player.canBuild(city, current_player.getManufactory())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getManufactory(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)

                    if card.content == IndustryType.COTTONMILL:
                        costs = current_player.canBuild(city, current_player.getCottonmill())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getCottonmill(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)

                    if card.content == IndustryType.POTTERY:
                        costs = current_player.canBuild(city, current_player.getPottery())
                        if costs is not None:
                            new_move = {
                                'type': MoveType.BUILD,
                                'city': city,
                                'building': current_player.getPottery(),
                                'costs': costs, 
                                'card_index': index
                            }
                            legal_moves.append(new_move)

        for city in current_player.available_cities:
            for link in city.adjacent:
                if link.owner_id is None:
                    if environment.first_era and link.link_type == LinkType.RAIL:
                        continue
                    
                    if not(environment.first_era) and link.link_type == LinkType.CANAL:
                        continue 

                    costs = current_player.canNetwork(link)
                    if costs is not None:
                        new_move = {
                            'type': MoveType.NETWORK,
                            'link': link,
                            'costs': costs
                        }
                        legal_moves.append(new_move)

        legal_moves.append({'type': MoveType.PASS})

        return legal_moves
    
    def applyMove(self, move):
        new_state = self.clone()
        new_state.actions_taken += 1

        if move['type'] == MoveType.BUILD:
            city = move['city']
            building = move['building']
            costs = move['costs']
            #print(move['card_index'])
            #print(new_state.getPlayer().cards)
            new_state.getPlayer().discardCardAtIndex(move['card_index']) # for build action the card you discard matters
            new_state.getPlayer().build(city, building, costs)

        elif move['type'] == MoveType.SELL:
            building_instance = move['building_instance']
            costs = move['costs']
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().sell(building_instance, costs)

        elif move['type'] == MoveType.DEVELOP:
            costs = move['costs']
            industry1 = move['industry1']
            industry2 = move['industry2']
            new_state.getPlayer().discardRandomCard()
            if industry2 is None:
                new_state.getPlayer().develop([industry1], costs)
            else:
                new_state.getPlayer().develop([industry1, industry2], costs, once=False)

        elif move['type'] == MoveType.NETWORK:
            costs = move['costs']
            link = move['link']
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().network(link, costs)

        elif move['type'] == MoveType.LOAN:
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().loan()

        elif move['type'] == MoveType.SCOUT:
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().discardRandomCard()
            new_state.getPlayer().scout()

        elif move['type'] == MoveType.PASS:
            new_state.getPlayer().discardRandomCard()
        else:
            print("Something went wrong when applying a move! Unknown move.")
    
        new_state.last_action = [new_state.current_player, move]
        if new_state.actions_taken == 2:
            for building_instance in new_state.getPlayer().buildings_on_board: # flip all mines with 0 resources
                industry_type = building_instance.building.industry_type
                if industry_type == IndustryType.IRONWORKS or industry_type == IndustryType.COALMINE or industry_type == IndustryType.BREWERY:
                    if building_instance.building.resources == 0:
                        costs = new_state.getPlayer().canSell(building_instance)
                        if costs is not None:
                            new_state.getPlayer().sell(building_instance, costs)
            new_state.getPlayer().endTurn()
            new_state.current_player = (new_state.current_player + 1) % new_state.number_of_players
            iterations = 0
            while len(new_state.getPlayer().cards) == 0 and len(new_state.cards) == 0 and iterations != 4:
                new_state.current_player = (new_state.current_player + 1) % new_state.number_of_players
                iterations += 1
            new_state.actions_taken = 0

        return new_state

    def isTerminal(self):
        if len(self.cards) != 0:
            return False 
       
        for player in self.players:
            if len(player.cards) != 0:
                return False 

        self.reached_end = True
        return True

    def getReward(self, current_player): # calculates score of current player
        opponents = []
        for player in self.players:
            if player.id != current_player.id:
                opponents.append([player, player.victory_points + self.calculateLinkPoints(player)])
        
        max_opponent = max(opponents, key=lambda x: x[1])[0] 
        max_opponent_score = max(opponents, key=lambda x: x[1])[1]
        
        player_score = current_player.victory_points + self.calculateLinkPoints(current_player)
        if self.reached_end:
            if player_score > max_opponent_score:
                return 1.0 
            elif player_score == max_opponent_score:
                if current_player.income > max_opponent.income:
                    return 1.0 
                elif current_player.income == max_opponent.income:
                    if current_player.coins > max_opponent.coins:
                        return 1.0
                    elif current_player.coins == max_opponent.coins:
                        # flip a coin
                        if random.choice([0,1]) == 0:
                            return 1.0
                        else: 
                            return 0.0
                    else:
                        return 0.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return player_score - max_opponent_score

class Environment:
    def __init__(self, number_of_players, first_era=True):
        self.first_era = first_era
        self.number_of_players = number_of_players
        self.can_overbuild_mines = False
        self.initial_state = State(number_of_players, 0)
        self.createPlayers(number_of_players)
        self.createCards(number_of_players)
        self.distributeCardsToPlayers(number_of_players)
    
    def createPlayers(self, number_of_players):
        for i in range(number_of_players):
            new_player = Player(i, self.initial_state, self)
            self.initial_state.players.append(new_player)

    def distributeCardsToPlayers(self, number_of_players):
        for j in range(9):
            for i in range(number_of_players):
                self.initial_state.players[i].drawCard(self.initial_state.cards.pop())

        for i in range(number_of_players):
            self.initial_state.players[i].discard_pile.append(self.initial_state.players[i].cards.pop())

    def createCards(self, number_of_players):
        if number_of_players == 2:
            card_packs = len(game_cards) - 10
        elif number_of_players == 3:
            card_packs = len(game_cards) - 5
        elif number_of_players == 4:
            card_packs = len(game_cards)
        else:
            raise Exception("Wrong number of players!")

        for i in range(card_packs):
            for j in range(game_cards[i][2]):
                new_card = Card(game_cards[i][0], game_cards[i][1])
                self.initial_state.cards.append(new_card)

        random.shuffle(self.initial_state.cards) # shuffle the deck
 
    def getInitialState(self):
        return self.initial_state

environment = Environment(2)

