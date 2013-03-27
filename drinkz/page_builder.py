import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml

########################################
# template builder functions
########################################

# header information for every webpage
def _headers(title, content_title, headers=""):
    header = \
"""<!DOCTYPE html>
<html>
<head>
    <title>""" + title + """</title>
    
    <style type='text/css'>
    h1 { color: #f00; }
    body
    {
        font-size: 14px;
    }
    </style>
    """ + headers + """
</head>
<body>

<h1>""" + content_title + """</h1>
"""
    
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
def _build_page(title="Welcome to Drinkz!", content_title="", content="", headers=""):
    page = _headers(title, content_title, headers) + content + _footers()
    return page

########################################
# content builder functions
########################################

# build index page
def build_index():
    # set page content
    title = "Welcome to Drinkz!"
    content_title = "Welcome to Drinkz!"
    headers = \
    """
    <script>
    function alertBox()
    {
        alert("Hello! I am an alert box!");
    }
    </script>
    """
    content = \
"""
<a href="convert_amount.html">Convert an amount to milliliters</a>
<br />
<br />
<input type="button" onClick="alertBox()" value="Show alert box" />
"""
    
    return _build_page(title, content_title, content, headers)

# build recipes list page
def build_recipes():
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
    content_title = "Recipes"
    content = \
"""
<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content_title, content)

# build inventory list page
def build_inventory():
    # get inventory with amounts
    list = "\n"
    items = drinkz.db.get_liquor_inventory()
    
    for (m,l) in items:
        amt = drinkz.db.get_liquor_amount(m,l)
        list += "<li><strong>" + m + ", " + l + ":</strong> " + str(amt) + " ml</li>\n"
    
    # set page content
    title = "Inventory"
    content_title = "Inventory"
    content = \
"""
<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content_title, content)

# build liquor types list page
def build_liquor_types():
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
    content_title = "Liquor Types"
    content = \
"""
<p>
<ul>""" + list + """</ul>
</p>
"""
    return _build_page(title, content_title, content)

# build liquor amount conversion form page
def build_liquor_conversion():
    # set page content
    title = "Convert to Milliliters"
    content_title = "Convert to Milliliters"
    content = \
"""
<form action='recv'>
Amount: <input type='text' name='amount' size='10'>
<input type='submit'>
<br />
<em>Supported types: ounces, gallons, liters, milliliters</em>
</form>
"""
    return _build_page(title, content_title, content)

# build liquor amount conversion results page
def build_conversion_results(in_amt):
    # run calculation
    out_amt = to_ml(in_amt)
    
    #set page content
    title = "Conversion Results"
    content_title = "Results"
    content = \
"""
<p>
<strong>You entered:</strong> %s
<br />
<br />
<strong>Amount in milliliters:</strong> %f ml
</p>
""" % (in_amt, out_amt)
    return _build_page(title, content_title, content)
