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

# run the app for testing
def _init_app(environ, start_response):
    app_obj = SimpleApp()
    app_obj.fake_init_page_builder('templates')
    results = app_obj(environ, start_response)
    return "".join(results)
