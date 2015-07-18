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
    print """
    <h1>%s</h1>
    ----------------------------------------------------------------------""" % username
    files_path = './files/'+username
    file_list = os.listdir(files_path)

    print """ <h2><a href="http://localhost:8000/index4.py?log_out=1">Log out</a></h2>
    -----------------------------------------------------------------------"""
    print """ <h2> Change password </h2>
        <form method="post" action="login8.py">
                new password:<input type="text" name="new_password"><br/>
                confirm new password:<input type="text" name="confirm_new_password"><br/>
                <input type="submit" value="Submit">
        </form>
    -----------------------------------------------------------------------"""
    print """
    <h2> Upload File </h2>
    <form enctype="multipart/form-data" action="login8.py" method="post">
        <p>File: <input type="file" name="filename" /></p>
        <p><input type="submit" value="Upload" /></p>
    </form>
    ----------------------------------------------------------------------"""
    print """
    <h2> Delete File </h2>
    <form action="login8.py" method="post" target="_blank">
    <select name="dropdown">"""
    #<option value="Maths" selected>Maths</option>
    for i in file_list:
        print "<option value=%s selected>%s</option>" % (i, i)
    print """
    </select>
    <input type="submit" value="Delete"/>
    </form>
    ----------------------------------------------------------------------"""
    print "<h2> file list </h2>"
    for i in file_list:
        print "<h4>%s</h4>" % (i, )
        print """
        <form method="get" action=%s>
        <button type="submit">Download!</button>
        </form>
        """ % ('./files/'+username+'/'+i, )


def upload_file(f):
    username = get_active_user()

    file_item = f['filename']

    # Test if the file was uploaded
    if file_item.filename:
        # strip leading path from file name to avoid
        # directory traversal attacks
        fn = os.path.basename(file_item.filename)
        file_path = './files/'+username+'/' + fn
        open(file_path, 'wb').write(file_item.file.read())
        message = '<h3>The file "' + fn + '" was uploaded successfully</h3>'
    else:
        message = '<h3>No file was uploaded</h3>'

    print message
    display_user_page()


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


def change_password(f):
    username = get_active_user()
    new_password = f.getvalue('new_password')
    confirm_new_password = f.getvalue('confirm_new_password')
    if new_password == confirm_new_password:
        conn = sqlite3.connect('server.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username, ))
        old_password = c.fetchone()[0]
        if old_password == new_password:
            message = 'old and new passwords are the same! try again'
        else:
            c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
            conn.commit()
            message = 'password change succesful!'
        conn.close()
    else:
        message = "passwords don't match! try again!"
    print message
    display_user_page()


# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""

if 'username' in form and 'password' in form:
    auth_user(form)

elif 'filename' in form:
    # print """<h3> processing form </h3>"""
    upload_file(form)

elif 'dropdown' in form:
    delete_file(form)

if 'new_password' in form and 'confirm_new_password' in form:
    change_password(form)

