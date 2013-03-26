import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml
from drinkz.app import SimpleApp

# add dummy bottle types
drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
drinkz.db.add_bottle_type('Evan Williams', 'Cinnamon Reserve', 'kentucky liqueor')

# add dummy inventory items
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
drinkz.db.add_to_inventory('Evan Williams', 'Cinnamon Reserve', '2000 ml')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '40oz')

# add dummy recipes
a = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
drinkz.db.add_recipe(a)
b = drinkz.recipes.Recipe('black label on the rocks', [('Black Label','6 oz')])
drinkz.db.add_recipe(b)

# test wsgi functionality
def test_recipes():
    simple_app = SimpleApp()
    
    environ = {'PATH_INFO': '/recipes.html'}
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    text = _init_app(environ, my_start_response)
    status, headers = d['status'], d['headers']
    
    assert text.find('scotch on the rocks') != -1, text
    assert text.find('black label on the rocks') != -1, text

# run the app for testing
def _init_app(environ, start_response):
    app_obj = SimpleApp()
    results = app_obj(environ, start_response)
    return "".join(results)
