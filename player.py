# classes related to storing player state
# such as victory points, money, income, hand (the cards you have), buildings available
# to reach a higher level building you first have to exhaust the lower level ones

# there are also actions you can take every round

from board import IndustryType
from board import BuildingInstance
from board import TradingHub
from board import BFS
from board import isBrewery
from board import isTradingHub
from board import isIronWorks
from board import isCoalMine
import random

class Building:
    def __init__(self, level, industry_type, stats, price, beers=0, resources=0):
        self.level = level
        self.industry_type = industry_type
        self.stats = stats
        self.price = price
        self.beers = beers # number of beers required for it to be sold
        self.resources = resources

    def __str__(self):
        return f"{self.industry_type} {self.level}   stats: {self.stats}   price: {self.price} {self.beers} produces: {self.resources}" 

    def __repr__(self):
        return f"{self.industry_type} {self.level}   stats: {self.stats}   price: {self.price} {self.beers} produces: {self.resources}" 

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
    def __init__(self, id, state, environment):
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
        self.income = 10
        self.coins = 17

        self.has_industry_wildcard = False
        self.has_city_wildcard = False
        self.cards = []
        self.discard_pile = [] # could be useful for checking the probability of getting a certain card 
        self.state = state # reference to the game you are playing
        self.environment = environment
        self.available_cities = []
        # reference to cities connected to the network
                                   # these cities can also be used when extending the network, since their adjacent links are 
                                   # the only ones that can be used to extend the current network
        self.links = [] # links placed by player, these form the player's network

    def createBuildingType(self, i):
        level = len(buildings[i])
        for building in reversed(buildings[i]): # taking in reverse so it's easier to remove buildings later
            for j in range(building[5]):
                industry_type = building[0]
                stats = building[1]
                price = building[2]
                beers = building[3]
                resources = building[4]
                new_building = Building(level, industry_type, stats, price, beers, resources)
                
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
            level -= 1
    
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
    
    def buildingPriority(self, target): # if it's yours, highest priority, if you have multiple buildings of the same type, the one with the lowest remaining resources should be even higher priority
        # if it's not yours, the more resources are left on it, the better
        priority = 0
        if not(isinstance(target, TradingHub)) and target.player_id == self.id:
            priority += 100
            priority -= target.building.resources
        elif isinstance(target, TradingHub):
            priority += 10
        else:
            priority +=  target.building.resources

        return priority

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
            if building_instance.building.industry_type == IndustryType.IRONWORKS:
                available_sources.append(building_instance)

        for player in self.state.players:
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
    
    def consumeResources(self, coal, coal_sources, iron, iron_sources, beer, beer_sources):
        if coal != 0:
            i = 0
            while coal > 0: # first the coal
                if isinstance(coal_sources[i] ,TradingHub):
                    while coal > 0:
                        coal -= 1 
                else:
                    while coal > 0 and coal_sources[i].building.resources > 0:
                        coal -= 1
                        coal_sources[i].building.resources -= 1

                i = i + 1 

        if iron != 0:
            i = 0
            while iron > 0 and i < len(iron_sources):  # consume the iron
                while iron > 0 and iron_sources[i].building.resources > 0:
                    iron -= 1
                    iron_sources[i].building.resources -= 1

                i = i + 1    

            while iron > 0: # couldn't get all the necessary iron from the board
                self.state.board.iron_market.removeResource()
                iron -= 1
 
        if beer != 0:
            i = 0
            while beer > 0 and i < len(beer_sources):  # consume the beer
                while beer > 0 and beer_sources[i].building.resources > 0:
                    beer -= 1
                    beer_sources[i].building.resources -= 1

                if beer > 0:
                    i = i + 1   

    def canBuild(self, location, building):
        if building is None:
            return None

        if not(self.environment.first_era) and building.level == 1 and building.industry_type != IndustryType.POTTERY:
            return None
        
        if not(location.isAvailable(self.id, building.industry_type)):
            return None
        
        if self.coins < building.price[0]:
            return None

        cost = building.price[0]
        needed_coal = building.price[1]
        needed_iron = building.price[2]
        coal_sources = []
        available_coal = 0
        iron_sources = []
        available_iron = 0

        if needed_coal > 0:
            coal_sources = self.findCoal(location)

        print(coal_sources)
        if needed_iron > 0:
            iron_sources = self.findIron()

        for coal_source in coal_sources:
            if not(isinstance(coal_source, TradingHub)):
                available_coal += coal_source.building.resources

        for iron_source in iron_sources:
            available_iron += iron_source.building.resources

        if available_coal < needed_coal:
            connected_to_market = False
            for coal_source in coal_sources:
                if isinstance(coal_source, TradingHub):
                    connected_to_market = True

            if not(connected_to_market):
                return None

            deficit = (needed_coal - available_coal) 
            cost += self.state.getCoalPrice(deficit)

        if available_iron < needed_iron:
            deficit = (needed_iron - available_iron)
            cost += self.state.getIronPrice(deficit)

        if self.coins < cost:
            return None
       
        return [cost, coal_sources, iron_sources]

    def build(self, location, building, costs): # builds a building
        cost = costs[0]
        needed_coal = building.price[1]
        coal_sources = costs[1]
        needed_iron = building.price[2]
        iron_sources = costs[2]
        
        self.consumeResources(needed_coal, coal_sources, needed_iron, iron_sources, 0, None)
        self.coins -= cost

        if building.industry_type == IndustryType.BREWERY and self.environment.first_era == False: # the brewery is the only industry that produces more in the second era
            building.resources = 2

        new_building = BuildingInstance(building, self.id)
        location.addBuilding(new_building)
        self.buildings_on_board.append(new_building) # this makes it easier to score up the buildings at the end
        if location not in self.available_cities:
            self.available_cities.append(location)

        for link in location.adjacent:
            link.points += building.stats[2] # doing this now so I don't have to travel the entire graph later

        if building.industry_type == IndustryType.IRONWORKS:
            self.iron_works.remove(building) 
        elif building.industry_type == IndustryType.COALMINE:
            self.coal_mines.remove(building) 
        elif building.industry_type == IndustryType.BREWERY:
            self.breweries.remove(building)
        elif building.industry_type == IndustryType.MANUFACTORY:
            self.manufactories.remove(building) 
        elif building.industry_type == IndustryType.COTTONMILL:
            self.cotton_mills.remove(building) 
        elif building.industry_type == IndustryType.POTTERY:
            self.potteries.remove(building)
      
    def canNetwork(self, link):
        if self.environment.first_era == True and self.coins >= 3:
            return [3]
        elif self.environment.first_era == False:
            coal_sources = []
            for city in link.cities:
                coal_sources.extend(self.findCoal(city))

            if len(coal_sources) != 0:
                cost = 5
                if isinstance(coal_sources[0], TradingHub):
                    cost += self.environment.getCoalPrice(self.state)
                
                if cost < self.coins:
                    return [5, 1, coal_sources]
                    
        return None

    def network(self, link, costs):   # build a canal/rail
                                                                # the agent may build a rail in the second era, followed by another one for free
                                                                # if it pays a price of 10 and has access to a beer
                                                                # will implement this when the agent chooses possible actions
        cost = costs[0]
        needed_coal = costs[1]
        coal_sources = costs[2]

        link.changeOwnership(self.id)
        self.links.append(link)
        for city in link.cities:
            if city not in self.available_cities:
                self.available_cities.append(city)
    
    def canDevelop(self, industry_types, once=True):
        if not(once) and industry_types[0] == industry_types[1]:
            if industry_types[0] == IndustryType.IRONWORKS:
                if len(self.iron_works) < 2:
                    return None
            elif industry_types[0] == IndustryType.COALMINE:
                if len(self.coal_mines) < 2:
                    return None
            elif industry_types[0] == IndustryType.MANUFACTORY:
                if len(self.manufactories) < 2:
                    return None
            elif industry_types[0] == IndustryType.COTTONMILL:
                if len(self.cotton_mills) < 2:
                    return None
            elif industry_types[0] == IndustryType.BREWERY:
                if len(self.breweries) < 2:
                    return None
            elif industry_types[0] == IndustryType.POTTERY:
                if len(self.potteries) < 2:
                    return None
            else:
                return None

        for industry_type in industry_types: 
            if industry_type == IndustryType.IRONWORKS:
                if len(self.iron_works) < 1:
                    return None
            elif industry_type == IndustryType.COALMINE:
                if len(self.coal_mines) < 1:
                    return None
            elif industry_type == IndustryType.MANUFACTORY:
                if len(self.manufactories) < 1:
                    return None
            elif industry_type == IndustryType.COTTONMILL:
                if len(self.cotton_mills) < 1:
                    return None
            elif industry_type == IndustryType.BREWERY:
                if len(self.breweries) < 1:
                    return None
            elif industry_type == IndustryType.POTTERY:
                if len(self.potteries) < 1:
                    return None
            else:
                return None

        needed_iron = 0
        if once:
            needed_iron = 1 
        else:
            needed_iron = 2

        iron_sources = self.findIron()    
        available_iron = 0

        for iron_source in iron_sources:
            available_iron += iron_source.building.resources
        
        cost = 0

        if available_iron < needed_iron:
            deficit = (needed_iron - available_iron)
            cost = self.state.getIronPrice(deficit)

        if self.coins >= cost:
            return [cost, needed_iron, iron_sources] 

        return None

    def develop(self, industry_types, costs, once=True): # removes one or two cards(lowest level possible) from the available buildings, granting access to higher level buildings
        cost = costs[0]
        needed_iron = costs[1]
        iron_sources = costs[2]
        self.consumeResources(0, None, needed_iron, iron_sources, 0, None)

        self.coins -= cost
        
        for industry_type in industry_types:
            if industry_type == IndustryType.IRONWORKS and len(self.iron_works) > 0:
                self.iron_works.pop()
            elif industry_type == IndustryType.COALMINE and len(self.coal_mines) > 0:
                self.coal_mines.pop()
            elif industry_type == IndustryType.POTTERY and len(self.potteries) > 0:
                self.potteries.pop()
            elif industry_type == IndustryType.MANUFACTORY and len(self.manufactories) > 0:
                self.manufactories.pop()
            elif industry_type == IndustryType.COTTONMILL and len(self.cotton_mills) > 0:
                self.cotton_mills.pop()
            elif industry_type == IndustryType.BREWERY and len(self.breweries) > 0:
                self.breweries.pop()
            else:
                return False # Unknown industry type

        return True

    def canSell(self, target): # check if you have access to a necessary market and the required beers
        if target.sold:
            return None
        
        industry_type = target.building.industry_type
        if industry_type == IndustryType.IRONWORKS or industry_type == IndustryType.COALMINE or industry_type == IndustryType.BREWERY:
            if target.building.resources == 0:
                return [0, None]
            return None

        needed_beer = target.building.beers
        markets = BFS(target, isTradingHub, full_search=True)
        beer_sources = self.findBeer(target)
        available_beer = 0
        for beer_source in beer_sources:
            available_beer += beer_source.building.resources

        #for market in markets:
        #    for i in range(len(market.squares)):
        #        square = market.squares[i]
        #        if market.taken[i] == False:
        #            for building_types in square.building_types:
        #                for building_type in building_types:
        #                    if target.industry_type == building_type and needed_beer == 1:
        #                       return [needed_beer, beer_sources, i, market] 
        # above code temporarily not used to reduce complexity for now

        if available_beer >= needed_beer:
            return [needed_beer, beer_sources]

        return None

    def sell(self, target, costs): # the target is a building or multiple buildings
        needed_beer = costs[0]
        beer_sources = costs[1] 

        self.consumeResources(0, None, 0, None, needed_beer, beer_sources)

        target.sold = True
        self.income += target.building.stats[1]
        self.victory_points += target.building.stats[0]

    def loan(self):
        self.coins += 30
        self.adjustIncome(loan=True)

    def scout(self, cards):
        for card in cards:
            self.discardCard(card)

        self.has_city_wildcard = True 
        self.has_industry_wildcard = True # basically you draw wildcards, but I don't represent them as usual cards because its easier to simply create 2 bools

    def drawCard(self, card):
        self.cards.append(card)

    def selectRandomCard(self):
        return random.choice(self.cards)

    def discardCard(self, target): # discard a card from hand
        self.discard_pile.append(target)
        self.cards.remove(target) # find a way to choose which card to discard
       
    def discardRandomCard(self):
        self.discardCard(self.selectRandomCard())

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

    def endTurn(self):
        for building_instance in self.buildings_on_board:
            industry_type = building_instance.building.industry_type
            if industry_type == IndustryType.IRONWORKS or industry_type == IndustryType.COALMINE or industry_type == IndustryType.BREWERY:
                if building_instance.building.resources == 0 and building_instance.sold == False:
                    self.sell(building_instance, [0, []])

        if self.income >= 10:
            self.coins += self.incomeStepsToLevel(self.income)

        while (len(self.cards) < 8):
           new_card = self.state.giveCardToPlayer(self.id) 
           if new_card == None: # no cards left 
               break
           else:
               self.cards.append(new_card)

    def getCoalmine(self):
        if len(self.coal_mines) == 0:
            return None

        return self.coal_mines[-1]

    def getIronworks(self):
        if len(self.iron_works) == 0:
            return None

        return self.iron_works[-1]

    def getManufactory(self):
        if len(self.manufactories) == 0:
            return None

        return self.manufactories[-1]

    def getCottonmill(self):
        if len(self.cotton_mills) == 0:
            return None

        return self.cotton_mills[-1]

    def getPottery(self):
        if len(self.potteries) == 0:
            return None

        return self.potteries[-1]

    def getBrewery(self):
        if len(self.breweries) == 0:
            return None

        return self.breweries[-1]

    def getStats(self):
        return [self.victory_points, self.income, self.coins]

    def printStats(self):
        print(f"player {self.id} VPs: {self.victory_points}, income: {self.income}, coins: {self.coins}")
