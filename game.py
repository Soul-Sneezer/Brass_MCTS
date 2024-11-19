from enum import Enum
from board import IndustryType

class CardType(Enum):
    LOCATION = 0
    INDUSTRY = 1
    WILD_LOCATION = 2
    WILD_INDUSTRY = 3

class CityEnum(Enum):
    BIRMINGHAM = 0
    REDDITCH = 1
    NUNEATON = 2
    STONE = 3
    DERBY = 4
    LEEK = 5
    KIDDERMINSTER = 6
    BURTON_ON_TRENT = 7
    UTTOXETER = 8
    BELPER = 9
    STOKE_ON_TRENT = 10
    COVENTRY = 11
    WOLVERHAMPTON = 12
    CANNOCK = 13
    WALSALL = 14
    STAFFORD = 15
    TAMWORTH = 16
    DUDLEY = 17
    WORCESTER = 18
    COALBROOKDALE = 19

class Card:
    def __init__(self, card_type, content):
        self.card_type = card_type
        self.content = content

game_cards = [[CardType.LOCATION, CityEnum.BIRMINGHAM, 3],
              [CardType.LOCATION, CityEnum.REDDITCH, 1],
              [CardType.LOCATION, CityEnum.NUNEATON, 1],
              [CardType.LOCATION, CityEnum.STONE, 2],
              [CardType.LOCATION, CityEnum.DERBY, 3],
              [CardType.LOCATION, CityEnum.LEEK, 2],
              [CardType.LOCATION, CityEnum.KIDDERMINSTER, 2],
              [CardType.LOCATION, CityEnum.DUDLEY, 2],
              [CardType.LOCATION, CityEnum.WORCESTER, 2],
              [CardType.LOCATION, CityEnum.COALBROOKDALE, 3],
              [CardType.LOCATION, CityEnum.UTTOXETER, 2],
              [CardType.LOCATION, CityEnum.BELPER, 2],
              [CardType.LOCATION, CityEnum.STOKE_ON_TRENT, 3],
              [CardType.LOCATION, CityEnum.COVENTRY, 3],
              [CardType.LOCATION, CityEnum.WOLVERHAMPTON, 2],
              [CardType.LOCATION, CityEnum.CANNOCK, 2],
              [CardType.LOCATION, CityEnum.STAFFORD, 2],
              [CardType.LOCATION, CityEnum.WALSALL ,1],
              [CardType.LOCATION, CityEnum.TAMWORTH, 1],
              [CardType.LOCATION, CityEnum.BURTON_ON_TRENT, 2],
              [CardType.INDUSTRY, (IndustryType.BREWERY), 5],
              [CardType.INDUSTRY, (IndustryType.POTTERY), 3],
              [CardType.INDUSTRY, (IndustryType.IRONWORKS), 4],
              [CardType.INDUSTRY, (IndustryType.COALMINE), 3],
              [CardType.INDUSTRY, (IndustryType.MANUFACTORY, IndustryType.COTTONMILL), 8],
              [CardType.WILD_LOCATION, None, 4],
              [CardType.WILD_INDUSTRY, None, 4]]


class Game:
    def __init__(self):
        self.can_overbuild_mines = False
        self.cards = []

    def createCards(self):
        for i in range(len(game_cards)):
            for j in range(game_cards[i][2]):
                new_card = Card(game_cards[i][0], game_cards[i][1])
                self.cards.append(new_card)

