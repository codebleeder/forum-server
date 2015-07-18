#!/usr/bin/env python

import BaseHTTPServer
import CGIHTTPServer
import sqlite3
from os import path, mkdir

if path.isfile('server.db'):
    print 'server.db already exists'
else:
    print 'creating server.db'
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute(''' CREATE TABLE users
              (username text, password text, active integer)''')
    conn.commit()
    conn.close()

print 'starting server'
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/"]

httpd = server(server_address, handler)
httpd.serve_forever()
