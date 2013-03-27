#! /usr/bin/python
import urlparse

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml

class SimpleApp(object):
    def load_database(self, filename):
        drinkz.db.load_db(filename)
    
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        path = environ['PATH_INFO']
        
        # PATH ROUTING
        # index page
        if path == '/' or path == '/index.html' or path == '/index':
            content_type = 'text/html'
            data = _build_index()
        
        # recipe list
        elif path == '/recipes.html' or path == '/recipes':
            content_type = 'text/html'
            data = _build_recipes()
        
        # inventory list
        elif path == '/inventory.html' or path == '/inventory':
            content_type = 'text/html'
            data = _build_inventory()
        
        # liquor types list
        elif path == '/liquor_types.html' or path == '/liquor_types':
            content_type = 'text/html'
            data = _build_liquor_types()
        
        # liquor amount conversion form
        elif path == '/convert_amount.html' or path == '/convert_amount':
            content_type = 'text/html'
            data = _build_liquor_conversion()
        
        # conversion form submission
        elif path =='/recv':
            formdata = environ['QUERY_STRING']
            results = urlparse.parse_qs(formdata)
            
            content_type = 'text/html'
            data = _build_conversion_results(results['amount'][0])
        
        # unexpected request
        else:
            content_type = 'text/plain'
            data = 'If "%s" does not appear in our records, it does not exist!' % path
        
        # build and return the data
        headers = [('Content-type', content_type)]
        start_response(status, headers)
        return [data]

########################################
# template builder functions
########################################

# header information for every webpage
def _headers(title):
    header = """<!DOCTYPE html>
<html>
<head>
    <title>""" + title + """</title>
</head>
<body>\n\n"""
    
    return header

# footer information for every webpage
def _footers():
    footer = """\n\n<!-- page footer -->
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
def _build_page(title="Welcome to Drinkz!", content=""):
    page = _headers(title) + content + _footers()
    return page

########################################
# content builder functions
########################################

# build index page
def _build_index():
    # set page content
    title = "Welcome to Drinkz!"
    content = \
"""
<h1>Welcome to Drinkz!</h1>

<a href="convert_amount.html">Convert an amount to milliliters</a>
"""
    
    return _build_page(title, content)

# build recipes list page
def _build_recipes():
    # get all recipes with ingredients status
    recipes = drinkz.db.get_all_recipes()
    list = "\n"
    
    for r in recipes:
        list += "<strong><li>" + r.name + ":</strong> "
        if not r.need_ingredients():
            list += "<em>Ready to go!</em>"
        else:
            list += "<em>Need more ingredients</em>"
        
        list += "</li>\n"
    
    # set page content
    title = "Recipes"
    content = \
"""
<h1>Recipes</h1>

<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content)

# build inventory list page
def _build_inventory():
    # get inventory with amounts
    list = "\n"
    items = drinkz.db.get_liquor_inventory()
    
    for (m,l) in items:
        amt = drinkz.db.get_liquor_amount(m,l)
        list += "<li><strong>" + m + ", " + l + ":</strong> " + str(amt) + " ml</li>\n"
    
    # set page content
    title = "Inventory"
    content = \
"""
<h1>Inventory</h1>

<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content)

# build liquor types list page
def _build_liquor_types():
    bottles = []
    
    # add all bottle types to list
    for i in drinkz.db._bottle_types_db:
        bottles.append(i)
    
    # get all of the bottle types in a string for html
    list = "\n"
    for i in bottles:
        list += "<li>" + str(i[0]) + ", " + str(i[1]) + ", " + str(i[2]) + "</li>\n"
    
    # set page content
    title = "Liquor Types"
    content = \
"""
<h1>Liquor Types</h1>

<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content)

# build liquor amount conversion form page
def _build_liquor_conversion():
    # set page content
    title = "Convert to Milliliters"
    content = \
"""
<h1>Convert to Milliliters</h1>

<form action='recv'>
Amount: <input type='text' name='amount' size='10'>
<input type='submit'>
<br />
<em>Supported types: ounces, gallons, liters, milliliters</em>
</form>
"""
    return _build_page(title, content)

# build liquor amount conversion results page
def _build_conversion_results(in_amt):
    # run calculation
    out_amt = to_ml(in_amt)
    
    #set page content
    title = "Conversion Results"
    content = \
"""
<h1>Results</h1>
<p>
<strong>You entered:</strong> %s
<br />
<br />
<strong>Amount in milliliters:</strong> %f ml
</p>
""" % (in_amt, out_amt)
    return _build_page(title, content)
