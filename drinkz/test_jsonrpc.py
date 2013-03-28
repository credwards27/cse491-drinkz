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
app.load_database('bin/database_file')

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
    
    json_conversion = _run_rpc_convert_units(environ, my_start_response)
    
    # decode response
    json_parsed = simplejson.loads("".join(json_conversion))
    
    # compare results
    assert json_parsed['result'] == to_ml('8oz')

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

def _run_rpc_convert_units(environ, start_response):
    json_conversion = app(environ, start_response)
    print json_conversion
    return json_conversion
