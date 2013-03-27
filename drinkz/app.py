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
    '/rpc' : 'dispatch_rpc'
}

# html headers for page encoding
html_headers = [('Content-Type', 'text/html')]

class SimpleApp(object):
    def load_database(self, filename):
        drinkz.db.load_db(filename)
    
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        #print "REQUEST_METHOD:", environ['REQUEST_METHOD']
        #print "CONTENT_LENGTH:", environ['CONTENT_LENGTH']
        #print "wsgi.input:", environ['wsgi.input']
        
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
        
        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to the 'path'
        fn = getattr(self, fn_name, None)
        
        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s is found" % path]
        
        return fn(environ, start_response)
    
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
    
    # liquor types list
    def liquor_types(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return [page_builder.build_index()]
    
    # liquor amount conversion form
    def convert_amount(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return [page_builder.build_liquor_conversion()]
    
    # conversion form submission
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        content_type = 'text/html'
        
        start_response('200 OK', list(html_headers))
        return [page_builder.build_conversion_results(results['amount'][0])]
    
    # unexpected request
    def error(self, environ, start_response):
        content_type = 'text/plain'
        data = 'If "%s" does not appear in our records, it does not exist!' % path
        
        start_response(status, list(html_headers))
        return [data]
    
    ########################################
    # simplejson handlers
    ########################################
    
    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data vi a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])
                
                return [response]
        
        # default to a non JSON-RPC error
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    def _decode(self, json):
        return simplejson.loads(json)
    
    def _dispatch(self, json):
        rpc_request = self._decode(json)
        
        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)
        
        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)
    
    # rpc unit conversion function
    def rpc_convert_units_to_ml(self, amount):
        return to_ml(amount)
    
    # rpc call to return a list of all recipe names
    def rpc_get_recipe_names(self):
        recipes = drinkz.db.get_all_recipes
        names = []
        for r in recipes:
            names.append(r.name)
        
        return names
    
    # rpc call to return a list of all items in the inventory
    def rpc_get_liquor_inventory(self):
        inventory = drinkz.db.get_liquor_inventory()
        items = []
        for (m,l) in inventory:
            items.append((m,l))
        
        return items
