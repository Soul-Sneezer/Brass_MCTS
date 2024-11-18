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

class LinkType(Enum):
    BOTH = 0
    RAIL = 1
    CANAL = 2

class BonusType(Enum):
    VICTORY_POINTS = 0
    COINS = 1
    INCOME = 2
    INNOVATION = 3

class IndustryType(Enum):
    IRONWORKS = 0
    COALMINE = 1
    BREWERY = 2 
    MANUFACTORY = 3
    COTTONMILL = 4
    POTTERY = 5

class TradingHub:
    def __init__(self, name, bonus):
        self.name = name
        self.bonus = bonus
        self.squares = []

    def addSquare(self, square):
        self.squares.append(square)

class Market:
    def __init__(self, resources, maximum_resources):
        self.resources = resources
        self.maximum_resources = maximum_resources

    def getPrice(self):
        resources_spent = self.maximum_resources - self.resources
        if resources_spent % 2 == 1:
            resources_spent = resources_spent + 1
        return 1 + resources_spent / 2

class BuildingSlot:
    def __init__(self, building, player_id):
        self.building = building
        self.player_id = player_id

class Square:
    def __init__(self, buildings):
        self.building_types = buildings
    
class City:
    def __init__(self, name):
        self.name = name
        self.adjacent = {}
        self.squares = []
    
    def add_square(self, square):
        self.squares.append(square)

    def add_neighbor(self, neighbor, connection_type):
        self.adjacent[neighbor] = connection_type

class Board:
    iron_works = []
    coal_mines = []
    breweries = []
    manufactories = []
    potteries = []
    cotton_mills = []

    cities = []
    trading_hubs = []
       
    
    def createLocations(self): # basically creates the whole map
        stoke_on_trent = City("Stoke-On-Trent")
        leek = City("Leek")
        belper = City("Belper")
        stone = City("Stone")
        uttoxeter = City("Uttoxeter")
        derby = City("Derby")
        stafford = City("Stafford")
        burton_on_trent = City("Burton-On-Trent")
        cannock = City("Cannock")
        tamworth = City("Tamworth")
        coalbrookdale = City("Coalbrookdale")
        wolverhampton = City("Wolverhampton")
        walsall = City("Walsall")
        nuneaton = City("Nuneaton")
        dudley = City("Dudley")
        birmingham = City("Birmingham")
        coventry = City("Coventry")
        kidderminster = City("Kidderminster")
        worcester = City("Worcester")
        redditch = City("Redditch")
        unnamed_city0 = City("City0")
        unnamed_city1 = City("City1")

        stoke_on_trent.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COTTONMILL)))
        stoke_on_trent.add_square(Square((IndustryType.POTTERY, IndustryType.IRONWORKS)))
        stoke_on_trent.add_square(Square((IndustryType.COTTONMILL)))

        leek.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COTTONMILL)))
        leek.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COALMINE)))

        belper.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COTTONMILL)))
        belper.add_square(Square((IndustryType.COALMINE)))
        belper.add_square(Square((IndustryType.POTTERY)))

        stone.add_square(Square((IndustryType.MANUFACTORY, IndustryType.BREWERY)))
        stone.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))

        uttoxeter.add_square(Square((IndustryType.COTTONMILL, IndustryType.BREWERY)))
        uttoxeter.add_square(Square((IndustryType.MANUFACTORY, IndustryType.BREWERY)))

        derby.add_square(Square((IndustryType.MANUFACTORY, IndustryType.BREWERY)))
        derby.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COTTONMILL)))
        derby.add_square(Square((IndustryType.IRONWORKS)))

        burton_on_trent.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))
        burton_on_trent.add_square(Square((IndustryType.BREWERY)))

        tamworth.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COALMINE)))
        tamworth.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COALMINE)))

        walsall.add_square(Square((IndustryType.IRONWORKS, IndustryType.COTTONMILL)))
        walsall.add_square(Square((IndustryType.COTTONMILL, IndustryType.BREWERY)))

        birmingham.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COTTONMILL)))
        birmingham.add_square(Square((IndustryType.COTTONMILL)))
        birmingham.add_square(Square((IndustryType.IRONWORKS)))
        birmingham.add_square(Square((IndustryType.COTTONMILL)))

        nuneaton.add_square(Square((IndustryType.COTTONMILL, IndustryType.BREWERY)))
        nuneaton.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COALMINE)))

        coventry.add_square(Square((IndustryType.POTTERY)))
        coventry.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))
        coventry.add_square(Square((IndustryType.IRONWORKS, IndustryType.COTTONMILL)))

        redditch.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))
        redditch.add_square(Square((IndustryType.IRONWORKS)))

        stafford.add_square(Square((IndustryType.COTTONMILL, IndustryType.BREWERY)))
        stafford.add_square(Square((IndustryType.POTTERY)))

        cannock.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))
        cannock.add_square(Square((IndustryType.COALMINE)))

        unnamed_city0.add_square(Square((IndustryType.BREWERY)))

        wolverhampton.add_square(Square((IndustryType.COTTONMILL)))
        wolverhampton.add_square(Square((IndustryType.COTTONMILL, IndustryType.COALMINE)))

        coalbrookdale.add_square(Square((IndustryType.IRONWORKS, IndustryType.BREWERY)))
        coalbrookdale.add_square(Square((IndustryType.IRONWORKS))) 
        coalbrookdale.add_square(Square((IndustryType.COALMINE)))

        dudley.add_square(Square((IndustryType.COALMINE)))
        dudley.add_square(Square((IndustryType.IRONWORKS)))

        kidderminster.add_square(Square((IndustryType.MANUFACTORY, IndustryType.COALMINE)))
        kidderminster.add_square(Square((IndustryType.MANUFACTORY)))

        worcester.add_square(Square((IndustryType.MANUFACTORY)))
        worcester.add_square(Square((IndustryType.MANUFACTORY)))

        unnamed_city1.add_square(Square((IndustryType.BREWERY)))

        stoke_on_trent.add_neighbor(stone, LinkType.BOTH)
        stoke_on_trent.add_neighbor(leek, LinkType.BOTH)
        
        leek.add_neighbor(belper, LinkType.RAIL)
        leek.add_neighbor(stoke_on_trent, LinkType.BOTH)

        belper.add_neighbor(leek, LinkType.RAIL)
        belper.add_neighbor(derby, LinkType.BOTH)

        derby.add_neighbor(belper, LinkType.BOTH)
        derby.add_neighbor(burton_on_trent, LinkType.BOTH)
        derby.add_neighbor(uttoxeter, LinkType.RAIL)

        uttoxeter.add_neighbor(derby, LinkType.RAIL)
        uttoxeter.add_neighbor(stone, LinkType.RAIL)

        burton_on_trent.add_neighbor(derby, LinkType.BOTH)
        burton_on_trent.add_neighbor(stone, LinkType.BOTH)
        burton_on_trent.add_neighbor(tamworth, LinkType.BOTH)
        burton_on_trent.add_neighbor(cannock, LinkType.RAIL)
        burton_on_trent.add_neighbor(walsall, LinkType.CANAL)

        stone.add_neighbor(burton_on_trent, LinkType.BOTH)
        stone.add_neighbor(stafford, LinkType.BOTH)
        stone.add_neighbor(uttoxeter, LinkType.RAIL)
        stone.add_neighbor(stoke_on_trent, LinkType.BOTH)

        stafford.add_neighbor(stone, LinkType.BOTH)
        stafford.add_neighbor(cannock, LinkType.BOTH)

        cannock.add_neighbor(stafford, LinkType.BOTH)
        cannock.add_neighbor(wolverhampton, LinkType.BOTH)
        cannock.add_neighbor(unnamed_city0, LinkType.BOTH)
        cannock.add_neighbor(burton_on_trent, LinkType.RAIL)

        unnamed_city0.add_neighbor(cannock, LinkType.BOTH)

        tamworth.add_neighbor(burton_on_trent, LinkType.BOTH)
        tamworth.add_neighbor(nuneaton, LinkType.BOTH)
        tamworth.add_neighbor(birmingham, LinkType.BOTH)
        tamworth.add_neighbor(walsall, LinkType.RAIL)

        nuneaton.add_neighbor(tamworth, LinkType.BOTH)
        nuneaton.add_neighbor(birmingham, LinkType.RAIL)
        nuneaton.add_neighbor(coventry, LinkType.RAIL)

        coventry.add_neighbor(nuneaton, LinkType.RAIL)
        coventry.add_neighbor(birmingham, LinkType.BOTH)

        birmingham.add_neighbor(coventry, LinkType.BOTH)
        birmingham.add_neighbor(nuneaton, LinkType.RAIL)
        birmingham.add_neighbor(tamworth, LinkType.BOTH)
        birmingham.add_neighbor(walsall, LinkType.BOTH)
        birmingham.add_neighbor(redditch, LinkType.RAIL)
        birmingham.add_neighbor(dudley, LinkType.BOTH)
        birmingham.add_neighbor(worcester, LinkType.BOTH)

        walsall.add_neighbor(birmingham, LinkType.BOTH)
        walsall.add_neighbor(tamworth, LinkType.RAIL)
        walsall.add_neighbor(burton_on_trent, LinkType.CANAL)
        walsall.add_neighbor(cannock, LinkType.BOTH)
        walsall.add_neighbor(wolverhampton, LinkType.BOTH)

        dudley.add_neighbor(birmingham, LinkType.BOTH)
        dudley.add_neighbor(wolverhampton, LinkType.BOTH)
        dudley.add_neighbor(kidderminster, LinkType.BOTH)

        redditch.add_neighbor(birmingham, LinkType.RAIL)

        worcester.add_neighbor(birmingham, LinkType.BOTH)
        worcester.add_neighbor(kidderminster, LinkType.BOTH)
        worcester.add_neighbor(unnamed_city1, LinkType.BOTH)

        unnamed_city1.add_neighbor(worcester, LinkType.BOTH)
        unnamed_city1.add_neighbor(kidderminster, LinkType.BOTH)

        wolverhampton.add_neighbor(walsall, LinkType.BOTH)
        wolverhampton.add_neighbor(dudley, LinkType.BOTH)
        wolverhampton.add_neighbor(coalbrookdale, LinkType.BOTH)
        wolverhampton.add_neighbor(cannock, LinkType.BOTH)

        coalbrookdale.add_neighbor(wolverhampton, LinkType.BOTH)
        coalbrookdale.add_neighbor(kidderminster, LinkType.BOTH)

        nottingham = TradingHub("Nottingham", (BonusType.VICTORY_POINTS, 3))
        oxford = TradingHub("Oxford", (BonusType.INCOME, 2))
        gloucester = TradingHub("Gloucester", (BonusType.INNOVATION, 1))
        shrewsbury = TradingHub("Shrewsbury", (BonusType.VICTORY_POINTS, 4)) 
        warrington = TradingHub("Warrington", (BonusType.COINS, 5))
       
        derby.add_neighbor(nottingham, LinkType.BOTH)
        stoke_on_trent.add_neighbor(warrington, LinkType.BOTH)
        birmingham.add_neighbor(oxford, LinkType.BOTH)
        redditch.add_neighbor(oxford, LinkType.BOTH)
        redditch.add_neighbor(gloucester, LinkType.BOTH)
        worcester.add_neighbor(gloucester, LinkType.BOTH)
        coalbrookdale.add_neighbor(shrewsbury, LinkType.BOTH)

        self.cities.append(stoke_on_trent)
        self.cities.append(stone)
        self.cities.append(leek)
        self.cities.append(belper)
        self.cities.append(uttoxeter)
        self.cities.append(derby)
        self.cities.append(burton_on_trent)
        self.cities.append(stafford)
        self.cities.append(cannock)
        self.cities.append(unnamed_city0)
        self.cities.append(walsall)
        self.cities.append(tamworth)
        self.cities.append(coalbrookdale)
        self.cities.append(wolverhampton)
        self.cities.append(birmingham)
        self.cities.append(nuneaton)
        self.cities.append(coventry)
        self.cities.append(dudley)
        self.cities.append(worcester)
        self.cities.append(unnamed_city1)
        self.cities.append(kidderminster)
        self.cities.append(redditch)

        self.trading_hubs.append(nottingham)
        self.trading_hubs.append(oxford)
        self.trading_hubs.append(gloucester)
        self.trading_hubs.append(shrewsbury)
        self.trading_hubs.append(warrington)

    def __init__(self):
        self.coal_market = Market(13, 14)
        self.iron_market = Market(8, 10)
        
        self.createLocations()

