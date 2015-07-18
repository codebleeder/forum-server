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
# store username in cookie
print "Set-Cookie:UserID=%s;\r\n" % (username, )
print """Content-type: text/html\r\n\r\n"""

if password == retrieved_password[0]:
    print """ password authentication successful!"""
    print """ <a href="http://localhost:8000/index3.py">Log out</a>
    <form enctype="multipart/form-data" action="save_file.py?username=%s" method="post">
        <p>File: <input type="file" name="filename" /></p>
        <p><input type="submit" value="Upload" /></p>
    </form>""" % (username, )

else:
    print """ wrong password! Try again:
    <a href="http://localhost:8000/index3.py">Log in</a>"""
