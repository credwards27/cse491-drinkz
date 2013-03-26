#! /usr/bin/python
import urlparse

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml

#
# DUMMY TEST CODE (WILL BE MOVED LATER)
#

# add dummy bottle types
#drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
#drinkz.db.add_bottle_type('Evan Williams', 'Cinnamon Reserve', 'kentucky liqueor')

# add dummy inventory items
#drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
#drinkz.db.add_to_inventory('Evan Williams', 'Cinnamon Reserve', '2000 ml')
#drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '40oz')

# add dummy recipes
#a = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
#drinkz.db.add_recipe(a)
#b = drinkz.recipes.Recipe('black label on the rocks', [('Black Label','6 oz')])
#drinkz.db.add_recipe(b)

class SimpleApp(object):
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        path = environ['PATH_INFO']
        
        # PATH ROUTING
        # index page
        if path == '/':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_index()]
        elif path == '/index.html':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_index()]
        
        # recipe list
        elif path == '/recipes.html':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_recipes()]
        
        # inventory list
        elif path == '/inventory.html':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_inventory()]
        
        # liquor types list
        elif path == '/liquor_types.html':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_liquor_types()]
        
        # liquor amount conversion form
        elif path == '/convert_amount.html':
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_liquor_conversion()]
        
        # conversion form submission
        elif path =='/recv':
            formdata = environ['QUERY_STRING']
            results = urlparse.parse_qs(formdata)
            
            content_type = 'text/html'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [_build_conversion_results(results['amount'][0])]

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
    # set page content
    title = "Recipes"
    content = ""
    return _build_page(title, content)

# build inventory list page
def _build_inventory():
    # set page content
    title = "Inventory"
    content = ""
    return _build_page(title, content)

# build liquor types list page
def _build_liquor_types():
    # set page content
    title = "Liquor Types"
    content = ""
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
</form>
<p><em>Supported types: ounces, gallons, liters, milliliters</em></p>
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
