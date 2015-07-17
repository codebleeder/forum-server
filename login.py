#!/usr/bin/env python

import cgi
import sqlite3

form = cgi.FieldStorage()

username = form.getvalue('username')
password = form.getvalue('password')

conn = sqlite3.connect('server.db')
c = conn.cursor()
c.execute("SELECT password FROM users WHERE username = ?", (username,))
retrieved_password = c.fetchone()

print """Content-type: text/html\r\n\r\n"""

if password == retrieved_password[0]:
    print """ password authentication successful!"""
else:
    print """ wrong password! Try again:
    <a href="http://localhost:8000/index3.py">Log in</a>"""
