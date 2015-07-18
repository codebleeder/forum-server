#!/usr/bin/env python
import cgi
import cgitb
import sqlite3

# Create instance of FieldStorage


def log_out(form):
    # Get data from fields
    val = form.getvalue('log_out')
    conn = sqlite3.connect('server.db')
    c = conn.cursor()
    c.execute("UPDATE users SET active = 0 WHERE active = 1")
    conn.commit()
    conn.close()
    print "<h3> log out successful!</h3><br/>"
    display_forms()


def display_forms():
    print """
    <html>
        <head>
            <title>The Forum </title>
        </head>
        <body>
            <h2>The Forum </h2><br/>
            <form method="post" action="login.py">
                username:<input type="text" name="username"><br/>
                password:<input type="text" name="password"><br/>
                <input type="submit" value="Submit">
            </form><br/><br/>

            <h3> sign up </h3><br/>
            <form method="post" action="signup.py">
                new username:<input type="text" name="new_username"><br/>
                new password:<input type="text" name="new_password"><br/>
                confirm new password:<input type="text" name="confirm_new_password"><br/>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""
if 'log_out' in form:
    log_out(form)
else:
    display_forms()
