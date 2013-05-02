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
    '/add_recipe' : 'add_recipe',
    '/add_recipe.html' : 'add_recipe',
    '/recv_add_recipe' : 'recv_add_recipe',
    '/inventory' : 'inventory',
    '/inventory.html' : 'inventory',
    '/add_inventory_item' : 'add_inventory_item',
    '/add_inventory_item.html' : 'add_inventory_item',
    '/recv_add_inventory_item' : 'recv_add_inventory_item',
    '/liquor_types' : 'liquor_types',
    '/liquor_types.html' : 'liquor_types',
    '/add_liquor_type' : 'add_liquor_type',
    '/add_liquor_type.html' : 'add_liquor_type',
    '/recv_add_liquor_type' : 'recv_add_liquor_type',
    '/convert_amount' : 'convert_amount',
    '/convert_amount.html' : 'convert_amount',
    '/convert_amount_post' : 'convert_amount_post',
    '/convert_amount_post.html' : 'convert_amount_post',
    '/recv_conversion' : 'recv_conversion',
    '/recv_conversion_post' : 'recv_conversion_post',
    '/error' : 'error',
    '/rpc' : 'dispatch_rpc'
}

# html headers for page encoding
html_headers = [('Content-Type', 'text/html; charset=UTF-8')]

path = None

class SimpleApp(object):
    def __init__(self):
        page_builder.init_page_builder('../templates')
    
    def fake_init_page_builder(self, templatePath):
        page_builder.init_page_builder(templatePath)
    
    def load_database(self, filename):
        drinkz.db.load_db(filename)
    
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        #print "REQUEST_METHOD:", environ['REQUEST_METHOD']
        #print "CONTENT_LENGTH:", environ['CONTENT_LENGTH']
        #print "wsgi.input:", environ['wsgi.input']
        
        global path
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
        
        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to the 'path'
        fn = getattr(self, fn_name, None)
        
        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s is found" % path]
        
        return [fn(environ, start_response).encode('utf-8')]
    
    # index page
    def index(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_index()
    
    # recipe list
    def recipes(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_recipes()
    
    # add recipe form
    def add_recipe(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_add_recipe()
    
    # add recipe form handler
    def recv_add_recipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        ingredients = []
        
        # add ingredients to the list
        for i in range(0,5):
            try:
                ingValue = "".join(results['in'+str(i)])
                amtValue = "".join(results['amt'+str(i)])
                ing = (ingValue, amtValue)
                ingredients.append(ing)
            except KeyError:
                continue
        
        # create the new recipe
        r = drinkz.recipes.Recipe("".join(results['name']), ingredients)
        
        try:
            drinkz.db.add_recipe(r)
        except drinkz.db.DuplicateRecipeName:
            pass
        
        # return to the recipe list page
        start_response('200 OK', list(html_headers))
        return page_builder.build_recipes()
    
    # inventory list
    def inventory(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_inventory()
    
    # add inventory item form
    def add_inventory_item(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_add_inventory_item()
    
    # add inventory item form handler
    def recv_add_inventory_item(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        # add the form entries to the database
        try:
            drinkz.db.add_to_inventory("".join(results['mfg']), "".join(results['liq']), "".join(results['amt']))
        except drinkz.db.LiquorMissing:
            pass
        
        start_response('200 OK', list(html_headers))
        return page_builder.build_inventory()
    
    # liquor types list
    def liquor_types(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_liquor_types()
    
    # add liquor type form
    def add_liquor_type(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_add_liquor_type()
    
    # add liquor type form handler
    def recv_add_liquor_type(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        # add the form entries to the database
        drinkz.db.add_bottle_type("".join(results['mfg']), "".join(results['liq']), "".join(results['typ']))
        
        start_response('200 OK', list(html_headers))
        return page_builder.build_liquor_types()
    
    # liquor amount conversion form
    def convert_amount(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_liquor_conversion()
    
    # POST version of conversion form
    def convert_amount_post(self, enviton, start_response):
        start_response('200 OK', list(html_headers))
        return page_builder.build_liquor_conversion_post()
    
    # conversion form submission
    def recv_conversion(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        start_response('200 OK', list(html_headers))
        return page_builder.build_conversion_results(results['amount'][0])
    
    # POST conversion form submission
    def recv_conversion_post(self, environ, start_response):
        """if environ["REQUEST_METHOD"].upper() != "POST":
            return error(environ, start_response)
        
        content_type = environ.get("CONTENT_TYPE", "application/x-www-form-urlencoded")
        
        if content_type.startswith("application/x-www-form-urlencoded") or content_type.startswith("multipart/form-data"):
            input = environ["wsgi.input"]
            post_form = environ.get("wsgi.post_form")
            
            if post_form is not None and post_form[0] is input:
                return post_form[2]
            
            environ.setdefault("QUERY_STRING", "")
            fs = cgi.FieldStorage(fp=input, environ=environ, keep_blank_values=1)
            
            new_input = InputProcessed("")
            post_form = (new_input, input, fs)
            
            environ["wsgi.post_form"] = post_form
            environ["wsgi.input"] = new_input
            
        else:
            return error(environ, start_response)"""
        
        results = environ["wsgi.input"]
        print "\n", results, "\n"
        
        start_response('200 OK', list(html_headers))
        return page_builder.build_conversion_results_post(results['amount'][0])
    
    # unexpected request
    def error(self, environ, start_response):
        content_type = 'text/plain'
        data = 'If "%s" does not appear in our records, it does not exist!' % path
        
        start_response('404 Not Found', list(html_headers))
        return data
    
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
                
                return response
        
        # default to a non JSON-RPC error
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
        
        start_response('200 OK', list(html_headers))
        return data
    
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
        recipes = drinkz.db.get_all_recipes()
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
    
    # rpc call to add a liquor type to the database
    def rpc_add_liquor_type(self):
        print "add liquor"
        pass
    
    # rpc call to add an inventory item to the database
    def rpc_add_inventory_item(self):
        print "add inventory item"
        pass
    
    # rpc call to add a recipe to the database
    def rpc_add_recipe(self):
        print "add recipe"
        pass
