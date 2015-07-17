#!/usr/bin/env python

import cgi
import sqlite3


def display_user_page(form):
    username = form.getvalue('username')
    password = form.getvalue('password')

    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    retrieved_password = c.fetchone()

    if password == retrieved_password[0]:
        print """ password authentication successful!"""
        print """ <a href="http://localhost:8000/index3.py">Log out</a>
        <form enctype="multipart/form-data" action="login2.py" method="post">
            <p>File: <input type="file" name="filename" /></p>
            <p><input type="submit" value="Upload" /></p>
        </form>"""
    else:
        print """ wrong password! Try again:
        <a href="http://localhost:8000/index3.py">Log in</a>"""


# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""

if 'username' in form and 'password' in form:
    display_user_page(form)
elif 'filename' in form:
    print """<h3> processing form </h3>"""
