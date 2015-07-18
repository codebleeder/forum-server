#!/usr/bin/env python

import cgi
import sqlite3
from os import makedirs
import hashlib
import uuid


def generate_hash(password):
    salt = uuid.uuid4().hex
    hash_val = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return hash_val, salt

# main
form = cgi.FieldStorage()
new_username = form.getvalue('new_username')
new_password = form.getvalue('new_password')
confirm_new_password = form.getvalue('confirm_new_password')
print """Content-type: text/html\r\n\r\n


"""
if new_password == confirm_new_password and len(new_password) >= 6 and new_password != new_username:
    hash_salt = generate_hash(new_password)
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    cmd = "SELECT rowid FROM users WHERE username = ?"
    c.execute(cmd, (new_username,))
    data = c.fetchone()
    if data is None:
        cmd = "INSERT INTO users (username, hash, salt) VALUES(?, ?, ?)"
        c.execute(cmd, (new_username, hash_salt[0], hash_salt[1]))
        conn.commit()
        conn.close()

        new_dir = './files/'+new_username
        makedirs(new_dir)
        print """
        <h3>Congratulations! New account created. Log in using new account:</h3><br/>
        <a href="http://localhost:8000/index.py">Home</a>
        """
    else:
        print """
        <h3> new username already exists, Try again:</h3><br/>
        <a href="http://localhost:8000/index.py">Sign up</a>
        """
else:
    print """
    <h3>passwords don't match! or \
                  length should be atleast 6 characters or \
                  password is same as username \
                   try again!
    <a href="http://localhost:8000/index.py">Sign up</a></h3>
    """