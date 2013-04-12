#! /usr/bin/env python
import sys
import simplejson
import urllib2
import StringIO

import drinkz.db
import drinkz.recipes
from drinkz.convert import to_ml
from drinkz.app import SimpleApp

app = SimpleApp()

# initialize database
def test_init():
    app = SimpleApp()
    app.load_database('bin/database_file')

# test unit conversion
def test_conversion():
    # encode things in a dict that is then converted into json
    d = dict(method='convert_units_to_ml', params=['8oz'], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    # compare results
    assert json_parsed['result'] == to_ml('8oz')

# test recipe names
def test_recipe_names():
    # encode things in a dict that is then converted into json
    d = dict(method='get_recipe_names', params=[], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    recipes = drinkz.db.get_all_recipes()
    recipe_names = []
    for r in recipes:
        recipe_names.append(r.name)
    
    # compare results
    assert json_parsed['result'] == recipe_names

# test liquor inventory
def test_liquor_inventory():
    # encode things in a dict that is then converted into json
    d = dict(method='get_liquor_inventory', params=[], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    #inventory = drinkz.db.get_liquor_inventory()
    #items = []
    #for (m,l) in inventory:
        #items.append((m,l))
    
    #items = app.rpc_get_liquor_inventory()
    
    items = [['Johnnie Walker', 'Black Label'], ['Evan Williams', 'Cinnamon Reserve']]
    
    # compare results
    assert json_parsed['result'] == items

# test rpc add liquor
def test_add_liquor():
    # encode things in a dict that is then converted into json
    d = dict(method='add_liquor_type', params=[], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    # compare results
    assert True

# test rpc add inventory item
def test_rpc_add_inventory_item():
    # encode things in a dict that is then converted into json
    d = dict(method='add_inventory_item', params=[], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    # compare results
    assert True

# test rpc add recipe
def test_rpc_add_recipe():
    # encode things in a dict that is then converted into json
    d = dict(method='add_recipe', params=[], id=1)
    encoded = simplejson.dumps(d)
    
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '1000',
        'wsgi.input': StringIO.StringIO(encoded)
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    json_conversion = _run_rpc_call(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    # compare results
    assert True

def call_remote(base, method, params, id):
    # determine the url to call
    url = base + 'rpc'
    
    # encode things in a dict that is then converted into json
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)
    
    # specify appropriate content-type
    headers = { 'Content-Type' : 'application/json' }
    
    # call remote server
    req = urllib2.Request(url, encoded, headers)
    
    # get response
    response_stream = urllib2.urlopen(req)
    json_response = response_stream.read()
    
    # decode response
    response = simplejson.loads(json_response)
    
    # return result
    return response['result']

def _run_rpc_call(environ, start_response):
    json_response = app(environ, start_response)
    return json_response
