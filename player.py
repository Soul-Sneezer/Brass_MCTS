# classes related to storing player state
# such as victory points, money, income, hand (the cards you have), buildings available
# to reach a higher level building you first have to exhaust the lower level ones

# there are also actions you can take every round

from board import IndustryType
from board import BuildingInstance
from game import Game

def getCost(price, game):
    return price[0] + price[1] * game.getCoalPrice() + price[2] * game.getIronPrice()

class Building:
    def __init__(self, industry_type, stats, price, beers=0, resources=0):
        self.industry_type = industry_type
        self.stats = stats
        self.price = price
        self.beers = beers # number of beers required for it to be sold
        self.resources = resources

buildings = [[[IndustryType.IRONWORKS,( 3, 3, 1), (5, 1, 0), 0, 4, 1],
              [IndustryType.IRONWORKS,( 5, 3, 1), (7, 1, 0), 0, 4, 1],
              [IndustryType.IRONWORKS,( 7, 2, 1), (9, 1, 0), 0, 5, 1],
              [IndustryType.IRONWORKS,( 9, 1, 1),(12, 1, 0), 0, 6, 1]],
             [[IndustryType.COALMINE,( 1, 4, 2), (5, 0, 0), 0, 2, 1],
              [IndustryType.COALMINE,( 2, 7, 1), (7, 0, 0), 0, 3, 2],
              [IndustryType.COALMINE,( 3, 6, 1), (8, 0, 1), 0, 4, 2],
              [IndustryType.COALMINE,( 4, 5, 1),(10, 0, 1), 0, 5, 2]],
             [[IndustryType.BREWERY,( 4, 4, 2), (5, 0, 1), 0, 1, 2],
              [IndustryType.BREWERY,( 5, 5, 2), (7, 0, 1), 0, 1, 2],
              [IndustryType.BREWERY,( 7, 5, 2), (9, 0, 1), 0, 1, 2],
              [IndustryType.BREWERY,(10, 5, 2), (9, 0, 1), 0, 1, 1]], # will have the modify the number of resources produced to 2 in second phase
             [[IndustryType.POTTERY,(10, 5, 1), (17, 0, 1), 1, 0, 1],
              [IndustryType.POTTERY,( 1, 1, 1), ( 0, 1, 0), 1, 0, 1],
              [IndustryType.POTTERY,(11, 5, 1), (22, 2, 0), 2, 0, 1],
              [IndustryType.POTTERY,( 1, 1, 1), ( 0, 1, 0), 1, 0, 1],
              [IndustryType.POTTERY,(20, 5, 1), (24, 2, 0), 2, 0, 1]],
             [[IndustryType.MANUFACTORY,( 5, 5, 1), (12, 0, 0), 1, 0, 3],
              [IndustryType.MANUFACTORY,( 5, 4, 2), (14, 1, 0), 1, 0, 2],
              [IndustryType.MANUFACTORY,( 9, 3, 1), (16, 1, 1), 1, 0, 3],
              [IndustryType.MANUFACTORY,(12, 2, 1), (18, 1, 1), 1, 0, 3]],
            [[IndustryType.COTTONMILL,( 3, 5, 2), ( 8, 1, 0), 1, 0, 1],
              [IndustryType.COTTONMILL,( 5, 1, 1), (10, 0, 1), 1, 0, 2],
              [IndustryType.COTTONMILL,( 4, 4, 0), (12, 2, 0), 0, 0, 1],
              [IndustryType.COTTONMILL,( 3, 6, 1), ( 8, 0, 1), 1, 0, 1],
              [IndustryType.COTTONMILL,( 8, 2, 2), (16, 1, 0), 2, 0, 2],
              [IndustryType.COTTONMILL,( 7, 6, 1), (20, 0, 0), 1, 0, 1],
              [IndustryType.COTTONMILL,( 9, 4, 0), (16, 1, 1), 0, 0, 1],
              [IndustryType.COTTONMILL,(11, 1, 0), (20, 0, 2), 1, 0, 2]]]

class Player:
    def createBuildingType(self, i):
        for building in reversed(buildings[i]):
            for i in range(building[5]):
                industry_type = building[0]
                stats = building[1]
                price = building[2]
                beers = building[3]
                resources = building[4]
                new_building = Building(industry_type, stats, price, beers, resources)
                
                if i == 0:
                    self.iron_works.append(new_building)
                elif i == 1:
                    self.coal_mines.append(new_building)
                elif i == 2:
                    self.breweries.append(new_building)
                elif i == 3:
                    self.potteries.append(new_building)
                elif i == 4:
                    self.manufactories.append(new_building)
                else:
                    self.cotton_mills.append(new_building)
    
    def createIronWorks(self):
        self.createBuildingType(0)
    def createCoalMines(self):
        self.createBuildingType(1) 
    def createBreweries(self):
        self.createBuildingType(2)
    def createManufactories(self):
        self.createBuildingType(3)
    def createPotteries(self):
        self.createBuildingType(4)
    def createCottonMills(self):
        self.createBuildingType(5)
   
    def createBuildings(self):
        self.createIronWorks()
        self.createCoalMines()
        self.createBreweries()
        self.createManufactories()
        self.createPotteries()
        self.createCottonMills()

    def __init__(self, id, game):
        self.id = id
        self.iron_works = []
        self.coal_mines = []
        self.breweries = []
        self.potteries = []
        self.manufactories = []
        self.cotton_mills = []

        self.buildings_on_board = []

        self.createBuildings()
        self.victory_points = 0
        self.income = 0
        self.coins = 17

        self.has_industry_wildcard = False
        self.has_city_wildcard = False
        self.cards = []
        self.discard_pile = [] # could be useful for checking the probability of getting a certain card 
        self.game = game # reference to the game you are playing

    def spendCoins(self, price):
        self.coins -= price[0]
        while price[1] > 0:
            self.game.board.coal_market.removeResources()
            price[1] -= 1

        while price[2] > 0:
            self.game.board.iron_market.removeResources()
            price[2] -= 1

    def canBuild(self, location, building):
        if not(self.game.first_era) and building.level == 1 and building.industry_type != IndustryType.POTTERY:
            return False    
        if not(location.isAvailable(building.industry_type, self.id)):
            return False
        if self.coins < getCost(building.cost, self.game):
            return False

        return True

    def build(self, location, building): # builds a building
        if self.canBuild(location, building):
            self.spendCoins(building.price)
           
            if building.industry_type == IndustryType.BREWERY and self.game.first_era == False:
                building.resources = 2

            new_building = BuildingInstance(building, self.id)
            location.addBuilding(new_building)
            self.buildings_on_board.append(new_building) # this makes it easier to score up the buildings at the end
            
            for link in location.parent.adjacent:
                link.points += building.stats[2] # doing this now so I don't have to travel the entrie graph when doing MTS 
            
            return True

        return False

    def network(self, city1, city2):         # build a canal/rail
        if self.game.first_era == True: 
            price = (3, 0, 0)
        else:
            price = (5, 1, 0)
            price2 = (15, 2, 1)
        for link in city1.adjacent:
            for city in links.cities:
                if city == city2:
                    if self.coins >= price[0] + price[1] * self.game.getCoalPrice(): # I'll also need to consider the case when you build 2 rails with one actions
                        # but I need the logic for finding access to a beer, which is also used in the sell action
                        self.coins -= price[0] + price[1] * self.game.getCoalPrice()
                        if price[1] != 0:
                            self.game.board.coal_market.removeResources()
                        
                        links.changeOwnership(self.id)
                        return True
                    return False

        return False

    def develop(self, industry_type, once=True): # removes one or two cards(lowest level possible) from the available buildings, granting access to higher level buildings
        price = self.game.getIronPrice()
        if not(once):
            price += self.game.getIronPrice()

        if self.coins < price:
            return False

        self.coins -= price

        if industry_type == IndustryType.IRONWORKS and len(self.iron_works) > 1:
            self.iron_works.pop()
            if not(once) and len(self.iron_works) > 1:
                self.iron_works.pop()
        elif industry_type == IndustryType.COALMINE and len(self.coal_mines) > 1:
            self.coal_mines.pop()
            if not(once) and len(self.coal_mines) > 1:
                self.iron_works.pop()
        elif industry_type == IndustryType.POTTERY and len(self.potteries) > 1:
            self.potteries.pop()
            if not(once) and len(self.potteries) > 1:
                self.potteries.pop()
        elif industry_type == IndustryType.MANUFACTORY and len(self.manufactories) > 1:
            self.manufactories.pop()
            if not(once) and len(self.manufactories) > 1:
                self.manufactories.pop()
        elif industry_type == IndustryType.COTTONMILL and len(self.cotton_mills) > 1:
            self.cotton_mills.pop()
            if not(once) and len(self.cotton_mills) > 1:
                self.cotton_mills.pop()
        elif industry_type == IndustryType.BREWERY and len(self.breweries) > 1:
            self.breweries.pop()
            if not(once) and len(self.breweries) > 1:
                self.breweries.pop()
        else:
            return False # Unknown industry type

        return True

    def availableBeer(self): # check if you have the necessary beer available
        available_beer = 0
        for building_instance in self.buildings_on_board:
            if building_instance.building.industry_type == IndustryType.BREWERY and building_instance.sold == False:
                available_beer += building_instance.building.resources
                
        # I need to do a graph traversal in order to find if player has access to other breweries, I should find a way to optimize this

    def sell(self, targets): # the target is a building or multiple buildings
        necessary_beer = 0
        for target in targets:
            necessary_beer += target.building.cost[3]
        if self.availableBeer() >= necessary_beer: # check if has access to enough beer, then you need to determine which beers to use
            target.sold = True
            self.income += target.stats[1]
            self.victory_points += target.stats[0]

    def loan(self):
        self.coins += 30
        self.adjustIncome(loan=True)

    def scout(self, cards):
        if len(cards) != 3:
            return -1

        for card in cards:
            self.discardCard(card)

        self.has_city_wildcard = True 
        self.has_industry_wildcard = True # basically you draw wildcards, but I don't represent them as usual cards because its easier to simply create 2 bools

    def drawCard(self, card):
        self.cards.append(card)

    def discardCard(self, target): # discard a card from hand
        self.discard_pile.append(target)
        self.cards.remove(target) # find a way to choose which card to discard
        
    # up to income level 0, there is one step between levels VP 0 - 10
    # up to income level 10, there are 2 steps between levels VP 11 -30
    # up to income level 20, there are 3 steps between levels VP 31 - 60
    # up to income level 29, there are 4 steps between levels VP 61 - 96
    # for income level 30, there are 3 steps, and I guess you can't have more than 30 income VP 97 - 99

    def incomeStepsToLevel(self, income):
        if income > 60:
            return 21 + int((income - 61) / 4)
        elif income > 30:
            return 11 + int((income - 31) / 3)
        elif income > 10:
            return 1 + int((income - 11) / 2)
        else
            return (income - 10)

    def incomeLevelToSteps(self, level):
        if level == 30:
            return 99
        elif level > 20:
            return 60 + (level - 20) * 4
        elif level > 10:
            return 30 + (level - 10) * 3 
        elif level > 0:
            return 10 + level * 2
        else:
            return 10 + level

    def adjustIncome(self, loan = False, steps = 0):
        if loan:
            self.income = self.incomeLevelToSteps(self.incomeStepsToLevel(self.income) - 3)
        else:
            self.income += steps

