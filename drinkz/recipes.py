# implementation of recipes

class Recipe(object):
    
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        print "name:", self.name
        print "ingredients:", self.ingredients
