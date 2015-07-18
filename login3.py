#!/usr/bin/env python

import cgi
import sqlite3
import os

def display_user_page(f):
    username = f.getvalue('username')
    password = f.getvalue('password')

    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    retrieved_password = c.fetchone()

    if retrieved_password is None:
        print """ Sign up for a new account:
        <a href="http://localhost:8000/index3.py">Go back/a>"""
    elif password == retrieved_password[0]:
        print """ password authentication successful!"""
        print """ <a href="http://localhost:8000/index3.py">Log out</a>
        <form enctype="multipart/form-data" action="login3.py" method="post">
            <p>File: <input type="file" name="filename" /></p>
            <p><input type="submit" value="Upload" /></p>
        </form>"""

        c.execute("UPDATE users SET active = 1 WHERE username = ?", (username, ))
        conn.commit()
        conn.close()
    else:
        print """ wrong password! Try again:
        <a href="http://localhost:8000/index3.py">Log in</a>"""


def display_load_page(f):
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE active = 1")
    username = c.fetchone()[0]
    print username

    file_item = f['filename']

    # Test if the file was uploaded
    if file_item.filename:
        # strip leading path from file name to avoid
        # directory traversal attacks
        fn = os.path.basename(file_item.filename)
        file_path = './files/'+username+'/' + fn

        open(file_path, 'wb').write(file_item.file.read())

        message = 'The file "' + fn + '" was uploaded successfully'

    else:
        message = 'No file was uploaded'

    print """\
    Content-Type: text/html\n
    <html>
    <body>
       <p>%s</p>

    </body>
    </html>
    """ % (message, )
    conn.close()

# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""

if 'username' in form and 'password' in form:
    display_user_page(form)

elif 'filename' in form:
    # print """<h3> processing form </h3>"""
    display_load_page(form)

