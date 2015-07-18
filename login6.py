#!/usr/bin/env python

import cgi
import sqlite3
import os


def get_active_user():
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE active = 1")
    username = c.fetchone()[0]
    conn.close()
    return username


def auth_user(f):
    username = f.getvalue('username')
    password = f.getvalue('password')

    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    retrieved_password = c.fetchone()

    if retrieved_password is None:
        print """ Sign up for a new account:
        <a href="http://localhost:8000/index4.py">Go back/a>"""
    elif password == retrieved_password[0]:
        print """ password authentication successful!"""
        c.execute("UPDATE users SET active = 1 WHERE username = ?", (username, ))
        conn.commit()
        conn.close()
        display_user_page()
    else:
        print """ wrong password! Try again:
        <a href="http://localhost:8000/index3.py">Log in</a>"""


def display_user_page():
    username = get_active_user()
    print username
    files_path = './files/'+username
    file_list = os.listdir(files_path)

    print """ <h4><a href="http://localhost:8000/index3.py">Log out</a></h4>
    -----------------------------------------------------------------------"""
    print """
    <form enctype="multipart/form-data" action="login6.py" method="post">
        <p>File: <input type="file" name="filename" /></p>
        <p><input type="submit" value="Upload" /></p>
    </form>
    ----------------------------------------------------------------------"""
    print """
    <form action="login6.py" method="post" target="_blank">
    <select name="dropdown">"""
    #<option value="Maths" selected>Maths</option>
    for i in file_list:
        print "<option value=%s selected>%s</option>" % (i, i)
    print """
    </select>
    <input type="submit" value="Delete"/>
    </form>
    ----------------------------------------------------------------------"""
    print "<h3> file list </h3>"
    for i in file_list:
        print "<h3>%s</h3>" % (i, )


def display_load_page(f):
    username = get_active_user()

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


def delete_file(f):
    username = get_active_user()
    if form.getvalue('dropdown'):
        file_name = form.getvalue('dropdown')
        file_path = './files/'+username+'/'+file_name
        os.remove(file_path)
        message = 'removed ', file_name
    else:
        message = "Not entered"

    print message
    display_user_page()



# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""

if 'username' in form and 'password' in form:
    auth_user(form)

elif 'filename' in form:
    # print """<h3> processing form </h3>"""
    display_load_page(form)

elif 'dropdown' in form:
    delete_file(form)
