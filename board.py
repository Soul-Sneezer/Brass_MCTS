# Representation of the board of the game 'Brass -Birmingham'
# it's basically an undirected graph with extra properties

# The nodes are the cities, and each city has 1 or more building slots 
# building slots can accept only certain types of buildings
# the types of buildings in the game are: coal mine, iron works, brewery, manufactory, pottery, cotton mill

# each building type has different properties depending on its level, the 6 main properties are:
# its price in coins, its price in resources(coal or iron), the victory points it provides once sold,
# the income it provides every round, once sold, how many points the building grants to adjacent links
# once again, after you sell it
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
        self.squares.append(square)https://towardsdatascience.com/the-mostly-complete-chart-of-neural-networks-explained-3fb6f2367464?gi=8d4f2e42595b

class Market:
    def __init__(self, resources, maximum_resources):
        self.resources = resources
        self.maximum_resources = maximum_resources

    def getPrice(self):
        resources_spent = self.maximum_resources - self.resources
        if resources_spent % 2 == 1:
            resources_spent = resources_spent + 1
        return 1 + resources_spent / 2

class BuildingInstance:
    def __init__(self, building, player_id, sold):
        self.building = building
        self.player_id = player_id
        self.sold = False

class Square:
    def __init__(self, buildings):
        self.building_types = buildings
   
class Link: 
    def __init__(self, connected_cities, link_type):
        self.owner_id = None
        self.link_type = link_type
        self.points = 0
        for city in connected_cities:
            self.cities.append(city)
            city.add_connection(self)
    
    def change_ownership(self, owner):
        self.owner_id = owner

class City:
    def __init__(self, name):
        self.name = name
        self.adjacent = []
        self.squares = []
    
    def add_square(self, square):
        self.squares.append(square)

    def add_connection(self, connection):
        self.adjacent.append(connection)

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
        
        nottingham = TradingHub("Nottingham", (BonusType.VICTORY_POINTS, 3))
        oxford = TradingHub("Oxford", (BonusType.INCOME, 2))
        gloucester = TradingHub("Gloucester", (BonusType.INNOVATION, 1))
        shrewsbury = TradingHub("Shrewsbury", (BonusType.VICTORY_POINTS, 4)) 
        warrington = TradingHub("Warrington", (BonusType.COINS, 5))

        shrewsbury_coalbrookdale = Link([coalbrookdale, shrewsbury], LinkType.BOTH)
        coalbrookdale_wolverhampton = Link([coalbrookdale, wolverhampton], LinkType.BOTH)
        coalbrookdale_kidderminster = Link([coalbrookdale, wolverhampton], LinkType.BOTH)
        kidderminster_worcester = Link([kidderminster, worcester, unnamed_city1], LinkType.BOTH)
        kidderminster_dudley = Link([kidderminster, dudley], LinkType.BOTH)
        worcester_gloucester = Link([worcester, gloucester], LinkType.BOTH)
        worcester_birmingham = Link([worcester, birmingham], LinkType.BOTH)
        dudley_wolverhampton = Link([dudley, wolverhampton], LinkType.BOTH)
        dudley_birmingham = Link([dudley, birmingham], LinkType.BOTH)
        wolverhampton_cannock = Link([wolverhampton, cannock], LinkType.BOTH)
        wolverhampton_walsall = Link([wolverhampton, walsall], LinkType.BOTH)
        walsall_birmingham = Link([walsall, birmingham], LinkType.BOTH)
        gloucester_redditch = Link([gloucester, redditch], LinkType.BOTH)
        redditch_birmingham = Link([redditch, birmingham], LinkType.RAIL)
        redditch_oxford = Link([redditch, oxford], LinkType.BOTH)
        oxford_birmingham = Link([oxford, birmingham], LinkType.BOTH)
        birmingham_coventry = Link([birmingham, coventry], LinkType.BOTH)
        coventry_nuneaton = Link([coventry, nuneaton], LinkType.RAIL)
        birmingham_nuneaton = Link([birmingham, nuneaton], LinkType.RAIL)
        birmingham_tamworth = Link([birmingham, tamworth], LinkType.BOTH)
        nuneaton_tamworth = Link([nuneaton, tamworth], LinkType.BOTH)
        tamworth_walsall = Link[tamworth, walsall], LinkType.BOTH)
        tamworth_burton = Link([tamworth, buton_on_trent], LinkType.BOTH)
        burton_walsall = Link([burton_on_trent, walsall], LinkType.CANAL)
        burton_cannock = Link([burton_on_trent, cannock], LinkType.RAIL)
        burton_derby = Link([burton_on_trent, derby], LinkType.BOTH)
        burton_stone = Link([burton_on_trent, stone], LinkType.BOTH)
        cannock_walsall = Link([cannock, walsall], LinkType.BOTH)
        cannock_wolverhampton = Link([cannock, wolverhampton], LinkType.BOTH)
        cannock_unnamed_city10 = Link([cannock, unnamed_city0], LinkType.BOTH)
        cannock_stafford = Link([cannock, stafford], LinkType.BOTH)
        stafford_stone = Link([stafford, stone], LinkType.BOTH)
        stone_stoke = Link([stone, stoke_on_trent], LinkType.BOTH)
        stone_uttoxeter = Link([stone, uttoxeter], LinkType.RAIL)
        derby_uttoxeter = Link([derby, uttoxeter], LinkType.RAIL)
        derby_nottingham = Link([derby, nottingham], LinkType.BOTH)
        derby_belper = Link([derby, belper], LinkType.BOTH)
        stoke_warrington = Link([stoke_on_trent, warrington], LinkType.BOTH)
        stoke_leek = Link([stoke_on_trent, leek], LinkType.BOTH)
        leek_belper = Link([leek, belper], LinkType.RAIL)

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

