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
from queue import PriorityQueue
import random

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
        self.taken = []
        self.adjacent = []

    def add_square(self, square):
        self.squares.append(square)
        self.taken.append(False)
  
    def apply_bonus(self, player): # TO DO
        pass

    def __str__(self):
        string = f"{self.name}: "
        for square in self.squares:
            string += f"{square.building_types}   "
        return string
    
    def __repr__(self):
        string = f"{self.name}: "
        for square in self.squares:
            string += f"{square.building_types} "
        return string

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, TradingHub) and self.name == other.name

    def add_link(self, link):
        self.adjacent.append(link)

class Market:
    def __init__(self, resources, maximum_resources):
        self.resources = resources
        self.maximum_resources = maximum_resources

    def get_price(self):
        resources_spent = self.maximum_resources - self.resources
        if resources_spent % 2 == 1:
            resources_spent = resources_spent - 1
        return 1 + resources_spent / 2
    
    def remove_resource(self):
        if self.resources != 0:
            self.resources -= 1

    def add_resource(self):
        if self.resources != self.maximum_resources:
            self.resources += 1
            return self.get_price()

        return 0

class BuildingInstance:
    def __init__(self, building, player_id):
        self.building = building
        self.player_id = player_id
        self.sold = False
    
    def get_stats(self):
        print(f"belongs to: {self.player_id}      sold: {self.sold}")
        print(f"stats: {self.building.stats}   resources: {self.building.resources}")

class Square:
    def __init__(self, building_types, parent):
        self.building_types = building_types # accepted building types
        self.building_instance = None # Reference to building instance
        self.parent = parent

    def add_building(self, building_instance):
        self.building_instance = building_instance

    def is_available(self, player_id, building_type):
        if self.building_instance is not None and self.building_instance.player_id == player_id and self.building_instance.building.industry_type == building_type: # I believe you can overbuild based on the building that is already there, not on the building types of the square
            return True
        if self.building_instance is None:
            for square_building_type in self.building_types:
                if square_building_type == building_type:
                    return True

        return False
  
    def get_stats(self):
        if self.building_instance is not None:
            self.building_instance.get_stats()

class Link: 
    def __init__(self, connected_cities, link_type):
        self.owner_id = None
        self.link_type = link_type
        self.points = 0
        self.cities = []
        for city in connected_cities:
            self.cities.append(city)
            city.add_link(self)
  
    def __str__(self):
        string = ""
        for city in self.cities:
            string += f"{city.name}   "
        string += f"({self.link_type})"
        return string

    def __repr__(self):
        string = ""
        for city in self.cities:
            string += city.name 
            string += " "
        return string

    def __hash__(self):
        string = ""
        for city in self.cities:
            string += city.name
        return hash(string)

    def __eq__(self, other):
        return isinstance(other, Link) and self.cities == other.cities

    def change_ownership(self, owner):
        self.owner_id = owner

class City:
    def __init__(self, name):
        self.name = name
        self.adjacent = []
        self.squares = []
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, City) and self.name == other.name
   
    def print_links(self):
        print(self)
        for link in self.adjacent:
            print(link)
        print("")

    def add_square(self, buildings):
        self.squares.append(Square(buildings, self))

    def add_link(self, link):
        self.adjacent.append(link)

    def is_available(self, player_id, building_type):
        for square in self.squares:
            if square.is_available(player_id, building_type):
                return True

        return False

    def is_connected(self, other_city):
        for link in self.adjacent:
            for city in link.cities:
                if city is other_city:
                    return True 
        return False

    def add_building(self, building_instance):
        for square in self.squares:
            if square.is_available(building_instance.player_id, building_instance.building.industry_type):
                square.add_building(building_instance)

def is_brewery(target):
    if not(is_trading_hub(target)) and not(isinstance(target, City)):
        return False

    for square in target.squares:
        if square.building_instance is not None and square.building_instance.building.industry_type == IndustryType.BREWERY:
            return True

    return False

def is_trading_hub(target):
    return isinstance(target, TradingHub)

def is_iron_works(target):
    if not(isinstance(target, City)):
        return False 

    for square in target.squares:
        if square.building_instance is not None and square.building_instance.building.industry_type == IndustryType.IRONWORKS:
            return True

    return False

def is_coal_mine(target):
    if is_trading_hub(target):
        return True

    if not(isinstance(target, City)):
        return False
    
    for square in target.squares:
        if square.building_instance is not None and square.building_instance.building.industry_type == IndustryType.COALMINE:
            return True

    return False

def node_clean_up(node):
    if is_trading_hub(node):
        return node  
    else:
        return node.building_instance

def BFS(starting_point, check, full_search = False): # used when searching for resources and links to markets
        pq = []
        current_index = 0
        pq.append((starting_point, 0))
        nodes = []
        hash_map = {}
        dist_cutoff = -1
        while (current_index != len(pq)):
            node = pq[current_index]
            current_index += 1

            hash_map[node[0]] = True
            if dist_cutoff != -1 and node[1] > dist_cutoff:
                return nodes
            elif check(node[0]):
                if full_search:
                    nodes.append(node_clean_up(node[0]))
                else:
                    dist_cutoff = node[1]
                    nodes.append(node_clean_up(node[0]))

            elif isinstance(node[0], City):
                for link in node[0].adjacent: 
                    if hash_map.get(link) != True:
                        pq.append((link, node[1] + 1))
            elif isinstance(node[0], Link):
                for city in node[0].cities:
                    if hash_map.get(city) != True:
                        pq.append((city, node[1] + 1))

        return nodes

class Board: 
    def create_locations(self, number_of_players): # basically creates the whole map
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

        stoke_on_trent.add_square([IndustryType.MANUFACTORY, IndustryType.COTTONMILL])
        stoke_on_trent.add_square([IndustryType.POTTERY, IndustryType.IRONWORKS])
        stoke_on_trent.add_square([IndustryType.COTTONMILL])

        leek.add_square([IndustryType.MANUFACTORY, IndustryType.COTTONMILL])
        leek.add_square([IndustryType.MANUFACTORY, IndustryType.COALMINE])

        belper.add_square([IndustryType.MANUFACTORY, IndustryType.COTTONMILL])
        belper.add_square([IndustryType.COALMINE])
        belper.add_square([IndustryType.POTTERY])

        stone.add_square([IndustryType.MANUFACTORY, IndustryType.BREWERY])
        stone.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])

        uttoxeter.add_square([IndustryType.COTTONMILL, IndustryType.BREWERY])
        uttoxeter.add_square([IndustryType.MANUFACTORY, IndustryType.BREWERY])

        derby.add_square([IndustryType.MANUFACTORY, IndustryType.BREWERY])
        derby.add_square([IndustryType.MANUFACTORY, IndustryType.COTTONMILL])
        derby.add_square([IndustryType.IRONWORKS])

        burton_on_trent.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])
        burton_on_trent.add_square([IndustryType.BREWERY])

        tamworth.add_square([IndustryType.MANUFACTORY, IndustryType.COALMINE])
        tamworth.add_square([IndustryType.MANUFACTORY, IndustryType.COALMINE])

        walsall.add_square([IndustryType.IRONWORKS, IndustryType.COTTONMILL])
        walsall.add_square([IndustryType.COTTONMILL, IndustryType.BREWERY])

        birmingham.add_square([IndustryType.MANUFACTORY, IndustryType.COTTONMILL])
        birmingham.add_square([IndustryType.COTTONMILL])
        birmingham.add_square([IndustryType.IRONWORKS])
        birmingham.add_square([IndustryType.COTTONMILL])

        nuneaton.add_square([IndustryType.COTTONMILL, IndustryType.BREWERY])
        nuneaton.add_square([IndustryType.MANUFACTORY, IndustryType.COALMINE])

        coventry.add_square([IndustryType.POTTERY])
        coventry.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])
        coventry.add_square([IndustryType.IRONWORKS, IndustryType.COTTONMILL])

        redditch.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])
        redditch.add_square([IndustryType.IRONWORKS])

        stafford.add_square([IndustryType.COTTONMILL, IndustryType.BREWERY])
        stafford.add_square([IndustryType.POTTERY])

        cannock.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])
        cannock.add_square([IndustryType.COALMINE])

        unnamed_city0.add_square([IndustryType.BREWERY])

        wolverhampton.add_square([IndustryType.COTTONMILL])
        wolverhampton.add_square([IndustryType.COTTONMILL, IndustryType.COALMINE])

        coalbrookdale.add_square([IndustryType.IRONWORKS, IndustryType.BREWERY])
        coalbrookdale.add_square([IndustryType.IRONWORKS])
        coalbrookdale.add_square([IndustryType.COALMINE])

        dudley.add_square([IndustryType.COALMINE])
        dudley.add_square([IndustryType.IRONWORKS])

        kidderminster.add_square([IndustryType.MANUFACTORY, IndustryType.COALMINE])
        kidderminster.add_square([IndustryType.MANUFACTORY])

        worcester.add_square([IndustryType.MANUFACTORY])
        worcester.add_square([IndustryType.MANUFACTORY])

        unnamed_city1.add_square([IndustryType.BREWERY])
        
        nottingham = TradingHub("Nottingham", (BonusType.VICTORY_POINTS, 3))
        oxford = TradingHub("Oxford", (BonusType.INCOME, 2))
        gloucester = TradingHub("Gloucester", (BonusType.INNOVATION, 1))
        shrewsbury = TradingHub("Shrewsbury", (BonusType.VICTORY_POINTS, 4)) 
        warrington = TradingHub("Warrington", (BonusType.COINS, 5))

        connections = [ 
            [(coalbrookdale, shrewsbury), LinkType.BOTH],
            [(coalbrookdale, wolverhampton), LinkType.BOTH],
            [(coalbrookdale, kidderminster), LinkType.BOTH],
            [(kidderminster, worcester, unnamed_city1), LinkType.BOTH],
            [(kidderminster, dudley), LinkType.BOTH],
            [(worcester, gloucester), LinkType.BOTH],
            [(worcester, birmingham), LinkType.BOTH],
            [(dudley, wolverhampton), LinkType.BOTH],
            [(dudley, birmingham), LinkType.BOTH],
            [(wolverhampton, cannock), LinkType.BOTH],
            [(wolverhampton, walsall), LinkType.BOTH],
            [(walsall, birmingham), LinkType.BOTH],
            [(gloucester, redditch), LinkType.BOTH],
            [(redditch, birmingham), LinkType.RAIL],
            [(redditch, oxford), LinkType.BOTH],
            [(oxford, birmingham), LinkType.BOTH],
            [(birmingham, coventry), LinkType.BOTH],
            [(coventry, nuneaton), LinkType.RAIL],
            [(birmingham, nuneaton), LinkType.RAIL],
            [(birmingham, tamworth), LinkType.BOTH],
            [(nuneaton, tamworth), LinkType.BOTH],
            [(tamworth, walsall), LinkType.RAIL],
            [(tamworth, burton_on_trent), LinkType.BOTH],
            [(burton_on_trent, walsall), LinkType.CANAL],
            [(burton_on_trent, cannock), LinkType.RAIL],
            [(burton_on_trent, derby), LinkType.BOTH],
            [(burton_on_trent, stone), LinkType.BOTH],
            [(cannock, walsall), LinkType.BOTH],
            [(cannock, wolverhampton), LinkType.BOTH],
            [(cannock, unnamed_city0), LinkType.BOTH],
            [(cannock, stafford), LinkType.BOTH],
            [(stafford,stone), LinkType.BOTH],
            [(stone, stoke_on_trent), LinkType.BOTH],
            [(stone, uttoxeter), LinkType.RAIL],
            [(derby, uttoxeter), LinkType.RAIL],
            [(derby, nottingham), LinkType.BOTH],
            [(derby, belper), LinkType.BOTH],
            [(stoke_on_trent, warrington), LinkType.BOTH],
            [(stoke_on_trent, leek), LinkType.BOTH],
            [(leek, belper), LinkType.RAIL]
        ]

        hub_industries = [ # used to generate trading hub accepted industry types
            (),
            (),
            (IndustryType.MANUFACTORY),
            (IndustryType.COTTONMILL),
            (IndustryType.COTTONMILL, IndustryType.POTTERY, IndustryType.MANUFACTORY),
            (),
            (IndustryType.POTTERY),
            (IndustryType.COTTONMILL),
            (IndustryType.MANUFACTORY)
        ]

        if number_of_players == 2:
            sublist = hub_industries[:5]
            random.shuffle(sublist)
            shrewsbury.add_square(Square(sublist[0], shrewsbury))
            gloucester.add_square(Square(sublist[1], gloucester))
            gloucester.add_square(Square(sublist[2], gloucester))
            oxford.add_square(Square(sublist[3], oxford))
            oxford.add_square(Square(sublist[4], oxford))
        elif number_of_players == 3:
            sublist = hub_industries[:7]
            random.shuffle(sublist)
            shrewsbury.add_square(Square(sublist[0], shrewsbury))
            gloucester.add_square(Square(sublist[1], gloucester))
            gloucester.add_square(Square(sublist[2], gloucester))
            oxford.add_square(Square(sublist[3], oxford))
            oxford.add_square(Square(sublist[4], oxford))
            warrington.add_square(Square(sublist[5], warrington))
            warrington.add_square(Square(sublist[6], warrington))
        else:
            random.shuffle(hub_industries)
            shrewsbury.add_square(Square(hub_industries[0], shrewsbury))
            gloucester.add_square(Square(hub_industries[1], gloucester))
            gloucester.add_square(Square(hub_industries[2], gloucester))
            oxford.add_square(Square(hub_industries[3], oxford))
            oxford.add_square(Square(hub_industries[4], oxford))
            warrington.add_square(Square(hub_industries[5], warrington))
            warrington.add_square(Square(hub_industries[6], warrington))
            nottingham.add_square(Square(hub_industries[7], nottingham))
            nottingham.add_square(Square(hub_industries[8], nottingham))

        for connection in connections:
            cities = connection[0]
            link_type = connection[1]
            new_link = Link(cities, link_type)
            self.links.append(new_link)
            
        self.cities.append(birmingham)
        self.cities.append(redditch)
        self.cities.append(nuneaton)
        self.cities.append(kidderminster)
        self.cities.append(dudley)
        self.cities.append(worcester)
        self.cities.append(coalbrookdale)
        self.cities.append(coventry)
        self.cities.append(wolverhampton)
        self.cities.append(cannock)
        self.cities.append(stafford)
        self.cities.append(walsall)
        self.cities.append(tamworth)
        self.cities.append(burton_on_trent)
        self.cities.append(belper)
        self.cities.append(derby)
        self.cities.append(leek)
        self.cities.append(stoke_on_trent)
        self.cities.append(stone)
        self.cities.append(uttoxeter)
        self.cities.append(unnamed_city0)
        self.cities.append(unnamed_city1)

        self.trading_hubs.append(nottingham)
        self.trading_hubs.append(oxford)
        self.trading_hubs.append(gloucester)
        self.trading_hubs.append(shrewsbury) # this one has only one slot
        self.trading_hubs.append(warrington)
    
    def __init__(self, number_of_players):
        self.coal_market = Market(13, 14)
        self.iron_market = Market(8, 10)

        self.cities = []
        self.trading_hubs = []
        self.links = [] 

        self.create_locations(number_of_players)

