# implementation of recipes

import db

class Recipe(object):
    
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        
    def need_ingredients(self):
        missing = []
        
        for (type, amt) in self.ingredients:
            # get a list of what types are in inventory
            have_types = db.check_inventory_for_type(type)
            
            # get the amount of the needed type that is already in the inventory
            have_amount = 0.0
            
            for (mfg, lqr) in have_types:
                # only the highest amount of one type counts as the total amount
                # this prevents mixing alcohols
                if db.get_liquor_amount(mfg,lqr) > have_amount:
                    have_amount = db.get_liquor_amount(mfg,lqr)
            
            # find out how much is needed
            need_amount = have_amount - db.convert_to_ml(amt)
            
            if need_amount < 0.0:
                missing.append((type, need_amount*-1))
        
        return missing