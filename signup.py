#!/usr/bin/env python

import cgi
import sqlite3
from os import makedirs

form = cgi.FieldStorage()

new_username = form.getvalue('new_username')
new_password = form.getvalue('new_password')
confirm_new_password = form.getvalue('confirm_new_password')
print """Content-type: text/html\r\n\r\n


"""
if new_password == confirm_new_password:
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT rowid FROM users WHERE username = ?", (new_username,))
    data = c.fetchone()
    if data is None:
        c.execute("INSERT INTO users (username, password) VALUES(?, ?)", (new_username, new_password))
        conn.commit()
        conn.close()

        new_dir = './files/'+new_username
        makedirs(new_dir)

        print """
        <h3>Congratulations! New account created. Log in using new account:</h3><br/>
        <a href="http://localhost:8000/index4.py">Homee</a>
        """
    else:
        print """
        <h3> new username already exists, Try again:</h3><br/>
        <a href="http://localhost:8000/index3.py">Sign up</a>
        """
else:
    print """
    <h3>new password and confirm new password don't match! Try again:</h3><br/>
    <a href="http://localhost:8000/index3.py">Sign up</a>
    """