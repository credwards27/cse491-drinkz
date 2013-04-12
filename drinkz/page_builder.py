import sys
import jinja2

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml

# jinja2 global variables
loader = None
env = None

# initializer function
def init_page_builder(templatePath):
    global loader, env
    loader = jinja2.FileSystemLoader(templatePath)
    env = jinja2.Environment(loader=loader)

########################################
# content builder functions
########################################

# build index page
def build_index():
    # render the correct template
    template = env.get_template('index.html')
    return template.render()

#build recipes list page
def build_recipes():
    # get all recipes with ingredients status
    list = []
    recipes = drinkz.db.get_all_recipes()
    
    # template expects list of tuples in the form (recipe name, ingredients status)
    for r in recipes:
        if not r.need_ingredients():
            status = "Ready to go!"
        else:
            status = "Needs more ingredients"
        
        list.append((r.name, status))
    
    # set the variables dictionary
    vars = dict(recipes=list)
    
    # render the correct template
    template = env.get_template('recipes.html')
    return template.render(vars)

# build add recipe form page
def build_add_recipe():
     # render the correct template
    template = env.get_template('add_recipe.html')
    return template.render()

# build inventory list page
def build_inventory():
    # template expects a list of tuples in the form (manufacturer, liquor type, amount)
    list = []
    items = drinkz.db.get_liquor_inventory()
    
    for (m,l) in items:
        amt = drinkz.db.get_liquor_amount(m,l)
        list.append((m,l,str(amt)))
    
    # set variables dictionary
    vars = dict(inventory=list)
    
    # render the correct template
    template = env.get_template('inventory.html')
    return template.render(vars)

# build add inventory item form page
def build_add_inventory_item():
    # render the correct template
    template = env.get_template('add_inventory_item.html')
    return template.render()

# build liquor types list page
def build_liquor_types():
    list = []
    bottles = []
    
    # add all bottle types to list
    for i in drinkz.db._bottle_types_db:
        bottles.append(i)
    
    # get all of the bottle types in a string format for html
    # template expects list of tuples in the form (manufacturer, liquor, type)
    for (mfg,liq,typ) in bottles:
        list.append((mfg,liq,typ))
    
    # set variables dictionary
    vars = dict(bottles=list)
    
    # render the correct template
    template = env.get_template('liquor_types.html')
    return template.render(vars)

#build add liquor type form page
def build_add_liquor_type():
    # render the correct template
    template = env.get_template('add_liquor_type.html')
    return template.render()

# build liquor amount conversion form page
def build_liquor_conversion():
    # render the correct template
    template = env.get_template('convert_to_ml.html')
    return template.render()

# build liquor amount conversion results page
def build_conversion_results(in_amt):
    # run calculation
    out_amt = to_ml(in_amt)
    
    # set variables dictionary
    vars = dict(inAmt=in_amt, outAmt=out_amt)
    
    # render the correct template
    template = env.get_template('conversion_results.html')
    return template.render(vars)
