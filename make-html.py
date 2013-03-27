#! /usr/bin/env python

import os
import drinkz.db
import drinkz.recipes

# site initializer that creates a dummy database and initializes the file structure
def init_site():
    try:
        os.mkdir('html')
    except OSError:
        # already exists
        pass
    
    drinkz.db.load_db('bin/database_file')

# header information for every webpage
def headers(title):
    header = """<!DOCTYPE html>
<html>
<head>
    <title>""" + title + """</title>
</head>
<body>\n"""
    
    return header

# footer information for every webpage
def footers():
    footer = """\n<!-- page footer -->
<hr />
<h3>Navigation</h3>
<p>
<a href="index.html">Home</a>
<br />
<a href="recipes.html">Recipes</a>
<br />
<a href="inventory.html">Inventory</a>
<br />
<a href="liquor_types.html">Liquor Types</a>
</p>

</body>
</html>"""
    
    return footer

# page builder function that links all page contents together
def build_page(title="Welcome to Drinkz!", content=""):
    page = headers(title) + content + footers()
    return page

###################################################
# file builder function definitions
###################################################

# create index page
def build_index():
    # set page content
    title = "Welcome to Drinkz!"
    content = "\n<h1>Welcome to Drinkz!</h1>\n"
    
    # create file
    fp = open('html/index.html', 'w')
    print >>fp, build_page(title, content)
    fp.close()

# create recipes page
def build_recipes():
    # get all recipes with ingredients status
    recipes = drinkz.db.get_all_recipes()
    li_string = "\n"
    
    for r in recipes:
        li_string += "<strong><li>" + r.name + ":</strong> "
        
        if not r.need_ingredients():
            li_string += "ready to go!"
        else:
            li_string += "need more ingredients"
        
        li_string += "</li>\n"
    
    # set page content
    title = "Recipes"
    content =\
"""
<h1>Recipes</h1>

<p>
<ul>""" + li_string + """</ul>
</p>
"""
    
    # create file
    fp = open('html/recipes.html', 'w')
    print >>fp, build_page(title, content)
    fp.close()
    
# create inventory page
def build_inventory():
    # get inventory with amounts
    s = "\n"
    items = drinkz.db.get_liquor_inventory()
    
    for (m,l) in items:
        amt = drinkz.db.get_liquor_amount(m,l)
        s += "<li><strong>" + m + ", " + l + ":</strong> " + str(amt) + " ml</li>\n"
    
    # set page content
    title = "Inventory"
    content =\
"""
<h1>Inventory</h1>
<p>
<ul>""" + s + """</ul>
</p>
"""
    
    # create file
    fp = open('html/inventory.html', 'w')
    print >>fp, build_page(title, content)
    fp.close()

# create liquor types page
def build_liquor_types():
    bottles = []
    
    # add all bottle types to list
    for i in drinkz.db._bottle_types_db:
        bottles.append(i)
    
    # get all of the bottle types in a string for html
    s = "\n"
    for i in bottles:
        s += "<li>" + str(i[0]) + ", " + str(i[1]) + ", " + str(i[2]) + "</li>\n"
    
    # set page content
    title = "Liquor Types"
    content =\
"""
<h1>Liquor Types</h1>
<p>
<ul>""" + s + """</ul>
</p>
"""
    
    # create file
    fp = open('html/liquor_types.html', 'w')
    print >>fp, build_page(title, content)
    fp.close()

###################################################
# create all files
###################################################

init_site()
build_index()
build_recipes()
build_inventory()
build_liquor_types()