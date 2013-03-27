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
    environ = {
        'PATH_INFO': '/rpc',
        'REQUEST_METHOD': 'POST',
        'CONTENT_LENGTH': '',
        'wsgi.input': StringIO.StringIO()
    }
    
    d = {}
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    amount = '8oz'
    
    #json_conversion = _run_rpc_convert_units(amount, environ, my_start_response)

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

def _run_rpc_convert_units(amt, environ, start_response):
    json_conversion = app(environ, start_response)
