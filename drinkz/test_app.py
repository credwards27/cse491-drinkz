import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml
from drinkz.app import SimpleApp

# test wsgi functionality
def test_recipes():
    simple_app = SimpleApp()
    simple_app.load_database('bin/database_file')
    
    environ = {'PATH_INFO': '/recipes.html'}
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    text = _init_app(environ, my_start_response)
    status, headers = d['status'], d['headers']
    
    assert text.find('scotch on the rocks') != -1, text
    assert text.find('black label on the rocks') != -1, text

# test add liquor type
def test_add_liquor_type():
    simple_app = SimpleApp()
    simple_app.load_database('bin/database_file')
    
    environ = {'PATH_INFO': '/recv_add_liquor_type', 'QUERY_STRING': 'mfg=Lucid&liq=Green+Fairy&typ=absinthe'}
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    text = _init_app(environ, my_start_response)
    status, headers = d['status'], d['headers']
    
    assert text.find('Lucid, Green Fairy, absinthe') != -1, text

# test add inventory item
def test_add_inventory_item():
    simple_app = SimpleApp()
    simple_app.load_database('bin/database_file')
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    # add the lucid green fairy bottle type
    simple_app.fake_init_page_builder('templates')
    environ = {'PATH_INFO': '/recv_add_liquor_type', 'QUERY_STRING': 'mfg=Lucid&liq=Green+Fairy&typ=absinthe'}
    simple_app(environ, my_start_response)
    
    environ = {'PATH_INFO': '/recv_add_inventory_item', 'QUERY_STRING': 'mfg=Lucid&liq=Green+Fairy&amt=8oz'}
    
    results = "".join(simple_app(environ, my_start_response))
    status, headers = d['status'], d['headers']
    
    assert results.find('Lucid, Green Fairy:') != -1, results

# test add recipe
def test_add_recipe():
    simple_app = SimpleApp()
    simple_app.load_database('bin/database_file')
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    environ = {'PATH_INFO': '/recv_add_recipe', 'QUERY_STRING': 'name=New+Recipe&in0=good+alcohol&amt0=6+gallons&in1=&amt1=&in2=&amt2=&in3=&amt3=&in4=&amt4='}
    
    results = _init_app(environ, my_start_response)
    status, headers = d['status'], d['headers']
    
    assert results.find('New Recipe:</strong> <em>Needs more ingredients') != -1, results

# run the app for testing
def _init_app(environ, start_response):
    app_obj = SimpleApp()
    app_obj.fake_init_page_builder('templates')
    results = app_obj(environ, start_response)
    return "".join(results)
