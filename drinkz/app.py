#! /usr/bin/python
import urlparse
import simplejson

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml
from drinkz import page_builder

# dispatch dictionary for json calls
dispatch = {
    '/' : 'index',
    '/index' : 'index',
    '/index.html' : 'index',
    '/recipes' : 'recipes',
    '/recipes.html' : 'recipes',
    '/inventory' : 'inventory',
    '/inventory.html' : 'inventory',
    '/liquor_types' : 'liquor_types',
    '/liquor_types.html' : 'liquor_types',
    '/convert_amount' : 'convert_amount',
    '/convert_amount.html' : 'convert_amount',
    '/recv' : 'recv',
    '/error' : 'error',
    '/convert' : 'convert_units_to_ml',
    '/recipe_names' : 'get_recipe_names',
    '/liquor_inventory' : 'get_liquor_inventory'
}

# html headers for page encoding
html_headers = [('Content-Type', 'text/html')]

class SimpleApp(object):
    def load_database(self, filename):
        drinkz.db.load_db(filename)
    
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
        
        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to the 'path'
        fn = getattr(self, fn_name, None)
        
        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s is found" % path]
        
        return fn(environ, start_response)
        
        # PATH ROUTING
        # index page
        if path == '/' or path == '/index.html' or path == '/index':
            content_type = 'text/html'
            data = page_builder.build_index()
        
        # recipe list
        elif path == '/recipes.html' or path == '/recipes':
            content_type = 'text/html'
            data = page_builder.build_recipes()
        
        # inventory list
        elif path == '/inventory.html' or path == '/inventory':
            content_type = 'text/html'
            data = page_builder.build_inventory()
        
        # liquor types list
        elif path == '/liquor_types.html' or path == '/liquor_types':
            content_type = 'text/html'
            data = page_builder.build_liquor_types()
        
        # liquor amount conversion form
        elif path == '/convert_amount.html' or path == '/convert_amount':
            content_type = 'text/html'
            data = page_builder.build_liquor_conversion()
        
        # conversion form submission
        elif path =='/recv':
            formdata = environ['QUERY_STRING']
            results = urlparse.parse_qs(formdata)
            
            content_type = 'text/html'
            data = page_builder.build_conversion_results(results['amount'][0])
        
        # unexpected request
        else:
            content_type = 'text/plain'
            data = 'If "%s" does not appear in our records, it does not exist!' % path
        
        # build and return the data
        start_response(status, list(html_headers))
        return [data]
    
    # index page
    def index(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return [page_builder.build_index()]
    
    # recipe list
    def recipes(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return [page_builder.build_recipes()]
    
    # inventory list
    def inventory(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return [page_builder.build_inventory()]
