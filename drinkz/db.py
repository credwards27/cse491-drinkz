"""
Database functionality for drinkz information.

Recipes are stored in a dictionary for retrieval.
Recipes are inherently name/value-paired objects(name, ingredient list), so a dictionary will be able to efficiently
store and retrieve them.
"""

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
        _inventory_db[(mfg, liquor)] = _convert_to_ml(amount)
    else:
        _inventory_db[(mfg, liquor)] += _convert_to_ml(amount)

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

def _convert_to_ml(amt):
    if "oz" in amt or "ounce" in amt or "ounces" in amt:
        amt = amt.strip('oz. ')
        amt = float(amt)
        amt *= 29.5735
    elif "gal" in amt or "gals" in amt or "gallon" in amt or "gallons" in amt:
        amt = amt.strip('gallons. ')
        amt = float(amt)
        amt *= 3785.41
    elif "ml" in amt or "milliliter" in amt or "milliliters" in amt:
        amt = amt.strip('ml. ')
        amt = float(amt)
    else:
        amt = float(amt)
    
    return amt

def add_recipe(r):
    "Add a recipe to the database"

def get_recipe(name):
    "Retrieve a recipe from the database"

def get_all_recipes():
    "Get a list of all recipes in the database that can be made from current inventory"

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db.keys():
        yield m, l
