#!/usr/bin/env python

import random
import socket
import time
from drinkz.app import SimpleApp

the_app = SimpleApp()
the_app.fake_init_page_builder("templates")

s = socket.socket() # create socket object
host = socket.gethostname() # get local machine name
port = 8181;
s.bind((host,port)) # bind to the port

print "Starting server on", host, port

s.listen(5) # wait for client connection

while True:
    c, addr = s.accept() # establish connection with client
    print "Got connection from", addr
    
    buffer = c.recv(1024)
    
    while "\r\n\r\n" not in buffer:
        data = c.recv(1024)
        if not data:
            break
        buffer += data
        print (buffer,)
        time.sleep(1)
        
    print "Got entire request:", (buffer,)
    
    # parse the http request
    lines = buffer.splitlines()
    request_line = lines[0]
    request_type, path, protocol = request_line.split()
    print "GOT", request_type, path, protocol
    
    request_headers = lines[1:] # discard for GET
    
    query_string = ""
    if "?" in path:
        path, query_string = path.split("?", 1)
    
    post_message = ""
    if request_type == "POST":
        post_message = "hello world"
    
    # build environ and start_response
    environ = {}
    environ["PATH_INFO"] = path
    environ["QUERY_STRING"] = query_string
    environ["wsgi.input"] = post_message
    
    d = {}
    def start_response(status, headers):
        d["status"] = status
        d["headers"] = headers
    
    results = the_app(environ, start_response)
    # start_response is called by the_app
    
    response_headers = []
    for k, v in d["headers"]:
        h = "%s: %s" % (k,v)
        response_headers.append(h)
    
    response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)
    
    c.send("HTTP/1.0 %s\r\n" % d["status"])
    c.send(response)
    c.close()
