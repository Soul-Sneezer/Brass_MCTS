from enum import Enum
import random
from . import board

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

game_cards = [[CardType.INDUSTRY, (board.IndustryType.BREWERY), 5],
              [CardType.INDUSTRY, (board.IndustryType.POTTERY), 3],
              [CardType.INDUSTRY, (board.IndustryType.IRONWORKS), 4],
              [CardType.INDUSTRY, (board.IndustryType.COALMINE), 3],
              [CardType.INDUSTRY, (board.IndustryType.MANUFACTORY, board.IndustryType.COTTONMILL), 8],
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
              [CardType.LOCATION, CityEnum.BELPER, 2],
              [CardType.LOCATION, CityEnum.DERBY, 3],
              [CardType.LOCATION, CityEnum.LEEK, 2],
              [CardType.LOCATION, CityEnum.STOKE_ON_TRENT, 3],
              [CardType.LOCATION, CityEnum.STONE, 2],
              [CardType.LOCATION, CityEnum.UTTOXETER, 2]]


class Game:
    def __init__(self, number_of_players):
        self.first_era = True
        self.can_overbuild_mines = False
        self.cards = []
        self.createCards(number_of_players)
        self.number_of_players = number_of_players
        self.board = board.Board(number_of_players)    
        self.players = []
        self.game = Game(number_of_players)
        self.distributeCardsToPlayers(number_of_players)
    
    def distributeCardsToPlayers(self, number_of_players):
        for j in range(9):
            for i in range(number_of_players):
                self.players[i].draw_card(self.game.cards.pop())

        for i in range(number_of_players):
            self.players[i].discard_pile.append(self.players[i].cards.pop())

    def createCards(self, number_of_players):
        card_packs = 0

        if number_of_players == 2:
            card_packs = len(game_cards) - 6
        elif number_of_players == 3:
            card_packs = len(game_cards) - 2
        elif number_of_players == 4:
            card_packs = len(game_cards)
        else:
            raise Exception("Wrong number of players!")

        for i in range(card_packs):
            for j in range(game_cards[i][2]):
                new_card = Card(game_cards[i][0], game_cards[i][1])
                self.cards.append(new_card)

        random.shuffle(self.cards) # shuffle the deck

    def getCoalPrice(self, count):
        if count > 0: # get price if we had already removed more than 1 resource
            count2 = count
            while count > 0:
                self.board.coal_market.removeResource()
                count -= 1
            price = self.board.coal_market.getPrice()

            while count2 > 0:
                self.board.coal_market.addResource()
                count2 -= 1

        else:
            price = self.board.coal_market.getPrice()
        
        return price

    def getIronPrice(self, count):
        if count > 0: # get price if we had already removed more than 1 resource
            count2 = count
            while count > 0:
                self.board.iron_market.removeResource()
                count -= 1
            price = self.board.iron_market.getPrice()

            while count2 > 0:
                self.board.iron_market.addResource()
                count2 -= 1
        else:
            price = self.board.iron_market.getPrice()
        
        return price

    def calculateLinkPoints(self):
        player_points = {i: 0 for i in range(4)}
        for link in self.board.links:
            if link.owner_id != None:
                player_points[link.owner_id] += link.points

        return player_points
