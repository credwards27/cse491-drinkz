"""
Database functionality for drinkz information.

Recipes are stored in a dictionary for retrieval.
Recipes are inherently name/value-paired objects(name, ingredient list), so a dictionary will be able to efficiently
store and retrieve them.
"""

from .convert import to_ml
from .recipes import Recipe
from .events import Event
from .venues import Venue
from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = {}

_venues_db = {}
_events_db = {}

# removes all information from the database
def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = {}
    
    _venues_db = {}
    _events_db = {}

# saves the contents of the database to a file
def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes_db, _venues_db, _events_db)
    dump(tosave, fp)

    fp.close()

# loads a database file into the database
def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes_db, _venues_db, _events_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes_db, _venues_db, _events_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class RecipeMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

class DuplicateVenueName(Exception):
    pass

class DuplicateEventName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    if not check_inventory(mfg, liquor):
        _inventory_db[(mfg, liquor)] = to_ml(amount)
    else:
        _inventory_db[(mfg, liquor)] += to_ml(amount)

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db.keys():
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    if (mfg, liquor) in _inventory_db.keys():
        return _inventory_db[(mfg, liquor)]
    else:
        return 0.0
    
def add_recipe(r):
    "Add a recipe to the database"
    err = ""
    try:
        _recipes_db[r.name]
        err = "The recipe, %s, is already in the database" % (r.name)
        raise DuplicateRecipeName(err)
    except KeyError:
        _recipes_db[r.name] = r

def get_recipe(name):
    "Retrieve a recipe from the database"
    try:
        return _recipes_db[name]
    except KeyError:
        # V V future functionality V V
        #err = "Missing Recipe: '%s'" % (name)
        #raise RecipeMissing(err)
        pass

def get_all_recipes():
    "Get a list of all recipes in the database"
    
    recipes = []
    
    for r in _recipes_db:
        recipes.append(_recipes_db[r])
    
    return recipes

# gets a list of all recipes that can be made from the items in the inventory
def get_possible_recipes():
    possible = []
    
    for r in _recipes_db:
        if not _recipes_db[r].need_ingredients():
            possible.append(r)
    
    return possible

# creates a new event and adds it to the database
def add_event(name, host, venue, date, time):
    e = Event()
    e.name = name
    e.host = host
    e.venue = venue
    e.date = date
    e.time = time
    
    try:
        _add_event_to_db(e)
        return e
    except DuplicateEventName:
        print "An event already exists in the database with the name %s" % (name)
        return

# creates a new venue and adds it to the database
def add_venue(name, address, city, state, zipcode, description):
    v = Venue()
    v.name = name
    v.address = address
    v.city = city
    v.state = state
    v.zipcode = zipcode
    v.description = description
    
    try:
        _add_venue_to_db(v)
        return v
    except DuplicateVenueName:
        print "A venue already exists in the database with the name %s" % (name)
        return

# adds an event to the database
def _add_event_to_db(e):
    err = ""
    try:
        _events_db[e.name]
        err = "An event already exists in the database with the name %s" % (e.name)
        raise DuplicateEventName(err)
    except KeyError:
        _events_db[e.name] = e

# adds a venue to the database
def _add_venue_to_db(v):
    err = ""
    try:
        _venues_db[v.name]
        err = "A venue already exists in the database with the name %s" % (v.name)
        raise DuplicateVenueName(err)
    except KeyError:
        _venues_db[v.name] = v

# get all events in the database
def get_all_events():
    list = []
    for n in _events_db.keys():
        list.append(_events_db[n])
    return list

# get all venues in the database
def get_all_venues():
    list = []
    for n in _venues_db.keys():
        list.append(_venues_db[n])
    return list

# checks if an event already exists with the specified name
def check_event_exists(evt_name):
    for name in _events_db.keys():
        if evt_name == name:
            return True
    return False

def check_inventory_for_type(type):
    have = set()
    
    # get a list of all the manufacturers and liquor that exist in bottle types
    for (m,l,t) in _bottle_types_db:
        if t == type:
            # type exists, check if in the inventory
            if check_inventory(m,l):
                # type is in the inventory, add it to the have list
                have.add((m,l))
                
    return have

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db.keys():
        yield m, l
