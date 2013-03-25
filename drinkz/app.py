#! /usr/bin/python
import urlparse

class SimpleApp(object):
    def __call__(self, environ, start_response):
        status = '200 OK'
        
        path = environ['PATH_INFO']
        
        if path == '/':
            content_type = 'text/html'
            data = _build_index()

########################################
# web page builder functions
########################################

def _build_index():
    print "build index"
