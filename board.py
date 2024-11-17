# Representation of the board of the game 'Brass -Birmingham'
# it's basically a undirected graph with extra properties

# The nodes are the cities, and each city has 1 or more building slots 
# building slots can accept only certain types of buildings
# the types of buildings in the game are: coal mine, iron works, brewery, manufactory, pottery, cotton mill

# each building type has different properties depending on its level, the 6 main properties are:
# its price in coins, its price in resources(coal or iron), the victory points it provides once sold,
# the income it provides every round, once sold, how many points the building grants to adjacent links
# and how many beers you need to use to sell that building

# iron works, coal mines and breweries don't require beers in order to be sold, they only need to exhaust
# the resources that they produce

# there are also trading hubs at the edge of the board, in this case you could call it 'the edge' of the graph
# there are 5 of them, and they kind of have their own building slots(1 or 2 of them)
# you cannot build there but based on the building types you need to connect to that hub in order to sell buildings
# of that type
# they also provide bonuses if you are the first to sell a building there, and that works by providing a 
# free beer for whoever sells first, so instead of consuming a beer produced by a brewery you consume 
# the beer that was on the trading hub
# the building types of a trading hub are selected arbitrarily at the start of the game
# some building slots may be empty,so if you have a link to that hub you can't sell any 
# building if the building slots are empty

from enum import Enum

class IndustryType(Enum):
    IRONWORKS = 0
    COALMINE = 1
    BREWERY = 2 
    MANUFACTORY = 3
    COTTONMILL = 4
    POTTERY = 5

class TradingHub:
    def __init__(self, name, bonus, buildings):
        self.name = name
        self.bonus = bonus
        self.buildings = buildings

class Building:
    def __init__(self, industry_type, stats, price, beers=0, resources=0):
        self.industry_type = industry_type
        self.stats = stats
        self.price = price
        self.beers = beers # number of beers required for it to be sold
        self.resources = resources

class BuildingSlot:
    def __init__(self, building, player_id):
        self.building = building
        self.player_id = player_id

class Square:
    def __init__(self):
        self.building_slots = []
    
    def add_building_slot(self, building_slot):
        self.building_slots.append(building_slot)

class City:
    def __init__(self, name):
        self.name = name
        self.adjacent = {}

    def add_neighbor(self, neighbor, connection_type):
        self.adjacent[neighbor] = connection_type

buildings = [[[IndustryType.IRONWORKS,( 3, 3, 1), (5, 1, 0), 0, 4],
              [IndustryType.IRONWORKS,( 5, 3, 1), (7, 1, 0), 0, 4],
              [IndustryType.IRONWORKS,( 7, 2, 1), (9, 1, 0), 0, 5],
              [IndustryType.IRONWORKS,( 9, 1, 1),(12, 1, 0), 0, 6]],
             [[IndustryType.COALMINE,( 1, 4, 2), (5, 0, 0), 0, 2],
              [IndustryType.COALMINE,( 2, 7, 1), (7, 0, 0), 0, 3],
              [IndustryType.COALMINE,( 3, 6, 1), (8, 0, 1), 0, 4],
              [IndustryType.COALMINE,( 4, 5, 1),(10, 0, 1), 0, 5]],
             [[IndustryType.BREWERY,( 4, 4, 2), (5, 0, 1), 0, 1],
              [IndustryType.BREWERY,( 5, 5, 2), (7, 0, 1), 0, 1],
              [IndustryType.BREWERY,( 7, 5, 2), (9, 0, 1), 0, 1],
              [IndustryType.BREWERY,(10,5, 2), (9, 0, 1), 0, 1]], # will have the modify the number of resources produced to 2 in second phase
             [[IndustryType.MANUFACTORY,( 5, 5, 1), (12, 0, 0), 1, 0],
              [IndustryType.MANUFACTORY,( 5, 4, 2), (14, 1, 0), 1, 0],
              [IndustryType.MANUFACTORY,( 9, 3, 1), (16, 1, 1), 1, 0],
              [IndustryType.MANUFACTORY,(12, 2, 1), (18, 1, 1), 1, 0]],
             [[IndustryType.POTTERY,(10, 5, 1), (17, 0, 1), 1, 0],
              [IndustryType.POTTERY,( 1, 1, 1), ( 0, 1, 0), 1, 0],
              [IndustryType.POTTERY,(11, 5, 1), (22, 2, 0), 2, 0],
              [IndustryType.POTTERY,( 1, 1, 1), ( 0, 1, 0), 1, 0],
              [IndustryType.POTTERY,(20, 5, 1), (24, 2, 0), 2, 0]],
             [[IndustryType.COTTONMILL,( 3, 5, 2), ( 8, 1, 0), 1, 0],
              [IndustryType.COTTONMILL,( 5, 1, 1), (10, 0, 1), 1, 0],
              [IndustryType.COTTONMILL,( 4, 4, 0), (12, 2, 0), 0, 0],
              [IndustryType.COTTONMILL,( 3, 6, 1), ( 8, 0, 1), 1, 0],
              [IndustryType.COTTONMILL,( 8, 2, 2), (16, 1, 0), 2, 0],
              [IndustryType.COTTONMILL,( 7, 6, 1), (20, 0, 0), 1, 0],
              [IndustryType.COTTONMILL,( 9, 4, 0), (16, 1, 1), 0, 0],
              [IndustryType.COTTONMILL,(11, 1, 0), (20, 0, 2), 1, 0]]]

class Board:
    iron_works = []
    coal_mines = []
    breweries = []
    manufactories = []
    potteries = []
    cotton_mills = []

    def __init__(self):
        pass
    
    def createIronWorks(self):
        building = Building(IndustryType.IRONWORKS, 4, 3, 1, (7, 1, 0) , 1, 0, 4)
        self.iron_works.append(building)
        building = Building(IndustryType.IRONWORKS, )
    def createCoalMines(self):
        pass 
    def createBreweries(self):
        pass
    def createManufactories(self):
        pass 
    def createPotteries(self):
        pass 
    def createCottonMills(self):
        pass
    
    def createBuildings(self):
        createIronWorks(self)
        createCoalMines(self)
        createBreweries(self)
        createManufactories(self)
        createPotteries(self)
        createCottonMills(self)

    
