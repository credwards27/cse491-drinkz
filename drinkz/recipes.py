# implementation of recipes

import db

class Recipe(object):
    
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        
    def need_ingredients(self):
        missing = []
        
        for i in self.ingredients:
            # get a list of what types are in inventory
            have_set = db.check_inventory_for_type(i[0])
            
            # if set is empty, type is not in inventory
            if not have_set:
                missing.append((i[0], db.convert_to_ml(i[1])))
        
        return missing