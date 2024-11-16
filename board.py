# Representation of the board of the game 'Brass -Birmingham'
# it's basically a undirected graph with extra properties

# The nodes are the cities, and each city has 1 or more building slots 
# building slots can accept only certain types of buildings
# the types of buildings in the game are: coal mine, iron works, brewery, manufacturer, pottery, cotton mill

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

class TradingHub:
    def __init__(self, name, bonus, buildings):
        self.name = name
        self.bonus = bonus
        self.buildings = buildings

class Building:
    def __init__(self, industry_type, income, victory_points, level, price, active, link_bonus, beers=0, resources=0):
        self.industry_type = industry_type
        self.income = income
        self.victory_points = victory_points
        self.level = level
        self.price = price
        self.active = active
        self.link_bonus = link_bonus
        self.beers = beers # number of beers required for it to be sold
        self.resources = resources

class BuildingSlot:
    def __init__(self, industry):
        self.industry = industry

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

class Board:
    def __init__(self):
        pass
