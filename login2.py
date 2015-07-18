#!/usr/bin/env python

import cgi
import sqlite3
import os


class App:
    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def display_user_page(self, f):
        username = f.getvalue('username')
        password = f.getvalue('password')

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

            self.set_username(username)

        else:
            print """ wrong password! Try again:
            <a href="http://localhost:8000/index3.py">Log in</a>"""

    def display_load_page(self, f):
        file_item = f['filename']

        # Test if the file was uploaded
        if file_item.filename:
            # strip leading path from file name to avoid
            # directory traversal attacks
            fn = os.path.basename(file_item.filename)
            file_path = './files/'+self.get_username()+'/' + fn

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


# main
form = cgi.FieldStorage()
print """Content-type: text/html\r\n\r\n"""
a = App()
if 'username' in form and 'password' in form:
    a.display_user_page(form)
    print a.username
elif 'filename' in form:
    # print """<h3> processing form </h3>"""
    print a.username
    a.display_load_page(form)
