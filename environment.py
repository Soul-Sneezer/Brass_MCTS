from enum import Enum
from player import Player
import random
import board

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

class Card:
    def __init__(self, card_type, content):
        self.card_type = card_type
        self.content = content

    def __str__(self):
        return f"({self.card_type} {self.content})\n"

    def __repr__(self):
        return f"({self.card_type}   {self.content})\n"

game_cards = [[CardType.INDUSTRY, (board.IndustryType.IRONWORKS), 4],
              [CardType.INDUSTRY, (board.IndustryType.BREWERY), 5],
              [CardType.INDUSTRY, (board.IndustryType.POTTERY), 2],
              [CardType.INDUSTRY, (board.IndustryType.COALMINE), 2],
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
              [CardType.INDUSTRY, (board.IndustryType.MANUFACTORY, board.IndustryType.COTTONMILL), 6],
              [CardType.LOCATION, CityEnum.LEEK, 2],
              [CardType.LOCATION, CityEnum.STOKE_ON_TRENT, 3],
              [CardType.LOCATION, CityEnum.STONE, 2],
              [CardType.LOCATION, CityEnum.UTTOXETER, 2],
              [CardType.LOCATION, CityEnum.BELPER, 2],
              [CardType.LOCATION, CityEnum.DERBY, 3],
              [CardType.INDUSTRY, (board.IndustryType.COALMINE), 1],
              [CardType.INDUSTRY, (board.IndustryType.POTTERY), 1],
              [CardType.INDUSTRY, (board.IndustryType.MANUFACTORY, board.IndustryType.COTTONMILL), 2]]


class State: # the state consists of the current board, and the stats of the players, such as income, vps, cards in hand
    def __init__(self, number_of_players, current_player):
        self.cards = []
        self.players = []
        self.current_player = current_player
        self.number_of_players = number_of_players
        self.board = board.Board(number_of_players) 
    
    def getPlayer(self):
        return self.players[current_player]

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

    def getCoalPrice(self, state, count=1):
        price = 0
        count2 = count
        while count > 0:
            state.board.coal_market.removeResource()
            count -= 1
            price += state.board.coal_market.getPrice()

        while count2 > 0:
            state.board.coal_market.addResource()
            count2 -= 1
        
        return price

    def getIronPrice(self, state, count=1):
        price = 0
        count2 = count
        while count > 0:
            price += state.board.iron_market.getPrice()
            state.board.iron_market.removeResource()
            count -= 1
            
        while count2 > 0:
            state.board.iron_market.addResource()
            count2 -= 1
        
        return price

    def calculateLinkPoints(self, state):
        player_points = {i: 0 for i in range(4)}
        for link in state.board.links:
            if link.owner_id is not None:
                player_points[link.owner_id] += link.points

        return player_points

    def getInitialState(self):
        return self.initial_state

    def getLegalMoves(self, state):
        legal_moves = []
        current_player = state.getPlayer()
        if current_player.income >= 3: # add loan movet t
            new_move = {
                'type': 'loan'
            }
            legal_moves.append(new_move)

        if len(current_player.cards) >= 3: # add scout move
            new_move = {
                'type': 'scout'
            }
            legal_moves.append(new_move)

        if len(current_player.buildings_on_board) > 0: # add sell moves
            for building_instance in current_player.building_on_board:
                if current_player.canSell(building_instance):
                    new_move = {
                        'type': 'sell',
                        'building_instance': building_instance
                    }
                    legal_moves.append(new_move)

        for i in range(6):
            for j in range(7):
                if j != 6:
                    costs = current_player.canDevelop([i,j], once=False)
                    if costs is not None:
                        new_move = {
                            'type': 'develop',
                            'industry1': i,
                            'industry2': j,
                            'cost': costs[0],
                            'needed_iron': costs[1],
                            'iron_sources': costs[2]
                        }
                        legal_moves.append(new_move)
                else:
                    costs = current_player.canDevelop([i])
                    if costs is not None:
                        new_move = {
                            'type': 'develop',
                            'industry1': i,
                            'industry2': j,
                            'cost': costs[0],
                            'needed_iron': costs[1],
                            'iron_sources': costs[2]
                        }
                        legal_moves.append(new_move)

        for card in current_player.cards: # add build moves
            pass 

        for link in state.board.links:
            if link.owner_id is None:
                if self.first_era and link.link_type == LinkType.RAIL:
                    continue
                
                if not(self.first_era) and link.link_type == LinkType.CANAL:
                    continue 

                costs = current_player.canNetwork(link)
                if costs is not None:
                    if environment.first_era:
                        new_move = {
                            'type': 'network',
                            'link': link,
                            'cost': costs[0]
                        }
                        legal_moves.append(new_move)
                    else:
                        new_move = {
                            'type': 'network',
                            'link': link,
                            'cost': costs[0],
                            'needed_coal': costs[1],
                            'coal_sources': costs[2]
                        }
                        legal_moves.append(new_move)

    def applyMove(self, move):
        new_state = 

    def isTerminal(self, state):
        if len(state.cards) != 0:
            return False 
       
        for player in state.players:
            if len(player.cards) != 0:
                return False 

        return True

    def getReward(self):
        pass 
