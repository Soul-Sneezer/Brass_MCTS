# classes related to storing player state
# such as victory points, money, income, hand (the cards you have), buildings available
# to reach a higher level building you first have to exhaust the lower level ones

# there are also actions you can take every round

from board import IndustryType
from board import BuildingInstance
from game import Game
from enum import Enum
from board import BFS
from board import isBrewery
from board import isTradingHub
from board import isIronWorks
from board import isCoalMine

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

    def buildingPriority(self, target): # if it's yours, highest priority, if you have multiple buildings of the same type, the one with the lowest remaining resources should be even higher priority
        # if it's not yours, the more resources are left on it, the better
        priority = 0
        if target.player_id == self.id:
            priority += 100
            priority -= target.building.resources
        else:
            priority +=  target.building.resources

        return priority

    def spendCoins(self, price):
        self.coins -= price[0]
        while price[1] > 0:
            self.game.board.coal_market.removeResources()
            price[1] -= 1

        while price[2] > 0:
            self.game.board.iron_market.removeResources()
            price[2] -= 1

    def findBeer(self, target):
        available_sources = [] 
        for building_instance in self.buildings_on_board:
            if building_instance.building.industry_type == IndustryType.BREWERY:
                available_sources.append(building_instance)

        external_sources = BFS(target, isBrewery, full_search=True)
        available_sources.extend(external_sources)

        available_sources.sort(key=self.buildingPriority)
        return available_sources

    def findIron(self):
        available_sources = [] 
        for building_instance in self.buildings_on_board:
            if building_instance.building.industry_type == IndustryType.BREWERY:
                available_sources.append(building_instance)

        for player in self.game.players:
            if player.id != self.id:
                for building_instance in player.buildings_on_board:
                    if building_instance.building.industry_type == IndustryType.IRONWORKS:
                        available_sources.append(building_instance)

        available_sources.sort(key=self.buildingPriority)
        return available_sources

    def findCoal(self, target):
        available_sources = BFS(target, isCoalMine)
        available_sources.sort(key=self.buildingPriority)
        return available_sources

    def canBuild(self, location, building):
        if not(self.game.first_era) and building.level == 1 and building.industry_type != IndustryType.POTTERY:
            return False    
        if not(location.isAvailable(building.industry_type, self.id)):
            return False
        if self.coins < building.cost[0]:
            return False

        cost = building.cost[0]
        needed_coal = building.cost[1]
        needed_iron = building.cost[2]
        coal_sources = []
        available_coal = 0
        iron_sources = []
        available_iron = 0

        if needed_coal > 0:
            coal_sources = self.findCoal(location)

        if needed_iron > 0:
            iron_sources = self.findIron()

        for coal_source in coal_sources:
            available_coal += coal_source.building.resources

        for iron_source in iron_sources:
            available_iron += iron_source.building.resources

        for beer_source in beer_sources:
            available_beer += beer_source.building.resources

        if available_coal < needed_coal:
            deficit = (needed_coal - available_coal) 
            cost += self.game.getCoalPrice(deficit)

        if available_iron < needed_iron:
            deficit = (needed_iron - available_iron)
            cost += self.game.getIronPrice(deficit)

        if self.coins < cost:
            return False
        else:
            self.coins -= cost
       
        # spend the resources now
        i = 0
        while needed_coal > 0 and i < len(coal_sources): # first the coal
            while needed_coal > 0 and coal_sources[i].building.resources > 0:
                needed_coal -= 1
                coal_sources[i].building.resources -= 1

            if needed_coal > 0:
                self.sell(coal_sources[i].building)
                i = i + 1 

        while needed_coal > 0: # couldn't get all the necessary coal from the board
            self.game.coal_market.removeResource()
            needed_coal -= 1

        i = 0
        while needed_iron > 0 and i < len(iron_sources):  # now the iron
            while needed_iron > 0 and iron_sources[i].building.resources > 0:
                needed_iron -= 1
                iron_sources[i].building.resources -= 1

            if needed_iron > 0:
                self.sell(iron_sources[i].building)
                i = i + 1    

        while needed_iron > 0: # couldn't get all the necessary beer from the board
            self.game.iron_market.removeResource()
            needed_iron -= 1

        return True

    def build(self, location, building): # builds a building
        if self.canBuild(location, building): # canBuild also handles the spending part, if you can build
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
            if self.coins >= 3:
                for link in city1.adjacent:
                    for city in link.cities:
                        if city == city2:
                            self.coins -= 3 
                            link.changeOwnership(self.id)
                            return True
            else:
                return False
        else:
            for link in city1.adjacent:
                for city in link.cities:
                    if city == city2:
                        coal_sources = self.findCoal(city2)
                        coal_sources.extend(self.findCoal(city1))

                        if len(coal_sources) == 0:
                            if self.coins >= 5 + self.game.getCoalPrice(): # I'll also need to consider the case when you build 2 rails with one actions
                                # but I need the logic for finding access to a beer, which is also used in the sell action
                                self.coins -= 5 + self.game.getCoalPrice()
                                self.game.board.coal_market.removeResources()
                                
                                link.changeOwnership(self.id)
                                return True
                            else:
                                return False
                        else:
                            coal_sources[0].building.resources -= 1
                            if coal_sources[0].building.resources == 0:
                                sell(coal_sources[0])
                            if self.coins >= 5:
                                self.coins -= 5
                                link.changeOwnership(self.id)
                                return True
                            else:
                                return False

                        return False

        return False

    def network2(self, city1, city2, city3, city4): # only available in second era 
        if city2 == city3: # so we make one long route


        i = 0
        while needed_coal > 0 and i < len(coal_sources): # first the coal
            while needed_coal > 0 and coal_sources[i].building.resources > 0:
                needed_coal -= 1
                coal_sources[i].building.resources -= 1

            if needed_coal > 0:
                self.sell(coal_sources[i].building)
                i = i + 1 

        while needed_coal > 0: # couldn't get all the necessary coal from the board
            self.game.coal_market.removeResource()
            needed_coal -= 1


    def develop(self, industry_types, once=True): # removes one or two cards(lowest level possible) from the available buildings, granting access to higher level buildings
        needed_iron = 0
        if once:
            needed_iron = 1 
        else:
            needed_iron = 2

        iron_sources = self.findIron()    
        available_iron = 0

        for iron_source in iron_sources:
            available_iron += iron_source.building.resources
        
        if available_iron < needed_iron:
            deficit = (needed_iron - available_iron)
            self.coins -= self.game.getIronPrice(deficit)

        i = 0
        while needed_iron > 0 and i < len(iron_sources):  # consume the iron
            while needed_iron > 0 and iron_sources[i].building.resources > 0:
                needed_iron -= 1
                iron_sources[i].building.resources -= 1

            if needed_iron > 0:
                self.sell(iron_sources[i].building)
                i = i + 1    

        while needed_iron > 0: # couldn't get all the necessary beer from the board
            self.game.iron_market.removeResource()
            needed_iron -= 1

        for industry_type in industry_types:
            if industry_type == IndustryType.IRONWORKS and len(self.iron_works) > 1:
                self.iron_works.pop()
            elif industry_type == IndustryType.COALMINE and len(self.coal_mines) > 1:
                self.coal_mines.pop()
            elif industry_type == IndustryType.POTTERY and len(self.potteries) > 1:
                self.potteries.pop()
            elif industry_type == IndustryType.MANUFACTORY and len(self.manufactories) > 1:
                self.manufactories.pop()
            elif industry_type == IndustryType.COTTONMILL and len(self.cotton_mills) > 1:
                self.cotton_mills.pop()
            elif industry_type == IndustryType.BREWERY and len(self.breweries) > 1:
                self.breweries.pop()
            else:
                return False # Unknown industry type

        return True

    def canSell(self, target, necessary_beer): # check if you have access to a necessary market and the required beers
        industry_type = target.building.industry_type
        if industry_type == IndustryType.IRONWORKS or industry_type == IndustryType.COALMINE or industry_type == IndustryType.BREWERY:
            if target.building.resources == 0:
                return True
            return False

        needed_beer = target.building.beers
        markets = BFS(target, isTradingHub, full_search=True)
        beer_sources = self.findBeer(target)
        available_beer = 0
        for beer_source in beer_sources:
            available_beer += beer_source.building.resources

        if available_beer < needed_beer:
            return False

        for market in markets:
            for square in market.squares:
                for building_types in square.building_types:
                    for building_type in building_types:
                        if target.industry_type == building_type and available_beer >= necessary_beer:
                            return True

        return False

    def sell(self, target): # the target is a building or multiple buildings
        necessary_beer = target.building.cost[3]
        
        if self.canSell(target, necessary_beer): # check if has access to enough beer, then you need to determine which beers to use
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
        else:
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

